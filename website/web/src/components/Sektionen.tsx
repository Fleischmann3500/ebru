import Image from 'next/image';
import Link from 'next/link';
import type { Inhalt } from '@/lib/cms/site';
import Formular from './Formular';
import Stimmen from './Stimmen';

/** Ablauf: eine Linie durch fünf Stationen, wie ein Maßband an der Wand. */
export function Ablauf({ ablauf }: Pick<Inhalt, 'ablauf'>) {
  return (
    <section id="ablauf" className="px-4 py-28 sm:px-8 lg:px-14 lg:py-40">
      <h2 className="max-w-[16ch] text-[clamp(40px,5vw,84px)]">{ablauf.titel}</h2>
      <ol className="relative mt-16 grid gap-12 lg:mt-24 lg:grid-cols-5 lg:gap-8">
        <span aria-hidden className="absolute left-[7px] top-2 bottom-2 w-px bg-text/25 lg:left-0 lg:right-0 lg:top-[7px] lg:bottom-auto lg:h-px lg:w-auto" />
        {ablauf.schritte.map((s) => (
          <li key={s.titel} className="relative pl-10 lg:pl-0 lg:pt-12">
            <span aria-hidden className="absolute left-0 top-1 h-[15px] w-[15px] rounded-full border border-text/50 bg-leinen lg:top-0" />
            <h3 className="text-[clamp(28px,2.4vw,38px)]">{s.titel}</h3>
            <p className="mt-3 max-w-[34ch] text-[16px] text-gedaempft">{s.text}</p>
          </li>
        ))}
      </ol>
    </section>
  );
}

/** Ebru: großes, echtes Foto. */
export function Ebru({ ebru }: Pick<Inhalt, 'ebru'>) {
  return (
    <section id="ebru" className="grid items-end gap-10 bg-hell px-4 py-24 sm:px-8 lg:grid-cols-[minmax(0,5fr)_minmax(0,6fr)] lg:gap-20 lg:px-14 lg:py-36">
      <div className="relative aspect-[1100/1199] w-full max-w-[640px]">
        <Image src={ebru.bild} alt={ebru.bildAlt} fill sizes="(min-width: 1024px) 45vw, 100vw" className="object-cover" />
      </div>
      <div className="lg:pb-6">
        <p className="text-[15px] tracking-wide text-gedaempft">{ebru.ueber}</p>
        <h2 className="mt-3 text-[clamp(56px,7vw,120px)]">{ebru.titel}</h2>
        {ebru.absaetze.map((a) => <p key={a} className="mt-6 max-w-[46ch] text-[clamp(17px,1.3vw,20px)]">{a}</p>)}
      </div>
    </section>
  );
}

export function StimmenSektion({ stimmen, stimmenTitel, firma }: Pick<Inhalt, 'stimmen' | 'stimmenTitel' | 'firma'>) {
  return (
    <section id="stimmen" className="px-4 py-28 sm:px-8 lg:px-14 lg:py-40">
      <h2 className="max-w-[20ch] text-[clamp(34px,3.6vw,60px)]">{stimmenTitel}</h2>
      <Stimmen stimmen={stimmen} />
      <p className="mt-10 flex flex-wrap gap-x-8 gap-y-3 text-[15px]">
        <a className="textlink py-2" href={firma.googleBewertungen} target="_blank" rel="noopener noreferrer">Alle Bewertungen auf Google</a>
        <a className="textlink py-2" href={firma.googleBewerten} target="_blank" rel="noopener noreferrer">ESTILO auf Google bewerten</a>
      </p>
    </section>
  );
}

/** Besuch: Adresse, Zeiten, Parken und Anfrage auf einer Karte. */
export function Besuch({ besuch, firma }: Pick<Inhalt, 'besuch' | 'firma'>) {
  return (
    <section id="besuch" className="bg-text px-4 py-24 text-hell sm:px-8 lg:px-14 lg:py-36">
      <div className="grid gap-16 lg:grid-cols-2 lg:gap-24">
        <div>
          <h2 className="text-[clamp(52px,6.4vw,110px)]">{besuch.titel}</h2>
          <p className="mt-6 max-w-[40ch] text-[clamp(17px,1.3vw,20px)] text-hell/85">{besuch.text}</p>
          <address className="mt-12 not-italic text-[18px] leading-relaxed">
            {firma.name}<br />{firma.strasse}<br />{firma.ort}
          </address>
          <table className="mt-8 text-[16px]">
            <caption className="sr-only">Öffnungszeiten</caption>
            <tbody>
              {firma.oeffnung.map((o) => (
                <tr key={o.tage}><th scope="row" className="py-1 pr-8 text-left font-light text-hell/70">{o.tage}</th><td className="py-1">{o.zeit}</td></tr>
              ))}
            </tbody>
          </table>
          <p className="mt-6 text-[16px] text-hell/70">{firma.telefonZeiten}<br />{firma.parken}</p>
          <p className="mt-10 flex flex-wrap gap-x-8 gap-y-3 text-[17px]">
            <a className="textlink py-2" href={firma.telefonLink}>{firma.telefon}</a>
            <a className="textlink py-2" href={`mailto:${firma.mail}`}>{firma.mail}</a>
            <a className="textlink py-2" href={firma.route} target="_blank" rel="noopener noreferrer">Route planen</a>
          </p>
        </div>
        <div className="bg-leinen p-6 text-text sm:p-10">
          <h3 className="text-[clamp(32px,3vw,48px)]">{besuch.formTitel}</h3>
          <Formular danke={besuch.danke} firma={firma} />
        </div>
      </div>
    </section>
  );
}

export function Fuss() {
  return (
    <footer className="flex flex-col gap-6 px-4 py-10 text-[14px] text-gedaempft sm:flex-row sm:items-center sm:justify-between sm:px-8 lg:px-14">
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img src="/estilo-logo.svg" alt="ESTILO Einrichtungsstudio" width={1400} height={615} className="h-10 w-auto text-text" />
      <nav aria-label="Rechtliches" className="flex gap-8">
        <Link href="/impressum" className="py-2">Impressum</Link>
        <Link href="/datenschutz" className="py-2">Datenschutz</Link>
        <Link href="/wohnwelten" className="py-2">Wohnwelten</Link>
      </nav>
      <p>© {new Date().getFullYear()} ESTILO Einrichtungsstudio, Götzis</p>
    </footer>
  );
}
