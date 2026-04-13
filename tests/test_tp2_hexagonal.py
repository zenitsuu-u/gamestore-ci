import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from domain.game_service import GameService
from adapters.in_memory_repo import InMemoryGameRepository


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def repo():
    return InMemoryGameRepository()


@pytest.fixture
def service(repo):
    return GameService(repo)


@pytest.fixture
def sample_game():
    return {
        "title": "Zelda",
        "genre": "RPG",
        "price": 59.99,
        "rating": 4.5,
        "stock": 10
    }


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestCreateGame:

    def test_create_valid_game(self, service, sample_game):
        game = service.create_game(sample_game)

        assert game["id"] is not None
        assert game["title"] == "Zelda"

    def test_create_game_without_title(self, service, sample_game):
        sample_game["title"] = ""

        with pytest.raises(ValueError):
            service.create_game(sample_game)

    def test_create_game_negative_price(self, service, sample_game):
        sample_game["price"] = -10

        with pytest.raises(ValueError):
            service.create_game(sample_game)

    @pytest.mark.parametrize("title,price", [
        ("", 10),
        ("Mario", -5),
        ("   ", 20),
    ])
    def test_create_game_validation_parametrize(self, service, title, price):
        with pytest.raises(ValueError):
            service.create_game({
                "title": title,
                "genre": "RPG",
                "price": price
            })


class TestGetGame:

    def test_get_existing_game(self, service, sample_game):
        created = service.create_game(sample_game)

        game = service.get_game(created["id"])

        assert game is not None
        assert game["title"] == "Zelda"

    def test_get_nonexistent_game(self, service):
        assert service.get_game(999) is None


class TestListGames:

    def test_list_games_empty(self, service):
        assert service.list_games() == []

    def test_list_games_after_insert(self, service, sample_game):
        service.create_game(sample_game)

        games = service.list_games()

        assert len(games) == 1
        assert isinstance(games, list)


class TestDeleteGame:

    def test_delete_existing_game(self, service, sample_game):
        created = service.create_game(sample_game)

        result = service.delete_game(created["id"])

        assert result is True
        assert service.get_game(created["id"]) is None

    def test_delete_nonexistent_game(self, service):
        assert service.delete_game(999) is False