"""
pages/add_game_modal_j5.py — Page Object : modal d'ajout de jeu
================================================================
Complétez les TODO avant d'utiliser cette classe dans test_playwright_j5.py.
"""
from playwright.sync_api import Page


class AddGameModal:

    def __init__(self, page: Page):
        self.page = page

        # TODO — Définir les locators du formulaire
        #
        # self.modal        = page.locator("...")  # le modal entier
        # self.input_title  = page.locator("...")  # champ titre
        # self.input_genre  = page.locator("...")  # champ genre
        # self.input_price  = page.locator("...")  # champ prix
        # self.submit_btn   = page.locator("...")  # bouton Ajouter
        # self.cancel_btn   = page.locator("...")  # bouton Annuler

    def fill_and_submit(self, title: str, genre: str, price: float):
        """
        TODO — Remplir le formulaire et soumettre.
        1. self.input_title.fill(title)
        2. self.input_genre.fill(genre)
        3. self.input_price.fill(str(price))
        4. self.submit_btn.click()
        """
        pass

    def cancel(self):
        """TODO — self.cancel_btn.click()"""
        pass

    def is_visible(self) -> bool:
        """TODO — return self.modal.is_visible()"""
        pass
