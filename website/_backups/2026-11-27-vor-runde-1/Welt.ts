// Die begehbare ESTILO-Wohnung: gebackenes Licht aus Blender, Kamerafahrt über Stationen, Sofa zum Drehen.
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { MeshoptDecoder } from 'three/examples/jsm/libs/meshopt_decoder.module.js';

type MatInfo = { tex?: string; farbe?: number[]; emit?: number[] | null; glas?: boolean };
type TexInfo = { datei: string; grau: boolean; farbe?: string };
export type Station = { pos: THREE.Vector3; quat: THREE.Quaternion; fov: number };

const SRGB_07 = Math.pow((0.7 + 0.055) / 1.055, 2.4); // Mittelwert der Graustruktur, linear

export type WeltOptionen = {
  canvas: HTMLCanvasElement;
  handy: boolean;
  ruhig: boolean; // prefers-reduced-motion: keine Nachlaufbewegung, kein Atmen
  basis?: string;
  onFortschritt?: (anteil: number) => void;
};

export class Welt {
  renderer: THREE.WebGLRenderer;
  szene = new THREE.Scene();
  kamera = new THREE.PerspectiveCamera(50, 1, 0.05, 400);
  stationen: Station[] = [];
  gruppen: Record<string, THREE.Object3D[]> = {};
  sofa?: THREE.Object3D;
  private sofaStoff: THREE.MeshBasicMaterial[] = [];
  private sofaDreh = 0; private sofaZiel = 0;
  private ziel = 0; private ist = 0;          // Fortschritt über die Stationen (0 .. n-1)
  private maus = new THREE.Vector2(); private mausIst = new THREE.Vector2();
  private uhr = new THREE.Clock();
  private laeuft = false; private sichtbar = true;
  private o: WeltOptionen;
  bereit = false;

