import time

from playwright.sync_api import expect

from ui.playwright.pages.base_page import BasePage


class OrderPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.name_input = page.get_by_role("textbox", name="Имя")
        self.second_name_input = page.get_by_role("textbox", name="Фамилия")
        self.adress_input = page.get_by_role("textbox", name="Адрес")
        self.metro_station_input = page.get_by_role('textbox', name='Станция')
        self.number_input = page.get_by_role("textbox", name='Телефон')
        self.next_button = page.get_by_role("button", name="Далее")

        self.date_input = page.get_by_role('textbox', name='привезти')
        self.rental_control = page.get_by_text('Срок аренды')
        self.comment = page.get_by_role('textbox', name='Комментарий')

        self.go_back_button = page.get_by_role('button', name='Назад')

        self.submit_button = '//button[contains(@class,"Button_Middle") and text()="Заказать"]'
        self.yes_button = '//button[contains(@class,"Button_Middle") and text()="Да"]'
        self.no_button = '//button[contains(@class,"Button_Middle") and text()="Нет"]'

        # Через get_by_role:
        # self.submit_button = page.get_by_role("button", name="Заказать")
        # self.yes_button = page.get_by_role("button", name="Да")
        # self.no_button = page.get_by_role("button", name="Нет")

    def make_order(
            self,
            name: str,
            second_name: str,
            adress: str,
            metro_station: str,
            number: str,
            date: str,
            rental_period: str,
            color: str,
            comment: str
    ):
        self.name_input.fill(name)
        self.second_name_input.fill(second_name)
        self.adress_input.fill(adress)
        self.select_metro_station(metro_station)
        self.number_input.fill(number)
        self.next_button.click()

        self.select_delivery_date(date)
        self.select_rental_period(rental_period)
        self.page.get_by_label(color).check()
        self.comment.fill(comment)
        self.page.click(self.submit_button)
        self.page.click(self.yes_button)


    def select_metro_station(self, station_name: str):
        self.metro_station_input.click()

        dropdown = self.page.locator('.select-search__select')
        expect(dropdown).to_be_visible()

        option = dropdown.get_by_role('menuitem', name=station_name).first
        expect(option).to_be_visible()

        option.click()
        expect(self.metro_station_input).to_have_value(station_name)

    def select_delivery_date(self, date: str):
        self.date_input.fill(date)
        self.date_input.press('Enter')

        expect(self.date_input).to_have_value(date)


    def select_rental_period(self, period: str):
        self.rental_control.click()

        menu = self.page.locator('.Dropdown-menu')
        expect(menu).to_be_visible()

        option = menu.locator(f'text={period}').first
        expect(option).to_be_visible()

        option.click()




