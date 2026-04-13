import pytest
import time
import os
import tempfile
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import app_gamestore
from app_gamestore import app, init_db

# ══════════════════════════════════════════════════════════════════════════════
# FIXTURES
# ══════════════════════════════════════════════════════════════════════════════


@pytest.fixture
def client_function():
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    test_db = tmp.name

    original_db = app_gamestore.DATABASE
    app_gamestore.DATABASE = test_db

    app.config["TESTING"] = True
    app.config["PROPAGATE_EXCEPTIONS"] = False

    with app.test_client() as c:
        with app.app_context():
            init_db()
        yield c

    app_gamestore.DATABASE = original_db
    os.unlink(test_db)


@pytest.fixture(scope="module")
def client_module():
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    test_db = tmp.name

    original_db = app_gamestore.DATABASE
    app_gamestore.DATABASE = test_db

    app.config["TESTING"] = True
    app.config["PROPAGATE_EXCEPTIONS"] = False

    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    init_db()

    yield client

    ctx.pop()
    app_gamestore.DATABASE = original_db
    os.unlink(test_db)


# ══════════════════════════════════════════════════════════════════════════════
# PARTIE 1 — SCOPE
# ══════════════════════════════════════════════════════════════════════════════


def test_scope_function_cree_jeu(client_function):
    r = client_function.post(
        "/games", json={"title": "Jeu Scope Function", "genre": "RPG", "price": 10.0}
    )
    assert r.status_code == 201


def test_scope_function_base_fraiche(client_function):
    r = client_function.get("/games")
    titres = [j["title"] for j in r.get_json()]
    assert "Jeu Scope Function" not in titres


def test_scope_module_cree_jeu(client_module):
    r = client_module.post(
        "/games",
        json={"title": "Jeu Persistant Module", "genre": "Action", "price": 20.0},
    )
    assert r.status_code == 201


def test_scope_module_jeu_toujours_present(client_module):
    r = client_module.get("/games")
    titres = [j["title"] for j in r.get_json()]
    assert "Jeu Persistant Module" in titres


# ══════════════════════════════════════════════════════════════════════════════
# PARTIE 2 — YIELD
# ══════════════════════════════════════════════════════════════════════════════


@pytest.fixture
def jeu_zelda(client_function):
    r = client_function.post(
        "/games", json={"title": "Zelda TOTK", "genre": "RPG", "price": 59.99}
    )
    game = r.get_json()
    yield game
    client_function.delete(f"/games/{game['id']}")


@pytest.fixture
def jeu_elden_ring(client_function):
    r = client_function.post(
        "/games", json={"title": "Elden Ring Test", "genre": "RPG", "price": 49.99}
    )
    game = r.get_json()
    yield game
    client_function.delete(f"/games/{game['id']}")


def test_yield_zelda_existe(client_function, jeu_zelda):
    r = client_function.get(f"/games/{jeu_zelda['id']}")
    assert r.status_code == 200


def test_yield_zelda_genre(jeu_zelda):
    assert jeu_zelda["genre"] == "RPG"


def test_yield_zelda_prix_positif(jeu_zelda):
    assert jeu_zelda["price"] > 0


def test_yield_deux_jeux_simultanement(client_function, jeu_zelda, jeu_elden_ring):
    r = client_function.get("/games")
    titres = [j["title"] for j in r.get_json()]
    assert "Zelda TOTK" in titres
    assert "Elden Ring Test" in titres


# ══════════════════════════════════════════════════════════════════════════════
# PARTIE 3 — PARAMETRIZE
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize(
    "payload,expected_status",
    [
        ({"title": "Jeu OK", "genre": "RPG", "price": 59.99}, 201),
        ({"title": "", "genre": "RPG", "price": 10}, 400),
        ({"title": "   ", "genre": "RPG", "price": 10}, 400),
        ({"title": "Jeu", "genre": "RPG", "price": -5}, 400),
        ({"title": "Jeu", "genre": "RPG", "price": "abc"}, 400),
        ({"title": "Jeu", "price": 10}, 400),
    ],
    ids=[
        "valide",
        "titre_vide",
        "titre_espaces",
        "prix_negatif",
        "prix_string",
        "genre_absent",
    ],
)
def test_validation_creation(client_function, payload, expected_status):
    assert client_function.post("/games", json=payload).status_code == expected_status


@pytest.mark.parametrize("sort", ["id", "title", "price", "rating"])
@pytest.mark.parametrize("order", ["asc", "desc"])
def test_tri_combinaisons(client_function, sort, order):
    r = client_function.get(f"/games?sort={sort}&order={order}")
    assert r.status_code == 200


@pytest.mark.parametrize(
    "genre,expected_min",
    [("RPG", 3), ("Platformer", 2), ("Sandbox", 1), ("GenreInexistant", 0)],
)
def test_filtre_genre(client_function, genre, expected_min):
    r = client_function.get(f"/games?genre={genre}")
    assert len(r.get_json()) >= expected_min


# ══════════════════════════════════════════════════════════════════════════════
# PARTIE 4 — MARKERS
# ══════════════════════════════════════════════════════════════════════════════


@pytest.mark.xfail(reason="Bug connu : espaces acceptés")
def test_titre_espaces_debut_xfail(client_function):
    r = client_function.post(
        "/games", json={"title": "  Zelda", "genre": "RPG", "price": 10}
    )
    assert r.status_code == 400


@pytest.mark.slow
def test_performance_100_requetes(client_function):
    start = time.perf_counter()
    for _ in range(100):
        client_function.get("/games")
    elapsed = time.perf_counter() - start
    assert elapsed < 2.0


# ══════════════════════════════════════════════════════════════════════════════
# PARTIE 5 — MONKEYPATCH
# ══════════════════════════════════════════════════════════════════════════════


def test_monkeypatch_variable_env(monkeypatch):
    monkeypatch.setenv("GAMESTORE_ENV", "test")
    assert os.environ.get("GAMESTORE_ENV") == "test"


def test_monkeypatch_panne_bdd(client_function, monkeypatch):
    def fake_get_db():
        raise Exception("Connexion BDD perdue")

    monkeypatch.setattr(app_gamestore, "get_db", fake_get_db)

    r = client_function.get("/games")
    assert r.status_code == 500


def test_monkeypatch_bdd_vide(client_function, monkeypatch):
    from unittest.mock import MagicMock

    def fake_get_db():
        mock_db = MagicMock()
        mock_db.execute.return_value.fetchall.return_value = []
        return mock_db

    monkeypatch.setattr(app_gamestore, "get_db", fake_get_db)

    r = client_function.get("/games")
    assert r.status_code == 200
    assert r.get_json() == []