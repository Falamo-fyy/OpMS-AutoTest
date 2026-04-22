import logging
import os
import datetime

import pytest
from playwright.sync_api import Page

from base.base_page import BasePage

# 项目根目录
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _screenshot_dir() -> str:
    """获取截图保存目录，不存在则自动创建"""
    path = os.path.join(ROOT_DIR, "image")
    os.makedirs(path, exist_ok=True)
    return path


def _log_dir() -> str:
    """获取日志保存目录，不存在则自动创建"""
    path = os.path.join(ROOT_DIR, "logs")
    os.makedirs(path, exist_ok=True)
    return path


def _timestamp() -> str:
    """获取当前时间戳字符串，格式：20260422_143000"""
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def _get_logger(name: str) -> logging.Logger:
    """创建并返回日志记录器，同时输出到文件和控制台

    Args:
        name: 日志记录器名称，通常为测试用例名
    """
    log_dir = _log_dir()
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(
            os.path.join(log_dir, f"{_timestamp()}.log"), encoding="utf-8"
        )
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        fmt = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        fh.setFormatter(fmt)
        ch.setFormatter(fmt)
        logger.addHandler(fh)
        logger.addHandler(ch)
    return logger


class BaseTest:
    """测试基类，提供 driver 管理、截图、日志、失败重试等通用能力

    子类继承后可直接使用 self.page、self.base_page、self.logger 等属性
    """

    page: Page
    base_page: BasePage
    logger: logging.Logger

    @pytest.fixture(autouse=True)
    def _setup(self, page: Page, request):
        """自动注入的 setup fixture，每个测试用例执行前初始化 page、base_page、logger"""
        self.page = page
        self.base_page = BasePage(page)
        self.logger = _get_logger(request.node.name)
        self._test_name = request.node.name

    def save_screenshot(self, name: str = None) -> str:
        """手动截图并保存到 image 目录

        Args:
            name: 截图标识名，默认使用当前测试用例名

        Returns:
            截图文件的完整路径
        """
        tag = name or self._test_name
        filename = f"{_timestamp()}_{tag}.png"
        path = os.path.join(_screenshot_dir(), filename)
        self.page.screenshot(path=path, full_page=True)
        self.logger.info(f"截图已保存: {path}")
        return path

    def save_screenshot_on_failure(self) -> str | None:
        """测试失败时自动截图，成功则不操作

        Returns:
            失败时返回截图路径，成功时返回 None
        """
        try:
            outcome = pytest.test_result  # type: ignore[attr-defined]
        except AttributeError:
            return None
        if outcome and outcome.excinfo is not None:
            return self.save_screenshot("fail")
        return None

    def log_step(self, msg: str):
        """记录测试步骤日志（INFO 级别）"""
        self.logger.info(f"[STEP] {msg}")

    def log_data(self, msg: str):
        """记录测试数据日志（DEBUG 级别）"""
        self.logger.debug(f"[DATA] {msg}")
