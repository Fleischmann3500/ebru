# Runde 0 · Erste Fassung (27.11.2026)

**Wunsch (wörtlich):** „https://estilo.at/ das ziel ist ihre aktuelle website in eine moderne krasse 3d animierte seite zu machen mit hilfe des blender mcp“

**Was jetzt gilt:** siehe Projekt.md (Entscheidungen) und website/CLAUDE.md (Regeln).

**Fallen, die Zeit gekostet haben**
- Poly-Haven-Stoffe sind farbig (Bouclé kariert, Leinen blau, Velours rot): vor dem Einfärben entsättigen (`eingefaerbt()` in szene.py).
- Flächenlicht strahlt entlang lokal −Z: Fensterlichter zeigten zuerst nach außen.
- Fensterlichter für Kamera, Glanz UND Transmission unsichtbar schalten, sonst weiße Flächen hinter Glas.
- glTF-Import mit mehreren Teilen: Drehung ging beim Zusammenfügen verloren → Zusammenfügen über Geometriedaten (bmesh).
- React setzt `dangerouslySetInnerHTML` beim Neuzeichnen neu ein → SVG-Transformationen weg. Lösung: SVG in gemerkte Komponente.
- three.js: `Object3D.lookAt` zeigt +Z, Kameras −Z. Für Kamerastationen eine Kamera zum Ausrichten nehmen.
- Dauer-Renderloop mit Software-WebGL blockiert Screenshots → nur bei Änderung rendern (spart auch Akku).
- Alter `next-server` lief weiter (EADDRINUSE) → Prozess über /proc finden und beenden.

**Geprüft:** tsc, eslint, next build, Playwright 1440×900 mit Software-WebGL über alle Stationen.
**Offen:** Handy-Ansicht prüfen, Handy-Variante der Szene, Formular mit echtem Resend-Schlüssel testen.
