import os
import datetime
import pytest
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
from utils.config_reader import config as cfg

# 项目根目录及输出目录
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(ROOT_DIR, "image")
LOG_DIR = os.path.join(ROOT_DIR, cfg.get("log", "dir", default="logs"))
if not os.path.isabs(LOG_DIR):
    LOG_DIR = os.path.join(ROOT_DIR, LOG_DIR)

# 确保输出目录存在
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# -------- playwright driver 管理 --------

_playwright = None
_browser = None
_context = None

# tracing 配置
_tracing_enabled = cfg.get_bool("tracing", "enabled", default=False)
_tracing_dir = cfg.get("tracing", "dir", default="reports/traces")
if not os.path.isabs(_tracing_dir):
    _tracing_dir = os.path.join(ROOT_DIR, _tracing_dir)


@pytest.fixture(scope="session")
def config():
    """返回全局配置字典，供测试用例直接读取配置"""
    return cfg.data


def pytest_configure():
    """pytest 初始化钩子，启动 Playwright 实例并打开浏览器"""
    global _playwright, _browser
    _playwright = sync_playwright().start()
    headless = cfg.get_bool("headless", default=True)
    browser_name = cfg.get("browser", default="chromium")
    launch_type = getattr(_playwright, browser_name, _playwright.chromium)
    _browser = launch_type.launch(headless=headless)
    # session 级别清理过期 trace
    if _tracing_enabled:
        from utils.cleanup import clean_traces
        clean_traces()


def pytest_unconfigure():
    """pytest 退出钩子，关闭浏览器并停止 Playwright 实例"""
    global _browser, _playwright
    if _browser:
        _browser.close()
    if _playwright:
        _playwright.stop()


@pytest.fixture
def context(request):
    """创建浏览器上下文，视口大小 1920x1080，测试结束后自动关闭"""
    global _context
    page_load_timeout = cfg.get_int("timeout", "page_load", default=30000)
    script_timeout = cfg.get_int("timeout", "script", default=10000)
    _context = _browser.new_context(
        viewport={"width": 1920, "height": 1080},
    )
    _context.set_default_timeout(script_timeout)
    _context.set_default_navigation_timeout(page_load_timeout)
    # 开启 tracing
    if _tracing_enabled:
        _context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield _context
    # 保存 tracing 文件：reports/traces/YYYY-MM-DD/test_name.zip
    if _tracing_enabled:
        date_dir = os.path.join(_tracing_dir, datetime.datetime.now().strftime("%Y-%m-%d"))
        os.makedirs(date_dir, exist_ok=True)
        safe_name = request.node.name.replace("::", "_").replace(" ", "_")
        trace_path = os.path.join(date_dir, f"{safe_name}.zip")
        _context.tracing.stop(path=trace_path)
    _context.close()


@pytest.fixture
def page(context: BrowserContext) -> Page:
    """创建新页面，测试结束后自动关闭"""
    p = context.new_page()
    yield p
    p.close()


# -------- 失败自动截图 --------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试执行报告钩子，当用例执行失败时自动截图保存到 image 目录"""
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
