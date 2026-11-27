// Gemeinsame Skizzen-Szene: Logo-Raum (Sofa, drei Pendelleuchten, sechs Lamellen) aus einfachen Formen.
import * as THREE from './node_modules/three/build/three.module.js';
import { RoundedBoxGeometry } from './node_modules/three/examples/jsm/geometries/RoundedBoxGeometry.js';

export const FARBE = {
  leinen: 0xf3eee7, hell: 0xfffdf9, gruen: 0x6f7f50, lehne: 0x687251, kissen: 0x5b5b49,
  text: 0x24251f, eiche: 0xc9a77c, putz: 0xe9e2d6,
};

export function renderer(canvas) {
  const r = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  r.setPixelRatio(Math.min(devicePixelRatio, 2));
  r.shadowMap.enabled = true; r.shadowMap.type = THREE.PCFSoftShadowMap;
  r.toneMapping = THREE.ACESFilmicToneMapping; r.toneMappingExposure = 1.05;
  r.outputColorSpace = THREE.SRGBColorSpace;
  return r;
}

const mat = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: 0.85, ...o });

export function sofa() {
  const g = new THREE.Group();
  const add = (geo, m, x, y, z, rz = 0) => { const k = new THREE.Mesh(geo, m); k.position.set(x, y, z); k.rotation.z = rz; k.castShadow = k.receiveShadow = true; g.add(k); return k; };
  const stoff = mat(FARBE.gruen), lehne = mat(FARBE.lehne), kis = mat(FARBE.kissen);
  add(new RoundedBoxGeometry(2.0, 0.32, 0.85, 4, 0.08), stoff, 0, 0.42, 0);            // Sitz
  add(new RoundedBoxGeometry(1.85, 0.62, 0.22, 4, 0.1), lehne, 0, 0.82, -0.34);        // Lehne
  add(new RoundedBoxGeometry(0.26, 0.5, 0.9, 4, 0.12), stoff, -1.05, 0.62, 0, 0.18);   // Armlehnen, nach außen gekippt wie im Logo
  add(new RoundedBoxGeometry(0.26, 0.5, 0.9, 4, 0.12), stoff, 1.05, 0.62, 0, -0.18);
  add(new RoundedBoxGeometry(0.5, 0.42, 0.14, 4, 0.12), kis, -0.5, 0.78, -0.18, 0.05);  // Kissen
  const bein = new THREE.CylinderGeometry(0.025, 0.012, 0.3, 8), bm = mat(FARBE.text, { roughness: 0.4 });
  for (const [x, z, r] of [[-0.85, 0.3, 0.25], [-0.75, -0.3, 0.25], [0.85, 0.3, -0.25], [0.75, -0.3, -0.25]]) add(bein, bm, x, 0.14, z, r);
  return g;
}

export function leuchten(licht = true) {
  const g = new THREE.Group(), schwarz = mat(FARBE.text, { roughness: 0.35, metalness: 0.3 });
  for (const [x, h, z] of [[-1.1, 2.05, 0.2], [-0.75, 1.8, 0.35], [-0.4, 2.15, 0.1]]) {
    const kabel = new THREE.Mesh(new THREE.CylinderGeometry(0.006, 0.006, 3.2 - h), schwarz); kabel.position.set(x, h + (3.2 - h) / 2, z); g.add(kabel);
    const k = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 0.32, 24), schwarz); k.position.set(x, h, z); k.castShadow = true; g.add(k);
    const glut = new THREE.Mesh(new THREE.CircleGeometry(0.085, 24), new THREE.MeshBasicMaterial({ color: 0xffe2b0 }));
    glut.rotation.x = Math.PI / 2; glut.position.set(x, h - 0.161, z); g.add(glut);
    if (licht) { const p = new THREE.PointLight(0xffd29a, 1.6, 4, 2); p.position.set(x, h - 0.25, z); g.add(p); }
  }
  return g;
}

export function lamellen() {
  const g = new THREE.Group(), m = mat(0x8a6a48, { roughness: 0.7 });
  [3.2, 3.2, 3.2, 3.2, 2.6, 2.3].forEach((h, i) => { const l = new THREE.Mesh(new THREE.BoxGeometry(0.045, h, 0.05), m); l.position.set(1.45 + i * 0.16, 3.2 - h / 2, -0.75); l.castShadow = l.receiveShadow = true; g.add(l); });
  return g;
}

export function raum({ breite = 9, tiefe = 7, hoehe = 3.2, fenster = true } = {}) {
  const g = new THREE.Group();
  const boden = new THREE.Mesh(new THREE.PlaneGeometry(breite, tiefe), mat(FARBE.eiche, { roughness: 0.6 }));
  boden.rotation.x = -Math.PI / 2; boden.position.z = tiefe / 2 - 1; boden.receiveShadow = true; g.add(boden);
  const wand = new THREE.Mesh(new THREE.PlaneGeometry(breite, hoehe), mat(FARBE.leinen)); wand.position.set(0, hoehe / 2, -0.85); wand.receiveShadow = true; g.add(wand);
  const seite = new THREE.Mesh(new THREE.PlaneGeometry(tiefe, hoehe), mat(FARBE.putz)); seite.rotation.y = Math.PI / 2; seite.position.set(-breite / 2, hoehe / 2, tiefe / 2 - 1); seite.receiveShadow = true; g.add(seite);
  const decke = new THREE.Mesh(new THREE.PlaneGeometry(breite, tiefe), mat(FARBE.hell)); decke.rotation.x = Math.PI / 2; decke.position.set(0, hoehe, tiefe / 2 - 1); g.add(decke);
  const teppich = new THREE.Mesh(new THREE.PlaneGeometry(3.2, 2.2), mat(0xe4dccd, { roughness: 1 })); teppich.rotation.x = -Math.PI / 2; teppich.position.set(0, 0.005, 0.6); teppich.receiveShadow = true; g.add(teppich);
  return g;
}

export function tageslicht(szene, staerke = 1) {
  szene.add(new THREE.HemisphereLight(0xfffaf0, 0xb59a7a, 0.9 * staerke));
  const s = new THREE.DirectionalLight(0xfff1dc, 2.2 * staerke); s.position.set(4, 6, 5); s.castShadow = true;
  s.shadow.mapSize.set(2048, 2048); Object.assign(s.shadow.camera, { left: -5, right: 5, top: 5, bottom: -5 }); s.shadow.bias = -0.0005; s.shadow.radius = 6;
  szene.add(s);
}

export { THREE };
