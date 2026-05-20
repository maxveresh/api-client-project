import allure
import pytest
from selenium.webdriver.common.by import By
from ui.selenium.apps.automation_exercise.models.product import Product

pytestmark = pytest.mark.selenium

@allure.epic('Automation Exercise')
@allure.feature('UI. Cart & Checkout')
class TestShoppingCases:
    SUCCESS_BUTTON = (By.XPATH, "//button[contains(text(),'Continue Shopping')]")
    VIEW_CART_BUTTON = (By.XPATH, '//div[@class="modal-content"]//a[@href="/view_cart"]')

    @allure.story('Add items to cart')
    @allure.title('Add multiple products to the cart and verify their details')
    def test_add_products_in_cart(self, logged_in_session, vignette_checker):
        home_page = logged_in_session.home_page
        with allure.step('Navigate to the Products page'):
            home_page.click_when_clickable(home_page.PRODUCTS_BUTTON)

        with allure.step('Catch Google Vignette ad'):
            vignette_checker()

        product_1 = Product(id=1, name='Blue Top')
        product_2 = Product(id=2, name='Men Tshirt')
        products_page = logged_in_session.products_page

        with allure.step(f'Add first product "{product_1.name}" to the cart'):
            products_page.add_to_cart(product_1)
            products_page.click_when_clickable(self.SUCCESS_BUTTON)

        with allure.step(f'Add second product "{product_2.name}" to the cart'):
            products_page.add_to_cart(product_2)
            products_page.click_when_clickable(self.VIEW_CART_BUTTON)

        cart_page = logged_in_session.cart_page
        with allure.step('Retrieve product information from the cart page'):
            product_1_info = cart_page.get_product_info(product_1.id)
            product_2_info = cart_page.get_product_info(product_2.id)

        with allure.step(f'Verify details for "{product_1.name}" (Price: Rs. 500)'):
            assert product_1_info['name'] == product_1.name
            assert product_1_info['price'] == 'Rs. 500'

        with allure.step(f'Verify details for "{product_2.name}" (Price: Rs. 400)'):
            assert product_2_info['name'] == product_2.name
            assert product_2_info['price'] == 'Rs. 400'
