"""
TP1 — Tests Unitaires avec pytest · API GameStore
==================================================
Objectif : écrire 10 tests unitaires couvrant les fonctions de l'API GameStore.
Coverage cible : > 80 %

Lancement :
  pytest test_tp1_unit.py -v --cov=app_gamestore --cov-report=html
"""

import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# On importe l'application en mode test (BDD en mémoire)
from app_gamestore import app, init_db, get_db

# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def client():
    """
    Crée un client de test Flask avec une BDD SQLite en mémoire.
    La BDD est réinitialisée à chaque test grâce au scope par défaut (function).
    """
    app.config['TESTING'] = True
    app.config['DATABASE'] = ':memory:'   # BDD en mémoire, isolée par test

    with app.test_client() as c:
        with app.app_context():
            init_db()
            db = get_db()
            db.execute("DELETE FROM games;")
            db.commit()
        yield c


@pytest.fixture
def sample_game(genre: str = "RPG", game_id: int = 0):
    """Données d'un jeu valide pour les tests."""
    return {
        'title':  f"title-{genre}-test",
        'genre':  genre,
        'price':  59.99,
        'rating': 4.9,
        'stock':  100,
    }


class TestListGames:

    def test_get_all_games_returns_200(self, client):
        assert client.get('/games').status_code == 200

    def test_get_all_games_returns_list(self, client):
        assert type(client.get('/games').json) == list

    def test_get_games_filter_by_genre(self, client, sample_game):
        client.post('/games', json={**sample_game, "genre": "Test"})
        assert len(client.get("/games?genre=Test").json) == 1


class TestCreateGame:

    def test_create_valid_game_returns_201(self, client, sample_game):
        assert client.post('/games', json=sample_game).status_code == 201

    def test_create_game_returns_id(self, client, sample_game):
        assert "id" in client.post('/games', json=sample_game).json

    def test_create_game_without_title_returns_400(self, client, sample_game):
        del sample_game['title']
        assert client.post('/games', json=sample_game).status_code == 400

    def test_create_game_with_negative_price_returns_400(self, client, sample_game):
        sample_game['price'] = -2
        assert client.post('/games', json=sample_game).status_code == 400

    def test_create_duplicate_title_returns_409(self, client, sample_game):
        assert client.post('/games', json=sample_game).status_code == 201
        assert client.post('/games', json=sample_game).status_code == 409

    @pytest.mark.parametrize("title,genre,price,expected_status,rating,stock", [
        ("Zelda", "RPG", "d59.99", 400, 1, 10),
        ("", "RPG", 29.99, 400, -2, 10),
        ("Mario", "RPG", 5.0, 400, 2,-1),
        ("Zelda", "RPG", 59.99, 201,3,4),
        ("", "RPG", 29.99, 400,4,5),
        ("Mario", "RPG", -5.0, 400,5,6),
        (None, "RPG", 9.99, 400,6,7),
    ])
    def test_create_game_validation(self, client, title, genre, price, expected_status, rating, stock):
        r = client.post("/games", json={"title": title, "genre": genre, "price": price, "rating": rating, "stock": stock})
        assert r.status_code == expected_status


class TestGetGame:

    def test_get_existing_game_returns_200(self, client, sample_game):
        game_id = client.post('/games', json=sample_game).json['id']
        assert client.get(f'/games/{game_id}').status_code == 200

    def test_get_nonexistent_game_returns_404(self, client):
        assert client.get(f'/games/-1').status_code == 404


    def test_update_not_found_game(self, client):
        assert client.put("games/-1").status_code == 404


class TestListGameGenre:

    def test_game_genres_200(self, client):
        assert client.get('/genres').status_code == 200

    def test_game_genres_is_list(self, client):
        assert type(client.get('/genres').json) == list



class TestDeleteGame:

    def test_delete_existing_game_returns_204(self, client, sample_game):
        game_id = client.post('/games', json=sample_game).json['id']
        assert client.delete(f'/games/{game_id}').status_code == 204

    def test_delete_nonexistent_game_returns_404(self, client):
        assert client.delete(f'/games/-1').status_code == 404
