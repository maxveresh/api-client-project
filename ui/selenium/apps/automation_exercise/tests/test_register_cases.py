from ui.selenium.apps.automation_exercise.flows.auth_flow import AutomationExerciseAuthFlow
from ui.selenium.apps.automation_exercise.models.user import User


class TestRegisterCases:
    def test_user_can_register(self, automation_exercise_auth_flow: AutomationExerciseAuthFlow, user: User):
        automation_exercise_auth_flow.register(user)
        assert automation_exercise_auth_flow.home_page.is_authorized()

    def test_register_fail_missing_required_field(self, automation_exercise_auth_flow, user: User):
        user.mobile_number = ""

        automation_exercise_auth_flow.fill_registration_data(user)
        signup_page = automation_exercise_auth_flow.signup_page
        signup_page.create_account_click()

        mobile_input = signup_page.find(
            signup_page.MOBILE_NUMBER
        )

        validity = mobile_input.get_property('validity')

        assert validity['valueMissing'] is True

    def test_register_fail_duplicate_email(self, automation_exercise_auth_flow, user: User):
        user.email = 'polinaok03@mail.ru'
        login_page = automation_exercise_auth_flow.login_page
        login_page.open_basic_auth(automation_exercise_auth_flow.base_url)
        login_page.signup_enter_name(user.name)
        login_page.signup_enter_email(user.email)
        login_page.signup_click_submit()

        error_element = login_page.find(login_page.DUPLICATE_EMAIL_ERROR)

        assert error_element.is_displayed()
