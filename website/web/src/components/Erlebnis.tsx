'use client';
// Einstieg und Wohnwelten: das Logo wird Raum, dann führt die Kamera durch die Wohnung.
import Link from 'next/link';
import { memo, useEffect, useRef, useState } from 'react';
import type { Inhalt } from '@/lib/cms/site';
import type { Welt } from './welt/Welt';

// Zeitachse in Bildschirmhöhen (Scroll)
const MORPH = 1.0;        // Logo fliegt in den Raum
const HALT_HERO = 0.7;    // Hero-Text steht
const STATIONEN = 6;      // Logo-Wand, Wohnen, Sofa, Schlafen, Essen, Büro
const FAHRT = 0.55;       // Anteil einer Einheit, in dem die Kamera fährt (Rest: Halt zum Lesen)
const GESAMT = MORPH + HALT_HERO + (STATIONEN - 1) + 0.6;

const glatt = (x: number) => { const t = Math.min(1, Math.max(0, x)); return t * t * (3 - 2 * t); };
const GRUPPEN = ['sofa', 'leuchten', 'lamellen', 'schrift'] as const;
const ZIELE: Record<string, string[]> = {
  sofa: ['sofa'],
  leuchten: ['pendel_0', 'pendel_1', 'pendel_2', 'pendel_kabel_0', 'pendel_kabel_1', 'pendel_kabel_2'],
  lamellen: ['lamelle_0', 'lamelle_1', 'lamelle_2', 'lamelle_3', 'lamelle_4', 'lamelle_5'],
};
const POSTER = ['station_0_logo', 'station_1_wohnen', 'station_1b_sofa', 'station_2_schlafen', 'station_3_essen', 'station_4_buero'];

type Rect = { x: number; y: number; w: number; h: number };

