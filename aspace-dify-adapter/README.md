# aspace-dify-adapter

Adapter A'Space pour **dify** (fork `Amdkn/dify`, gel `b29552a`, amont
`langgenius/dify`, version 1.19.0). Couture **contrat seul** (D-N048 §1.5) :
validation hors-ligne du dépôt, jamais de démarrage de serveur.

## Surface

- `python3 aspace-dify-adapter/validate.py [--repo <chemin>]` — structure
  (`api/`, `web/`, `LICENSE`, `docker/`), LICENSE (deux conditions
  additionnelles), logos `web/` intacts (sha256 épinglés dans
  `contract.json`), version 1.19.0.
- `python3 aspace-dify-adapter/validate.py --version` — version + gel.
- `python3 aspace-dify-adapter/validate.py --doctor` — posture télémétrie
  par défaut, informative (aucun envoi).
- `python3 aspace-dify-adapter/smoke_test.py` — 10 cas, stdlib seule.

## Ce que l'adapter ne fait jamais

- Démarrer `api/` (Flask) ou `web/` (Next.js).
- Toucher à `web/` ni à un logo (licence : LOGO et copyright intacts).
- Opérer en multi-tenant (licence : mono-tenant uniquement, sans
  autorisation écrite de Dify).
- Appeler le réseau (payant ou non), lire ou écrire un secret.

## Télémétrie (audit : `dify-TELEMETRY-AUDIT.md`)

- **Télémétrie communautaire api/ : DÉFAUT ON** — `DISABLE_TELEMETRY=false`,
  endpoints `https://otel.dify.ai/v1/events` (+ fallback `.cn`), événements
  `install` (1×) + `heartbeat` (≤1/jour), charge anonyme, porte : édition
  COMMUNITY. Coupure par contrat : `DISABLE_TELEMETRY=true` +
  `DO_NOT_TRACK=true` + `CI=true`.
- Sentry api/web : OFF sans DSN. OpenTelemetry : OFF (`ENABLE_OTEL=false`).
  Amplitude web : OFF sans clé, opt-out par défaut. OTel entreprise : OFF.
- PostHog : dépendance transitive inutilisée de chromadb (jamais importé).

## Règles maison (AGENTS.md local)

L'`AGENTS.md` racine de dify est un contrat liant — **non édité** ; cet
adapter porte son propre `AGENTS.md` local (ce dossier).
