import pytest

from data.config import BASE_URL, YANDEX_LOGO_REDIRECT_HOST
from data.order_data import OrderData
from pages.main_page import MainPage
from pages.order_personal_info_page import OrderPersonalInfoPage
from pages.order_rent_info_page import OrderRentInfoPage

FIRST_DATA_SET = OrderData(
    first_name="Александр",
    last_name="Фирсов",
    address="Санкт-Петербург, ул. Правды, д. 23",
    metro_station="Маяковская",
    phone="+79667885463",
    delivery_date="12.12.2026",
    rent_period="двое суток",
    scooter_color="black",
    comment="Срочная доставка",
)

SECOND_DATA_SET = OrderData(
    first_name="Игорь",
    last_name="Пиков",
    address="Москва, Ленина пр-т, д. 103",
    metro_station="Комсомольская",
    phone="+79448239393",
    delivery_date="11.10.2026",
    rent_period="пятеро суток",
    scooter_color="grey",
    comment="",
)

ORDER_SCENARIOS = [
    ("top", FIRST_DATA_SET),
    ("bottom", SECOND_DATA_SET),
]

@pytest.mark.parametrize(
    "entry_point, data",
    ORDER_SCENARIOS,
    ids=[f"{ep}-{data}" for ep, data in ORDER_SCENARIOS],
)
def test_positive_order_scenario(driver, entry_point, data):
    main_page = MainPage(driver).open()

    if entry_point == "top":
        main_page.click_order_button_top()
    else:
        main_page.click_order_button_bottom()
    personal_info_page = OrderPersonalInfoPage(driver)
    personal_info_page.fill_and_go_next(data)
    rent_info_page = OrderRentInfoPage(driver)
    rent_info_page.fill_and_submit(data)
    assert rent_info_page.is_success_modal_displayed(), ("Модальное окно об успешном заказе должно появиться")
    assert "Заказ оформлен" in rent_info_page.get_success_modal_text(), ("Текст модального окна должен подтверждать оформление заказа")
    main_page.click_scooter_logo()
    assert main_page.current_url == BASE_URL, ("Клик по логотипу самоката должен вести на главную страницу")
    new_tab_host = main_page.click_yandex_logo_and_get_new_tab_host()
    assert YANDEX_LOGO_REDIRECT_HOST in new_tab_host, (f"Логотип Яндекса должен открывать {YANDEX_LOGO_REDIRECT_HOST}, "f"а открылось: {new_tab_host}")
