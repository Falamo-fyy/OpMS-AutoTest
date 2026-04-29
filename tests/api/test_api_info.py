import os

import pytest
import allure
from dotenv import load_dotenv

from base.base_test import BaseTest
from base.base_api import BaseApi
from utils.logger import Logger

load_dotenv()


@allure.feature("用户信息模块")
@allure.story("用户信息接口")
class TestApiInfo(BaseTest):
    """用户信息接口自动化测试用例"""

    API_USER_INFO = "user_info"

    @pytest.fixture(autouse=True)
    def _setup_api(self, logged_in_api, request):
        """注入已登录的 API 客户端，初始化测试属性"""
        self._api = logged_in_api
        self._original_token = logged_in_api.get_token()
        self.logger = Logger.get("opms")
        self._test_name = request.node.name
        self.logger.info(f"初始化接口测试用例: {self._test_name}")
        yield
        self._api.set_token(self._original_token)

    @allure.title("携带有效 token 获取用户信息成功")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_user_info_success(self):
        """携带登录返回的 token 请求 /user/info，验证返回 code=1 且包含用户数据"""
        response = self._api.send(self.API_USER_INFO)

        assert response.status_code == 200, f"请求失败, 状态码: {response.status_code}"
        body = self._api.parse_json(response)
        assert body["code"] == 1, f"期望 code=1, 实际 code={body['code']}, message={body.get('message', '')}"
        assert body["data"] is not None, "返回 data 为空"
        self.logger.success("携带有效 token 获取用户信息验证通过")

    @allure.title("不携带 token 获取用户信息失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_user_info_no_token(self):
        """不携带 Authorization 请求 /user/info，验证接口拒绝访问"""
        self._api.set_token(None)
        response = self._api.send(self.API_USER_INFO)

        body = self._api.parse_json(response)
        assert body["code"] != 1, f"无 token 应请求失败, 实际 code={body['code']}"
        self.logger.success("不携带 token 请求失败验证通过")

    @allure.title("携带无效 token 获取用户信息失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_user_info_invalid_token(self):
        """携带无效 token 请求 /user/info，验证接口拒绝访问"""
        self._api.set_token("invalid_token_12345")
        response = self._api.send(self.API_USER_INFO)

        body = self._api.parse_json(response)
        assert body["code"] != 1, f"无效 token 应请求失败, 实际 code={body['code']}"
        self.logger.success("携带无效 token 请求失败验证通过")
