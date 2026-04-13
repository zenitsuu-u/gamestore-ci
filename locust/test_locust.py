"""
TP Locust — Load Test sur l'API GameStore
==========================================
Lancement :
  locust -f test_locust.py --host=http://localhost:5000
Interface : http://localhost:8089
"""
from locust import HttpUser, task, between


class GameStoreUser(HttpUser):
    """
    Simule un utilisateur naviguant sur le GameStore.
    wait_time : délai entre chaque requête (entre 1 et 3 secondes).
    """
    wait_time = between(1, 3)

    def on_start(self):
        """Exécuté une fois par utilisateur simulé au démarrage."""
        # Vérifier que l'API est disponible
        self.client.get("/health")

    @task(5)
    def browse_games(self):
        """Navigation principale — 5x plus souvent que les autres."""
        self.client.get("/games", name="GET /games")

    @task(3)
    def browse_games_by_genre(self):
        """Filtrage par genre."""
        for genre in ["RPG", "Action", "Platformer"]:
            self.client.get(f"/games?genre={genre}", name="GET /games?genre=")

    @task(2)
    def get_game_detail(self):
        """Détail d'un jeu."""
        for game_id in [1, 2, 3, 5, 10]:
            self.client.get(f"/games/{game_id}", name="GET /games/<id>")

    @task(1)
    def get_stats(self):
        """
        Endpoint stats — intentionnellement lent.
        Permet d'observer la dégradation sous charge.
        """
        self.client.get("/games/stats", name="GET /games/stats (slow ⚠)")

    @task(1)
    def search_games(self):
        """Recherche — intentionnellement lente."""
        self.client.get("/games/search?q=elden", name="GET /games/search (slow ⚠)")

    @task(1)
    def health_check(self):
        """Health check léger."""
        self.client.get("/health", name="GET /health")
