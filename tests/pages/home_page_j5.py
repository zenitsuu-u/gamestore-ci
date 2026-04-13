"""
pages/home_page_j5.py — Page Object : page d'accueil GameStore
===============================================================
Complétez les TODO avant d'utiliser cette classe dans test_playwright_j5.py.

Principe POM : tous les sélecteurs sont ici.
Les tests n'ont aucun sélecteur — ils appellent seulement les méthodes.
"""
from playwright.sync_api import Page

BASE_URL = "http://localhost:5000"


class HomePage:

    def __init__(self, page: Page):
        self.page = page

        # TODO — Définir un locator pour chaque élément interactif.
        # Utilisez page.locator("[data-testid=...]")
        #
        # self.game_list  = page.locator("...")  # la grille des jeux
        # self.game_count = page.locator("...")  # le compteur
        # self.add_btn    = page.locator("...")  # bouton Ajouter un jeu
        # self.search_inp = page.locator("...")  # barre de recherche
        # self.genre_sel  = page.locator("...")  # filtre par genre

    def navigate(self):
        """Naviguer vers la page d'accueil."""
        # TODO — self.page.goto(BASE_URL)
        pass

    def get_game_cards(self):
        """Retourner le locator de toutes les cartes de jeux."""
        # TODO — return self.game_list.locator("[data-testid=game-card]")
        pass

    def open_add_form(self):
        """Cliquer sur le bouton Ajouter un jeu."""
        # TODO — self.add_btn.click()
        pass

    def search(self, query: str):
        """Taper une recherche dans la barre de recherche."""
        # TODO — self.search_inp.fill(query)
        pass

    def filter_genre(self, genre: str):
        """Sélectionner un genre dans le filtre déroulant."""
        # TODO — self.genre_sel.select_option(genre)
        pass
