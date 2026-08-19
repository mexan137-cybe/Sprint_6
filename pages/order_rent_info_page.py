import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from data.order_data import OrderData
from pages.base_page import BasePage

DATE_INPUT = (By.CSS_SELECTOR, "input[placeholder='* Когда привезти самокат']")
RENT_PERIOD_CONTROL = (By.CLASS_NAME, "Dropdown-control")
COLOR_BLACK_CHECKBOX = (By.ID, "black")
COLOR_GREY_CHECKBOX = (By.ID, "grey")
COMMENT_INPUT = (By.CSS_SELECTOR, "input[placeholder='Комментарий для курьера']")
BACK_BUTTON = (By.XPATH, "//button[text()='Назад']")
ORDER_BUTTON = (By.XPATH, "//div[contains(@class,'Order_Buttons')]//button[text()='Заказать']")
MODAL_HEADER = (By.CSS_SELECTOR, ".Order_Modal__YZ-d3 .Order_ModalHeader__3FDaJ")
MODAL_NEXT_BUTTON = (By.XPATH,"//div[contains(@class,'Order_Modal')]//button[text()='Посмотреть статус']",)
CONFIRM_YES_BUTTON = (By.XPATH, "//div[contains(@class,'Order_Modal')]//button[text()='Да']")
CONFIRM_NO_BUTTON = (By.XPATH, "//div[contains(@class,'Order_Modal')]//button[text()='Нет']")
SUCCESS_MODAL_TEXT = "Заказ оформлен"

def _rent_period_option(period: str):
    return (By.XPATH, f"//div[contains(@class,'Dropdown-option') and text()='{period}']")

class OrderRentInfoPage(BasePage):
    @allure.step("Указать дату доставки")
    def set_delivery_date(self, date: str) -> None:
        self.type(DATE_INPUT, date)
        self.wait_visible(DATE_INPUT).send_keys(Keys.ESCAPE)

    @allure.step("Выбрать срок аренды")
    def select_rent_period(self, period: str) -> None:
        self.click(RENT_PERIOD_CONTROL)
        self.click(_rent_period_option(period))

    @allure.step("Выбрать цвет самоката")
    def select_color(self, color: str) -> None:
        color = color.lower()
        if color == "black":
            self.click(COLOR_BLACK_CHECKBOX)
        elif color in ("grey", "gray"):
            self.click(COLOR_GREY_CHECKBOX)
        else:
            raise ValueError(f"Unknown scooter color: {color}")

    @allure.step("Заполнить комментарий для курьера")
    def fill_comment(self, comment: str) -> None:
        if comment:
            self.type(COMMENT_INPUT, comment)

    @allure.step("Нажать на кнопку «Назад»")
    def click_back(self) -> None:
        self.click(BACK_BUTTON)

    @allure.step("Нажать на кнопку «Заказать» на форме")
    def click_order(self) -> None:
        self.click(ORDER_BUTTON)

    @allure.step("Подтвердить заказ в окне «Хотите оформить заказ?»")
    def confirm_order(self) -> None:
        self.js_click(CONFIRM_YES_BUTTON)
        self.wait.until(EC.text_to_be_present_in_element(MODAL_HEADER, SUCCESS_MODAL_TEXT))

    @allure.step("Отменить заказ в модалке «Хотите оформить заказ?»")
    def decline_order(self) -> None:
        self.js_click(CONFIRM_NO_BUTTON)

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
        return self.is_visible(MODAL_HEADER)

    @allure.step("Получить текст модалки об успешном заказе")
    def get_success_modal_text(self) -> str:
        return self.wait_visible(MODAL_HEADER).text.strip()

    @allure.step("Кликнуть по кнопке «Посмотреть статус» в модалке успеха")
    def click_view_status(self) -> None:
        self.js_click(MODAL_NEXT_BUTTON)
