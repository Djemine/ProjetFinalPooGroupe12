# Rakieta Transport — Réservation de Bus

Deux programmes qui communiquent en HTTP :
- **`backend/`** : API FastAPI (logique métier + persistance SQLite)
- **`desktop_client/`** : application desktop CustomTkinter (Administrateur, seul acteur)

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

## Lancement (2 terminaux, venv activé dans les deux)

**Terminal 1 — API**, depuis `backend/` :
```bash
cd backend
uvicorn main:app --reload
```
Vérifier sur `http://127.0.0.1:8000/docs`.

**Terminal 2 — Client desktop**, depuis la **racine du projet** (important, ne pas se placer dans `desktop_client/`) :
```bash
python -m desktop_client.main
```

## Connexion

```
Identifiant  : admin
Mot de passe : admin123
```

## Notes

- Les données sont sauvegardées dans `backend/reservation_bus.db` (persistant entre les sessions).
- L'API doit toujours être lancée **avant** le client desktop.
