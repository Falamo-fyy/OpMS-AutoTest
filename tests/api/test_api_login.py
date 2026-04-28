import os
import json

import pytest
import allure
import requests
from dotenv import load_dotenv

from base.base_test import BaseTest
from utils.logger import Logger
from utils.config_reader import ConfigReader, config as cfg

load_dotenv()

logger = Logger.get("opms")

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "test_api_login_data.yaml")
login_data = ConfigReader(DATA_PATH)

API_BASE_URL = cfg.get("api_base_url", default=cfg.get("base_url", default=""))
LOGIN_PATH = "/user/login"
TIMEOUT = cfg.get_int("timeout", "page_load", default=30000) / 1000


@allure.feature("登录模块")
@allure.story("用户登录接口")
class TestApiLogin(BaseTest):
    """登录接口自动化测试用例"""

    @pytest.fixture(autouse=True)
    def _setup_api(self, request):
        """初始化接口测试所需属性"""
        self.logger = Logger.get("opms")
        self._test_name = request.node.name
        self.logger.info(f"初始化接口测试用例: {self._test_name}")

    def _login(self, username: str, password: str, headers: dict = None) -> requests.Response:
        """发送登录请求，返回 Response 对象"""
        url = API_BASE_URL + LOGIN_PATH
        params = {"username": username, "password": password}
        hdrs = {"Content-Type": "application/json"}
        if headers:
            hdrs.update(headers)
        logger.step(f"发送登录请求: {url}, 参数: {params}")
        response = requests.post(url, params=params, headers=hdrs, timeout=TIMEOUT)
        logger.step(f"响应状态码: {response.status_code}, 响应体: {response.text}")
        return response

    def _parse_json(self, response: requests.Response) -> dict:
        """解析响应体为 JSON，非 JSON 响应直接断言失败"""
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            pytest.fail(f"响应体非 JSON 格式, 状态码: {response.status_code}, 内容: {response.text[:200]}")

    @allure.title("正确的账号密码登录成功")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.smoke
    def test_login_success(self):
        """使用正确的账号密码登录，验证返回 code=1"""
        data = login_data.get("login_success")
        username = os.getenv("TEST_USER", data["username"])
        password = os.getenv("TEST_PASSWORD", data["password"])
        logger.step(f"执行登录: {data['description']}")

        response = self._login(username, password)
        assert response.status_code == 200, f"请求失败, 状态码: {response.status_code}"
        body = self._parse_json(response)

        assert body["code"] == 1, f"期望 code=1, 实际 code={body['code']}, message={body.get('message', '')}"
        logger.success("登录接口成功验证通过")

    @allure.title("错误的用户名登录失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_login_wrong_username(self):
        """使用错误的用户名登录，验证返回 code!=1"""
        data = login_data.get("login_wrong_username")
        logger.step(f"执行登录: {data['description']}")

        response = self._login(data["username"], data["password"])
        assert response.status_code == 200, f"请求失败, 状态码: {response.status_code}"
        body = self._parse_json(response)

        assert body["code"] != 1, f"错误用户名应登录失败, 实际 code={body['code']}"
        logger.success("错误用户名登录失败验证通过")

    @allure.title("错误的密码登录失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_login_wrong_password(self):
        """使用错误的密码登录，验证返回 code!=1"""
        data = login_data.get("login_wrong_password")
        logger.step(f"执行登录: {data['description']}")

        response = self._login(data["username"], data["password"])
        assert response.status_code == 200, f"请求失败, 状态码: {response.status_code}"
        body = self._parse_json(response)

        assert body["code"] != 1, f"错误密码应登录失败, 实际 code={body['code']}"
        logger.success("错误密码登录失败验证通过")

    @allure.title("空用户名登录失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_login_empty_username(self):
        """用户名为空时登录，验证接口拒绝请求"""
        data = login_data.get("login_empty_username")
        logger.step(f"执行登录: {data['description']}")

        response = self._login(data["username"], data["password"])
        body = self._parse_json(response)

        assert response.status_code == 400, f"空用户名应返回 400, 实际状态码: {response.status_code}"
        assert body["code"] != 1, f"空用户名应登录失败, 实际 code={body['code']}"
        logger.success("空用户名登录失败验证通过")

    @allure.title("空密码登录失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_login_empty_password(self):
        """密码为空时登录，验证接口拒绝请求"""
        data = login_data.get("login_empty_password")
        logger.step(f"执行登录: {data['description']}")

        response = self._login(data["username"], data["password"])
        body = self._parse_json(response)

        assert response.status_code == 400, f"空密码应返回 400, 实际状态码: {response.status_code}"
        assert body["code"] != 1, f"空密码应登录失败, 实际 code={body['code']}"
        logger.success("空密码登录失败验证通过")
