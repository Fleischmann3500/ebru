import type { Metadata } from 'next';
import Link from 'next/link';
import Kopf from '@/components/Kopf';
import { Fuss } from '@/components/Sektionen';
import { raeume } from '@/lib/content';
import galerie from '@/lib/galerie.json';

export const metadata: Metadata = { title: 'Wohnwelten', description: 'Wohnzimmer, Schlafzimmer, Esszimmer und Büro: Einrichtungsideen und Modelle aus dem Sortiment von ESTILO in Götzis.' };

const alt = (a: string) => [...new Set(a.split(', '))].join(', ');

export default function Wohnwelten() {
  return (
    <>
      <Kopf />
      <main id="inhalt" className="px-4 pt-32 sm:px-8 lg:px-14 lg:pt-44">
        <h1 className="text-[clamp(56px,8vw,140px)]">Wohnwelten</h1>
        <p className="mt-6 max-w-[48ch] text-[clamp(17px,1.3vw,20px)] text-gedaempft">
          Modelle aus dem Sortiment. Welche Ausführungen, Maße und Bezüge es jeweils gibt, klären wir gemeinsam in der Beratung.
        </p>
        <nav aria-label="Räume" className="mt-10 flex flex-wrap gap-x-8 gap-y-2 text-[16px]">
          {raeume.map((r) => <a key={r.id} href={`#${r.id}`} className="textlink py-2">{r.name}</a>)}
        </nav>
        {raeume.map((r) => (
          <section key={r.id} id={r.id} className="scroll-mt-28 border-t border-text/15 pt-12 mt-24 first-of-type:mt-20">
            <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_minmax(0,2fr)] lg:gap-16">
              <div className="lg:sticky lg:top-32 lg:self-start">
                <h2 className="text-[clamp(44px,5vw,84px)]">{r.name}</h2>
                <p className="mt-4 max-w-[36ch] text-[18px]">{r.satz}</p>
                <p className="mt-4 max-w-[40ch] text-[15px] text-gedaempft">{r.details}</p>
                <Link href="/#besuch" className="knopf mt-8">Beratung anfragen</Link>
              </div>
              <div>
                {galerie.filter((g) => g.raum === r.id).map((g) => (
                  <div key={g.titel} className="mb-16">
                    <h3 className="mb-6 text-[clamp(28px,2.4vw,40px)]">{g.titel}</h3>
                    <div className="columns-1 gap-4 sm:columns-2 [&>*]:mb-4">
                      {g.bilder.map((b) => (
                        // eslint-disable-next-line @next/next/no-img-element
                        <img key={b.src} src={`${b.src}-klein.webp`} srcSet={`${b.src}-klein.webp 720w, ${b.src}.webp 1400w`} sizes="(min-width: 1024px) 32vw, (min-width: 640px) 50vw, 100vw"
                          width={b.w} height={b.h} alt={alt(b.alt)} loading="lazy" decoding="async" className="block h-auto w-full" />
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </section>
        ))}
      </main>
      <div className="mt-24"><Fuss /></div>
    </>
  );
}
