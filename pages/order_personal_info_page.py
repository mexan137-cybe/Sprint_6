import allure
from selenium.webdriver.common.by import By
from data.order_data import OrderData
from pages.base_page import BasePage

NAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='* Имя']")
SURNAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='* Фамилия']")
ADDRESS_INPUT = (By.CSS_SELECTOR, "input[placeholder='* Адрес: куда привезти заказ']")
METRO_INPUT = (By.CSS_SELECTOR, ".select-search__input")
PHONE_INPUT = (By.CSS_SELECTOR, "input[placeholder='* Телефон: на него позвонит курьер']")
NEXT_BUTTON = (By.XPATH, "//button[text()='Далее']")

def _metro_option(station: str):
    return (By.XPATH,"//div[contains(@class,'select-search__select')]"f"//li//button[contains(., '{station}')]",)

class OrderPersonalInfoPage(BasePage):
    @allure.step("Заполнить поле «Имя»")
    def fill_first_name(self, value: str) -> None:
        self.type(NAME_INPUT, value)

    @allure.step("Заполнить поле «Фамилия»")
    def fill_last_name(self, value: str) -> None:
        self.type(SURNAME_INPUT, value)

    @allure.step("Заполнить поле «Адрес»")
    def fill_address(self, value: str) -> None:
        self.type(ADDRESS_INPUT, value)

    @allure.step("Выбрать станцию метро")
    def select_metro_station(self, station: str) -> None:
        self.type(METRO_INPUT, station)
        self.click(_metro_option(station))

    @allure.step("Заполнить поле «Телефон»")
    def fill_phone(self, value: str) -> None:
        self.type(PHONE_INPUT, value)

    @allure.step("Кликнуть по кнопке «Далее»")
    def click_next(self) -> None:
        self.click(NEXT_BUTTON)

    @allure.step("Заполнить первую страницу формы заказа данными и перейти дальше")
    def fill_and_go_next(self, data: OrderData) -> None:
        self.fill_first_name(data.first_name)
        self.fill_last_name(data.last_name)
        self.fill_address(data.address)
        self.select_metro_station(data.metro_station)
        self.fill_phone(data.phone)
        self.click_next()
