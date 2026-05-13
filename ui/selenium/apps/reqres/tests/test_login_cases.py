# import allure
#
# @allure.epic('Authentication')
# @allure.feature('Selenium UI Login')
# class TestAuthSeleniumUI:
#     @allure.story('Real API login')
#     @allure.title('User can authenticate via real API and receive token')
#     def test_user_can_login_via_api(self, auth_flow_selenium):
#         with allure.step('Login via real API'):
#             token = auth_flow_selenium.login_via_api(
#                 'eve.holt@reqres.in',
#                 'cityslicka'
#             )
#
#         with allure.step('Validate token is returned'):
#             allure.attach(
#                 str(token),
#                 name='JWT token',
#                 attachment_type=allure.attachment_type.TEXT
#             )
#             assert token