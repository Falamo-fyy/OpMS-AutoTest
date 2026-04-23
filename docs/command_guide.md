# OpMS-AutoTest 项目命令指南

## 环境准备

```bash
# 安装项目依赖
pip install playwright pytest pytest-rerunfailures allure-pytest PyYAML python-dotenv

# 安装 Playwright 浏览器（首次使用必须执行）
playwright install

# 安装 Allure 命令行工具（生成报告需要）
# Windows (Scoop)
scoop install allure
# macOS (Homebrew)
brew install allure

# 配置测试凭证
cp .env.example .env
# 编辑 .env 填入测试账号密码
```

## pytest 测试命令

### 基本运行

| 命令 | 说明 |
|------|------|
| `pytest` | 运行全部测试 |
| `pytest tests/web/test_login.py` | 运行指定测试文件 |
| `pytest tests/web/test_login.py::TestLogin::test_login_success` | 运行指定测试方法 |
| `pytest tests/web/` | 运行指定目录下所有测试 |

### 标记筛选 (-m)

| 命令 | 说明 |
|------|------|
| `pytest -m smoke` | 运行冒烟测试用例 |
| `pytest -m critical` | 运行核心功能用例 |
| `pytest -m slow` | 运行耗时用例 |
| `pytest -m regression` | 运行回归测试用例 |
| `pytest -m api` | 运行 API 测试用例 |
| `pytest -m web` | 运行 Web UI 测试用例 |
| `pytest -m "smoke and web"` | 运行同时拥有两个标记的用例 |
| `pytest -m "smoke or critical"` | 运行拥有任一标记的用例 |
| `pytest -m "not slow"` | 排除耗时用例 |

### 常用选项

| 参数 | 说明 |
|------|------|
| `-v` | 详细输出（已默认启用） |
| `-s` | 显示 print 标准输出（已默认启用） |
| `--tb=short` | 短格式错误回溯（已默认启用） |
| `--reruns 2` | 失败用例自动重试 2 次（已默认启用） |
| `--reruns-delay 1` | 重试间隔 1 秒（已默认启用） |
| `-k "login"` | 按用例名模糊匹配 |
| `-x` | 遇到第一个失败立即停止 |
| `--maxfail=3` | 累计 3 个失败后停止 |
| `-n auto` | 多进程并行执行（需安装 pytest-xdist） |
| `--headed` | 强制显示浏览器窗口 |
| `--headed --slowmo 500` | 每步操作间隔 500ms，便于调试观察 |

### 调试相关

| 命令 | 说明 |
|------|------|
| `pytest -k "login" --headed --slowmo 500` | 登录用例慢放调试 |
| `pytest --tb=long` | 完整错误堆栈 |
| `pytest -k "login" -v -s 2>&1 | tee run.log` | 输出同时写入日志文件 |

## Allure 报告命令

### 使用脚本（推荐）

| 命令 | 说明 |
|------|------|
| `python scripts/allure_report.py` | 运行测试 + 生成报告 |
| `python scripts/allure_report.py --skip-test` | 跳过测试，仅根据已有数据生成报告 |
| `python scripts/allure_report.py --open` | 生成报告并自动打开浏览器查看 |
| `python scripts/allure_report.py -m smoke` | 仅运行 smoke 用例后生成报告 |
| `python scripts/allure_report.py tests/web/test_login.py` | 指定测试文件后生成报告 |
| `python scripts/allure_report.py --skip-test --open` | 仅生成报告并打开浏览器 |

### 直接使用 allure 命令

| 命令 | 说明 |
|------|------|
| `allure generate ./temps -o ./reports --clean` | 根据 temps 生成报告到 reports |
| `allure open ./reports` | 启动本地服务查看报告 |
| `allure serve ./temps` | 实时生成并打开报告（不落盘） |

## 配置修改

### config.yaml 常用配置项

| 配置路径 | 说明 | 默认值 |
|----------|------|--------|
| `base_url` | 测试目标地址 | `http://47.253.182.106` |
| `browser` | 浏览器类型 chromium/firefox/webkit | `chromium` |
| `headless` | 无头模式 | `false` |
| `tracing.enabled` | 是否启用 Playwright Tracing | `false` |
| `timeout.page_load` | 页面加载超时(ms) | `30000` |
| `timeout.script` | 脚本执行超时(ms) | `10000` |
| `log.level` | 日志级别 | `DEBUG` |
| `log.dir` | 日志保存目录 | `logs` |
| `report.title` | Allure 报告标题 | `OpMS 自动化测试报告` |

### .env 环境变量

| 变量名 | 说明 |
|--------|------|
| `TEST_USER` | 测试账号用户名 |
| `TEST_PASSWORD` | 测试账号密码 |

## 目录说明

| 目录 | 说明 |
|------|------|
| `config/` | 配置文件(config.yaml) |
| `base/` | 基类(BasePage, BaseTest) |
| `page/` | 页面对象类 |
| `tests/` | 测试用例 |
| `scripts/` | 工具脚本 |
| `data/` | 测试数据 |
| `image/` | 失败自动截图 |
| `logs/` | 运行日志 |
| `temps/` | Allure 原始数据(pytest 生成) |
| `reports/` | Allure HTML 报告 |

## pytest.ini 默认参数

pytest 运行时自动附加以下参数，无需手动指定：

```
-v -s --tb=short --reruns 2 --reruns-delay 1 --alluredir=./temps --clean-alluredir
```
