import Kopf from './Kopf';
import { Fuss } from './Sektionen';

/** Rechtsseiten: ruhig, ohne Scroll-Effekte. */
export default function Rechtsseite({ titel, stand, children }: { titel: string; stand: string; children: React.ReactNode }) {
  return (
    <>
      <Kopf />
      <main id="inhalt" className="px-4 pb-24 pt-32 sm:px-8 lg:px-14 lg:pt-44">
        <h1 className="text-[clamp(48px,6vw,96px)]">{titel}</h1>
        <p className="mt-4 text-[14px] text-gedaempft">Stand {stand}</p>
        <div className="recht mt-12 max-w-[72ch] text-[16px] leading-[1.7] [&_h2]:mt-14 [&_h2]:text-[32px] [&_h3]:mt-8 [&_h3]:text-[24px] [&_p]:mt-4 [&_a]:underline [&_a]:underline-offset-4 [&_th]:py-1 [&_th]:pr-6 [&_th]:text-left [&_th]:align-top [&_th]:font-normal [&_th]:text-gedaempft [&_td]:py-1 [&_table]:mt-4">
          {children}
        </div>
      </main>
      <Fuss />
    </>
  );
}
