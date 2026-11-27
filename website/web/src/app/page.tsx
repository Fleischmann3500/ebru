import { readFileSync } from 'node:fs';
import path from 'node:path';
import Kopf from '@/components/Kopf';
import Erlebnis from '@/components/Erlebnis';
import SmoothScroll from '@/components/SmoothScroll';
import { Ablauf, Besuch, Ebru, Fuss, StimmenSektion } from '@/components/Sektionen';
import { getInhalt } from '@/lib/cms/site';

export const revalidate = 120;

const logoSvg = readFileSync(path.join(process.cwd(), 'public', 'estilo-logo.svg'), 'utf8');

export default async function Startseite() {
  const i = await getInhalt();
  return (
    <>
      <SmoothScroll />
      <Kopf ueberSzene />
      <main id="inhalt">
        <Erlebnis logoSvg={logoSvg} hero={i.hero} raeume={i.raeume} sofa={i.sofa} />
        <Ablauf ablauf={i.ablauf} />
        <Ebru ebru={i.ebru} />
        <StimmenSektion stimmen={i.stimmen} stimmenTitel={i.stimmenTitel} firma={i.firma} />
        <Besuch besuch={i.besuch} firma={i.firma} />
      </main>
      <Fuss />
    </>
  );
}
