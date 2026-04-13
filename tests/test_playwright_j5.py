"""
test_playwright_j5.py — TP J5 · Tests UI GameStore
====================================================
Complétez les TODO dans l'ordre.

Lancement :
    pytest tests/test_playwright_j5.py -v --headed
    pytest tests/test_playwright_j5.py -v          # headless (CI)
"""
from playwright.sync_api import Page, expect
from tests.pages.home_page_j5 import HomePage
from tests.pages.add_game_modal_j5 import AddGameModal

BASE_URL = "http://localhost:5000"


# ══════════════════════════════════════════════════════════════════════════════
# PARTIE 1 — Tests basiques (sans POM)
# Vous écrivez les sélecteurs directement dans les tests.
# Objectif : comprendre les locators Playwright avant de les encapsuler.
# ══════════════════════════════════════════════════════════════════════════════

def test_page_charge(page: Page):
    """
    TODO :
    1. page.goto(BASE_URL)
    2. assert page.title() == "GameStore"
    3. expect(page.locator("[data-testid=game-list]")).to_be_visible()
    """
    pass


def test_compteur_affiche_nombre_positif(page: Page):
    """
    TODO :
    1. Naviguer vers BASE_URL
    2. Attendre que [data-testid=game-count] soit visible
    3. Extraire le texte → "20 jeux" → extraire 20
    4. assert count > 0
    """
    pass


def test_recherche_filtre_resultats(page: Page):
    """
    TODO :
    1. Naviguer vers BASE_URL
    2. page.locator("[data-testid=search-input]").fill("Zelda")
    3. Attendre que les résultats se mettent à jour
    4. Vérifier que le premier game-title contient "Zelda"
    """
    pass


def test_filtre_genre_rpg(page: Page):
    """
    TODO :
    1. Naviguer vers BASE_URL
    2. page.locator("[data-testid=genre-filter]").select_option("RPG")
    3. Récupérer toutes les cartes avec locator("[data-testid=game-card]")
    4. Pour chaque carte, vérifier que game-genre contient "RPG"
    """
    pass


# ══════════════════════════════════════════════════════════════════════════════
# PARTIE 2 — Page Object Model
# Mêmes scénarios mais via les classes POM.
# Plus aucun sélecteur dans les tests — tout passe par HomePage / AddGameModal.
# ══════════════════════════════════════════════════════════════════════════════

def test_pom_page_charge(page: Page):
    """
    TODO :
    1. home = HomePage(page)
    2. home.navigate()
    3. assert page.title() == "GameStore"
    4. expect(home.game_list).to_be_visible()
    """
    pass


def test_pom_ajouter_jeu(page: Page):
    """
    TODO :
    1. home = HomePage(page) · modal = AddGameModal(page)
    2. home.navigate()
    3. home.open_add_form()
    4. modal.fill_and_submit("Jeu POM Test", "Action", 19.99)
    5. expect(home.game_list).to_contain_text("Jeu POM Test")
    """
    pass


def test_pom_annuler_formulaire(page: Page):
    """
    TODO :
    1. home.navigate()
    2. home.open_add_form()
    3. modal.cancel()
    4. expect(modal.modal).not_to_be_visible()
    """
    pass


def test_pom_recherche(page: Page):
    """
    TODO :
    1. home.navigate()
    2. home.search("Zelda")
    3. Vérifier que la première carte contient "Zelda"
    """
    pass
