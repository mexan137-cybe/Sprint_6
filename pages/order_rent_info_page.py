import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from data.order_data import OrderData
from pages.base_page import BasePage
import locators.order_rent_info_page_locators as loc


def _rent_period_option(period: str):
    by, path = loc.RENT_PERIOD_OPTION
    return (by, path.format(period=period))

class OrderRentInfoPage(BasePage):
    @allure.step("Указать дату доставки")
    def set_delivery_date(self, date: str) -> None:
        self.type(loc.DATE_INPUT, date)
        self.wait_visible(loc.DATE_INPUT).send_keys(Keys.ESCAPE)

    @allure.step("Выбрать срок аренды")
    def select_rent_period(self, period: str) -> None:
        self.click(loc.RENT_PERIOD_CONTROL)
        self.click(_rent_period_option(period))

    @allure.step("Выбрать цвет самоката")
    def select_color(self, color: str) -> None:
        color = color.lower()
        if color == "black":
            self.click(loc.COLOR_BLACK_CHECKBOX)
        elif color in ("grey", "gray"):
            self.click(loc.COLOR_GREY_CHECKBOX)
        else:
            raise ValueError(f"Unknown scooter color: {color}")

    @allure.step("Заполнить комментарий для курьера")
    def fill_comment(self, comment: str) -> None:
        if comment:
            self.type(loc.COMMENT_INPUT, comment)

    @allure.step("Нажать на кнопку «Назад»")
    def click_back(self) -> None:
        self.click(loc.BACK_BUTTON)

    @allure.step("Нажать на кнопку «Заказать» на форме")
    def click_order(self) -> None:
        self.click(loc.ORDER_BUTTON)

    @allure.step("Подтвердить заказ в окне «Хотите оформить заказ?»")
    def confirm_order(self) -> None:
        self.js_click(loc.CONFIRM_YES_BUTTON)
        self.wait.until(EC.text_to_be_present_in_element(loc.MODAL_HEADER, loc.SUCCESS_MODAL_TEXT))

    @allure.step("Отменить заказ в модалке «Хотите оформить заказ?»")
    def decline_order(self) -> None:
        self.js_click(loc.CONFIRM_NO_BUTTON)

    @allure.step("Заполнить вторую страницу формы данными и подтвердить заказ")
    def fill_and_submit(self, data: OrderData) -> None:
        self.set_delivery_date(data.delivery_date)
        self.select_rent_period(data.rent_period)
        self.select_color(data.scooter_color)
        self.fill_comment(data.comment)
        self.click_order()
        self.confirm_order()

    @allure.step("Проверить видимость модалки об успешном заказе")
    def is_success_modal_displayed(self) -> bool:
        return self.is_visible(loc.MODAL_HEADER)

    @allure.step("Получить текст модалки об успешном заказе")
    def get_success_modal_text(self) -> str:
        return self.wait_visible(loc.MODAL_HEADER).text.strip()

    @allure.step("Кликнуть по кнопке «Посмотреть статус» в модалке успеха")
    def click_view_status(self) -> None:
        self.js_click(loc.MODAL_NEXT_BUTTON)
