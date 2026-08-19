## Структура проекта

```
data/
  config.py          — базовый URL, прочие константы
  order_data.py       — dataclass с набором данных для сценария заказа

pages/
  base_page.py               — общий родитель Page Object (ожидания, robust-клик)
  main_page.py                — главная страница: шапка (логотипы, кнопки «Заказать»), блок FAQ
  order_personal_info_page.py — 1-й шаг формы заказа («Для кого самокат»)
  order_rent_info_page.py     — 2-й шаг формы заказа («Про аренду») + модалка об успехе

tests/
  conftest.py     — фикстура driver: поднимает/закрывает браузер (Firefox по
                     умолчанию, либо Chrome через --browser=chrome) для каждого теста,
                     при падении теста сохраняет отладочные артефакты в test-failures/
  test_faq.py     — параметризованный тест блока «Вопросы о важном» (8 вопросов)
  test_order.py   — параметризованный позитивный сценарий заказа (2 набора данных,
                     2 точки входа — каждая точка входа используется один раз)

utils/
  failure_artifacts.py — сохранение скриншота/HTML/логов при падении теста

test-failures/
  — сюда автоматически складываются артефакты упавших тестов (см. раздел ниже)
```

## Установка и запуск

Нужны Python 3.9+ и установленный Firefox (по умолчанию) или Chrome.

```bash
pip install -r requirements.txt
pytest
```

По умолчанию тесты запускаются в **Firefox**. Драйвер браузера (geckodriver)
подтягивается автоматически через `webdriver-manager`.

Запуск в Chrome вместо Firefox:

```bash
pytest --browser=chrome
```

Запуск в headless-режиме (можно сочетать с `--browser`):

```bash
pytest --headless
pytest --browser=chrome --headless
```

Запустить только один файл тестов:

```bash
pytest tests/test_faq.py
pytest tests/test_order.py -v
```

## Отладка падений (test-failures)

Если тест падает, фикстура `driver` (см. `tests/conftest.py`) автоматически
сохраняет отладочные артефакты в `test-failures/<время>_<имя_теста>/`:

* `screenshot.png` — скриншот страницы в момент падения;
* `page_source.html` — HTML DOM страницы в момент падения (можно открыть
  в браузере, чтобы посмотреть, что реально отрендерилось);
* `info.txt` — текущий URL, заголовок страницы, время падения;
* `browser_console.log` — консольные логи браузера (ошибки JS, warnings и т.д.).


## Allure-отчёты

Зависимость `allure-pytest` уже в `requirements.txt`. Сбор результатов:

```bash
pytest --alluredir=allure_results
```

```bash
allure serve allure_results        # поднимет локальный сервер с отчётом
# или
allure generate allure_results -o allure_report --clean
```

## Параметризация

* `test_faq.py` — `@pytest.mark.parametrize`, один набор параметров
  (индекс вопроса, текст вопроса, ожидаемый текст ответа) на каждый из 8
  вопросов блока FAQ.
* `test_order.py` — `@pytest.mark.parametrize`, два набора параметров:
  (точка входа `"top"`/`"bottom"`, набор данных `OrderData`). Сценарий один и
  тот же, поэтому каждая точка входа проверяется только один раз — но за счёт
  этого обе точки входа и оба набора данных оказываются покрыты без
  дублирования прогона всего сценария.

