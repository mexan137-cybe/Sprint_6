from selenium.webdriver.common.by import By

NAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='* Имя']")
SURNAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='* Фамилия']")
ADDRESS_INPUT = (By.CSS_SELECTOR, "input[placeholder='* Адрес: куда привезти заказ']")
METRO_INPUT = (By.CSS_SELECTOR, ".select-search__input")
PHONE_INPUT = (By.CSS_SELECTOR, "input[placeholder='* Телефон: на него позвонит курьер']")
NEXT_BUTTON = (By.XPATH, "//button[text()='Далее']")