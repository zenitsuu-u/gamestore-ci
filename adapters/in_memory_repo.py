from domain.game_repository import GameRepository

class InMemoryGameRepository(GameRepository):

    def __init__(self):
        self._store = {}
        self._next_id = 1

    def save(self, game) -> dict:
        game.id = self._next_id
        self._next_id += 1
        self._store[game.id] = game
        return vars(game)

    def find_by_id(self, game_id: int):
        game = self._store.get(game_id)
        return vars(game) if game else None

    def find_all(self):
        return [vars(game) for game in self._store.values()]

    def delete(self, game_id: int) -> bool:
        if game_id in self._store:
            del self._store[game_id]
            return True
        return False