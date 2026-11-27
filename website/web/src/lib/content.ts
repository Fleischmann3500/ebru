// Alle Texte der Seite mit Standardwerten. Quelle: estilo.at (Stand 25.11.2026), gekürzt, nichts hinzuerfunden.
// Sanity überschreibt einzelne Felder (lib/cms/site.ts). Leeres CMS-Feld = dieser Standardtext.

export const firma = {
  name: 'ESTILO Einrichtungsstudio',
  inhaberin: 'Ebru Filiz',
  strasse: 'Am Garnmarkt 17',
  ort: '6840 Götzis',
  land: 'Österreich',
  telefon: '+43 650 2328811',
  telefonLink: 'tel:+436502328811',
  mail: 'office@estilo.at',
  oeffnung: [
    { tage: 'Montag bis Freitag', zeit: '9:00 bis 18:00' },
    { tage: 'Samstag', zeit: '9:00 bis 14:00' },
  ],
  telefonZeiten: 'Telefonisch Montag bis Samstag, 8:00 bis 19:00',
  parken: 'Kostenfrei parken in der Tiefgarage Am Garnmarkt',
  route: 'https://www.google.com/maps/dir/?api=1&destination=Am+Garnmarkt+17%2C+6840+G%C3%B6tzis',
  googleBewertungen: 'https://share.google/VfRotR9CPtWFtI6X1',
  googleBewerten: 'https://g.page/r/Ca5Ramr4LGekEAE/review',
};

export const hero = {
  titel: ['Räume, die', 'zu Ihnen', 'passen.'],
  unter: 'Polstermöbel, Betten, Schränke, Esszimmer und Büro, ausgesucht und aufeinander abgestimmt von Ebru Filiz. Am Garnmarkt 17 in Götzis.',
  knopf: 'Beratung anfragen',
  link: 'Wohnwelten ansehen',
};

export type Raum = {
  id: 'wohnzimmer' | 'schlafzimmer' | 'esszimmer' | 'buero';
  name: string;
  satz: string;
  gruppen: string[];
  details: string;
};

export const raeume: Raum[] = [
  {
    id: 'wohnzimmer',
    name: 'Wohnzimmer',
    satz: 'Polstergarnituren und Wohnwände, abgestimmt auf Ihren Raum und Ihren Stil.',
    gruppen: ['Sofas und Wohnlandschaften', 'Relaxsessel', 'Wohnwände und Sideboards'],
    details: 'Je nach Modell lassen sich Maße, Sitzgefühl und Bezug anpassen, in Stoff oder Leder. Ausgewählte Modelle gibt es mit Relax- oder Schlaffunktion.',
  },
  {
    id: 'buero',
    name: 'Büro',
    satz: 'Individuell geplante Büromöbel für klare Arbeitsbereiche und durchdachte Stauraumlösungen.',
    gruppen: ['Schreibtische', 'Regale', 'Stauraum'],
    details: 'Oberflächen, Farben und Zusammenstellungen werden auf Raum und Arbeitsabläufe abgestimmt.',
  },
  {
    id: 'esszimmer',
    name: 'Esszimmer',
    satz: 'Tische, Sitzplätze und Möbel für eine persönliche Esszimmergestaltung.',
    gruppen: ['Esstische', 'Stühle', 'Sitz- und Eckbänke'],
    details: 'Formen, Größen, Oberflächen, Gestelle und Auszüge je nach Modell, dazu passende Bezüge und Holztöne.',
  },
  {
    id: 'schlafzimmer',
    name: 'Schlafzimmer',
    satz: 'Betten und Schränke mit unterschiedlichen Materialien und Gestaltungsoptionen.',
    gruppen: ['Massivholzbetten', 'Komfortbetten', 'Schranksysteme'],
    details: 'Auch Betten mit besonderen Paneelen, integrierter Beleuchtung und Steckdosen, abgestimmt auf Ihre Maße.',
  },
];

export const sofa = {
  titel: 'Probieren Sie den Bezug.',
  text: 'Das Sofa aus unserem Logo. Drehen Sie es mit der Maus oder dem Finger und wählen Sie einen Bezug. Im Studio liegen die echten Stoffe und Leder zum Anfassen.',
  bezuege: [
    { name: 'Salbei', farbe: '#6F7F50' },
    { name: 'Cognac', farbe: '#8A5A36' },
    { name: 'Leinen', farbe: '#CFC5B4' },
    { name: 'Anthrazit', farbe: '#45463F' },
  ],
};

export const ablauf = {
  titel: 'Von der ersten Idee bis zum fertigen Zuhause.',
  schritte: [
    { titel: 'Gespräch', text: 'Jedes Einrichtungskonzept beginnt mit einem persönlichen Gespräch über Ihre Vorstellungen, Ihren Geschmack und Ihren Alltag.' },
    { titel: 'Konzept', text: 'Daraus entstehen gestalterische Einrichtungsvorschläge mit Möbel- und Materialauswahl. Grundriss- und Haustechnikplanung gehören nicht zu meinem Leistungsangebot.' },
    { titel: 'Vor Ort', text: 'Ich komme zu Ihnen, sehe mir die Räume an und nehme Maß. Gemeinsam wählen wir Farben, Materialien und Möbel passend zum Raum.' },
    { titel: 'Nach Maß', text: 'Wo Standard nicht reicht, entwerfe ich Möbel nach Maß. Technische Planung und Ausführung übernehmen befugte Fachbetriebe.' },
    { titel: 'Ihr Zuhause', text: 'Lieferung und Montage, und am Ende eine Einrichtung, in der Materialien, Farben und Möbel zusammenpassen.' },
  ],
};

