import os
import yaml


class ConfigReader:
    """YAML 配置文件读取器，支持链式取值与环境变量覆盖"""

    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "..", "config", "config.yaml"
            )
        self._path = os.path.normpath(config_path)
        if not os.path.isfile(self._path):
            raise FileNotFoundError(f"配置文件不存在: {self._path}")
        with open(self._path, "r", encoding="utf-8") as f:
            self._data = yaml.safe_load(f) or {}

    def get(self, *keys, default=None):
        """按层级键获取配置值，找不到时返回 default"""
        node = self._data
        for key in keys:
            if isinstance(node, dict) and key in node:
                node = node[key]
            else:
                return default
        return node

    def get_int(self, *keys, default: int = 0) -> int:
        val = self.get(*keys, default=default)
        try:
            return int(val)
        except (TypeError, ValueError):
            return default

    def get_bool(self, *keys, default: bool = False) -> bool:
        val = self.get(*keys, default=default)
        if isinstance(val, bool):
            return val
        if isinstance(val, str):
            return val.lower() in ("true", "1", "yes")
        return default

    @property
    def data(self) -> dict:
        return self._data

    @property
    def path(self) -> str:
        return self._path


# 模块级单例，方便全局引用
config = ConfigReader()
