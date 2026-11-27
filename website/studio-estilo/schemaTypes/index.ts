import { defineField, defineType } from 'sanity';

// Jedes Feld ist freiwillig: leer = die Website zeigt ihren Standardtext.
const hinweis = 'Leer lassen = Standardtext der Website.';
const text = (name: string, title: string, zeilen = 1) =>
  defineField({ name, title, type: zeilen > 1 ? 'text' : 'string', rows: zeilen > 1 ? zeilen : undefined, description: hinweis } as never);

const raum = defineType({
  name: 'raum', title: 'Raum', type: 'object',
  fields: [
    defineField({ name: 'id', title: 'Raum', type: 'string', options: { list: [
      { title: 'Wohnzimmer', value: 'wohnzimmer' }, { title: 'Schlafzimmer', value: 'schlafzimmer' },
      { title: 'Esszimmer', value: 'esszimmer' }, { title: 'Büro', value: 'buero' }] }, validation: (r) => r.required() }),
    text('satz', 'Ein Satz zum Raum', 2),
    defineField({ name: 'gruppen', title: 'Produktgruppen', type: 'array', of: [{ type: 'string' }] }),
    text('details', 'Details', 3),
  ],
  preview: { select: { title: 'id' } },
});

const seite = defineType({
  name: 'seite', title: 'Startseite', type: 'document',
  fields: [
    defineField({ name: 'heroTitel', title: 'Große Überschrift (drei Teile, der mittlere kursiv)', type: 'array', of: [{ type: 'string' }], validation: (r) => r.max(3), description: hinweis }),
    text('heroUnter', 'Text unter der Überschrift', 3),
    defineField({ name: 'raeume', title: 'Räume', type: 'array', of: [{ type: 'raum' }] }),
    text('ablaufTitel', 'Ablauf: Überschrift'),
    defineField({ name: 'schritte', title: 'Ablauf: Schritte', type: 'array', of: [{ type: 'object', fields: [text('titel', 'Titel'), text('text', 'Text', 3)] }] }),
    defineField({ name: 'ebruAbsaetze', title: 'Über Ebru: Absätze', type: 'array', of: [{ type: 'text', rows: 3 }], description: hinweis }),
    defineField({ name: 'ebruBild', title: 'Über Ebru: Foto', type: 'image', options: { hotspot: true }, description: hinweis }),
    text('besuchTitel', 'Besuch: Überschrift'),
    text('besuchText', 'Besuch: Text', 3),
  ],
});

const studio = defineType({
  name: 'studio', title: 'Studio', type: 'document',
  fields: [
    defineField({ name: 'oeffnung', title: 'Öffnungszeiten', type: 'array', of: [{ type: 'object', fields: [text('tage', 'Tage'), text('zeit', 'Zeit')], preview: { select: { title: 'tage', subtitle: 'zeit' } } }], description: hinweis }),
    text('telefonZeiten', 'Telefonische Erreichbarkeit'),
    text('parken', 'Parken'),
    text('telefon', 'Telefon'),
    text('mail', 'E-Mail'),
  ],
});

const stimmen = defineType({
  name: 'stimmen', title: 'Bewertungen', type: 'document',
  fields: [defineField({ name: 'liste', title: 'Google-Bewertungen (nur echte, Kürzungen mit […] markieren)', type: 'array', of: [{ type: 'text', rows: 5 }], description: hinweis })],
});

export const schemaTypes = [raum, seite, studio, stimmen];
