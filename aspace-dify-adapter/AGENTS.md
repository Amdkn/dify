# AGENTS.md (local — aspace-dify-adapter)

Règles maison de ce dossier d'adapter. L'`AGENTS.md` racine de dify
n'est pas édité (H-M2).

- Cet adapter est du **contrat seul** : validation hors-ligne, jamais de
  démarrage de serveur, jamais d'appel réseau, jamais de secret.
- Ne jamais toucher à `web/` (licence : LOGO et copyright intacts).
- Ne jamais proposer ni préparer du multi-tenant (licence : mono-tenant
  uniquement, sans autorisation écrite de Dify).
- Python stdlib seule dans `validate.py` et `smoke_test.py`.
- Les sha256 des logos sont épinglés dans `contract.json` ; un logo qui
  change = l'adapter refuse (pas de mise à jour silencieuse).
