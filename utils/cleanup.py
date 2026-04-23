import os
import datetime
from utils.config_reader import config as cfg


def clean_traces(traces_dir: str = None, days: int = None):
    """清理指定天数前的 trace 文件

    Args:
        traces_dir: trace 文件根目录，默认从 config.yaml 读取
        days: 保留最近多少天的文件，默认从 config.yaml 读取
    """
    if traces_dir is None:
        traces_dir = cfg.get("tracing", "dir", default="reports/traces")
        if not os.path.isabs(traces_dir):
            traces_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))), traces_dir
            )
    if days is None:
        days = cfg.get_int("tracing", "cleanup_days", default=7)

    if not os.path.isdir(traces_dir):
        return

    cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
    # trace 目录按日期组织：traces_dir/YYYY-MM-DD/test_name.zip
    for entry in os.listdir(traces_dir):
        date_dir = os.path.join(traces_dir, entry)
        if not os.path.isdir(date_dir):
            continue
        try:
            dir_date = datetime.datetime.strptime(entry, "%Y-%m-%d")
        except ValueError:
            continue
        if dir_date < cutoff:
            for f in os.listdir(date_dir):
                os.remove(os.path.join(date_dir, f))
            os.rmdir(date_dir)
