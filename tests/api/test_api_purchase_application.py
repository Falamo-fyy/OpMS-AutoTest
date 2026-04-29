import os

import pytest
import allure
from dotenv import load_dotenv

from base.base_test import BaseTest
from utils.logger import Logger
from utils.config_reader import ConfigReader

load_dotenv()

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "api", "test_api_purchase_application_data.yaml")
query_data = ConfigReader(DATA_PATH)


@allure.feature("采购申请模块")
@allure.story("采购申请查询接口")
class TestApiPurchaseApplication(BaseTest):
    """采购申请查询接口自动化测试用例"""

    API_PURCHASE_APPLICATION_QUERY = "purchase_application_query"

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

    @allure.title("默认条件查询采购申请列表成功")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.smoke
    def test_query_default_success(self):
        """携带有效 token 以默认条件查询，验证返回 code=1 且包含列表数据"""
        data = query_data.get("query_default")
        self.logger.step(f"执行查询: {data['description']}")

        response = self._api.send(
            self.API_PURCHASE_APPLICATION_QUERY,
            params=data["params"],
            json_data=data["body"],
        )

        assert response.status_code == 200, f"请求失败, 状态码: {response.status_code}"
        body = self._api.parse_json(response)
        assert body["code"] == 1, f"期望 code=1, 实际 code={body['code']}, message={body.get('message', '')}"
        assert body["data"] is not None, "返回 data 为空"
        self.logger.success("默认条件查询采购申请列表验证通过")

    @allure.title("按筛选条件查询采购申请成功")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    @pytest.mark.parametrize("case", [
        pytest.param("query_by_urgency", id="按紧急程度"),
        pytest.param("query_by_audit_status", id="按审核状态"),
        pytest.param("query_by_application_no", id="按申请编号"),
    ])
    def test_query_with_filter_success(self, case):
        """携带筛选条件查询，验证返回 code=1 且包含数据"""
        data = query_data.get(case)
        self.logger.step(f"执行查询: {data['description']}")

        response = self._api.send(
            self.API_PURCHASE_APPLICATION_QUERY,
            params=data["params"],
            json_data=data["body"],
        )

        assert response.status_code == 200, f"请求失败, 状态码: {response.status_code}"
        body = self._api.parse_json(response)
        assert body["code"] == 1, f"期望 code=1, 实际 code={body['code']}, message={body.get('message', '')}"
        assert body["data"] is not None, "返回 data 为空"
        self.logger.success(f"{data['description']}验证通过")

    @allure.title("不携带 token 查询采购申请失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_query_no_token(self):
        """不携带 Authorization 查询采购申请，验证接口拒绝访问"""
        data = query_data.get("query_no_token")
        self.logger.step(f"执行查询: {data['description']}")

        self._api.set_token(None)
        body_data = query_data.get("query_default")
        response = self._api.send(
            self.API_PURCHASE_APPLICATION_QUERY,
            params=body_data["params"],
            json_data=body_data["body"],
        )

        body = self._api.parse_json(response)
        assert body["code"] != 1, f"无 token 应请求失败, 实际 code={body['code']}"
        self.logger.success("不携带 token 查询失败验证通过")

    @allure.title("携带无效 token 查询采购申请失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_query_invalid_token(self):
        """携带无效 token 查询采购申请，验证接口拒绝访问"""
        data = query_data.get("query_invalid_token")
        self.logger.step(f"执行查询: {data['description']}")

        self._api.set_token("invalid_token_12345")
        body_data = query_data.get("query_default")
        response = self._api.send(
            self.API_PURCHASE_APPLICATION_QUERY,
            params=body_data["params"],
            json_data=body_data["body"],
        )

        body = self._api.parse_json(response)
        assert body["code"] != 1, f"无效 token 应请求失败, 实际 code={body['code']}"
        self.logger.success("携带无效 token 查询失败验证通过")
