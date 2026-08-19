import pytest
from data.config import FIRST_DATA_SET, SECOND_DATA_SET, YANDEX_LOGO_REDIRECT_HOST
from pages.main_page import MainPage
from pages.order_personal_info_page import OrderPersonalInfoPage
from pages.order_rent_info_page import OrderRentInfoPage


def test_positive_order_scenario(driver):
    data = FIRST_DATA_SET
    MainPage(driver).open().click_order_button_top()
    OrderPersonalInfoPage(driver).fill_and_go_next(data)
    OrderRentInfoPage(driver).fill_and_submit(data)
    main_page = MainPage(driver)
    main_page.click_scooter_logo()
    new_tab_host = main_page.click_yandex_logo_and_get_new_tab_host()
    assert YANDEX_LOGO_REDIRECT_HOST in new_tab_host, (f"Логотип Яндекса должен открывать {YANDEX_LOGO_REDIRECT_HOST}, "f"а открылось: {new_tab_host}")

def test_order_via_bottom_button(driver):
    data = SECOND_DATA_SET
    MainPage(driver).open().click_order_button_bottom()
    OrderPersonalInfoPage(driver).fill_and_go_next(data)
    OrderRentInfoPage(driver).fill_and_submit(data)
    main_page = MainPage(driver)
    main_page.click_scooter_logo()
    new_tab_host = main_page.click_yandex_logo_and_get_new_tab_host()
    assert YANDEX_LOGO_REDIRECT_HOST in new_tab_host, (f"Логотип Яндекса должен открывать {YANDEX_LOGO_REDIRECT_HOST}, "f"а открылось: {new_tab_host}")