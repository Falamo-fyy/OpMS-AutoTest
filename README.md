# OpMS-AutoTest

基于 Playwright + Pytest 的 OpMS 综合运维服务平台自动化测试框架，采用 Page Object Model 设计模式，支持 Web UI 和 API 双维度测试。

## 功能特性

- **Web UI 测试** — 基于 Playwright 的浏览器自动化，支持 Chromium/Firefox/WebKit
- **API 接口测试** — 基于 requests 的接口验证，支持 JSON 数据处理
- **Page Object Model** — 页面对象与测试逻辑分离，定位器集中管理
- **数据驱动** — 测试数据存储在 YAML 文件中，与测试代码解耦
- **共享登录态** — 类级别 fixture 支持同一测试类共享浏览器实例与登录状态
- **自动重试** — 失败用例自动重跑 2 次，间隔 1 秒
- **失败截图** — 测试失败自动截图保存，便于问题定位
- **Allure 报告** — 自动生成图文并茂的测试报告
- **运行日志** — 统一日志管理，自动清理过期日志与 trace 文件
- **灵活配置** — 通过 `config.yaml` 统一管理浏览器、超时、日志等运行参数

## 项目结构

```
OpMS-AutoTest/
├── config/                  # 配置文件
│   └── config.yaml          # 全局运行配置
├── base/                    # 基础类
│   ├── base_page.py         # 页面操作基类（封装 Playwright 交互 + 日志 + 断言截图）
│   └── base_test.py         # 测试基类（注入 logger/page/截图能力）
├── page/                    # 页面对象
│   ├── login_page.py        # 登录页面
│   └── purchase_request_page.py  # 采购申请页面
├── tests/                   # 测试用例
│   ├── web/                 # Web UI 测试
│   │   ├── test_login.py    # 登录测试（4 个用例）
│   │   └── test_purchase_request_search.py  # 采购申请搜索测试（11 个用例）
│   └── api/                 # API 接口测试
│       └── test_api_login.py  # 登录接口测试（5 个用例）
├── data/                    # 测试数据（YAML）
│   ├── test_login_data.yaml
│   ├── test_api_login_data.yaml
│   └── test_purchase_request_search_data.yaml
├── utils/                   # 工具类
│   ├── config_reader.py     # YAML 配置读取器
│   ├── logger.py            # 日志管理器
│   └── cleanup.py           # 过期文件自动清理
├── scripts/                 # 辅助脚本
│   ├── run_tests.py         # 测试运行器
│   ├── allure_report.py     # Allure 报告生成器
│   └── clean_images.py      # 截图清理工具
├── conftest.py              # Pytest fixture 定义
├── pytest.ini               # Pytest 配置
└── .env.example             # 环境变量模板
```

## 快速开始

### 环境要求

- Python 3.8+
- pip

### 安装

```bash
# 克隆仓库
git clone https://github.com/falamo/OpMS-AutoTest.git
cd OpMS-AutoTest

# 安装依赖
pip install playwright pytest pytest-rerunfailures allure-pytest PyYAML python-dotenv requests

# 安装 Playwright 浏览器
playwright install

# 配置测试账号
cp .env.example .env
# 编辑 .env，填入 TEST_USER 和 TEST_PASSWORD
```

### 运行测试

```bash
# 运行全部测试
pytest

# 运行单个测试文件
pytest tests/web/test_login.py

# 运行单个测试方法
pytest tests/web/test_login.py::TestLogin::test_login_success

# 按标记运行
pytest -m smoke          # 冒烟测试
pytest -m web            # Web UI 测试
pytest -m api            # API 接口测试
pytest -m critical       # 关键功能测试
pytest -m regression     # 回归测试

# 使用脚本运行器
python scripts/run_tests.py                # 运行全部
python scripts/run_tests.py -t web         # 仅 Web 测试
python scripts/run_tests.py -t api         # 仅 API 测试
python scripts/run_tests.py -m smoke       # 按标记运行
python scripts/run_tests.py -l             # 列出用例不执行
python scripts/run_tests.py --no-report    # 跳过 Allure 报告
```

