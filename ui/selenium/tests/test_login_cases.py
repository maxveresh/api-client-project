def test_user_can_login_via_ui(auth_flow_ui):
    secure_page = auth_flow_ui.login_via_ui(
        'tomsmith',
        'SuperSecretPassword!'
    )
    assert secure_page.is_loaded()
    assert secure_page.find(secure_page._logout_button).is_displayed()

def test_user_can_logout(auth_flow_ui):
    secure_page = auth_flow_ui.login_via_ui(
        'tomsmith',
        'SuperSecretPassword!'
    )
    secure_page.click_logout_button()
    logout_message = secure_page.get_flash_message()
    assert 'You logged out of the secure area!' in logout_message

def test_login_with_invalid_credentials(auth_flow_ui, base_url_ui):
    login_page = auth_flow_ui.login_page
    secure_page = auth_flow_ui.secure_page
    login_page.open_basic_auth(base_url_ui)

    login_page.enter_username('tomsmith')
    login_page.enter_password('wrong_password')
    login_page.submit()

    error_text = secure_page.get_flash_message()
    assert 'Your password is invalid' in error_text


def test_login_with_error_displayed(auth_flow_ui, base_url_ui):
    login_page = auth_flow_ui.login_page
    secure_page = auth_flow_ui.secure_page
    login_page.open_basic_auth(base_url_ui)

    login_page.submit()
    assert secure_page.is_error_displayed()

