"""
TP6 — Tests UI avec Playwright Python · API GameStore
======================================================
Objectif : tester l'interface web avec Playwright + Page Object Model.

Prérequis :
  pip install playwright pytest-playwright pytest-html
  playwright install chromium
  python app_gamestore.py  (dans un autre terminal)

Lancement :
  pytest test_tp6_playwright.py -v --headed              # avec navigateur visible
  pytest test_tp6_playwright.py -v --html=report_e2e.html
"""

import pytest
from playwright.sync_api import Page, expect
import time

BASE_URL = 'http://localhost:5000'

# ── conftest.py (à créer dans tests/) ────────────────────────────────────────
# Décommente et place dans tests/conftest.py pour activer les screenshots auto :
#
# @pytest.fixture(autouse=True)
# def screenshot_on_fail(page, request):
#     yield
#     if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
#         import os
#         os.makedirs('screenshots', exist_ok=True)
#         page.screenshot(path=f'screenshots/{request.node.name}.png')


# ── Partie 1 — Tests basiques (sans POM) ─────────────────────────────────────

def test_page_charge(page: Page):
    """La page d'accueil doit charger et afficher le titre 'GameStore'."""
    page.goto(BASE_URL)
    # TODO : vérifier page.title() == 'GameStore'
    pass


def test_liste_jeux_visible(page: Page):
    """Le conteneur game-list doit être visible après chargement."""
    page.goto(BASE_URL)
    # TODO : attendre que [data-testid=game-list] soit visible
    # expect(page.locator('[data-testid=game-list]')).to_be_visible()
    pass


def test_compteur_jeux(page: Page):
    """Le compteur de jeux doit afficher un nombre > 0."""
    page.goto(BASE_URL)
    # TODO : vérifier [data-testid=game-count] contient un nombre
    pass


def test_ajouter_un_jeu(page: Page):
    """Ouvrir le formulaire, remplir, soumettre, vérifier l'apparition dans la liste."""
    page.goto(BASE_URL)
    # TODO :
    # 1. Cliquer sur [data-testid=add-game-btn]
    # 2. Vérifier que [data-testid=add-game-modal] est visible
    # 3. Remplir [data-testid=input-title], [data-testid=input-genre], [data-testid=input-price]
    # 4. Cliquer sur [data-testid=submit-btn]
    # 5. Vérifier que le nouveau jeu apparaît dans [data-testid=game-list]
    pass


def test_annuler_formulaire(page: Page):
    """Cliquer Annuler doit fermer le modal sans ajouter de jeu."""
    page.goto(BASE_URL)
    # TODO
    pass


# ── Partie 2 — Page Object Model ─────────────────────────────────────────────

class HomePage:
    """
    Page Object pour la page d'accueil du GameStore.
    Centralise les sélecteurs et les actions sur la page.
    """

    def __init__(self, page: Page):
        self.page       = page
        # TODO : définir les locators
        # self.game_list  = page.locator('[data-testid=game-list]')
        # self.game_count = page.locator('[data-testid=game-count]')
        # self.add_btn    = page.locator('[data-testid=add-game-btn]')
        # self.search     = page.locator('[data-testid=search-input]')
        # self.genre_sel  = page.locator('[data-testid=genre-filter]')

    def navigate(self):
        self.page.goto(BASE_URL)

    def get_game_count_text(self) -> str:
        """Retourne le texte du compteur de jeux."""
        # TODO : retourner self.game_count.inner_text()
        return ''

    def get_game_cards(self):
        """Retourne tous les cards de jeux."""
        # TODO : retourner self.game_list.locator('[data-testid=game-card]')
        pass

    def search(self, query: str):
        """Tape dans la barre de recherche."""
        # TODO
        pass

    def filter_by_genre(self, genre: str):
        """Sélectionne un genre dans le filtre."""
        # TODO
        pass

    def open_add_form(self):
        """Clique sur le bouton Ajouter."""
        # TODO
        pass


class AddGameModal:
    """Page Object pour le modal d'ajout de jeu."""

    def __init__(self, page: Page):
        self.page   = page
        # TODO : définir les locators du formulaire
        pass

    def fill_form(self, title: str, genre: str, price: float):
        """Remplit le formulaire d'ajout."""
        # TODO
        pass

    def submit(self):
        """Clique sur le bouton Ajouter du formulaire."""
        # TODO
        pass

    def cancel(self):
        """Clique sur le bouton Annuler."""
        # TODO
        pass


# ── Tests avec POM ────────────────────────────────────────────────────────────

def test_pom_home_charge(page: Page):
    """La page d'accueil charge correctement (avec POM)."""
    home = HomePage(page)
    home.navigate()
    # TODO : vérifier le titre de la page
    pass


def test_pom_ajouter_jeu(page: Page):
    """Ajouter un jeu via le POM et vérifier son apparition."""
    home  = HomePage(page)
    modal = AddGameModal(page)
    home.navigate()

    title = f'Jeu POM {int(time.time())}'
    # TODO :
    # 1. home.open_add_form()
    # 2. modal.fill_form(title, 'Platformer', 9.99)
    # 3. modal.submit()
    # 4. Vérifier que le jeu apparaît dans la liste
    pass


def test_pom_recherche(page: Page):
    """La recherche filtre correctement les jeux."""
    home = HomePage(page)
    home.navigate()
    # TODO : chercher "Zelda" et vérifier les résultats
    pass
