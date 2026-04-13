# GameStore — API Flask · Fil rouge 2TES3

Application de gestion de jeux vidéo. Sert de base pour tous les TPs du module.

## Démarrage rapide

```bash
# 1. Installer les dépendances (une seule fois)
pip install flask

# 2. Lancer l'application
python app_gamestore.py

# → Interface web  : http://localhost:5000
# → API JSON       : http://localhost:5000/games
```

## Endpoints API

| Méthode | Route              | Description                      | Status |
|---------|--------------------|----------------------------------|--------|
| GET     | `/`                | Interface HTML                   | 200    |
| GET     | `/health`          | Health check (Locust)            | 200    |
| GET     | `/games`           | Liste tous les jeux              | 200    |
| POST    | `/games`           | Crée un jeu                      | 201    |
| GET     | `/games/<id>`      | Récupère un jeu                  | 200/404|
| PUT     | `/games/<id>`      | Met à jour un jeu                | 200/404|
| DELETE  | `/games/<id>`      | Supprime un jeu                  | 204/404|
| GET     | `/games/stats`     | Stats par genre ⚠ lent           | 200    |
| GET     | `/games/search`    | Recherche ⚠ lente                | 200    |
| GET     | `/genres`          | Liste des genres disponibles     | 200    |

### Filtres disponibles sur GET /games
```
GET /games?genre=RPG
GET /games?sort=price&order=desc
GET /games?genre=Action&sort=rating&order=desc
```

### Exemple POST /games
```json
{
  "title": "Mon Jeu",
  "genre": "RPG",
  "price": 29.99,
  "rating": 4.2,
  "stock": 50,
  "publisher": "Studio XYZ",
  "year": 2024
}
```

## Structure pour les TPs

```
GameStore/
├── app_gamestore.py      ← Application principale (ce fichier)
├── requirements.txt      ← Dépendances
├── gamestore.db          ← Base SQLite (créée au premier lancement)
├── tests/
│   ├── test_tp1_unit.py          ← TP1 : Tests unitaires pytest
│   ├── test_tp2_hexagonal.py     ← TP2 : Architecture hexagonale
│   ├── test_tp3_containers.py    ← TP3 : TestContainers
│   ├── test_tp4_profile.py       ← TP4 : cProfile (bottleneck à corriger)
│   ├── test_tp5_api.py           ← TP5 : Tests API pytest + requests
│   └── test_tp6_playwright.py    ← TP6 : Tests UI Playwright
└── locust/
    └── test_locust.py            ← TP Locust : load test
```

## ⚠ Bottlenecks pour TP4 Profiling

Deux endpoints contiennent des bugs de performance **intentionnels** :

### 1. `GET /games/stats` — Boucle O(n²)
La fonction `_calculate_stats()` parcourt toute la liste pour chaque jeu.
**Correction** : utiliser `SELECT genre, COUNT(*), AVG(price) FROM games GROUP BY genre`

### 2. `GET /games/search` — Chargement total + filtrage Python  
Charge tous les jeux en mémoire avant de filtrer.
**Correction** : utiliser `WHERE title LIKE ? AND genre = ?` dans le SQL

## Lancer les tests

```bash
# TP1 : tests unitaires
pytest tests/test_tp1_unit.py -v --cov=app_gamestore --cov-report=html

# TP4 : profiling
python -m cProfile -s cumulative app_gamestore.py
snakeviz profile.out

# TP5 : tests API
pytest tests/test_tp5_api.py -v --html=report_api.html

# TP6 : tests UI Playwright (nécessite playwright install chromium)
pytest tests/test_tp6_playwright.py -v --html=report_e2e.html

# Locust : load test
locust -f locust/test_locust.py --host=http://localhost:5000
```