export const ebru = {
  ueber: 'Die Person hinter ESTILO',
  titel: 'Ebru Filiz',
  absaetze: [
    'Seit 2001 richte ich Wohnräume ein. Vor ESTILO habe ich in verschiedenen renommierten Möbelhäusern gearbeitet, heute berate ich in meinem eigenen Studio in Götzis.',
    'Ob zeitlos elegant, klassisch oder modern und außergewöhnlich: Wir finden gemeinsam Ihren Wohnstil und Möbel, die zu Ihrem Alltag passen.',
  ],
  bild: '/bilder/ebru-filiz.webp',
  bildAlt: 'Ebru Filiz, Inhaberin von ESTILO, mit Kaffeetasse am Tisch',
};

export type Stimme = { text: string };
// Google-Bewertungen, wie auf estilo.at veröffentlicht (Verfasser neutral, Selbstnennungen entfernt). Kürzungen sind mit […] markiert.
export const stimmen: Stimme[] = [
  { text: 'Kleines aber sehr feines, exklusives Einrichtungsstudio mit Topberatung von der Chefin Ebru Filiz persönlich. Haben heute neues Sofa und Sidebord geliefert bekommen und sind total zufrieden. Die Abwicklung von Beratung, Bestellung und Auslieferung war sehr professionell, Wir können estilo nur weiterempfehlen.' },
  { text: 'Wir haben unser komplettes Haus mit estilo Einrichtungsstudio eingerichtet. Von der Planung über die Einrichtung bis zur Lieferung war alles perfekt. Die Pünktlichkeit war hervorragend, es hat alles perfekt gepasst, und die Ideen von Frau Filiz waren ebenfalls ausgezeichnet. Wir können estilo Einrichtungsstudio uneingeschränkt empfehlen. […]' },
  { text: 'Ich war bei Estilo zur Bettenvorführung und bin begeistert. Die Beratung war sehr informativ und die Inhaberin Ebru hat sich viel Zeit genommen, um alles ausführlich zu erklären und vorzuführen. Man merkt sofort, dass ihr die Zufriedenheit ihrer Kunden wichtig ist. […]' },
  { text: 'Wir kennen Frau Filitz schon einige Jahre. Vor allen Dingen hat Sie bei uns immer SEHR viel Geduld gezeigt, da sich unsere Wünsche häufig geändert haben! Wir waren mit Ihrer Beratung extrem zufrieden. Wurde etwas nicht ordnungsgemäß montiert hat sie sich darum gekümmert, dass das behoben wurde! […]' },
  { text: 'Wir sind durch Freunde auf das Estilo Einrichtungsstudio gekommen. Wir haben zuerst eine Couch und dann noch ein Bett gekauft. Ebru hat uns durch ihr fachliches Wissen, ihre Beratung und ihre Freundlichkeit begeistert. Die abgemachten Liefertermine wurden termingerecht eingehalten und die Montage super ausgeführt. […]' },
  { text: 'Kompetente und freundliche Beratung. Lieferung wie versprochen, sogar mit persönlicher Zustellung. Sehr zu empfehlen.' },
  { text: 'Estilo - ein Einrichtungsstudio die keine Wünsche offen lässt. Hervorragende Beratung durch die herzliche Inhaberin Ebru. […] Große Auswahl an Polster, Möbel, Teppichen, Betten, und Accessoires in einer exzellenten Qualität. So vieles wird auch nach Wunsch maßangefertigt. […]' },
  { text: '[…] Besonders hervorheben möchten wir den hervorragenden Service nach dem Kauf: Ebru kam persönlich bei uns vorbei, um unsere Couch zu imprägnieren und sich zu vergewissern, dass alles einwandfrei funktioniert und unseren Vorstellungen entspricht. […]' },
];
export const stimmenTitel = 'Was Kundinnen und Kunden auf Google schreiben.';

export const besuch = {
  titel: 'Kommen Sie vorbei.',
  text: 'Im Studio sehen Sie die Möbel, sitzen Probe und greifen die Stoffe an. Für eine Beratung in Ruhe schreiben Sie mir vorher kurz, wann es Ihnen passt.',
  formTitel: 'Beratung anfragen',
  danke: 'Danke, Ihre Nachricht ist angekommen. Ich melde mich bei Ihnen.',
};

export const navigation = [
  { href: '/#wohnwelten', text: 'Wohnwelten' },
  { href: '/#ablauf', text: 'Ablauf' },
  { href: '/#ebru', text: 'Über Ebru' },
  { href: '/#besuch', text: 'Besuch' },
];
