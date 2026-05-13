import allure

@allure.epic('Authentication')
@allure.feature('Selenium UI Login')
class TestAuthSeleniumUI:
    @allure.story('Successful login')
    @allure.title('User can login via UI')
    def test_user_can_login_via_ui(self, the_internet_auth_flow):
        with allure.step('Login via UI'):
            secure_page = the_internet_auth_flow.login_via_ui(
                'tomsmith',
                'SuperSecretPassword!'
            )

        with allure.step('Verify secure page is loaded'):
            assert secure_page.is_loaded()

        with allure.step('Verify logout button is visible'):
            assert secure_page.find(secure_page.LOGOUT_BUTTON).is_displayed()

    @allure.story('Logout')
    @allure.title('User can logout successfully')
    def test_user_can_logout(self, the_internet_auth_flow):
        with allure.step('Login via UI'):
            secure_page = the_internet_auth_flow.login_via_ui(
                'tomsmith',
                'SuperSecretPassword!'
            )

        with allure.step('Click logout button'):
            secure_page.click_logout_button()

        with allure.step('Verify logout message'):
            logout_message = secure_page.get_flash_message()
            assert 'You logged out of the secure area!' in logout_message

    @allure.story('Invalid login')
    @allure.title('Error message displayed with wrong credentials')
    def test_login_with_invalid_credentials(self, the_internet_auth_flow):
        login_page = the_internet_auth_flow.login_page
        secure_page = the_internet_auth_flow.secure_page

        with allure.step('Open login page'):
            login_page.open_basic_auth(the_internet_auth_flow.base_url)

        with allure.step('Enter invalid credentials'):
            login_page.enter_username('tomsmith')
            login_page.enter_password('wrong_password')
            login_page.submit()

        with allure.step('Verify error message'):
            error_text = secure_page.get_flash_message()
            assert 'Your password is invalid' in error_text

    @allure.story('Validation')
    @allure.title('Error displayed when submitting empty form')
    def test_login_with_error_displayed(self, the_internet_auth_flow):
        login_page = the_internet_auth_flow.login_page
        secure_page = the_internet_auth_flow.secure_page

        with allure.step('Open login page'):
            login_page.open_basic_auth(the_internet_auth_flow.base_url)

        with allure.step('Submit empty form'):
            login_page.submit()

        with allure.step('Verify error is displayed'):
            assert secure_page.is_error_displayed()

