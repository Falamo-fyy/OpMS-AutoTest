"""
截图清理脚本

用法:
    python scripts/clean_images.py               # 清空 image 目录下所有截图
    python scripts/clean_images.py --days 7      # 仅保留最近 7 天的截图
    python scripts/clean_images.py -n            # 预览模式，仅列出将删除的文件，不实际删除
"""

import os
import sys
import argparse
import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from utils.logger import Logger

logger = Logger.get("clean_images")

IMAGE_DIR = os.path.join(PROJECT_ROOT, "image")


def list_images(days: int = None):
    """列出将要清理的截图文件

    Args:
        days: 保留最近多少天的文件，None 表示全部删除

    Returns:
        待删除文件路径列表
    """
    if not os.path.isdir(IMAGE_DIR):
        logger.fail(f"截图目录不存在: {IMAGE_DIR}")
        return []

    to_delete = []
    cutoff = datetime.datetime.now() - datetime.timedelta(days=days) if days else None

    for filename in os.listdir(IMAGE_DIR):
        filepath = os.path.join(IMAGE_DIR, filename)
        if not os.path.isfile(filepath):
            continue
        if cutoff:
            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
            if mtime >= cutoff:
                continue
        to_delete.append(filepath)

    return to_delete


def clean_images(days: int = None, dry_run: bool = False):
    """清理截图文件

    Args:
        days: 保留最近多少天的文件，None 表示全部删除
        dry_run: 预览模式，仅列出文件不实际删除
    """
    files = list_images(days)

    if not files:
        logger.info("没有需要清理的截图文件")
        return

    logger.info(f"共找到 {len(files)} 个截图文件待清理")

    for filepath in files:
        if dry_run:
            logger.info(f"[预览] 将删除: {filepath}")
        else:
            os.remove(filepath)
            logger.info(f"已删除: {filepath}")

    if dry_run:
        logger.info(f"[预览] 共 {len(files)} 个文件将被删除 (使用不带 -n 的命令执行实际删除)")
    else:
        size_kb = len(files)
        logger.success(f"清理完成，共删除 {size_kb} 个截图文件")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="OpMS 截图清理脚本")
    parser.add_argument(
        "--days", type=int, default=None,
        help="保留最近多少天的截图，不指定则清空全部",
    )
    parser.add_argument(
        "-n", "--dry-run", action="store_true",
        help="预览模式，仅列出将删除的文件，不实际删除",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.days is not None:
        logger.info(f"清理 {args.days} 天前的截图，保留最近的")
    else:
        logger.info("清空全部截图")

    clean_images(days=args.days, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
