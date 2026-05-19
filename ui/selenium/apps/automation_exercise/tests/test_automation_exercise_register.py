import allure
from ui.selenium.apps.automation_exercise.flows.auth_flow import AutomationExerciseAuthFlow
from ui.selenium.apps.automation_exercise.models.user import User


@allure.epic('Automation Exercise')
@allure.feature('UI Registration')
class TestRegisterCases:
    @allure.story('Successful Registration')
    @allure.title('User can register with valid credentials')
    def test_user_can_register(self, automation_exercise_auth_flow: AutomationExerciseAuthFlow, user: User):
        with allure.step('Register with valid credentials and random email'):
            automation_exercise_auth_flow.register(user)

        with allure.step('Verify logout button is present'):
            assert automation_exercise_auth_flow.home_page.is_authorized()

    @allure.story('Registration fails')
    @allure.title('Registration fails when required field is missing')
    def test_register_fail_missing_required_field(self, automation_exercise_auth_flow, user: User):
        user.mobile_number = ""

        with allure.step('Fill in registration form without mobile number'):
            automation_exercise_auth_flow.fill_registration_data(user)

        with allure.step('Click "create account" button'):
            signup_page = automation_exercise_auth_flow.signup_page
            signup_page.create_account_click()

        mobile_input = signup_page.find(signup_page.MOBILE_NUMBER)
        validity = mobile_input.get_property('validity')

        with allure.step('Verify browser validation error for missing required field is displayed'):
            assert validity['valueMissing'] is True

    @allure.story('Registration fails')
    @allure.title('Registration fails with an already registered email')
    def test_register_fail_duplicate_email(self, automation_exercise_auth_flow, user: User):
        user.email = 'polinaok03@mail.ru'
        login_page = automation_exercise_auth_flow.login_page

        with allure.step('Open signup / login page'):
            login_page.open_basic_auth(automation_exercise_auth_flow.base_url)

        with allure.step(f'Enter existing user name and email ({user.email})'):
            login_page.signup_enter_name(user.name)
            login_page.signup_enter_email(user.email)

        with allure.step('Submit signup form'):
            login_page.signup_click_submit()

        with allure.step('Verify "Email Address already exist!" error message is displayed'):
            error_element = login_page.find(login_page.DUPLICATE_EMAIL_ERROR)
            assert error_element.is_displayed()
