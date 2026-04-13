import pytest
import psycopg2
from testcontainers.postgres import PostgresContainer
from unittest.mock import MagicMock


# ── Fixture PostgreSQL (container Docker) ─────────────────────────────────────

@pytest.fixture(scope="session")
def pg_conn():
    with PostgresContainer("postgres:15") as pg:
        conn = psycopg2.connect(
            pg.get_connection_url().replace("postgresql+psycopg2://", "postgresql://")
        )
        cur = conn.cursor()

        # Création table
        cur.execute("""
        CREATE TABLE games (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            price REAL NOT NULL CHECK(price >= 0),
            UNIQUE (title)
        )
        """)
        conn.commit()

        yield conn

        conn.close()


# ── Helper pour reset entre tests ─────────────────────────────────────────────

@pytest.fixture(autouse=True)
def clean_db(pg_conn):
    cur = pg_conn.cursor()
    cur.execute("DELETE FROM games;")
    pg_conn.commit()


# ── Tests ─────────────────────────────────────────────────────────────────────

# 1️⃣ INSERT + SELECT
def test_insert_and_get_game(pg_conn):
    cur = pg_conn.cursor()

    cur.execute(
        "INSERT INTO games(title, genre, price) VALUES (%s,%s,%s) RETURNING id",
        ("Zelda", "RPG", 59.99)
    )
    game_id = cur.fetchone()[0]
    pg_conn.commit()

    cur.execute("SELECT title, genre, price FROM games WHERE id = %s", (game_id,))
    game = cur.fetchone()

    assert game_id == 1
    assert game == ("Zelda", "RPG", 59.99)


# 2️⃣ UNIQUE constraint
def test_unique_title_constraint(pg_conn):
    cur = pg_conn.cursor()

    cur.execute("INSERT INTO games(title,genre,price) VALUES('Zelda','RPG',59.99)")
    pg_conn.commit()

    with pytest.raises(psycopg2.errors.UniqueViolation):
        cur.execute("INSERT INTO games(title,genre,price) VALUES('Zelda','RPG',39.99)")
        pg_conn.commit()

    pg_conn.rollback()  # 🔥 indispensable


# 3️⃣ CHECK constraint (price >= 0)
def test_price_check_constraint(pg_conn):
    cur = pg_conn.cursor()

    with pytest.raises(psycopg2.errors.CheckViolation):
        cur.execute("INSERT INTO games(title,genre,price) VALUES('Mario','RPG',-10)")
        pg_conn.commit()

    pg_conn.rollback()


# 4️⃣ LIST (COUNT)
def test_list_games(pg_conn):
    cur = pg_conn.cursor()

    games = [
        ("Zelda", "RPG", 59.99),
        ("Mario", "Platformer", 49.99),
        ("FIFA", "Sport", 69.99),
    ]

    for g in games:
        cur.execute("INSERT INTO games(title,genre,price) VALUES (%s,%s,%s)", g)

    pg_conn.commit()

    cur.execute("SELECT COUNT(*) FROM games")
    count = cur.fetchone()[0]

    assert count == 3


# 5️⃣ DELETE
def test_delete_game(pg_conn):
    cur = pg_conn.cursor()

    cur.execute("INSERT INTO games(title,genre,price) VALUES('Zelda','RPG',59.99) RETURNING id")
    game_id = cur.fetchone()[0]
    pg_conn.commit()

    cur.execute("DELETE FROM games WHERE id = %s", (game_id,))
    pg_conn.commit()

    cur.execute("SELECT * FROM games WHERE id = %s", (game_id,))
    game = cur.fetchone()

    assert game is None


# 6️⃣ UPDATE
def test_update_game_price(pg_conn):
    cur = pg_conn.cursor()

    cur.execute("INSERT INTO games(title,genre,price) VALUES('Zelda','RPG',59.99) RETURNING id")
    game_id = cur.fetchone()[0]
    pg_conn.commit()

    cur.execute("UPDATE games SET price = %s WHERE id = %s", (39.99, game_id))
    pg_conn.commit()

    cur.execute("SELECT price FROM games WHERE id = %s", (game_id,))
    price = cur.fetchone()[0]

    assert price == 39.99


# ── Test comparaison MOCK vs vraie BDD ─────────────────────────────────────────

def test_mock_does_not_catch_duplicate():
    mock_repo = MagicMock()

    mock_repo.save.return_value = {"id": 1, "title": "Zelda"}

    # ❌ Le mock ne respecte PAS la contrainte UNIQUE
    result1 = mock_repo.save({"title": "Zelda", "genre": "RPG", "price": 59.99})
    result2 = mock_repo.save({"title": "Zelda", "genre": "RPG", "price": 39.99})

    assert result1["title"] == "Zelda"
    assert result2["title"] == "Zelda"

    # ⚠️ Aucune erreur → faux positif !
    # En vraie base PostgreSQL, une erreur UniqueViolation serait levée