import os

import pytest
import allure
from dotenv import load_dotenv

from base.base_test import BaseTest
from base.base_api import BaseApi
from utils.logger import Logger
from utils.config_reader import ConfigReader

load_dotenv()

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "api", "test_api_login_data.yaml")
login_data = ConfigReader(DATA_PATH)


@allure.feature("登录模块")
@allure.story("用户登录接口")
class TestApiLogin(BaseTest):
    """登录接口自动化测试用例"""

    @pytest.fixture(autouse=True)
    def _setup_api(self, request):
        """初始化接口测试所需属性"""
        self.logger = Logger.get("opms")
        self._test_name = request.node.name
        self._api = BaseApi()
        self.logger.info(f"初始化接口测试用例: {self._test_name}")

    @allure.title("正确的账号密码登录成功")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.smoke
    def test_login_success(self):
        """使用正确的账号密码登录，验证返回 code=1"""
        data = login_data.get("login_success")
        username = os.getenv("TEST_USER", data["username"])
        password = os.getenv("TEST_PASSWORD", data["password"])
        self.logger.step(f"执行登录: {data['description']}")

        token = self._api.login(username, password)
        assert token, "登录成功但未返回 token"
        self.logger.success("登录接口成功验证通过")

    @allure.title("错误的用户名登录失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_login_wrong_username(self):
        """使用错误的用户名登录，验证返回 code!=1"""
        data = login_data.get("login_wrong_username")
        self.logger.step(f"执行登录: {data['description']}")

        response = self._api.send("user_login", params={"username": data["username"], "password": data["password"]})
        assert response.status_code == 200, f"请求失败, 状态码: {response.status_code}"
        body = self._api.parse_json(response)

        assert body["code"] != 1, f"错误用户名应登录失败, 实际 code={body['code']}"
        self.logger.success("错误用户名登录失败验证通过")

    @allure.title("错误的密码登录失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_login_wrong_password(self):
        """使用错误的密码登录，验证返回 code!=1"""
        data = login_data.get("login_wrong_password")
        self.logger.step(f"执行登录: {data['description']}")

        response = self._api.send("user_login", params={"username": data["username"], "password": data["password"]})
        assert response.status_code == 200, f"请求失败, 状态码: {response.status_code}"
        body = self._api.parse_json(response)

        assert body["code"] != 1, f"错误密码应登录失败, 实际 code={body['code']}"
        self.logger.success("错误密码登录失败验证通过")

    @allure.title("空用户名登录失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_login_empty_username(self):
        """用户名为空时登录，验证接口拒绝请求"""
        data = login_data.get("login_empty_username")
        self.logger.step(f"执行登录: {data['description']}")

        response = self._api.send("user_login", params={"username": data["username"], "password": data["password"]})
        body = self._api.parse_json(response)

        assert response.status_code == 400, f"空用户名应返回 400, 实际状态码: {response.status_code}"
        assert body["code"] != 1, f"空用户名应登录失败, 实际 code={body['code']}"
        self.logger.success("空用户名登录失败验证通过")

    @allure.title("空密码登录失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_login_empty_password(self):
        """密码为空时登录，验证接口拒绝请求"""
        data = login_data.get("login_empty_password")
        self.logger.step(f"执行登录: {data['description']}")

        response = self._api.send("user_login", params={"username": data["username"], "password": data["password"]})
        body = self._api.parse_json(response)

        assert response.status_code == 400, f"空密码应返回 400, 实际状态码: {response.status_code}"
        assert body["code"] != 1, f"空密码应登录失败, 实际 code={body['code']}"
        self.logger.success("空密码登录失败验证通过")
