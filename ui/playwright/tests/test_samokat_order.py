import allure
import pytest
from ui.playwright.pages.order_page import OrderPage

pytestmark = pytest.mark.playwright

@allure.epic('Yandex Samokat')
@allure.feature('Order creation')
@allure.story('Successful order creation')
@allure.title('User can make order with valid data')
def test_make_order(page, config):
    order_page = OrderPage(page)

    with allure.step('Open order page'):
        order_page.open(f'{config.BASE_URLS['samokat']}order')

    with allure.step('Make order with valid data'):
        order_page.make_order(
            'Макс',
            'Верещагин',
            'Ул.Фомичева 12,88',
            'Бульвар Рокоссовского',
            '80336230818',
            '03.03.2026',
            'сутки',
            'чёрный',
            'ничего..'
        )
