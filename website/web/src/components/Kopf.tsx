'use client';
import Link from 'next/link';
import { useEffect, useState } from 'react';
import { navigation } from '@/lib/content';

/** Kopfzeile: Logo links, Navigation rechts. Auf dem Handy ein Menü-Knopf. */
export default function Kopf({ ueberSzene = false }: { ueberSzene?: boolean }) {
  const [offen, setOffen] = useState(false);
  const [aktiv, setAktiv] = useState('');
  const [frei, setFrei] = useState(ueberSzene); // transparent nur über der 3D-Strecke
  useEffect(() => {
    if (!ueberSzene) return;
    const pruefen = () => { const w = document.getElementById('wohnwelten'); setFrei(!!w && w.getBoundingClientRect().bottom > 80); };
    pruefen(); window.addEventListener('scroll', pruefen, { passive: true });
    return () => window.removeEventListener('scroll', pruefen);
  }, [ueberSzene]);
  useEffect(() => {
    const ids = navigation.map((n) => n.href.split('#')[1]).filter(Boolean);
    const io = new IntersectionObserver((e) => e.forEach((x) => x.isIntersecting && setAktiv(x.target.id)), { rootMargin: '-45% 0px -50% 0px' });
    ids.forEach((id) => { const el = document.getElementById(id); if (el) io.observe(el); });
    return () => io.disconnect();
  }, []);
  return (
    <header className={`fixed inset-x-0 top-0 z-40 flex items-center justify-between px-4 py-4 sm:px-8 lg:px-14 lg:py-6 ${frei ? '' : 'bg-leinen'}`}>
      <Link href="/" aria-label="ESTILO Einrichtungsstudio, zur Startseite" className="block" data-logo-kopf>
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src="/estilo-logo.svg" alt="" width={1400} height={615} className="h-9 w-auto lg:h-12" style={{ opacity: 'var(--kopf-logo, 1)' as unknown as number }} />
      </Link>
      <nav aria-label="Hauptnavigation" className="hidden items-center gap-9 text-[15px] tracking-wide md:flex">
        {navigation.map((n) => {
          const an = aktiv && n.href.endsWith('#' + aktiv);
          return (
            <Link key={n.href} href={n.href} className={`relative py-2 ${an ? 'text-text' : 'text-text/80 hover:text-text'}`} aria-current={an ? 'location' : undefined}>
              {n.text}
              {an && <span aria-hidden className="absolute inset-x-0 -bottom-0.5 h-[2px] bg-gruen" />}
            </Link>
          );
        })}
      </nav>
      <button className="min-h-11 px-2 text-[15px] md:hidden" aria-expanded={offen} aria-controls="menue" onClick={() => setOffen(!offen)}>
        {offen ? 'Schließen' : 'Menü'}
      </button>
      {offen && (
        <nav id="menue" aria-label="Hauptnavigation" className="fixed inset-x-0 top-[68px] bottom-0 flex flex-col gap-2 bg-leinen px-4 pt-6 md:hidden">
          {navigation.map((n) => (
            <Link key={n.href} href={n.href} onClick={() => setOffen(false)} className="font-serif text-4xl leading-[1.4]">{n.text}</Link>
          ))}
        </nav>
      )}
    </header>
  );
}
