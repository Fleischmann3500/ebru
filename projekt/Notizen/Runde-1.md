# Runde 1 · V2 Penthouse (27.11.2026)

**Wunsch (wörtlich):** „ich finde halt die 3d dinger ned so schön modelliert mach eine v2 aber geh diese mal neu an die sach mabe so dass man duch eine ablout clean penhouse wohnung geht udn dann so die zeimmer vorgestellt werden“

**Entscheidungen (per Rückfrage):**
- Stimmung: warm minimal (helle Eiche, Travertin, Kalkputz, Leinen, Sofa in Logo-Grün, Nussholz-Lamellen, später Nachmittag, Ausblick Alpen/Rheintal)
- Möbel: selbst modellieren, viel feiner (Polsterkissen, Nähte, dünne Metallbeine, Fasen)
- Rundgang: durchgehender Gang mit Halten in jedem Zimmer
- Einstieg „Das Logo wird Raum“ bleibt, V1 gesichert (Git-Tag `v1-erste-fassung`, Backup `website/_backups/2026-11-27-vor-runde-1/`)

**Ursache der Kritik:** V1-Möbel waren abgerundete Quader ohne Details (keine Kissen, Nähte, Proportionen), Räume nebeneinander wie Kojen statt einer echten Wohnung.

**Umsetzung:** `website/blender/penthouse.py` (ersetzt szene.py als Quelle), Kette `kette.sh` (Vorschau → Backen 128 Samples, Atlanten 2048 → Export → Handy → Meshopt → Texturen → Stationsbilder).
Web: Stationen + Wegpunkte aus Blender (`station_<n>_*`, `weg_<n>_<i>`), Kamera auf einer Kurve durch alle Punkte, auf langen Wegen Blick in Gehrichtung. Reihenfolge: Logo-Wand, Wohnen, Sofa, Büro, Essen, Schlafen.

**Fallen:** Glas blockiert in Cycles die Sonne (Schattenstrahlen) → `visible_shadow = False`. Zwischengespeicherte eingefärbte Texturen (texturen_web) nach Materialänderung löschen. V1-Bug: `lookAt` war in einen Kommentar gerutscht.

**Geprüft:** tsc, eslint, build, 0 Schwachstellen, Playwright 1440×900 und 390×844 mit Software-WebGL.
**Offen:** Logo-Übergang trifft die Leuchten nicht exakt; Relaxsessel ragt im Büro ins Bild; GLB 8,2 MB (Handy 5,8 MB).
