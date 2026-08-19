import pytest
from pages.main_page import MainPage
from data.config import FAQ_DATA

@pytest.mark.parametrize(
    "question_index, question, expected_answer",
    FAQ_DATA,
    ids=[item[1] for item in FAQ_DATA],
)
def test_faq_answer_is_shown_on_click(driver, question_index, question, expected_answer):
    main_page = MainPage(driver).open()
    main_page.click_faq_question(question_index)
    assert main_page.is_faq_answer_visible(question_index) and main_page.get_faq_answer_text(question_index) == expected_answer, (
        f'Ответ на вопрос "{question}" должен стать видимым после клика'
    )
