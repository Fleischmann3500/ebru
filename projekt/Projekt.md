# ESTILO Einrichtungsstudio · Website

**Stand (27.11.2026):** Erste vollständige Fassung gebaut: Blender-Wohnung mit gebackenem Licht, Website mit Übergang Logo → Raum, Kamerafahrt durch vier Räume, Sofa zum Drehen, Ablauf, Ebru, Google-Stimmen, Besuch mit Formular, Galerie, Impressum, Datenschutz, Sanity-Studio. Noch nicht live. Größtes offenes Thema: Preis vereinbaren, dann Vertrag.

**Status:** Umsetzung
**Geld:** Preis noch nicht vereinbart · bezahlt 0 € · offen 0 € · Ausgaben 0 €

---

## Kunde

| Feld | Wert |
| --- | --- |
| Firma | ESTILO Einrichtungsstudio (Einzelunternehmen, ohne Firmenbucheintrag) |
| Inhaberin | Ebru Filiz |
| Adresse | Am Garnmarkt 17, 6840 Götzis, Österreich |
| Telefon | +43 650 2328811 (telefonisch Mo–Sa 08:00–19:00) |
| E-Mail | office@estilo.at |
| Öffnungszeiten | Mo–Fr 9:00–18:00, Sa 9:00–14:00 · kostenfrei parken in der Tiefgarage Am Garnmarkt |
| UID | ATU80845757 |
| Gewerbe | Gestalterische Einrichtungsvorschläge (GISA 37267223), Handelsgewerbe (GISA 37267285), BH Feldkirch, WK Vorarlberg |
| Google | Bewertungen: https://share.google/VfRotR9CPtWFtI6X1 · Bewerten: https://g.page/r/Ca5Ramr4LGekEAE/review |
| Alte Seite | https://estilo.at (Astro auf Netlify, Stand 25.11.2026) |

Was sie macht: Möbelhandel und persönliche Einrichtungsberatung (Wohnzimmer, Schlafzimmer, Esszimmer, Büro), Maßanfertigungen über Fachbetriebe. Seit 2001 in der Branche.

**Gewerberechtlich wichtig:** Ebru darf Einrichtungsvorschläge nur „nach rein optischen und geschmacklichen Gesichtspunkten“ machen, **keine Grundriss- und Haustechnikplanung**. Die Seite darf nie „Planung“ im Sinne von Grundriss versprechen (deshalb kein Grundriss-Motiv in der 3D-Szene).

## Antworten aus den Fragen

| Thema | Antwort |
| --- | --- |
| Für wen | Kunde bezahlt |
| Ziel | estilo.at als moderne, 3D-animierte Seite neu bauen, mit Blender |
| Geld über die Seite | nein, nur Anfrage |
| Rechtsraum | Österreich (Impressum § 5 ECG + Offenlegung § 25 MedienG) |
| Angebote/Preise | wie auf der alten Seite: Leistungen und Wohnwelten, **ohne Preise** (es gibt online keine) |
| Referenzen | 18 Google-Bewertungen (anonym „ESTILO-Kunde“). Bilder unter „Referenzen“ sind laut alter Seite **keine** Kundenprojekte, sondern Inspirationsmotive |
| Assets | Bilder der alten Seite (Herstellerbilder + Foto von Ebru), Logo als großes PNG (4465 × 1961, hell und dunkel), Domain und E-Mail vorhanden |
| Vorbilder | keine, Entscheidung bei mir |
| Stil | Editorial ruhig |
| Farben | Grund `#F3EEE7` Leinen · Papier `#FFFDF9` · Akzent `#6E8450` Sofa-Grün · Text `#24251F` |
| Schrift | Cormorant Garamond (Überschriften) + Jost (Text), lokal über @fontsource |
| Bewegung | ruhig gleiten |
| Leitmotiv | **Das Logo wird Raum** |
| 3D | begehbare Echtzeit-Szene (Blender, gebackenes Licht, Three.js) + Objekt zum Anfassen |
| Poly Haven | ja |
| Ton | nein |
| CMS | Sanity-Studio |
| Formular | Resend-Mail an office@estilo.at |
| Hosting | Vercel |
| Code-Ordner | Repo `fleischmann3500/ebru`, Ordner `website/` (Rechner war nicht erreichbar) |
| Deadline / Stunden | ❓ |
| Notion | nicht angelegt (Notion-Verbindung fehlgeschlagen) |
| Anzahlung | keine |
| Korrekturrunden | 2 |
| Preis / Stundensatz | ❓ noch nicht vereinbart |

