import json
import os

import pytest
import requests

from utils.config_reader import ConfigReader, config as cfg
from utils.logger import Logger

logger = Logger.get("opms")

# 接口配置文件路径
_API_CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "api_config.yaml"
)
_api_config = ConfigReader(_API_CONFIG_PATH)


class BaseApi:
    """接口请求基类，封装 requests 通用方法，所有 API 测试通过此类发送请求"""

    def __init__(self):
        self._base_url = cfg.get("api_base_url", default=cfg.get("base_url", default=""))
        self._timeout = cfg.get_int("timeout", "page_load", default=30000) / 1000
        self._token = None

    def _get_api_config(self, api_name: str) -> dict:
        """根据接口名称从 api_config.yaml 读取接口配置

        Args:
            api_name: 接口名称，如 user_login

        Returns:
            包含 path 和 method 的字典
        """
        api_info = _api_config.get(api_name)
        if not api_info:
            pytest.fail(f"接口配置未找到: {api_name}")
        if "path" not in api_info or "method" not in api_info:
            pytest.fail(f"接口配置缺少 path 或 method: {api_name}")
        return api_info

    def send(self, api_name: str, params: dict = None, json_data: dict = None,
             data: dict = None, headers: dict = None) -> requests.Response:
        """根据接口名称发送请求，从 api_config.yaml 读取 path 和 method

        Args:
            api_name: 接口名称，对应 api_config.yaml 中的键名
            params: URL 查询参数
            json_data: 请求体（JSON 序列化）
            data: 请求体（表单）
            headers: 自定义请求头，会覆盖默认头和 token 头

        Returns:
            requests.Response 对象
        """
        api_info = self._get_api_config(api_name)
        return self.api_request(api_info["method"], api_info["path"],
                                params=params, json_data=json_data,
                                data=data, headers=headers)

    def api_request(self, method: str, path: str, params: dict = None,
                    json_data: dict = None, data: dict = None, headers: dict = None) -> requests.Response:
        """发送 HTTP 请求

        Args:
            method: 请求方法（GET/POST/PUT/DELETE 等）
            path: 接口路径，如 /user/login
            params: URL 查询参数
            json_data: 请求体（JSON 序列化）
            data: 请求体（表单）
            headers: 自定义请求头，会覆盖默认头和 token 头

        Returns:
            requests.Response 对象
        """
        url = self._base_url + path
        hdrs = {}
        if self._token:
            hdrs["Authorization"] = self._token
        if headers:
            hdrs.update(headers)

        safe_params = {k: ("******" if k in ("password", "pwd", "secret") else v) for k, v in (params or {}).items()}
        safe_hdrs = {k: (v[:20] + "..." if k == "Authorization" and len(v) > 20 else v) for k, v in hdrs.items()}
        logger.step(f"发送{method.upper()}请求: {url}, headers: {safe_hdrs}, params: {safe_params}")

        response = requests.request(method, url, params=params, json=json_data,
                                    data=data, headers=hdrs, timeout=self._timeout)
        logger.step(f"响应状态码: {response.status_code}, 响应体: {response.text}")

        return response

    def get(self, path: str, **kwargs) -> requests.Response:
        """发送 GET 请求"""
        return self.api_request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        """发送 POST 请求"""
        return self.api_request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        """发送 PUT 请求"""
        return self.api_request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        """发送 DELETE 请求"""
        return self.api_request("DELETE", path, **kwargs)

    def parse_json(self, response: requests.Response) -> dict:
        """解析响应体为 JSON，非 JSON 响应直接断言失败"""
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            pytest.fail(f"响应体非 JSON 格式, 状态码: {response.status_code}, 内容: {response.text[:200]}")

    def login(self, username: str, password: str) -> str:
        """登录并保存 token，返回 token 值

        登录成功后自动设置 token，后续请求自动携带 Authorization 头
        """
        response = self.send("user_login", params={"username": username, "password": password})

        assert response.status_code == 200, f"登录请求失败, 状态码: {response.status_code}"
        body = self.parse_json(response)
        assert body["code"] == 1, f"登录失败, code={body['code']}, message={body.get('message', '')}"

        token = body["data"]
        assert token, "登录成功但 data 中未返回 token"
        self._token = token
        logger.success(f"登录成功, 获取 token: {token[:20]}...")
        return token

    def logout(self):
        """注销并清除 token"""
        self.send("user_logout")
        self._token = None
        logger.success("注销成功, token 已清除")

    def set_token(self, token: str):
        """手动设置 token"""
        self._token = token

    def get_token(self) -> str:
        """获取当前 token"""
        return self._token
