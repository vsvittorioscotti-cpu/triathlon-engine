# supabase/ — edge function

`functions/intervals-import/index.ts` e' la funzione che importa le attivita' da
intervals.icu in `seduta_eseguita` con `fonte = dispositivo` (il terzo scrittore di C7).
E' pubblicata sul progetto Supabase con il connettore (deploy_edge_function); il sorgente
sta qui per storia e per modifiche. Si chiama dalla pagina (`SB.importaIntervals`) con il
token dell'utente; legge `collegamento_intervals` e scrive con il ruolo di servizio.
Idempotente su (`esterno_fonte`, `esterno_id`).

Le migrazioni dello schema (01–07) sono state applicate con il connettore e sono elencate
nella mappa del progetto; non sono ancora copiate in questa cartella.
