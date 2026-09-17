from selenium.webdriver.common.by import By

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
RENT_PERIOD_OPTION = (By.XPATH, "//div[contains(@class,'Dropdown-option') and text()='{period}']")