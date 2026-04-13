from abc import ABC, abstractmethod

class GameRepository(ABC):

    @abstractmethod
    def save(self, game) -> dict:
        pass

    @abstractmethod
    def find_by_id(self, game_id: int) -> dict | None:
        pass

    @abstractmethod
    def find_all(self) -> list[dict]:
        pass

    @abstractmethod
    def delete(self, game_id: int) -> bool:
        pass