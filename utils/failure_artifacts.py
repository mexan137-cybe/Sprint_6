import datetime
import re
from pathlib import Path

"""Сохранение отладочных артефактов при падении теста.

Для каждого упавшего теста создаётся отдельная папка внутри test-failures/
с именем вида "<время>_<имя теста>", куда складываются:
    screenshot.png       — скриншот страницы в момент падения
    page_source.html     — HTML DOM страницы в момент падения
    info.txt              — текущий URL, заголовок страницы, время падения
    browser_console.log  — консольные логи браузера (если драйвер их отдаёт)
"""

# Корень проекта = на уровень выше папки utils/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
FAILURES_DIR = PROJECT_ROOT / "test-failures"


def _sanitize(name: str) -> str:
    """Убирает из имени теста символы, недопустимые в именах файлов/папок."""
    return re.sub(r'[<>:"/\\|?*\s]+', "_", name).strip("_")[:150]


def save_failure_artifacts(driver, test_name: str) -> Path:
    """Сохраняет скриншот, page source, текущий URL и консольные логи
    браузера в отдельную папку под test-failures/. Возвращает путь к папке.
    """
    FAILURES_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder = FAILURES_DIR / f"{timestamp}_{_sanitize(test_name)}"
    folder.mkdir(parents=True, exist_ok=True)

    # 1. Скриншот
    try:
        driver.save_screenshot(str(folder / "screenshot.png"))
    except Exception as e:
        _write(folder / "screenshot_error.txt", f"Не удалось сделать скриншот: {e}")

    # 2. HTML страницы
    try:
        (folder / "page_source.html").write_text(driver.page_source, encoding="utf-8")
    except Exception as e:
        _write(folder / "page_source_error.txt", f"Не удалось сохранить page source: {e}")

    # 3. Текущий URL / заголовок / время
    try:
        info = (
            f"Тест: {test_name}\n"
            f"Время падения: {timestamp}\n"
            f"URL: {driver.current_url}\n"
            f"Заголовок страницы: {driver.title}\n"
        )
        _write(folder / "info.txt", info)
    except Exception as e:
        _write(folder / "info_error.txt", f"Не удалось собрать info.txt: {e}")

    # 4. Консольные логи браузера (доступны только для Chrome/Chromium)
    try:
        logs = driver.get_log("browser")
        lines = [f"[{entry['level']}] {entry['message']}" for entry in logs]
        _write(folder / "browser_console.log", "\n".join(lines) or "(логов нет)")
    except Exception as e:
        _write(folder / "browser_console_error.txt", f"Не удалось получить консольные логи: {e}")

    return folder


def _write(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")
