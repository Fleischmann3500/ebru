'use client';
import { useState } from 'react';
import type { Stimme } from '@/lib/content';

/** Ein Zitat groß, darunter Blättern. Kein automatisches Weiterlaufen. */
export default function Stimmen({ stimmen }: { stimmen: Stimme[] }) {
  const [i, setI] = useState(0);
  const s = stimmen[i];
  return (
    <figure className="mt-14 lg:mt-20">
      <blockquote aria-live="polite" className="max-w-[44ch] font-serif text-[clamp(26px,2.6vw,44px)] leading-[1.22]">
        <p>„{s.text}“</p>
      </blockquote>
      <figcaption className="mt-6 text-[15px] text-gedaempft">Google-Bewertung</figcaption>
      <div className="mt-10 flex items-center gap-4 text-[15px]">
        <button className="min-h-11 border border-text/25 px-5" onClick={() => setI((i - 1 + stimmen.length) % stimmen.length)} aria-label="Vorherige Bewertung">Zurück</button>
        <button className="min-h-11 border border-text/25 px-5" onClick={() => setI((i + 1) % stimmen.length)} aria-label="Nächste Bewertung">Weiter</button>
      </div>
    </figure>
  );
}