### 查看报告

```bash
# 生成 Allure 报告并启动本地服务查看
allure serve ./temps

# 使用脚本生成报告
python scripts/allure_report.py            # 运行测试 + 生成报告
python scripts/allure_report.py --skip-test  # 仅生成报告（不运行测试）
python scripts/allure_report.py --open     # 生成报告并在浏览器中打开
```

## 配置说明

核心配置在 `config/config.yaml` 中管理：

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `base_url` | Web 平台地址 | `http://47.253.182.106` |
| `api_base_url` | API 接口地址 | `http://47.253.182.106:8080` |
| `browser` | 浏览器类型 | `chromium` |
| `headless` | 无头模式 | `false` |
| `timeout.page_load` | 页面加载超时(ms) | `30000` |
| `timeout.script` | 脚本执行超时(ms) | `10000` |
| `log.level` | 日志级别 | `DEBUG` |
| `log.cleanup_days` | 日志保留天数 | `7` |
| `tracing.enabled` | 是否启用 Playwright Trace | `false` |
| `tracing.cleanup_days` | Trace 保留天数 | `7` |

测试账号通过 `.env` 文件配置，不硬编码在代码中：

```
TEST_USER = your_username
TEST_PASSWORD = your_password
```

获取账号密码请联系 falamo@qq.com。

## 架构设计

### 四层架构

```
Config 层  →  Base 层  →  Page 层  →  Test 层
配置读取      基础封装     页面对象     测试用例
```

1. **Config 层** — `config.yaml` 统一管理运行参数，`ConfigReader` 提供层级键访问
2. **Base 层** — `BasePage` 封装所有 Playwright 交互（自动日志 + 断言失败截图），`BaseTest` 注入通用测试能力
3. **Page 层** — 每个页面一个类，定位器作为类常量，业务方法对外暴露
4. **Test 层** — 继承 `BaseTest`，调用页面对象完成测试，数据从 YAML 加载

### Fixture 生命周期

| Fixture | 作用域 | 说明 |
|---------|--------|------|
| `browser` | session | 整个测试会话共享一个浏览器实例 |
| `context` | function | 每个用例独立上下文（隔离 cookie/storage） |
| `page` | function | 每个用例独立页面 |
| `shared_context` | class | 测试类内共享上下文 |
| `shared_page` | class | 测试类内共享页面 |
| `login_page` | class | 共享登录页面对象 |
| `logged_in_page` | class | 共享已登录页面（自动完成登录） |

需要登录态的测试类使用 `logged_in_page`，登录只执行一次，后续用例共享 session。

### 输出目录

| 目录 | 用途 |
|------|------|
| `image/` | 失败截图与手动截图 |
| `logs/` | 测试执行日志 |
| `temps/` | Allure 原始结果 |
| `reports/` | Allure HTML 报告与 Playwright Trace |

## 测试标记

| 标记 | 说明 |
|------|------|
| `smoke` | 冒烟测试 |
| `critical` | 关键功能（阻塞发布） |
| `slow` | 慢速用例 |
| `regression` | 回归测试 |
| `api` | API 接口测试 |
| `web` | Web UI 测试 |

## 扩展指南

### 新增页面对象

1. 在 `page/` 下新建类，继承 `BasePage`
2. 定义类级别定位器常量（如 `USERNAME = "input[placeholder='请输入用户名']"`）
3. 封装业务操作方法（每个方法自动记录日志）
4. 断言方法委托给 `BasePage.assert_*`

### 新增测试用例

1. 在 `data/` 下创建对应的 YAML 测试数据文件
2. 在 `tests/web/` 或 `tests/api/` 下新建测试类，继承 `BaseTest`
3. 需要登录态时使用 `logged_in_page` fixture
4. 通过 `ConfigReader("data/xxx.yaml")` 加载测试数据

## 许可证

MIT License
