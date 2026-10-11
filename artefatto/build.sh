#!/bin/sh
# Assembla la pagina "Ironman 226" dalle quattro parti, in due forme:
#  - ironman226.html : senza <html>/<head>/<body>, per l'Artifact tool di claude.ai
#                      (che aggiunge lo scheletro e serve engine.js come file di supporto)
#  - ../site/index.html : documento completo per l'hosting statico (Cloudflare Pages,
#                      Netlify…), con engine.js accanto. Fuori da claude.ai le librerie
#                      arrivano da Supabase via REST con la chiave pubblica.
cd "$(dirname "$0")"
cat 01_head.html 02_model.html 03_charts.html 04_views.html > ironman226.html
cp ../engine/dist/engine.js engine.js
mkdir -p ../site
{
  printf '%s' '<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
  printf '%s' '<style>:root{color-scheme:light}body{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif;background:#faf9f5;color:#141413}img{max-width:100%}[hidden]:not([hidden=until-found]){display:none!important}</style></head><body>'
  printf '\n'
  cat ironman226.html
  printf '\n</body></html>\n'
} > ../site/index.html
cp engine.js ../site/engine.js
echo "ironman226.html: $(wc -c < ironman226.html) byte — site/index.html: $(wc -c < ../site/index.html) byte"
