// Inhalte aus Sanity, Feld für Feld mit den Standardtexten aus content.ts zusammengeführt.
// Ohne NEXT_PUBLIC_SANITY_PROJECT_ID (oder bei einem Fehler) gelten nur die Standardtexte.
import { createClient } from 'next-sanity';
import imageUrlBuilder from '@sanity/image-url';
import * as std from '@/lib/content';

export type Inhalt = {
  firma: typeof std.firma; hero: typeof std.hero; raeume: std.Raum[]; sofa: typeof std.sofa;
  ablauf: typeof std.ablauf; ebru: typeof std.ebru; stimmen: std.Stimme[]; stimmenTitel: string; besuch: typeof std.besuch;
};

const projectId = process.env.NEXT_PUBLIC_SANITY_PROJECT_ID;
const dataset = process.env.NEXT_PUBLIC_SANITY_DATASET || 'production';
const voll = (s: unknown): s is string => typeof s === 'string' && s.trim().length > 0;
const oder = (s: unknown, d: string) => (voll(s) ? s.trim() : d);

type Roh = {
  seite?: { heroTitel?: string[]; heroUnter?: string; raeume?: { id: string; satz?: string; gruppen?: string[]; details?: string }[];
    ablaufTitel?: string; schritte?: { titel?: string; text?: string }[]; ebruAbsaetze?: string[]; ebruBild?: unknown; besuchTitel?: string; besuchText?: string };
  studio?: { oeffnung?: { tage?: string; zeit?: string }[]; telefonZeiten?: string; parken?: string; telefon?: string; mail?: string };
  stimmen?: { liste?: string[] };
};

export function standard(): Inhalt {
  return { firma: std.firma, hero: std.hero, raeume: std.raeume, sofa: std.sofa, ablauf: std.ablauf, ebru: std.ebru, stimmen: std.stimmen, stimmenTitel: std.stimmenTitel, besuch: std.besuch };
}

export async function getInhalt(): Promise<Inhalt> {
  const d = standard();
  if (!projectId) return d;
  try {
    const client = createClient({ projectId, dataset, apiVersion: '2025-01-01', useCdn: true });
    const r = await client.fetch<Roh>(`{ "seite": *[_id == "seite"][0], "studio": *[_id == "studio"][0], "stimmen": *[_id == "stimmen"][0] }`, {}, { next: { revalidate: 120 } });
    const s = r.seite ?? {}, st = r.studio ?? {};
    const titel = s.heroTitel?.filter(voll);
    const telefon = oder(st.telefon, d.firma.telefon);
    const bild = s.ebruBild ? imageUrlBuilder({ projectId, dataset }).image(s.ebruBild as never).width(1100).url() : null;
    return {
      ...d,
      firma: { ...d.firma, telefon, telefonLink: 'tel:' + telefon.replace(/[^+\d]/g, ''), mail: oder(st.mail, d.firma.mail),
        oeffnung: (() => { const o = (st.oeffnung ?? []).filter((x) => voll(x.tage) && voll(x.zeit)).map((x) => ({ tage: x.tage!, zeit: x.zeit! })); return o.length ? o : d.firma.oeffnung; })(),
        telefonZeiten: oder(st.telefonZeiten, d.firma.telefonZeiten), parken: oder(st.parken, d.firma.parken) },
      hero: { ...d.hero, titel: titel?.length === 3 ? titel : d.hero.titel, unter: oder(s.heroUnter, d.hero.unter) },
      raeume: d.raeume.map((raum) => {
        const c = s.raeume?.find((x) => x.id === raum.id);
        return c ? { ...raum, satz: oder(c.satz, raum.satz), details: oder(c.details, raum.details), gruppen: c.gruppen?.filter(voll).length ? c.gruppen.filter(voll) : raum.gruppen } : raum;
      }),
      ablauf: { titel: oder(s.ablaufTitel, d.ablauf.titel),
        schritte: s.schritte?.filter((x) => voll(x.titel) && voll(x.text)).length ? s.schritte.filter((x) => voll(x.titel) && voll(x.text)).map((x) => ({ titel: x.titel!, text: x.text! })) : d.ablauf.schritte },
      ebru: { ...d.ebru, absaetze: s.ebruAbsaetze?.filter(voll).length ? s.ebruAbsaetze.filter(voll) : d.ebru.absaetze, bild: bild ?? d.ebru.bild },
      stimmen: r.stimmen?.liste?.filter(voll).length ? r.stimmen.liste.filter(voll).map((text) => ({ text })) : d.stimmen,
      besuch: { ...d.besuch, titel: oder(s.besuchTitel, d.besuch.titel), text: oder(s.besuchText, d.besuch.text) },
    };
  } catch (e) {
    console.error('Sanity nicht erreichbar, Standardtexte', e);
    return d;
  }
}
