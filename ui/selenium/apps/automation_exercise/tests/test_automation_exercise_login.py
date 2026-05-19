import allure
from ui.selenium.apps.automation_exercise.conftest import auth_credentials


@allure.epic('Automation Exercise')
@allure.feature('UI Authentication')
class TestLoginCases:
    @allure.story('Successful Login')
    @allure.title('User can login with valid credentials')
    def test_user_can_login(self, automation_exercise_auth_flow, auth_credentials):
        with allure.step('Login via UI'):
            automation_exercise_auth_flow.login(
                auth_credentials.email,
                auth_credentials.password
            )

        home_page = automation_exercise_auth_flow.home_page
        with allure.step('Verify logout button is present'):
            assert home_page.is_authorized()

    @allure.story('Logout')
    @allure.title('User can logout successfully')
    def test_user_can_logout(self, logged_in_session):
        with allure.step('Login via UI'):
            home_page = logged_in_session.home_page

        with allure.step('Click logout button'):
            home_page.logout_click()

        with allure.step('Verify user is on the login page'):
            assert "/login" in home_page.driver.current_url

    @allure.story('Invalid login')
    @allure.title('Login fails with wrong credentials')
    def test_login_fail_invalid_credentials(self, automation_exercise_auth_flow, auth_credentials):
        with allure.step('Try to login with wrong credentials'):
            automation_exercise_auth_flow.login(
                auth_credentials.email,
                'wrong_password'
            )

        login_page = automation_exercise_auth_flow.login_page

        with allure.step('Verify error message is displayed'):
            error_message = login_page.find(login_page.INCORRECT_DATA_ERROR)
            assert error_message.is_displayed()
