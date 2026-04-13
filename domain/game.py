from dataclasses import dataclass
from typing import Optional

@dataclass
class Game:
    title: str
    genre: str
    price: float
    id: Optional[int] = None
    rating: float = 0.0
    stock: int = 0

    def validate(self):
        if not self.title.strip():
            raise ValueError("Le titre est obligatoire")
        if self.price < 0:
            raise ValueError("Le prix doit être positif")