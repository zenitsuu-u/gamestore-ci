"""
TP5 — Tests API REST · pytest + requests
=========================================
Objectif : tester les endpoints de l'API GameStore avec requests.

Prérequis :
  pip install requests pytest-html
  python app_gamestore.py   (dans un autre terminal)

Lancement :
  pytest test_tp5_api.py -v --html=report_api.html
"""

import pytest
import requests
import subprocess
import time
import sys, os

BASE_URL = 'http://localhost:5000'

# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope='session')
def api():
    """
    Démarre l'API GameStore en sous-processus pour la durée des tests.
    Le serveur est arrêté automatiquement à la fin de la session.
    """
    # TODO : démarrer app_gamestore.py en subprocess
    # Indice : subprocess.Popen(['python', '../app_gamestore.py'])
    # Attendre 1 seconde le démarrage : time.sleep(1)
    # Yield BASE_URL
    # Terminer le processus : proc.terminate()
    yield BASE_URL  # À remplacer par la fixture complète


@pytest.fixture
def new_game(api):
    """Crée un jeu de test et le supprime après chaque test."""
    payload = {
        'title':  f'Test Game TP5 {time.time()}',  # titre unique
        'genre':  'Test',
        'price':  19.99,
        'rating': 4.0,
        'stock':  50,
    }
    r = requests.post(f'{api}/games', json=payload)
    game = r.json()
    yield game
    # Nettoyage : supprimer le jeu après le test
    requests.delete(f'{api}/games/{game["id"]}')


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestHealthCheck:

    def test_health_returns_ok(self, api):
        """GET /health doit retourner {'status': 'ok'}."""
        # TODO
        pass


class TestListGames:

    def test_list_games_status_200(self, api):
        """GET /games doit retourner 200."""
        # TODO
        pass

    def test_list_games_returns_list(self, api):
        """GET /games doit retourner une liste non vide (données de démo)."""
        # TODO
        pass

    def test_list_games_fast(self, api):
        """GET /games doit répondre en moins de 500ms."""
        # TODO : vérifier r.elapsed.total_seconds() < 0.5
        pass


class TestCreateGame:

    def test_create_game_returns_201(self, api):
        """POST /games avec données valides → 201."""
        # TODO
        pass

    def test_create_game_response_has_id(self, api):
        """La réponse POST /games doit inclure un 'id'."""
        # TODO
        pass

    def test_create_game_title_required(self, api):
        """POST /games sans titre → 400."""
        # TODO
        pass

    def test_create_game_negative_price_rejected(self, api):
        """POST /games avec price=-1 → 400."""
        # TODO
        pass


class TestGetGame:

    def test_get_existing_game(self, api, new_game):
        """GET /games/<id> pour un jeu existant → 200 avec le bon titre."""
        # TODO
        pass

    def test_get_nonexistent_game(self, api):
        """GET /games/99999 → 404."""
        # TODO
        pass


class TestDeleteGame:

    def test_delete_game_returns_204(self, api, new_game):
        """DELETE /games/<id> → 204."""
        r = requests.delete(f'{api}/games/{new_game["id"]}')
        assert r.status_code == 204

    def test_deleted_game_not_found(self, api, new_game):
        """Après DELETE, GET /games/<id> → 404."""
        # TODO : supprimer le jeu puis vérifier qu'il est introuvable
        pass
