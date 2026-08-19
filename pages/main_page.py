from urllib.parse import urlparse
import allure
from selenium.webdriver.common.by import By
from data.config import BASE_URL, YANDEX_LOGO_REDIRECT_HOST
from pages.base_page import BasePage

SCOOTER_LOGO = (By.CSS_SELECTOR, "a.Header_LogoScooter__3lsAR")
YANDEX_LOGO = (By.CSS_SELECTOR, "a.Header_LogoYandex__3TSOI")
ORDER_BUTTON_TOP = (By.XPATH, "(//button[text()='Заказать'])[1]")
ORDER_BUTTON_BOTTOM = (By.XPATH, "(//button[text()='Заказать'])[2]")
FAQ_HEADING_ID = "accordion__heading-"
FAQ_PANEL_ID = "accordion__panel-"

class MainPage(BasePage):
    @allure.step("Открыть главную страницу")
    def open(self) -> "MainPage":
        self.open_url(BASE_URL)
        return self

    @allure.step("Нажать на кнопку «Заказать» в шапке")
    def click_order_button_top(self) -> None:
        self.click(ORDER_BUTTON_TOP)

    @allure.step("Нажать на кнопку «Заказать» в футере")
    def click_order_button_bottom(self) -> None:
        self.scroll_to(ORDER_BUTTON_BOTTOM)
        self.click(ORDER_BUTTON_BOTTOM)

    @allure.step("Нажать на логотип «Самоката» в шапке")
    def click_scooter_logo(self) -> None:
        self.click_robust(SCOOTER_LOGO)

    @allure.step("Нажать на логотип яндекса и получить ссылку страницы")
    def click_yandex_logo_and_get_new_tab_host(self) -> str:
        original_window = self.current_window_handle
        windows_before = self.window_handles
        self.click_robust(YANDEX_LOGO)
        new_window = self.wait_for_new_window(windows_before)
        self.switch_to_window(new_window)
        self.wait_url_contains(YANDEX_LOGO_REDIRECT_HOST)
        current_url = self.current_url
        self.close_current_window()
        self.switch_to_window(original_window)
        return urlparse(current_url).hostname

    @allure.step("Нажать на вопросу №{index} в FAQ")
    def click_faq_question(self, index: int) -> None:
        heading = (By.ID, f"{FAQ_HEADING_ID}{index}")
        self.scroll_to(heading)
        self.click(heading)

    @allure.step("Проверить видимость ответа на вопрос FAQ №{index}")
    def is_faq_answer_visible(self, index: int) -> bool:
        return self.is_visible((By.ID, f"{FAQ_PANEL_ID}{index}"))

    @allure.step("Получить текст ответа на вопрос FAQ №{index}")
    def get_faq_answer_text(self, index: int) -> str:
        return self.wait_visible((By.ID, f"{FAQ_PANEL_ID}{index}")).text.strip()
