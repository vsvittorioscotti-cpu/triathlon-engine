# site — la pagina statica

Generata da `artefatto/build.sh`: `index.html` (documento completo) + `engine.js`.
Non si modifica a mano: si cambiano le parti in `artefatto/` e si rilancia il build.

Hosting: Cloudflare Pages (o Netlify) collegato al repo GitHub, **senza comando di build**,
cartella di pubblicazione `site`. Ogni push su `main` ripubblica.

Le librerie arrivano da Supabase via REST con la chiave pubblica `anon` (ruolo che puo'
solo leggere le quattro tabelle delle librerie, per RLS). I dati dell'atleta restano nel
browser finche' non c'e' l'autenticazione Supabase.

## Account e dati (dal 12/10)

Nella pagina pubblica l'atleta accede con email e password (Supabase Auth); i suoi dati
vanno nelle tabelle del contratto C1-C8 con policy RLS per proprietario (migrazione 06):
`piano_versione` + `seduta_prescritta` a ogni cambio di parametri, `seduta_eseguita`,
`test`, `benessere`, `soglia`, `annotazione`. Senza accesso i dati restano nel browser.
`artefatto/test_auth.mjs` collauda login e sincronizzazione con un finto backend in memoria.
