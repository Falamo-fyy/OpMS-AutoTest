import os
from dotenv import load_dotenv
from base.base_page import BasePage

load_dotenv()

TEST_USER = os.getenv("TEST_USER", "")
TEST_PASSWORD = os.getenv("TEST_PASSWORD", "")


class LoginPage(BasePage):
    """登录页面对象，封装登录页面的元素定位和操作方法"""

    # 元素定位器
    USERNAME = "input[placeholder='请输入用户名']"
    PASSWORD = "input[placeholder='请输入密码']"
    LOGIN_BTN = "button.login-button"
    SUCCESS_TEXT = "综合运维服务平台"

    def navigate_to_login_page(self):
        """导航到登录页面"""
        self.goto("/#/login")

    def input_username(self, username=TEST_USER):
        """输入用户名"""
        self.fill(self.USERNAME, username)

    def input_password(self, password=TEST_PASSWORD):
        """输入密码"""
        self.fill(self.PASSWORD, password)

    def click_login_button(self):
        """点击登录按钮"""
        self.locator(self.LOGIN_BTN).click()

    def assert_login_success(self):
        """断言登录成功"""
        self.wait_for_load_state("domcontentloaded")
        self.assert_visible(f"text={self.SUCCESS_TEXT}")

    def login(self, username=TEST_USER, password=TEST_PASSWORD):
        """执行完整登录流程"""
        self.navigate_to_login_page()
        self.input_username(username)
        self.input_password(password)
        self.click_login_button()
