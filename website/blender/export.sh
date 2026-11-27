#!/bin/bash
# Roh-GLB -> Web-GLB: Meshopt-Kompression mit Quantisierung (Decoder ist in three.js dabei).
set -e
cd "$(dirname "$0")"
W=../web/public/welt
for v in "" ".handy"; do
  [ -f "$W/estilo$v.roh.glb" ] || continue
  npx gltf-transform meshopt "$W/estilo$v.roh.glb" "$W/estilo$v.glb" --level medium
  rm "$W/estilo$v.roh.glb"
  ls -la "$W/estilo$v.glb"
done