  constructor(o: WeltOptionen) {
    this.o = o;
    this.renderer = new THREE.WebGLRenderer({ canvas: o.canvas, antialias: !o.handy, powerPreference: 'high-performance' });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, o.handy ? 1.5 : 2));
    this.renderer.toneMapping = THREE.NeutralToneMapping; // erhält Farbtöne (AgX entsättigte das Sofa)
    this.renderer.toneMappingExposure = 0.62;
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    this.szene.background = new THREE.Color('#F3EEE7');
  }

  async laden() {
    const b = this.o.basis ?? '/welt/';
    const h = this.o.handy ? '.handy' : '';
    const mgr = new THREE.LoadingManager();
    mgr.onProgress = (_u, fertig, gesamt) => this.o.onFortschritt?.(fertig / gesamt);
    const tl = new THREE.TextureLoader(mgr);
    const [mats, texInfo] = await Promise.all([
      fetch(b + 'material.json').then((r) => r.json()) as Promise<Record<string, MatInfo>>,
      fetch(b + 'tex.json').then((r) => r.json()) as Promise<Record<string, TexInfo>>,
    ]);
    const lade = (url: string, farbig: boolean) => {
      const t = tl.load(url);
      t.flipY = false; t.colorSpace = farbig ? THREE.SRGBColorSpace : THREE.NoColorSpace;
      t.anisotropy = this.o.handy ? 2 : 8;
      return t;
    };
    const licht: Record<string, THREE.Texture> = {
      arch: lade(`${b}licht_arch${h}.webp`, false),
      moebel: lade(`${b}licht_moebel${h}.webp`, false),
    };
    for (const t of Object.values(licht)) { t.channel = 1; t.generateMipmaps = true; }
    const himmel = tl.load(b + 'himmel.webp');
    himmel.colorSpace = THREE.SRGBColorSpace; himmel.mapping = THREE.EquirectangularReflectionMapping;
    const texCache: Record<string, THREE.Texture> = {};
    const tex = (datei: string) => {
      if (!texCache[datei]) { const t = lade(`${b}tex/${datei}${h}.webp`, true); t.wrapS = t.wrapT = THREE.RepeatWrapping; texCache[datei] = t; }
      return texCache[datei];
    };

    const loader = new GLTFLoader(mgr); loader.setMeshoptDecoder(MeshoptDecoder);
    const gltf = await loader.loadAsync(`${b}estilo${h}.glb`).catch(() => loader.loadAsync(`${b}estilo.glb`));
    const welt = gltf.scene;

    // Himmel: große Kugel hinter den Fenstern (nicht als Hintergrund, damit der Leinen-Grund im Einstieg bleibt)
    const kugel = new THREE.Mesh(new THREE.SphereGeometry(150, 48, 24), new THREE.MeshBasicMaterial({ map: himmel, side: THREE.BackSide, depthWrite: false }));
    kugel.rotation.y = THREE.MathUtils.degToRad(-108 + 90); kugel.position.set(9, 0, 0); kugel.renderOrder = -1;
    this.szene.add(kugel);

    const matCache = new Map<string, THREE.Material>();
    welt.traverse((obj) => {
      const m = obj as THREE.Mesh;
      if (!m.isMesh) return;
      const gruppe = (m.userData.gruppe as string) || (m.parent?.userData.gruppe as string) || 'ohne';
      (this.gruppen[gruppe] ??= []).push(m);
      const alt = m.material as THREE.MeshStandardMaterial;
      const name = alt.name;
      const schluessel = name + '|' + gruppe;
      let neu = matCache.get(schluessel) as THREE.MeshBasicMaterial | undefined;
      if (!neu) {
        const info = mats[name] ?? {};
        if (info.glas) {
          neu = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.07, depthWrite: false });
        } else if (info.emit) {
          neu = new THREE.MeshBasicMaterial({ color: new THREE.Color().setRGB(info.emit[0] * 2.4, info.emit[1] * 2.4, info.emit[2] * 2.4) });
        } else if (gruppe === 'vc') {
          // Farbe und Licht stecken in den Vertex-Farben (x0.25 gespeichert)
          neu = new THREE.MeshBasicMaterial({ vertexColors: true, color: new THREE.Color(4, 4, 4) });
        } else {
          neu = new THREE.MeshBasicMaterial();
          const ti = info.tex ? texInfo[name] : undefined;
          if (ti) {
            neu.map = tex(ti.datei);
            if (ti.grau && ti.farbe) neu.color = new THREE.Color(ti.farbe).multiplyScalar(1 / SRGB_07);
          } else if (info.farbe) {
            neu.color = new THREE.Color().setRGB(info.farbe[0], info.farbe[1], info.farbe[2]);
          }
          if (licht[gruppe]) {
            neu.lightMap = licht[gruppe]; neu.lightMapIntensity = Math.PI;
            neu.onBeforeCompile = (s) => {
              // Lichtatlas ist als sqrt(L/(1+L)) gespeichert: zurückrechnen
              s.fragmentShader = s.fragmentShader.replace(
                'vec4 lightMapTexel = texture2D( lightMap, vLightMapUv );',
                'vec4 lightMapTexel = texture2D( lightMap, vLightMapUv ); { vec3 e2 = lightMapTexel.rgb * lightMapTexel.rgb; lightMapTexel.rgb = e2 / max( vec3(1.0) - e2, vec3(0.002) ); }',
              );
            };
          }
        }
        neu.name = name;
        matCache.set(schluessel, neu);
      }
      if (name === 'sofa_gruen' || name === 'sofa_lehne') {
        // eigenes Material für das Sofa (Bezug umfärbbar, ohne andere Objekte mitzufärben)
        neu = (neu as THREE.MeshBasicMaterial).clone();
        const quelle = matCache.get(schluessel) as THREE.MeshBasicMaterial;
        neu.onBeforeCompile = quelle.onBeforeCompile; // geht beim clone() verloren
        neu.userData.basis = neu.color.clone();
        this.sofaStoff.push(neu);
      }
      m.material = neu;
    });
    this.sofa = welt.getObjectByName('sofa') ?? undefined;
    this.szene.add(welt);

    // Kamerastationen aus Blender
    welt.updateMatrixWorld(true);
    const namen = ['station_0_logo', 'station_1_wohnen', 'station_2_schlafen', 'station_3_essen', 'station_4_buero'];
    for (const n of namen) {
      const c = welt.getObjectByName(n) as THREE.Object3D | undefined;
      const cam = (c && ((c as THREE.PerspectiveCamera).isPerspectiveCamera ? c : c.children.find((x) => (x as THREE.PerspectiveCamera).isPerspectiveCamera))) as THREE.PerspectiveCamera | undefined;
      if (!cam) continue;
      const pos = new THREE.Vector3(), quat = new THREE.Quaternion();
      cam.getWorldPosition(pos); cam.getWorldQuaternion(quat);
      this.stationen.push({ pos, quat, fov: cam.fov });
    }
    // Zusatzstation: nah am Sofa (zum Drehen und Bezug wählen), zwischen Wohnen und Schlafen
    if (this.sofa) {
      const box = new THREE.Box3().setFromObject(this.sofa); const mitte = box.getCenter(new THREE.Vector3());
      const pos = mitte.clone().add(new THREE.Vector3(0.55, 0.95, 3.2));
      const blick = new THREE.PerspectiveCamera(); blick.position.copy(pos); // Kamera: lookAt zeigt entlang -Z blick.lookAt(mitte.clone().add(new THREE.Vector3(0.25, -0.05, 0)));
      this.stationen.splice(2, 0, { pos, quat: blick.quaternion.clone(), fov: 42 });
    }
    this.bereit = true;
    this.setzeKamera(0, true);
    return this;
  }

  /** Fortschritt 0 .. stationen-1 (Bruchteile = zwischen zwei Stationen) */
  setFortschritt(p: number) { this.ziel = THREE.MathUtils.clamp(p, 0, this.stationen.length - 1); if (this.o.ruhig) { this.ist = this.ziel; this.schmutzig = true; } }
  setMaus(x: number, y: number) { this.maus.set(x, y); }
  drehen(dx: number) { this.sofaZiel += dx; }
  setBezug(hex: string | null) {
    for (const m of this.sofaStoff) {
      if (!hex) { m.color.copy(m.userData.basis); continue; }
      const c = new THREE.Color(hex).multiplyScalar(1 / SRGB_07);
      if (m.name === 'sofa_lehne') c.multiplyScalar(0.92);
      m.color.copy(c);
    }
    this.schmutzig = true;
  }

  /** Bildschirm-Rechteck (CSS-Pixel) einer Objektgruppe, für den Übergang Logo -> Raum */
  rechteck(namen: string[]) {
    const box = new THREE.Box3();
    for (const n of namen) { const o = this.szene.getObjectByName(n); if (o) box.expandByObject(o); }
    if (box.isEmpty()) return null;
    const ecken = [0, 1].flatMap((x) => [0, 1].flatMap((y) => [0, 1].map((z) => new THREE.Vector3(x ? box.max.x : box.min.x, y ? box.max.y : box.min.y, z ? box.max.z : box.min.z))));
    const w = this.o.canvas.clientWidth, h = this.o.canvas.clientHeight;
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    for (const e of ecken) { e.project(this.kamera); const sx = (e.x + 1) / 2 * w, sy = (1 - e.y) / 2 * h; x0 = Math.min(x0, sx); x1 = Math.max(x1, sx); y0 = Math.min(y0, sy); y1 = Math.max(y1, sy); }
    return { x: x0, y: y0, w: x1 - x0, h: y1 - y0 };
  }

  private setzeKamera(p: number, sofort = false) {
    const n = this.stationen.length; if (!n) return;
    const i = Math.min(Math.floor(p), n - 2), f = p - i;
    const a = this.stationen[i], b = this.stationen[Math.min(i + 1, n - 1)];
    const s = f * f * (3 - 2 * f);
    // Position auf einer Catmull-Rom-Kurve (weich, ohne Knick an den Stationen)
    const v0 = this.stationen[Math.max(i - 1, 0)].pos, v3 = this.stationen[Math.min(i + 2, n - 1)].pos;
    const kurve = new THREE.CatmullRomCurve3([v0, a.pos, b.pos, v3], false, 'centripetal');
    const pos = kurve.getPoint((1 + s) / 3);
    const quat = a.quat.clone().slerp(b.quat, s);
    let fov = THREE.MathUtils.lerp(a.fov, b.fov, s);
    // Hochformat: Brennweite so öffnen, dass die Breite des Bildes erhalten bleibt
    const asp = this.kamera.aspect;
    if (asp < 1.2) {
      const hfov = 2 * Math.atan(Math.tan(THREE.MathUtils.degToRad(fov) / 2) * 1.5);
      fov = Math.min(84, THREE.MathUtils.radToDeg(2 * Math.atan(Math.tan(hfov / 2) / asp)));
      pos.add(new THREE.Vector3(0, 0, 0.25).applyQuaternion(quat));
    }
    if (!this.o.ruhig && !sofort) {
      // ein wenig Mausblick, wie ein Mensch, der sich umsieht
      this.mausIst.lerp(this.maus, 0.06);
      const blick = new THREE.Quaternion().setFromEuler(new THREE.Euler(-this.mausIst.y * 0.025, -this.mausIst.x * 0.04, 0));
      quat.multiply(blick);
    }
    this.kamera.position.copy(pos); this.kamera.quaternion.copy(quat);
    if (Math.abs(this.kamera.fov - fov) > 0.01) { this.kamera.fov = fov; this.kamera.updateProjectionMatrix(); }
  }

  private versatz = 0; private versatzY = 0;
  /** Bild verschieben (CSS-Pixel): Desktop nach rechts (Text links), Handy nach oben (Text unten) */
  setVersatz(px: number, py = this.versatzY) {
    if (Math.abs(px - this.versatz) < 0.5 && Math.abs(py - this.versatzY) < 0.5) return; this.versatz = px; this.versatzY = py;
    const c = this.o.canvas; const w = c.clientWidth, h = c.clientHeight;
    if (px === 0 && py === 0) this.kamera.clearViewOffset(); else this.kamera.setViewOffset(w, h, -px, py, w, h);
    this.schmutzig = true;
  }

  groesse() {
    const c = this.o.canvas; const w = c.clientWidth, h = c.clientHeight;
    this.renderer.setSize(w, h, false); this.kamera.aspect = w / h;
    const v = this.versatz, vy = this.versatzY; this.versatz = -1; this.setVersatz(v, vy);
    this.kamera.updateProjectionMatrix();
    this.setzeKamera(this.ist, true); this.schmutzig = true; this.render();
  }

  /** true, solange sich noch etwas bewegt (sonst wird nicht neu gezeichnet) */
  private bewegt() {
    return Math.abs(this.ziel - this.ist) > 1e-4 || Math.abs(this.sofaZiel - this.sofaDreh) > 1e-4 || this.mausIst.distanceToSquared(this.maus) > 1e-6;
  }
  private schmutzig = true;
  neuZeichnen() { this.schmutzig = true; }

  render() {
    if (!this.bereit) return;
    const dt = Math.min(this.uhr.getDelta(), 0.05);
    if (!this.schmutzig && !this.bewegt()) return;
    this.schmutzig = false;
    if (!this.o.ruhig) this.ist += (this.ziel - this.ist) * (1 - Math.exp(-dt * 5));
    this.setzeKamera(this.ist);
    if (this.sofa) {
      this.sofaDreh += (this.sofaZiel - this.sofaDreh) * (this.o.ruhig ? 1 : 1 - Math.exp(-dt * 8));
      this.sofa.rotation.y = this.sofaDreh;
    }
    this.renderer.render(this.szene, this.kamera);
  }

  start() {
    if (this.laeuft) return; this.laeuft = true;
    const schleife = () => { if (!this.laeuft) return; if (this.sichtbar) this.render(); requestAnimationFrame(schleife); };
    requestAnimationFrame(schleife);
  }
  setSichtbar(v: boolean) { this.sichtbar = v; }
  stopp() { this.laeuft = false; }
  entsorgen() { this.stopp(); this.renderer.dispose(); }
}
