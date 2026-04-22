from playwright.sync_api import Page, expect


class BasePage:
    """页面操作基类，封装 Playwright 通用元素操作方法"""

    def __init__(self, page: Page):
        """初始化页面实例

        Args:
            page: Playwright Page 对象
        """
        self.page = page

    def goto(self, url: str):
        """导航到指定 URL 地址"""
        self.page.goto(url)

    def locator(self, selector: str):
        """根据选择器查找元素，返回 Locator 对象"""
        return self.page.locator(selector)

    def click(self, selector: str, **kwargs):
        """点击指定选择器对应的元素"""
        self.locator(selector).click(**kwargs)

    def fill(self, selector: str, value: str, **kwargs):
        """清空输入框并填入指定值"""
        self.locator(selector).fill(value, **kwargs)

    def type(self, selector: str, value: str, **kwargs):
        """模拟键盘逐字符输入，触发键盘事件"""
        self.locator(selector).type(value, **kwargs)

    def clear(self, selector: str, **kwargs):
        """清空输入框内容"""
        self.locator(selector).clear(**kwargs)

    def text(self, selector: str) -> str:
        """获取元素的 text_content，包含子元素的文本"""
        return self.locator(selector).text_content()

    def inner_text(self, selector: str) -> str:
        """获取元素的 inner_text，仅返回可见文本"""
        return self.locator(selector).inner_text()

    def input_value(self, selector: str) -> str:
        """获取输入框当前值"""
        return self.locator(selector).input_value()

    def get_attribute(self, selector: str, name: str):
        """获取元素指定属性的值"""
        return self.locator(selector).get_attribute(name)

    def select_option(self, selector: str, value=None, label=None, index=None):
        """在下拉选择框中选中选项，支持按 value、label 或 index 选择"""
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
        self.locator(selector).check(**kwargs)

    def uncheck(self, selector: str, **kwargs):
        """取消勾选复选框或单选框"""
        self.locator(selector).uncheck(**kwargs)

    def hover(self, selector: str, **kwargs):
        """鼠标悬停在指定元素上"""
        self.locator(selector).hover(**kwargs)

    def wait_for_selector(self, selector: str, **kwargs):
        """等待指定选择器的元素出现在页面中"""
        self.page.wait_for_selector(selector, **kwargs)

    def wait_for_url(self, url: str, **kwargs):
        """等待页面导航到指定 URL"""
        self.page.wait_for_url(url, **kwargs)

    def wait_for_load_state(self, state: str = "load"):
        """等待页面加载到指定状态（load/domcontentloaded/networkidle）"""
        self.page.wait_for_load_state(state)

    def assert_visible(self, selector: str):
        """断言元素可见"""
        expect(self.locator(selector)).to_be_visible()

    def assert_hidden(self, selector: str):
        """断言元素不可见"""
        expect(self.locator(selector)).to_be_hidden()

    def assert_text(self, selector: str, expected: str):
        """断言元素的文本内容等于预期值"""
        expect(self.locator(selector)).to_have_text(expected)

    def assert_value(self, selector: str, expected: str):
        """断言输入框的值等于预期值"""
        expect(self.locator(selector)).to_have_value(expected)

    def assert_url(self, expected: str):
        """断言当前页面 URL 等于预期值"""
        expect(self.page).to_have_url(expected)

    def assert_title(self, expected: str):
        """断言当前页面标题等于预期值"""
        expect(self.page).to_have_title(expected)

    def assert_count(self, selector: str, count: int):
        """断言匹配选择器的元素数量等于预期值"""
        expect(self.locator(selector)).to_have_count(count)

    def accept_dialog(self):
        """自动接受弹窗（alert/confirm/prompt）"""
        self.page.on("dialog", lambda dialog: dialog.accept())

    def frame(self, name: str = None, url: str = None):
        """根据 name 或 url 获取 iframe 的 Frame 对象"""
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
        self.page.screenshot(path=path, full_page=full_page)
