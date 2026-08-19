from selenium.webdriver.common.by import By

SCOOTER_LOGO = (By.CSS_SELECTOR, "a.Header_LogoScooter__3lsAR")
YANDEX_LOGO = (By.CSS_SELECTOR, "a.Header_LogoYandex__3TSOI")
ORDER_BUTTON_TOP = (By.XPATH, "(//button[text()='Заказать'])[1]")
ORDER_BUTTON_BOTTOM = (By.XPATH, "(//button[text()='Заказать'])[2]")
FAQ_HEADING_ID = "accordion__heading-"
FAQ_PANEL_ID = "accordion__panel-"