from conftest import samokat_url
from ui.playwright.pages.order_page import OrderPage


def test_make_order(page, samokat_url):
    order_page = OrderPage(page)
    order_page.open(f'{samokat_url}order')

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











