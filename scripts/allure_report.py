"""
Allure 测试报告生成脚本

用法:
    python scripts/allure_report.py              # 运行测试并生成报告
    python scripts/allure_report.py --skip-test  # 跳过测试，仅根据已有数据生成报告
    python scripts/allure_report.py --open       # 生成报告后自动打开浏览器
    python scripts/allure_report.py -m smoke     # 仅运行 smoke 标记的用例
    python scripts/allure_report.py tests/web/   # 指定测试目录或文件
"""

import os
import sys
import argparse
import subprocess

# 将项目根目录加入 sys.path，以便导入 utils
PROJECT_ROOT = os.path.normpath(os.path.join(os.path.abspath(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from utils.logger import Logger
from utils.config_reader import config

logger = Logger.get("allure_report")

# 目录配置
ALLURE_RESULTS_DIR = os.path.join(PROJECT_ROOT, "temps")
REPORT_DIR = os.path.join(PROJECT_ROOT, "reports")


def run_pytest(extra_args: list) -> int:
    """执行 pytest 并生成 Allure 原始数据，返回退出码"""
    cmd = [
        sys.executable, "-m", "pytest",
        f"--alluredir={ALLURE_RESULTS_DIR}",
        "--clean-alluredir",
    ] + extra_args

    logger.step(f"执行测试: {' '.join(cmd)}")
    exit_code = subprocess.call(cmd, cwd=PROJECT_ROOT)

    if exit_code == 0:
        logger.success("测试执行完毕，全部通过")
    else:
        logger.fail(f"测试执行完毕，存在失败用例 (退出码: {exit_code})")

    return exit_code


def generate_report(open_browser: bool = False) -> bool:
    """调用 allure generate 生成 HTML 报告，返回是否成功"""
    if not os.path.isdir(ALLURE_RESULTS_DIR) or not os.listdir(ALLURE_RESULTS_DIR):
        logger.fail(f"Allure 结果目录为空或不存在: {ALLURE_RESULTS_DIR}")
        return False

    os.makedirs(REPORT_DIR, exist_ok=True)

    cmd = [
        "allure", "generate",
        ALLURE_RESULTS_DIR,
        "-o", REPORT_DIR,
        "--clean",
    ]

    logger.step(f"生成报告: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)

    if result.returncode != 0:
        logger.fail("Allure 报告生成失败，请确认已安装 allure 并加入 PATH")
        return False

    logger.success(f"报告已生成: {REPORT_DIR}")

    if open_browser:
        open_report()

    return True


def open_report():
    """调用 allure open 启动本地服务并在浏览器中查看报告"""
    logger.step("启动 Allure 本地服务查看报告 ...")
    try:
        subprocess.run(["allure", "open", REPORT_DIR], cwd=PROJECT_ROOT)
    except KeyboardInterrupt:
        logger.info("已关闭 Allure 本地服务")


def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="OpMS Allure 测试报告生成脚本")
    parser.add_argument(
        "--skip-test", action="store_true",
        help="跳过测试执行，仅根据已有 allure 结果数据生成报告",
    )
    parser.add_argument(
        "--open", action="store_true",
        help="生成报告后自动打开浏览器查看",
    )
    parser.add_argument(
        "pytest_args", nargs="*",
        help="传递给 pytest 的额外参数，如 -m smoke / tests/web/test_login.py",
    )
    return parser.parse_args()


def main():
    report_config = config.get("report", default={})
    title = report_config.get("title", "OpMS 自动化测试报告")
    logger.info(f"=== {title} ===")

    args = parse_args()

    if not args.skip_test:
        exit_code = run_pytest(args.pytest_args)
        if exit_code not in (0, 1):
            # 退出码 >=2 表示 pytest 本身出错（如参数错误），直接返回
            logger.fail(f"pytest 异常退出 (退出码: {exit_code})")
            sys.exit(exit_code)

    if not generate_report(open_browser=args.open):
        sys.exit(1)


if __name__ == "__main__":
    main()
