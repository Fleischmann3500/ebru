'use client';
import { useRef, useState } from 'react';
import type { firma as FirmaT } from '@/lib/content';

/** Anfrage an office@estilo.at. Ohne Scroll-Effekte. Fällt bei Fehlern auf einen Mail-Link zurück. */
export default function Formular({ danke, firma }: { danke: string; firma: typeof FirmaT }) {
  const [status, setStatus] = useState<'leer' | 'sendet' | 'ok' | 'fehler'>('leer');
  const [fehler, setFehler] = useState('');
  const geoeffnet = useRef(Date.now());

  async function senden(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const f = new FormData(e.currentTarget);
    const daten = Object.fromEntries(f.entries());
    setStatus('sendet'); setFehler('');
    try {
      const r = await fetch('/api/anfrage', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ ...daten, dauer: Date.now() - geoeffnet.current }) });
      const j = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(j.fehler || 'Senden hat nicht geklappt.');
      setStatus('ok');
    } catch (err) {
      setStatus('fehler'); setFehler((err as Error).message);
    }
  }

  if (status === 'ok') return <p role="status" className="mt-8 text-[18px]">{danke}</p>;

  const feld = 'mt-2 block w-full min-h-12 border border-text/25 bg-hell px-4 py-3 text-[16px] outline-none focus:border-text';
  return (
    <form onSubmit={senden} className="mt-8 grid gap-6" noValidate={false}>
      <label className="text-[15px]">Name<input name="name" required autoComplete="name" className={feld} /></label>
      <div className="grid gap-6 sm:grid-cols-2">
        <label className="text-[15px]">E-Mail<input name="email" type="email" required autoComplete="email" className={feld} /></label>
        <label className="text-[15px]">Telefon <span className="text-gedaempft">(freiwillig)</span><input name="telefon" type="tel" autoComplete="tel" className={feld} /></label>
      </div>
      <label className="text-[15px]">Worum geht es?
        <select name="thema" className={feld} defaultValue="Beratung im Studio">
          <option>Beratung im Studio</option><option>Beratung bei mir zu Hause</option><option>Wohnzimmer</option><option>Schlafzimmer</option><option>Esszimmer</option><option>Büro</option><option>Etwas anderes</option>
        </select>
      </label>
      <label className="text-[15px]">Nachricht<textarea name="nachricht" required rows={5} className={feld} /></label>
      {/* Falle für Bots: Menschen sehen das Feld nicht */}
      <label className="absolute -left-[9999px]" aria-hidden>Website<input name="website" tabIndex={-1} autoComplete="off" /></label>
      <p className="text-[14px] text-gedaempft">Ihre Angaben verwende ich nur für die Antwort auf Ihre Anfrage. Mehr dazu in der <a href="/datenschutz" className="textlink">Datenschutzinformation</a>.</p>
      {status === 'fehler' && (
        <p role="alert" className="text-[15px]">{fehler} Schreiben Sie direkt an <a className="textlink" href={`mailto:${firma.mail}`}>{firma.mail}</a> oder rufen Sie an: <a className="textlink" href={firma.telefonLink}>{firma.telefon}</a>.</p>
      )}
      <div><button type="submit" className="knopf" disabled={status === 'sendet'}>{status === 'sendet' ? 'Wird gesendet' : 'Anfrage abschicken'}</button></div>
    </form>
  );
}
