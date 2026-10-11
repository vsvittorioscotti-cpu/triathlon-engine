#!/bin/sh
# Assembla la pagina dell'artefatto "Ironman 226" dalle sue quattro parti e copia il
# bundle del motore. La pagina si pubblica con l'Artifact tool insieme a engine.js
# (file di supporto) e alla capability mcp verso il connettore Supabase.
cd "$(dirname "$0")"
cat 01_head.html 02_model.html 03_charts.html 04_views.html > ironman226.html
cp ../engine/dist/engine.js engine.js
echo "ironman226.html: $(wc -c < ironman226.html) byte"
