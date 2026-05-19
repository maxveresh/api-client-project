from selenium.webdriver.common.by import By

from ui.selenium.apps.automation_exercise.models.product import Product
from ui.selenium.apps.automation_exercise.pages.home_page import HomePage

class ProductsPage(HomePage):

    def add_to_cart(self, product: Product):
        locator = (By.XPATH, f"//a[@data-product-id='{product.id}']")
        self.click_when_clickable(locator)

    def view_product(self, product: Product):
        locator = (By.XPATH, f"//a[@href='/product_details/{product.id}']")
        self.click_when_clickable(locator)