from ui.selenium.apps.automation_exercise.conftest import auth_credentials


class TestLoginCases:
    def test_user_can_login(self, automation_exercise_auth_flow, auth_credentials):
        automation_exercise_auth_flow.login(
            auth_credentials.email,
            auth_credentials.password
        )

        home_page = automation_exercise_auth_flow.home_page

        assert home_page.is_authorized()

    def test_user_can_logout(self, automation_exercise_auth_flow, auth_credentials, logged_in_session):
        home_page = logged_in_session.home_page
        home_page.logout_click()

        assert "/login" in home_page.driver.current_url


    def test_login_fail_invalid_credentials(self, automation_exercise_auth_flow, auth_credentials):
        automation_exercise_auth_flow.login(
            auth_credentials.email,
            'wrong_password'
        )

        login_page = automation_exercise_auth_flow.login_page
        error_message = login_page.find(login_page.INCORRECT_DATA_ERROR)

        assert error_message.is_displayed()
