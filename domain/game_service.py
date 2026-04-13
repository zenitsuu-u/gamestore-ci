from domain.game import Game
from domain.game_repository import GameRepository

class GameService:

    def __init__(self, repo: GameRepository):
        self.repo = repo

    def create_game(self, data: dict) -> dict:
        game = Game(**data)
        game.validate()
        return self.repo.save(game)

    def get_game(self, game_id: int) -> dict | None:
        return self.repo.find_by_id(game_id)

    def list_games(self) -> list[dict]:
        return self.repo.find_all()

    def delete_game(self, game_id: int) -> bool:
        return self.repo.delete(game_id)