export default function Erlebnis({ logoSvg, hero, raeume, sofa: sofaText }: { logoSvg: string } & Pick<Inhalt, 'hero' | 'raeume' | 'sofa'>) {
  const huelle = useRef<HTMLElement>(null);
  const canvas = useRef<HTMLCanvasElement>(null);
  const logo = useRef<HTMLDivElement>(null);
  const welt = useRef<Welt | null>(null);
  const [p, setP] = useState(0);            // Kamerafortschritt (0 .. STATIONEN-1)
  const [m, setM] = useState(0);            // Logo-Übergang (0 .. 1)
  const [geladen, setGeladen] = useState(false);
  const [ohne3d, setOhne3d] = useState(false);
  const [bezug, setBezug] = useState<string | null>(null);
  const [laden, setLaden] = useState(0);
  const start = useRef<Record<string, Rect>>({});
  const ziel = useRef<Record<string, Rect | null>>({});

  // Welt laden (nur im Browser, three.js als eigener Teil)
  useEffect(() => {
    const c = canvas.current; if (!c) return;
    const gl = c.getContext('webgl2');
    if (!gl) { setOhne3d(true); return; }
    let aus = false;
    const handy = window.matchMedia('(max-width: 760px)').matches || navigator.hardwareConcurrency <= 2;
    const ruhig = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    import('./welt/Welt').then(async ({ Welt }) => {
      const w = new Welt({ canvas: c, handy, ruhig, onFortschritt: setLaden });
      try { await w.laden(); } catch (e) { console.error(e); setOhne3d(true); return; }
      if (aus) { w.entsorgen(); return; }
      welt.current = w; w.groesse(); w.start(); setGeladen(true);
      (window as unknown as { __welt?: Welt }).__welt = w;
      messen();
    }).catch(() => setOhne3d(true));
    const onResize = () => { welt.current?.groesse(); messen(); };
    window.addEventListener('resize', onResize);
    return () => { aus = true; window.removeEventListener('resize', onResize); welt.current?.entsorgen(); welt.current = null; };
    // messen() liest nur Refs, darf beim Laden einmal laufen
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Start- und Zielrechtecke für den Logo-Übergang
  function messen() {
    const box = logo.current; if (!box) return;
    for (const g of GRUPPEN) {
      const el = box.querySelector<SVGGElement>(`#logo-${g}`); if (!el) continue;
      el.style.transform = ''; const r = el.getBoundingClientRect();
      start.current[g] = { x: r.left, y: r.top, w: r.width, h: r.height };
    }
    const w = welt.current;
    if (w) {
      w.setFortschritt(0); w.setVersatz(0); w.groesse();
      for (const g of ['sofa', 'leuchten', 'lamellen']) ziel.current[g] = w.rechteck(ZIELE[g]);
    }
    const kopf = document.querySelector('[data-logo-kopf] img')?.getBoundingClientRect();
    if (kopf && start.current.schrift) {
      // Schriftzug fliegt an seine Stelle im Kopf-Logo (dort rechts im Logo)
      const s = start.current, gesamt = { x: s.sofa.x, w: s.schrift.x + s.schrift.w - s.sofa.x };
      const k = kopf.width / gesamt.w;
      ziel.current.schrift = { x: kopf.left + (s.schrift.x - gesamt.x) * k, y: kopf.top + (s.schrift.y - s.leuchten.y) * k, w: s.schrift.w * k, h: s.schrift.h * k };
    }
    anwenden(mRef.current);
  }

  const mRef = useRef(0);
  function anwenden(mm: number) {
    const box = logo.current; if (!box) return;
    const e = glatt(mm);
    for (const g of GRUPPEN) {
      const el = box.querySelector<SVGGElement>(`#logo-${g}`); const a = start.current[g]; const z = ziel.current[g];
      if (!el || !a) continue;
      if (!z) { el.style.transform = ''; continue; }
      const sx = 1 + (z.w / a.w - 1) * e, sy = 1 + (z.h / a.h - 1) * e;
      const dx = (z.x - a.x) * e, dy = (z.y - a.y) * e;
      el.style.transformBox = 'fill-box'; el.style.transformOrigin = '0 0';
      el.style.transform = `translate(${dx / (a.w / el.getBBox().width)}px, ${dy / (a.h / el.getBBox().height)}px) scale(${sx}, ${sy})`;
    }
  }

  // Scroll -> Zeitachse
  useEffect(() => {
    let raf = 0;
    const tick = () => {
      raf = 0;
      const h = huelle.current; if (!h) return;
      const vh = window.innerHeight;
      const u = Math.max(0, -h.getBoundingClientRect().top) / vh;
      const mm = Math.min(1, u / MORPH);
      const rest = u - MORPH - HALT_HERO;
      let pp = 0;
      if (rest > 0) { const i = Math.floor(rest), f = rest - i; pp = Math.min(STATIONEN - 1, i + glatt(f / FAHRT)); }
      mRef.current = mm; setM(mm); setP(pp); anwenden(mm);
      document.documentElement.style.setProperty('--kopf-logo', String(glatt((mm - 0.9) / 0.1)));
      const w = welt.current;
      if (w) {
        w.setFortschritt(pp);
        const breit = window.innerWidth >= 900;
        w.setVersatz(breit ? glatt((u - MORPH - 0.05) / 0.5) * window.innerWidth * 0.17 : 0);
        w.setSichtbar(u < GESAMT + 1.2);
      }
    };
    const onScroll = () => { if (!raf) raf = requestAnimationFrame(tick); };
    tick(); window.addEventListener('scroll', onScroll, { passive: true });
    return () => { window.removeEventListener('scroll', onScroll); cancelAnimationFrame(raf); };
  }, []);

  // Sofa drehen: Ziehen auf der Szene (nur an der Sofa-Station), dazu Knöpfe als zweiter Weg
  const amSofa = Math.abs(p - 2) < 0.35;
  useEffect(() => {
    const c = canvas.current; if (!c || !amSofa) return;
    let x0: number | null = null;
    const ab = (e: PointerEvent) => { x0 = e.clientX; c.setPointerCapture(e.pointerId); };
    const zug = (e: PointerEvent) => { if (x0 === null) return; welt.current?.drehen((e.clientX - x0) * 0.01); x0 = e.clientX; };
    const auf = () => { x0 = null; };
    c.addEventListener('pointerdown', ab); c.addEventListener('pointermove', zug); c.addEventListener('pointerup', auf); c.addEventListener('pointercancel', auf);
    return () => { c.removeEventListener('pointerdown', ab); c.removeEventListener('pointermove', zug); c.removeEventListener('pointerup', auf); c.removeEventListener('pointercancel', auf); };
  }, [amSofa]);
  useEffect(() => {
    const bewegen = (e: PointerEvent) => welt.current?.setMaus(e.clientX / window.innerWidth * 2 - 1, e.clientY / window.innerHeight * 2 - 1);
    window.addEventListener('pointermove', bewegen, { passive: true });
    return () => window.removeEventListener('pointermove', bewegen);
  }, []);
  useEffect(() => { welt.current?.setBezug(bezug); }, [bezug]);

  const sichtbar = (k: number) => 1 - glatt((Math.abs(p - k) - 0.12) / 0.2);
  const szeneDeckkraft = geladen ? glatt((m - 0.25) / 0.5) : 0;
  const posterIndex = Math.round(p);

  return (
    <section ref={huelle} id="wohnwelten" aria-label="Wohnwelten" className="relative" style={{ height: `${(GESAMT + 1) * 100}svh` }}>
      <div className="sticky top-0 h-svh overflow-hidden">
        {/* Rückfall ohne WebGL (oder solange die Szene lädt): fertige Renders aus Blender */}
        {(ohne3d || !geladen) && m > 0.3 && (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={`/welt/stationen/${POSTER[posterIndex]}.webp`} alt="" className="absolute inset-0 h-full w-full object-cover" style={{ opacity: glatt((m - 0.3) / 0.4) }} />
        )}
        <canvas ref={canvas} className={`absolute inset-0 h-full w-full ${amSofa ? 'cursor-grab touch-pan-y active:cursor-grabbing' : ''}`} style={{ opacity: szeneDeckkraft }} aria-hidden />
        {/* Leinen-Verlauf links für die Texte (nur Desktop) */}
        <div aria-hidden className="pointer-events-none absolute inset-y-0 left-0 hidden w-[52vw] bg-gradient-to-r from-leinen via-leinen/85 to-transparent lg:block" style={{ opacity: glatt((m - 0.6) / 0.4) }} />
        <div aria-hidden className="pointer-events-none absolute inset-x-0 bottom-0 h-[58svh] bg-gradient-to-t from-leinen via-leinen/90 to-transparent lg:hidden" style={{ opacity: glatt((m - 0.6) / 0.4) }} />

        {/* Das Logo: die Gruppen fliegen auf Sofa, Leuchten und Lamellen im Raum */}
        <div ref={logo} aria-hidden className="pointer-events-none absolute left-1/2 top-[47%] w-[min(86vw,1080px)] -translate-x-1/2 -translate-y-1/2 text-text [&_svg]:block [&_svg]:h-auto [&_svg]:w-full [&_svg]:overflow-visible"
          style={{ opacity: 1 - glatt((m - 0.82) / 0.18) }}><LogoSvg svg={logoSvg} /></div>
        <h1 className="sr-only">ESTILO Einrichtungsstudio in Götzis</h1>
        {!geladen && !ohne3d && laden > 0 && laden < 1 && (
          <div aria-hidden className="absolute bottom-6 left-1/2 h-px w-40 -translate-x-1/2 bg-text/15"><div className="h-px bg-text/60" style={{ width: `${laden * 100}%` }} /></div>
        )}

        {/* Texte zu den Stationen */}
        <Tafel deckkraft={glatt((m - 0.85) / 0.15) * sichtbar(0)}>
          <p className="font-serif text-[clamp(52px,7.4vw,124px)] leading-[0.92]">{hero.titel[0]}<br /><em>{hero.titel[1]}</em> {hero.titel[2]}</p>
          <p className="mt-6 max-w-[34ch] text-[clamp(16px,1.25vw,19px)] text-gedaempft">{hero.unter}</p>
          <div className="mt-8 flex flex-wrap items-center gap-x-8 gap-y-4">
            <a href="#besuch" className="knopf">{hero.knopf}</a>
            <Link href="/wohnwelten" className="textlink py-3">{hero.link}</Link>
          </div>
        </Tafel>
        {raeume.map((r, i) => {
          const k = i === 0 ? 1 : i + 2;
          return (
            <Tafel key={r.id} deckkraft={sichtbar(k)}>
              <h2 className="text-[clamp(44px,5.6vw,92px)]">{r.name}</h2>
              <p className="mt-5 max-w-[36ch] text-[clamp(17px,1.3vw,20px)]">{r.satz}</p>
              <ul className="mt-6 space-y-1 text-[15px] text-gedaempft">{r.gruppen.map((g) => <li key={g}>{g}</li>)}</ul>
              <p className="mt-6 max-w-[40ch] text-[15px] text-gedaempft">{r.details}</p>
              <Link href={`/wohnwelten#${r.id}`} className="textlink mt-7 inline-block py-2">Bilder: {r.name}</Link>
            </Tafel>
          );
        })}
        <Tafel deckkraft={sichtbar(2)}>
          <h2 className="text-[clamp(40px,4.8vw,80px)]">{sofaText.titel}</h2>
          <p className="mt-5 max-w-[38ch] text-[clamp(16px,1.2vw,19px)] text-gedaempft">{sofaText.text}</p>
          <div className="mt-7 flex flex-wrap gap-3" role="radiogroup" aria-label="Bezug">
            {sofaText.bezuege.map((b, i) => {
              const an = (bezug ?? sofaText.bezuege[0].farbe) === b.farbe;
              return (
                <button key={b.name} role="radio" aria-checked={an} onClick={() => setBezug(i === 0 ? null : b.farbe)}
                  className={`flex min-h-11 items-center gap-3 border px-3 text-[14px] ${an ? 'border-gruen' : 'border-text/20'}`}>
                  <span aria-hidden className="h-5 w-5 rounded-full" style={{ background: b.farbe }} />{b.name}
                </button>
              );
            })}
          </div>
          <div className="mt-4 flex gap-3 text-[14px]">
            <button className="min-h-11 border border-text/20 px-4" onClick={() => welt.current?.drehen(-Math.PI / 4)}>Nach links drehen</button>
            <button className="min-h-11 border border-text/20 px-4" onClick={() => welt.current?.drehen(Math.PI / 4)}>Nach rechts drehen</button>
          </div>
        </Tafel>
      </div>
    </section>
  );
}

// Eigene, gemerkte Komponente: React darf das SVG beim Scrollen nicht neu einsetzen (sonst gehen die Transformationen verloren)
const LogoSvg = memo(function LogoSvg({ svg }: { svg: string }) {
  return <div dangerouslySetInnerHTML={{ __html: svg }} />;
});

function Tafel({ deckkraft, children }: { deckkraft: number; children: React.ReactNode }) {
  if (deckkraft <= 0.01) return null;
  return (
    <div className="absolute inset-x-4 bottom-8 sm:inset-x-8 lg:inset-x-auto lg:bottom-auto lg:left-14 lg:top-1/2 lg:w-[min(40vw,620px)] lg:-translate-y-1/2"
      style={{ opacity: deckkraft, transform: undefined }}>
      {children}
    </div>
  );
}
