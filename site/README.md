# site — la pagina statica

Generata da `artefatto/build.sh`: `index.html` (documento completo) + `engine.js`.
Non si modifica a mano: si cambiano le parti in `artefatto/` e si rilancia il build.

Hosting: Cloudflare Pages (o Netlify) collegato al repo GitHub, **senza comando di build**,
cartella di pubblicazione `site`. Ogni push su `main` ripubblica.

Le librerie arrivano da Supabase via REST con la chiave pubblica `anon` (ruolo che puo'
solo leggere le quattro tabelle delle librerie, per RLS). I dati dell'atleta restano nel
browser finche' non c'e' l'autenticazione Supabase.