## Entscheidungen

| Datum | Was | Warum |
| --- | --- | --- |
| 27.11.2026 | Leistungen ohne Preise | Auf der alten Seite stehen keine Preise; nichts erfinden |
| 27.11.2026 | Inspirationsbilder bleiben als solche gekennzeichnet | Alte Seite sagt ausdrücklich „kein dokumentiertes Kundenprojekt“ |
| 27.11.2026 | Ablage im Repo statt Onur-Websiten | Rechner in der Sitzung nicht erreichbar; später übertragen |
| 27.11.2026 | Eigene Cloud-Umgebung „ebru“ | estilo.at war im Standard-Netz gesperrt |
| 27.11.2026 | Hero: A + C (Logo wird Raum per Dolly-Zoom, Sofa zum Drehen an der Wohnzimmer-Station) | Leitmotiv aus dem eigenen Logo, beide 3D-Wünsche in einer Geschichte |
| 27.11.2026 | Knopf in `#56683E` statt `#6E8450` | Heller Text auf `#6E8450` nur ca. 4,4 : 1, AA verlangt 4,5 |
| 27.11.2026 | Einstieg als Match-Cut statt Dolly-Zoom | Mit echtem Gebäude sähe man beim Dolly-Zoom über und unter dem Raum ins Freie; so fliegen die Logo-Teile direkt auf Sofa, Leuchten, Lamellen |
| 27.11.2026 | Hauptmöbel selbst modelliert, Poly Haven nur für Sessel, Lowboard, Pflanzen, Deko | Poly-Haven-Möbel sind fast alle antik/rustikal, passen nicht zu ESTILO |
| 27.11.2026 | Keine Google-Karte, nur Link „Route planen“ | Kein Einwilligungsbanner nötig, keine Verbindung zu Google beim Laden |
| 27.11.2026 | Sitemap: `/`, `/wohnwelten`, `/impressum`, `/datenschutz` | Kein Shop, Formular ohne Upload, Galerie der alten Seite braucht Platz |
| 27.11.2026 | Startseite: Logo wird Raum, Wohnwelten (4 Kamerastationen), 5 Schritte, Ebru, Stimmen, Besuch + Formular | Reihenfolge wie ein Besuch im Studio: ansehen, verstehen, kennenlernen, vorbeikommen |

## Offen

- ❓ Datenschutz: Anbieterangaben und AV-Verträge von Vercel und Resend vor Livegang prüfen (Text steht in `website/web/src/app/datenschutz/page.tsx`), Resend-Domain estilo.at verifizieren
- ❓ Sanity-Projekt anlegen (Konto auf Ebru), Projekt-ID in Vercel eintragen
- ❓ Bewertungen: Erlaubnis der Verfasser gilt laut alter Seite; Kürzungen sind mit […] markiert, ok für Ebru?

- ❓ Preis, Stundensatz → danach Vertrag (3.4)
- ❓ Deadline und Stunden pro Woche
- ❓ Nutzungsrecht der Herstellerbilder (Himolla, Seda, RMW, Schlösswender, Hassena, Carpe Diem, Morasutti laut Ordnernamen) auf der neuen Seite
- ❓ Dürfen Markennamen auf der Seite genannt werden?
- ❓ Eigene Fotos vom Studio in Götzis (bisher nur Herstellerbilder)
- ❓ Logo als Vektor (SVG/AI)? Sonst wird es nachgebaut
- Projekt in `Onur-Websiten/Kunden/Estilo/` übertragen, Zeile im Blatt Projekte anlegen

## Verlauf

- 27.11.2026 · Projekt angelegt, Fragen geklärt, alte Seite (Texte + 343 Bilder) nach `Vom Kunden/estilo-at/` gesichert
- 27.11.2026 · Logo vektorisiert (`website/logo/estilo-logo.svg`), drei Hero-Skizzen gezeigt, A + C gewählt
- 27.11.2026 · Blender-Szene (szene.py), Licht gebacken (128 Samples), Website gebaut und in Chromium geprüft (Desktop), Sanity-Studio baut
- 27.11.2026 · Möbel-Lichtatlas 2048 px, Handy-Variante (4,8 MB), Farben im Browser korrigiert (Neutral-Tonemapping), Handy-Layout, Kopfzeile; geprüft Desktop + Handy
