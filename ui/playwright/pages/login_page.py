from ui.playwright.pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_input = '#username'
        self.password_input = '#password'
        self.submit_button = 'button[type="submit"]'
        self.flash_message = '.flash'
        self.error_message = '.error'

    def login(self, username: str, password: str):
        self.page.fill(self.username_input, username)
        self.page.fill(self.password_input, password)
        self.page.click(self.submit_button)

    def get_flash_message(self) -> str:
        return self.page.text_content(self.flash_message)

    def is_error_visible(self) -> bool:
        return self.page.locator(self.error_message).to_be_visible()