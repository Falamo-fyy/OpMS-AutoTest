import os
import pytest
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(ROOT_DIR, "image")
LOG_DIR = os.path.join(ROOT_DIR, "logs")

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# -------- playwright driver 管理 --------

_playwright = None
_browser: Browser | None = None
_context: BrowserContext | None = None


def pytest_configure(config):
    global _playwright, _browser
    _playwright = sync_playwright().start()
    headless = config.getini("headless") if config.hasini("headless") else True
    _browser = _playwright.chromium.launch(headless=headless)


def pytest_unconfigure(config):
    global _browser, _playwright
    if _browser:
        _browser.close()
    if _playwright:
        _playwright.stop()


@pytest.fixture
def context():
    global _context
    _context = _browser.new_context(viewport={"width": 1920, "height": 1080})
    yield _context
    _context.close()


@pytest.fixture
def page(context: BrowserContext) -> Page:
    p = context.new_page()
    yield p
    p.close()


# -------- 失败自动截图 --------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page: Page | None = item.funcargs.get("page")
        if page:
            ts = __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(IMAGE_DIR, f"{ts}_{item.name}_fail.png")
            try:
                page.screenshot(path=path, full_page=True)
            except Exception:
                pass
