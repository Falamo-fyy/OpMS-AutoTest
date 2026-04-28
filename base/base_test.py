import os
import datetime

import pytest
from playwright.sync_api import Page

from base.base_page import BasePage
from utils.logger import Logger

# 项目根目录
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _screenshot_dir() -> str:
    """获取截图保存目录，不存在则自动创建"""
    path = os.path.join(ROOT_DIR, "image")
    os.makedirs(path, exist_ok=True)
    return path


def _timestamp() -> str:
    """获取当前时间戳字符串，格式：20260422_143000"""
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


class BaseTest:
    """测试基类，提供 driver 管理、截图、日志等通用能力

    子类继承后可直接使用 self.page、self.base_page、self.logger 等属性
    """

    page: Page
    base_page: BasePage
    logger: Logger

    @pytest.fixture(autouse=True)
    def _setup(self, request):
        """自动注入的 setup fixture，每个测试用例执行前初始化 logger
        page 和 base_page 由子类 fixture 注入，避免与共享 fixture 创建重复浏览器窗口
        """
        self.logger = Logger.get("opms")
        self._test_name = request.node.name
        self.logger.info(f"初始化测试用例: {self._test_name}")

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

    def save_screenshot_on_failure(self):
        """测试失败时自动截图，成功则不操作

        Returns:
            失败时返回截图路径，成功时返回 None
        """
        try:
            outcome = pytest.test_result  # type: ignore[attr-defined]
        except AttributeError:
            self.logger.warning("未获取到测试结果，跳过失败截图")
            return None
        if outcome and outcome.excinfo is not None:
            self.logger.error(f"测试用例{self._test_name}失败，准备截图")
            return self.save_screenshot("fail")
        return None
