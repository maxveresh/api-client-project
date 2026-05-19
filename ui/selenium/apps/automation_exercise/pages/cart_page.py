from selenium.webdriver.common.by import By
from ui.selenium.apps.automation_exercise.pages.home_page import HomePage


class CartPage(HomePage):
    def get_product_info(self, product_id):
        base = f"//tr[@id='product-{product_id}']"

        name = self.get_text((By.XPATH, base + "//h4/a"))
        price = self.get_text((By.XPATH, base + "//td[@class='cart_price']//p"))
        quantity = self.get_text((By.XPATH, base + "//td[@class='cart_quantity']//button"))
        total = self.get_text((By.XPATH, base + "//p[@class='cart_total_price']"))

        return {
            "name": name,
            "price": price,
            "quantity": int(quantity),
            "total": total
        }
