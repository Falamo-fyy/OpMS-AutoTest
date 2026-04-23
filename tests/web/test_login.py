import os
import allure
import pytest

from base.base_test import BaseTest
from page.login_page import LoginPage
from utils.logger import Logger
from utils.config_reader import ConfigReader

logger = Logger.get("test_login")

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "test_login_data.yaml")
login_data = ConfigReader(DATA_PATH)


@allure.feature("登录模块")
@allure.story("用户登录")
class TestLogin(BaseTest):
    """登录功能测试用例"""

    def _get_login_page(self) -> LoginPage:
        return LoginPage(self.page)

    @allure.title("正确的账号密码登录成功")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_success(self):
        """使用正确的账号密码登录，验证登录成功"""
        login = self._get_login_page()
        logger.step("执行登录流程")
        login.login()
        logger.step("验证登录成功")
        login.assert_login_success()
        logger.success("登录成功")

    @allure.title("错误的用户名登录失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_with_wrong_username(self):
        """使用错误的用户名登录，验证登录失败"""
        data = login_data.get("login_wrong_username")
        login = self._get_login_page()
        logger.step(f"执行登录流程: {data['description']}")
        login.login(username=data["username"], password=data["password"])
        logger.step("验证仍在登录页面")
        login.assert_visible(f"text={login.LOGIN_BTN}")
        logger.success("错误用户名登录失败验证通过")

    @allure.title("空用户名登录失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_with_empty_username(self):
        """用户名为空时登录，验证登录失败"""
        data = login_data.get("login_empty_username")
        login = self._get_login_page()
        logger.step(f"执行登录流程: {data['description']}")
        login.login(username=data["username"], password=data["password"])
        logger.step("验证仍在登录页面")
        login.assert_visible(f"text={login.LOGIN_BTN}")
        logger.success("空用户名登录失败验证通过")

    @allure.title("空密码登录失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_with_empty_password(self):
        """密码为空时登录，验证登录失败"""
        data = login_data.get("login_empty_password")
        login = self._get_login_page()
        logger.step(f"执行登录流程: {data['description']}")
        login.login(username=data["username"], password=data["password"])
        logger.step("验证仍在登录页面")
        login.assert_visible(f"text={login.LOGIN_BTN}")
        logger.success("空密码登录失败验证通过")
