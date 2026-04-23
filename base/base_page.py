import os
import datetime
from playwright.sync_api import Page, expect
from utils.config_reader import config as cfg
from utils.logger import Logger
from typing import Literal, Optional

logger = Logger.get("base_page")

# 截图目录
_IMAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "image")
os.makedirs(_IMAGE_DIR, exist_ok=True)

class BasePage:
    """页面操作基类，封装 Playwright 通用元素操作方法"""

    def __init__(self, page: Page):
        """初始化页面实例

        Args:
            page: Playwright Page 对象
        """
        self.page = page

    def _screenshot_on_fail(self, label: str):
        """断言失败时自动截图保存到 image 目录"""
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(_IMAGE_DIR, f"{ts}_{label}.png")
        try:
            self.page.screenshot(path=path, full_page=True)
            logger.error(f"断言失败，截图已保存: {path}")
        except Exception as e:
            logger.error(f"断言失败截图异常: {e}")

    def goto(self, url: str):
        """导航到指定 URL 地址"""
        self.page.goto(cfg["base_url"] + f"{url}")
        logger.info(f"导航到{cfg['base_url'] + url}")

    def locator(self, selector: str):
        """根据选择器查找元素，返回 Locator 对象"""
        logger.info(f"根据选择器查找元素{selector}")
        return self.page.locator(selector)

    def get_by_text(self, text: str):
        """根据文本内容查找元素，返回 Locator 对象"""
        logger.info(f"根据文本内容查找元素{text}")
        return self.page.get_by_text(text)

    def click(self, selector: str, **kwargs):
        """点击指定选择器对应的元素"""
        self.locator(selector).click(**kwargs)
        logger.info(f"点击元素{selector}")

    def fill(self, selector: str, value: str, **kwargs):
        """清空输入框并填入指定值"""
        self.locator(selector).fill(value, **kwargs)
        logger.info(f"清空输入框{selector}并填入值{value}")

    def type(self, selector: str, value: str, **kwargs):
        """模拟键盘逐字符输入，触发键盘事件"""
        self.locator(selector).type(value, **kwargs)
        logger.info(f"模拟键盘逐字符输入，触发键盘事件{selector}")

    def clear(self, selector: str, **kwargs):
        """清空输入框内容"""
        self.locator(selector).clear(**kwargs)
        logger.info(f"清空输入框{selector}")

    def text(self, selector: str) -> str:
        """获取元素的 text_content，包含子元素的文本"""
        logger.info(f"获取元素{selector}的text_content")
        text = self.locator(selector).text_content()
        logger.info(f"元素{selector}的text_content为: {text}")
        return text

    def inner_text(self, selector: str) -> str:
        """获取元素的 inner_text，仅返回可见文本"""
        logger.info(f"获取元素{selector}的inner_text")
        inner_text = self.locator(selector).inner_text()
        logger.info(f"元素{selector}的inner_text为: {inner_text}")
        return inner_text

    def input_value(self, selector: str) -> str:
        """获取输入框当前值"""
        logger.info(f"获取元素{selector}的input_value")
        input_value = self.locator(selector).input_value()
        logger.info(f"元素{selector}的input_value为: {input_value}")
        return input_value

    def get_attribute(self, selector: str, name: str):
        """获取元素指定属性的值"""
        logger.info(f"获取元素{selector}的属性{name}")
        attribute = self.locator(selector).get_attribute(name)
        logger.info(f"元素{selector}的属性{name}为: {attribute}")
        return attribute

    def select_option(self, selector: str, value=None, label=None, index=None):
        """在下拉选择框中选中选项，支持按 value、label 或 index 选择"""
        logger.info(f"在下拉选择框{selector}中选中选项，参数: value={value}, label={label}, index={index}")
        kwargs = {}
        if value is not None:
            kwargs["value"] = value
        if label is not None:
            kwargs["label"] = label
        if index is not None:
            kwargs["index"] = index
        self.locator(selector).select_option(**kwargs)

    def check(self, selector: str, **kwargs):
        """勾选复选框或单选框"""
        logger.info(f"勾选元素{selector}")
        self.locator(selector).check(**kwargs)

    def uncheck(self, selector: str, **kwargs):
        """取消勾选复选框或单选框"""
        logger.info(f"取消勾选元素{selector}")
        self.locator(selector).uncheck(**kwargs)

    def hover(self, selector: str, **kwargs):
        """鼠标悬停在指定元素上"""
        logger.info(f"鼠标悬停在元素{selector}上")
        self.locator(selector).hover(**kwargs)

    def wait_for_selector(self, selector: str, **kwargs):
        """等待指定选择器的元素出现在页面中"""
        logger.info(f"等待元素{selector}出现在页面中")
        self.page.wait_for_selector(selector, **kwargs)

    def wait_for_url(self, url: str, **kwargs):
        """等待页面导航到指定 URL"""
        logger.info(f"等待页面导航到{url}")
        self.page.wait_for_url(url, **kwargs)

    def wait_for_load_state(self, state: Optional[Literal["domcontentloaded", "load", "networkidle"]] = "load"):
        """等待页面加载到指定状态（load/domcontentloaded/networkidle）"""
        logger.info(f"等待页面加载到{state}")
        self.page.wait_for_load_state(state)

    def assert_visible(self, selector: str):
        """断言元素可见"""
        logger.info(f"断言元素{selector}可见")
        try:
            expect(self.locator(selector)).to_be_visible()
        except AssertionError:
            self._screenshot_on_fail("assert_visible")
            raise

    def assert_hidden(self, selector: str):
        """断言元素不可见"""
        logger.info(f"断言元素{selector}不可见")
        try:
            expect(self.locator(selector)).to_be_hidden()
        except AssertionError:
            self._screenshot_on_fail("assert_hidden")
            raise

    def assert_text(self, selector: str, expected: str):
        """断言元素的文本内容等于预期值"""
        logger.info(f"断言元素{selector}的文本内容等于{expected}")
        try:
            expect(self.locator(selector)).to_have_text(expected)
        except AssertionError:
            self._screenshot_on_fail("assert_text")
            raise

    def assert_value(self, selector: str, expected: str):
        """断言输入框的值等于预期值"""
        logger.info(f"断言元素{selector}的值等于{expected}")
        try:
            expect(self.locator(selector)).to_have_value(expected)
        except AssertionError:
            self._screenshot_on_fail("assert_value")
            raise

    def assert_url(self, expected: str):
        """断言当前页面 URL 等于预期值"""
        logger.info(f"断言当前页面URL等于{expected}")
        try:
            expect(self.page).to_have_url(expected)
        except AssertionError:
            self._screenshot_on_fail("assert_url")
            raise

    def assert_title(self, expected: str):
        """断言当前页面标题等于预期值"""
        logger.info(f"断言当前页面标题等于{expected}")
        try:
            expect(self.page).to_have_title(expected)
        except AssertionError:
            self._screenshot_on_fail("assert_title")
            raise

    def assert_count(self, selector: str, count: int):
        """断言匹配选择器的元素数量等于预期值"""
        logger.info(f"断言元素{selector}的数量等于{count}")
        try:
            expect(self.locator(selector)).to_have_count(count)
        except AssertionError:
            self._screenshot_on_fail("assert_count")
            raise

    def accept_dialog(self):
        """自动接受弹窗（alert/confirm/prompt）"""
        logger.info("自动接受弹窗")
        self.page.on("dialog", lambda dialog: dialog.accept())

    def frame(self, name: str = None, url: str = None):
        """根据 name 或 url 获取 iframe 的 Frame 对象"""
        logger.info(f"获取iframe，参数: name={name}, url={url}")
        if name:
            return self.page.frame(name=name)
        if url:
            return self.page.frame(url=url)
        return None

    def screenshot(self, path: str, full_page: bool = False):
        """对当前页面进行截图并保存到指定路径

        Args:
            path: 截图保存路径
            full_page: 是否截取整个页面，默认仅截取可视区域
        """
        logger.info(f"截图保存到{path}，full_page={full_page}")
        self.page.screenshot(path=path, full_page=full_page)
