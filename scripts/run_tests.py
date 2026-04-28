"""
测试运行脚本

用法:
    python scripts/run_tests.py                        # 运行所有测试
    python scripts/run_tests.py -t web                 # 仅运行 web UI 测试
    python scripts/run_tests.py -t api                 # 仅运行 API 接口测试
    python scripts/run_tests.py -m smoke               # 按 marker 运行
    python scripts/run_tests.py -t web -m smoke        # web 测试中运行 smoke 用例
    python scripts/run_tests.py --no-report            # 不生成 Allure 报告
    python scripts/run_tests.py -l                     # 列出所有测试文件
    python scripts/run_tests.py -l -t web              # 列出 web 测试文件
    python scripts/run_tests.py tests/web/test_login.py  # 指定测试文件
"""

import os
import sys
import argparse
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from utils.logger import Logger

logger = Logger.get("run_tests")

# 测试类型到目录的映射
TYPE_DIR_MAP = {
    "web": "tests/web",
    "api": "tests/api",
}


def build_cmd(args: argparse.Namespace) -> list:
    """根据参数构建 pytest 命令"""
    cmd = [sys.executable, "-m", "pytest"]

    # 指定测试目录或文件
    if args.test_path:
        cmd.append(args.test_path)
    elif args.type:
        test_dir = TYPE_DIR_MAP.get(args.type)
        if test_dir and os.path.isdir(os.path.join(PROJECT_ROOT, test_dir)):
            cmd.append(test_dir)
        else:
            logger.fail(f"测试类型 '{args.type}' 对应的目录不存在")
            sys.exit(1)
    else:
        # 未指定类型，运行全部测试
        cmd.append("tests")

    # 测试标记
    if args.marker:
        cmd.extend(["-m", args.marker])

    # 失败重试
    cmd.extend(["--reruns", "2", "--reruns-delay", "1"])

    # 是否生成 Allure 报告
    if args.no_report:
        cmd.append("-p")
        cmd.append("no:allure_pytest")
    else:
        allure_dir = os.path.join(PROJECT_ROOT, "temps")
        cmd.extend([f"--alluredir={allure_dir}", "--clean-alluredir"])

    return cmd


def list_tests(args: argparse.Namespace) -> int:
    """列出匹配的测试文件"""
    target = ""
    if args.test_path:
        target = args.test_path
    elif args.type:
        target = TYPE_DIR_MAP.get(args.type, "tests")
    else:
        target = "tests"

    cmd = [sys.executable, "-m", "pytest", "--collect-only", "-q"]
    if target:
        cmd.append(target)
    if args.marker:
        cmd.extend(["-m", args.marker])

    logger.step(f"列出测试: {' '.join(cmd)}")
    return subprocess.call(cmd, cwd=PROJECT_ROOT)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="OpMS 测试运行脚本")
    parser.add_argument(
        "-t", "--type", choices=list(TYPE_DIR_MAP.keys()),
        help="测试类型: web / api，不指定则运行全部",
    )
    parser.add_argument(
        "-m", "--marker",
        help="pytest 标记表达式，如 smoke / 'smoke and critical'",
    )
    parser.add_argument(
        "--no-report", action="store_true",
        help="不生成 Allure 报告",
    )
    parser.add_argument(
        "-l", "--list", action="store_true",
        help="仅列出匹配的测试用例，不执行",
    )
    parser.add_argument(
        "test_path", nargs="?",
        help="指定测试文件或目录路径",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.list:
        sys.exit(list_tests(args))

    cmd = build_cmd(args)
    logger.step(f"执行测试: {' '.join(cmd)}")
    exit_code = subprocess.call(cmd, cwd=PROJECT_ROOT)

    if exit_code == 0:
        logger.success("测试执行完毕，全部通过")
    else:
        logger.fail(f"测试执行完毕，存在失败用例 (退出码: {exit_code})")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
