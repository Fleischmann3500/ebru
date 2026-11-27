#!/bin/bash
# Komplette Kette Blender -> Web (nach penthouse.py)
cd "$(dirname "$0")"
set -e
rm -f vorschau/station_*.jpg
python3 vorschau.py 40 1440 2>&1 | grep -E "gerendert|rror" || true
python3 backen.py 128 1024 2>&1 | grep -E "Atlas|Vertex|fertig|rror|Traceback"
python3 export.py 2>&1 | grep -E "Lichtatlas|exportiert|rror|Traceback"
python3 export.py handy 2>&1 | grep -E "exportiert|rror|Traceback"
rm -f ../web/public/welt/estilo.glb ../web/public/welt/estilo.handy.glb
./export.sh 2>&1 | grep -E "→|rror"
python3 texturen_web.py 2>&1 | tail -1
python3 web_dateien.py 2>&1 | grep -vE "^Read|INFO"
echo ENDE
