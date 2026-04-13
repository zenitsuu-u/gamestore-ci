"""
locust_j5.py — TP J5 · Test de charge GameStore
=================================================

Lancement (headless — sans interface web) :
    locust -f tests/locust_j5.py --host=http://localhost:5000 \
           --headless -u 20 -r 2 --run-time 30s

Lancement (avec interface web) :
    locust -f tests/locust_j5.py --host=http://localhost:5000
    # Ouvrir http://localhost:8089
"""
from locust import HttpUser, task, between
import random


class GameStoreUser(HttpUser):
    """
    Utilisateur simulé naviguant sur le catalogue GameStore.
    wait_time : temps d'attente entre chaque action (simule un vrai utilisateur).
    """
    wait_time = between(1, 3)

    # ── Tâche 1 : Lister les jeux ─────────────────────────────────────────────
    @task(5)
    def lister_jeux(self):
        """Action la plus fréquente : consulter le catalogue."""
        with self.client.get("/games", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Inattendu : {response.status_code}")

    # ── Tâche 2 : Filtrer par genre ───────────────────────────────────────────
    @task(3)
    def filtrer_genre(self):
        """Filtrer par genre — comportement courant."""
        genre = random.choice(["RPG", "Action", "Platformer", "Sandbox"])

        # Le paramètre 'name' permet de regrouper les métriques
        with self.client.get(
            f"/games?genre={genre}",
            name="/games?genre=[genre]",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(
                    f"Filtre genre '{genre}' inattendu : {response.status_code}"
                )

    # ── Tâche 3 : Health check ────────────────────────────────────────────────
    @task(2)
    def health_check(self):
        """Monitoring — vérifier que l'API est vivante."""
        with self.client.get("/health", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Status inattendu : {response.status_code}")
                return

            try:
                data = response.json()
                if data.get("status") == "ok":
                    response.success()
                else:
                    response.failure(
                        f"Health check invalide : {data}"
                    )
            except Exception as e:
                response.failure(f"Réponse non JSON : {e}")

    # ── Tâche 4 : Consulter les jeux featured ─────────────────────────────────
    @task(1)
    def consulter_featured(self):
        """
        GET /games/featured avec validation :
        - status == 200
        - le premier jeu a un rating >= au dernier jeu (tri décroissant)
        """
        with self.client.get("/games/featured", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Status inattendu : {response.status_code}")
                return

            try:
                games = response.json()

                if not isinstance(games, list) or len(games) == 0:
                    response.failure("Réponse featured invalide ou vide")
                    return

                first_rating = games[0].get("rating")
                last_rating = games[-1].get("rating")

                if first_rating is None or last_rating is None:
                    response.failure("Champ 'rating' manquant")
                elif first_rating >= last_rating:
                    response.success()
                else:
                    response.failure("Tri featured incorrect")

            except Exception as e:
                response.failure(f"Erreur parsing JSON : {e}")

    # ── Tâche 5 : Consulter les statistiques ──────────────────────────────────
    @task(1)
    def consulter_stats(self):
        """
        Stats par genre — endpoint lent volontairement.
        Observer le temps de réponse comparé à /games.
        """
        with self.client.get("/games/stats", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(
                    f"Stats inattendues : {response.status_code}"
                )