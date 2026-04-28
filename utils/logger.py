import os
import datetime
import logging
from typing import Dict, Optional
from utils.config_reader import config


class Logger:
    """项目日志工具类，基于 config.yaml 中 log 节的配置自动初始化

    支持两种使用方式：
    1. Logger.get(name) 获取标准 logging.Logger 实例
    2. Logger 实例方法直接记录各级别日志，支持额外处理器

    运行级别日志：调用 set_run_log() 后，所有 logger 共享同一个日志文件，
    不再为每个 name 生成独立文件；调用 remove_run_log() 恢复默认行为。
    """

    _instances: Dict[str, "Logger"] = {}
    _loggers: Dict[str, logging.Logger] = {}
    _run_handler: logging.FileHandler = None

    def __init__(self, name: str = "opms"):
        self._name = name
        self._logger = self._ensure_logger(name)
        self._extra_handlers = []

    @classmethod
    def get(cls, name: str = "opms") -> "Logger":
        """获取 Logger 实例（单例），同名复用"""
        if name not in cls._instances:
            cls._instances[name] = Logger(name)
        return cls._instances[name]

    @classmethod
    def get_raw(cls, name: str = "opms") -> logging.Logger:
        """获取底层 logging.Logger 实例，兼容旧代码直接调用"""
        cls._ensure_logger(name)
        return cls._loggers[name]

    @classmethod
    def _ensure_logger(cls, name: str) -> logging.Logger:
        if name in cls._loggers:
            return cls._loggers[name]

        level = config.get("log", "level", default="INFO")
        fmt = config.get("log", "format", default="%(asctime)s [%(levelname)s] %(name)s - %(message)s")
        datefmt = config.get("log", "date_format", default="%Y-%m-%d %H:%M:%S")
        log_dir = config.get("log", "dir", default="logs")

        if not os.path.isabs(log_dir):
            log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", log_dir)
        log_dir = os.path.normpath(log_dir)
        os.makedirs(log_dir, exist_ok=True)

        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))

        if not logger.handlers:
            formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)

            sh = logging.StreamHandler()
            sh.setFormatter(formatter)
            logger.addHandler(sh)

            # 如果已设置运行级别日志，不再为每个 name 创建独立文件
            if cls._run_handler is None:
                fh = logging.FileHandler(
                    os.path.join(log_dir, f"{name}.log"), encoding="utf-8"
                )
                fh.setFormatter(formatter)
                logger.addHandler(fh)

        # 已有 logger 也需要绑定运行日志处理器
        if cls._run_handler is not None and cls._run_handler not in logger.handlers:
            logger.addHandler(cls._run_handler)

        cls._loggers[name] = logger
        return logger

    @classmethod
    def set_run_log(cls, filepath: str = None):
        """设置运行级别日志文件，所有 logger 共享该文件

        调用后新建和已有的 logger 都会写入同一个文件，不再生成按 name 命名的独立文件。

        Args:
            filepath: 日志文件路径，默认为 logs/run_YYYYMMDD_HHMMSS.log
        """
        if filepath is None:
            log_dir = config.get("log", "dir", default="logs")
            if not os.path.isabs(log_dir):
                log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", log_dir)
            log_dir = os.path.normpath(log_dir)
            os.makedirs(log_dir, exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(log_dir, f"run_{timestamp}.log")

        fmt = config.get("log", "format", default="%(asctime)s [%(levelname)s] %(name)s - %(message)s")
        datefmt = config.get("log", "date_format", default="%Y-%m-%d %H:%M:%S")
        cls._run_handler = logging.FileHandler(filepath, encoding="utf-8")
        cls._run_handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))

        # 为所有已有 logger 绑定运行日志处理器
        for lg in cls._loggers.values():
            if cls._run_handler not in lg.handlers:
                lg.addHandler(cls._run_handler)

    @classmethod
    def remove_run_log(cls):
        """移除运行级别日志文件处理器，恢复默认行为"""
        if cls._run_handler is None:
            return
        for lg in cls._loggers.values():
            if cls._run_handler in lg.handlers:
                lg.removeHandler(cls._run_handler)
        cls._run_handler.close()
        cls._run_handler = None

    # -------- 日志处理器管理 --------

    def add_handler(self, handler: logging.Handler) -> "Logger":
        """添加自定义日志处理器，返回自身支持链式调用"""
        handler.setFormatter(logging.Formatter(
            fmt=config.get("log", "format", default="%(asctime)s [%(levelname)s] %(name)s - %(message)s"),
            datefmt=config.get("log", "date_format", default="%Y-%m-%d %H:%M:%S"),
        ))
        self._logger.addHandler(handler)
        self._extra_handlers.append(handler)
        return self

    def remove_handler(self, handler: logging.Handler) -> "Logger":
        """移除指定日志处理器"""
        if handler in self._extra_handlers:
            self._logger.removeHandler(handler)
            self._extra_handlers.remove(handler)
        return self

    def remove_extra_handlers(self) -> "Logger":
        """移除所有通过 add_handler 添加的额外处理器"""
        for handler in self._extra_handlers:
            self._logger.removeHandler(handler)
        self._extra_handlers.clear()
        return self

    def add_file_handler(self, filepath: str, level: str = None) -> "Logger":
        """添加文件处理器，将日志输出到指定文件

        Args:
            filepath: 日志文件路径
            level: 处理器日志级别，默认使用全局配置
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        fh = logging.FileHandler(filepath, encoding="utf-8")
        if level:
            fh.setLevel(getattr(logging, level.upper(), logging.NOTSET))
        return self.add_handler(fh)

    def add_stream_handler(self, level: str = None) -> "Logger":
        """添加控制台处理器

        Args:
            level: 处理器日志级别，默认使用全局配置
        """
        sh = logging.StreamHandler()
        if level:
            sh.setLevel(getattr(logging, level.upper(), logging.NOTSET))
        return self.add_handler(sh)

    def add_rotating_file_handler(
        self,
        filepath: str,
        max_bytes: int = 10485760,
        backup_count: int = 5,
        level: str = None,
    ) -> "Logger":
        """添加按大小轮转的文件处理器

        Args:
            filepath: 日志文件路径
            max_bytes: 单个日志文件最大字节数，默认 10MB
            backup_count: 保留的备份文件数量，默认 5
            level: 处理器日志级别
        """
        from logging.handlers import RotatingFileHandler

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        rh = RotatingFileHandler(
            filepath, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
        )
        if level:
            rh.setLevel(getattr(logging, level.upper(), logging.NOTSET))
        return self.add_handler(rh)

    def add_timed_rotating_file_handler(
        self,
        filepath: str,
        when: str = "midnight",
        interval: int = 1,
        backup_count: int = 7,
        level: str = None,
    ) -> "Logger":
        """添加按时间轮转的文件处理器

        Args:
            filepath: 日志文件路径
            when: 轮转周期，可选 S/M/H/D/midnight/W0-W6，默认 midnight
            interval: 轮转间隔，默认 1
            backup_count: 保留的备份文件数量，默认 7
            level: 处理器日志级别
        """
        from logging.handlers import TimedRotatingFileHandler

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        th = TimedRotatingFileHandler(
            filepath, when=when, interval=interval,
            backupCount=backup_count, encoding="utf-8",
        )
        if level:
            th.setLevel(getattr(logging, level.upper(), logging.NOTSET))
        return self.add_handler(th)

    # -------- 各级别日志记录 --------

    def debug(self, msg: str, *args, **kwargs):
        """记录 DEBUG 级别日志"""
        self._logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs):
        """记录 INFO 级别日志"""
        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        """记录 WARNING 级别日志"""
        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        """记录 ERROR 级别日志"""
        self._logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs):
        """记录 CRITICAL 级别日志"""
        self._logger.critical(msg, *args, **kwargs)

    def exception(self, msg: str, *args, **kwargs):
        """记录 ERROR 级别日志，同时附加异常堆栈信息"""
        self._logger.exception(msg, *args, **kwargs)

    # -------- 便捷方法 --------

    def step(self, msg: str):
        """记录测试步骤（INFO 级别，带 [STEP] 前缀）"""
        self.info(f"[STEP] {msg}")

    def data(self, msg: str):
        """记录测试数据（DEBUG 级别，带 [DATA] 前缀）"""
        self.debug(f"[DATA] {msg}")

    def success(self, msg: str):
        """记录操作成功（INFO 级别，带 [PASS] 前缀）"""
        self.info(f"[PASS] {msg}")

    def fail(self, msg: str):
        """记录操作失败（ERROR 级别，带 [FAIL] 前缀）"""
        self.error(f"[FAIL] {msg}")

    @property
    def raw(self) -> logging.Logger:
        """获取底层 logging.Logger 实例"""
        return self._logger

    @property
    def level(self) -> int:
        """获取当前日志级别"""
        return self._logger.level

    @level.setter
    def level(self, value):
        """设置日志级别，支持字符串或整数"""
        if isinstance(value, str):
            value = getattr(logging, value.upper(), logging.INFO)
        self._logger.setLevel(value)

    @property
    def effective_level(self) -> int:
        """获取生效的日志级别"""
        return self._logger.getEffectiveLevel()

    def is_enabled(self, level: str) -> bool:
        """判断指定级别日志是否启用"""
        return self._logger.isEnabledFor(getattr(logging, level.upper(), logging.CRITICAL))
