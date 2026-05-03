# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

```bash
pip install playwright pytest pytest-rerunfailures allure-pytest PyYAML python-dotenv requests
playwright install

cp .env.example .env
# Edit .env: set TEST_USER and TEST_PASSWORD
```

No `requirements.txt` exists — the above is the complete dependency list.

## Common Commands

```bash
# Run all tests (no auto-rerun, no Allure — plain pytest)
pytest

# Run a single test file
pytest tests/web/test_login.py

# Run a single test method
pytest tests/web/test_login.py::TestLogin::test_login_success

# Run by marker
pytest -m smoke
pytest -m web
pytest -m api

# Script runner (adds --reruns 2 --reruns-delay 1 --alluredir=./temps --clean-alluredir)
python scripts/run_tests.py                        # run all
python scripts/run_tests.py -t web                 # run web tests only
python scripts/run_tests.py -m smoke               # run by marker
python scripts/run_tests.py -l                     # list tests without running
python scripts/run_tests.py --no-report            # skip Allure report

# Allure report
python scripts/allure_report.py                    # run tests + generate report
python scripts/allure_report.py --skip-test        # generate report from existing data
python scripts/allure_report.py --open             # open report in browser

# Clean old screenshots
python scripts/clean_images.py                     # delete screenshots older than 30 days
python scripts/clean_images.py --days 7            # keep only last 7 days
python scripts/clean_images.py -n                  # dry run (preview only)
```

**Important:** `pytest.ini` only sets `-v -s --tb=short`. Auto-rerun and Allure flags only apply when running via `scripts/run_tests.py`. Bare `pytest` will not retry failures or generate Allure data.

No linter/formatter is configured.

## Architecture

Playwright-based web UI test framework using Page Object Model, testing a Chinese-language operations management platform (OpMS).

### Four-layer structure

1. **Config** — `config/config.yaml` holds all runtime settings (base URL, `api_base_url`, browser, headless, timeouts, logging, tracing, reports). `config/api_config.yaml` defines all API endpoints (path + method per interface). `utils/config_reader.py` provides a singleton `config` object with `get(*keys, default)`, `get_int()`, `get_bool()` for nested key access. Also used to load test data YAML files: `ConfigReader("data/api/test_api_login_data.yaml")`.

2. **Base classes** — `base/base_page.py` (`BasePage`) wraps all Playwright Page interactions with `logger.info()` calls before/after each action; assertion methods auto-screenshot on failure to `image/`. `base/base_api.py` (`BaseApi`) wraps all `requests` interactions — `send(api_name)` reads path/method from `api_config.yaml`, auto-injects token into `Authorization` header, logs request/response; `login()` authenticates and stores token; `parse_json()` parses responses. `base/base_test.py` (`BaseTest`) uses `@pytest.fixture(autouse=True)` to inject only `self.logger` and `self._test_name`. Page objects and API client are injected by each test class's own `_setup_*` fixture — **not** by `BaseTest`.

3. **Page objects** — `page/` directory. Each page class inherits from `BasePage`, defines locators as class attributes, and exposes business-action methods (navigate, input, click, assert).

4. **Tests** — `tests/` directory, organized by type (`tests/web/`, `tests/api/`). Test classes inherit from `BaseTest`. Web tests use page objects to perform actions and assertions; API tests use `BaseApi` to send requests and verify responses. Allure decorators for reporting. Test data is loaded from `data/api/*.yaml` or `data/web/*.yaml` via `ConfigReader`.

### API test architecture (`BaseApi`)

API tests use `BaseApi` from `base/base_api.py` as the single entry point for all HTTP requests:

- **`send(api_name, ...)`** — primary method: reads `path` and `method` from `config/api_config.yaml` by interface name, then sends the request. Example: `self._api.send("user_info")` sends a GET to `/user/info` with auto-injected token.
- **`api_request(method, path, ...)`** — low-level method for ad-hoc requests with explicit method/path (still auto-injects token and logs).
- **`get/post/put/delete(path, ...)`** — shortcuts for `api_request` with fixed method.
- **`login(username, password)`** — authenticates via `user_login` config, stores token; all subsequent `send()`/`api_request()` calls auto-attach `Authorization` header.
- **`set_token(token)` / `get_token()`** — manually override token (for testing no-token or invalid-token scenarios).
- **`parse_json(response)`** — parses response body with `json.loads()`, calls `pytest.fail()` on non-JSON responses.

API endpoint configuration lives in `config/api_config.yaml`:
```yaml
user_login:
  path: /user/login
  method: POST
user_info:
  path: /user/info
  method: GET
```

Adding a new API endpoint: add an entry to `api_config.yaml`, then call `self._api.send("new_api_name")`.

### Fixture lifecycle (`conftest.py`)

| Fixture | Scope | Purpose |
|---------|-------|---------|
| `config` | session | Full config dictionary (`cfg.data`) for direct config reads |
| `browser` | session | Single browser instance for entire test session |
| `context` | function | Isolated browser context per test (separate cookies/storage) |
| `page` | function | New page per test from function-scoped context |
| `shared_context` | class | Shared context for all tests in a class |
| `shared_page` | class | Shared page for all tests in a class |
| `login_page` | class | Shared `LoginPage` instance wrapping `shared_page` |
| `logged_in_page` | class | `shared_page` after performing login — use this for tests needing auth |
| `logged_in_api` | class | Pre-authenticated `BaseApi` instance — use for API tests; yield后恢复token防止状态污染 |

Tests that need login should request `logged_in_page` in their class-level `_setup_*` fixture. Login executes once per class and all methods share the session.

`pytest_configure` / `pytest_unconfigure` handle session-scoped browser launch/teardown, set run-level log file, and clean expired logs/traces via `utils/cleanup.py`.

### Test class fixture pattern

Every test class defines an `autouse=True` fixture named `_setup_*` that:
1. Receives the appropriate fixture (`logged_in_page` for web, `logged_in_api` for API)
2. Creates the page object or assigns the `BaseApi` instance
3. Sets `self.logger`, `self._test_name`, and type-specific attributes
4. Performs setup actions (navigate to page, login, etc.)

Web test example:
```python
@pytest.fixture(autouse=True)
def _setup_search(self, logged_in_page, request):
    self._purchase_page = PurchaseRequestPage(logged_in_page)
    self.page = logged_in_page
    self.base_page = self._purchase_page
    self.logger = Logger.get("opms")
    self._test_name = request.node.name
    self._purchase_page.navigate_to_purchase_request()
```

API test example (using `logged_in_api`):
```python
@pytest.fixture(autouse=True)
def _setup_api(self, logged_in_api, request):
    self._api = logged_in_api
    self._original_token = logged_in_api.get_token()
    self.logger = Logger.get("opms")
    self._test_name = request.node.name
    yield
    self._api.set_token(self._original_token)  # 恢复 token 防止用例间状态污染
```

### Output directories

| Directory | Purpose |
|-----------|---------|
| `image/` | Failure screenshots (auto) and manual screenshots |
| `logs/` | Test execution logs |
| `temps/` | Allure raw results (cleaned each run) |
| `reports/` | Allure HTML reports and Playwright traces |

### Test data directories

| Directory | Purpose |
|-----------|---------|
| `data/api/` | API test data (e.g., `test_api_login_data.yaml`) |
| `data/web/` | Web UI test data (e.g., `test_login_data.yaml`, `test_purchase_request_search_data.yaml`) |

### Logging (`utils/logger.py`)

`Logger.get(name)` returns a singleton. Convenience methods with prefixes: `step()` → `[STEP]`, `data()` → `[DATA]`, `success()` → `[PASS]`, `fail()` → `[FAIL]`. All `BasePage` methods log at INFO level. Configuration (level, format, dir) comes from `config.yaml` `log` section.

During pytest runs, `Logger.set_run_log()` is called in `pytest_configure` to create a shared log file `logs/run_YYYYMMDD_HHMMSS.log`. All loggers write to this single file instead of per-name files. Expired logs are auto-cleaned by `clean_logs()` based on `log.cleanup_days` in config.

## Conventions

- All code comments, log messages, and docstrings are in Chinese
- Every `BasePage` method must log its action before (and after for getters that return values)
- Test credentials are accessed from `.env` via `os.getenv()` (no hardcoded defaults — `.env` 缺失时直接报错，避免隐藏配置问题)
- Test data for parameterized/negative cases lives in `data/api/*.yaml` or `data/web/*.yaml`, loaded via `ConfigReader(path)`, not inline in test files
- Custom pytest markers: `smoke`, `critical`, `slow`, `regression`, `api`, `web`
- API 测试用例必须引入 `json` 库处理接口返回的 JSON 数据：字符串处理用 `json.loads()` / `json.dumps()`，文件处理用 `json.load()` / `json.dump()`
- API 接口信息统一维护在 `config/api_config.yaml`，通过 `BaseApi.send(api_name)` 读取配置发请求，不在测试代码中硬编码接口路径

### Locators 目录 (`locators/`)

结构化的页面元素语义定义，用于减少 Playwright 浏览网页时的 token 消耗。

| 文件 | 页面 |
|------|------|
| `locators/login.yaml` | 登录页 |
| `locators/purchase_request.yaml` | 采购申请页 |
| `locators/project_management.yaml` | 项目管理页 |

**使用规则：**

1. **优先读取 `locators/` YAML** — 需要定位元素时，先查 `locators/` 下对应页面的 YAML 文件，不要重新浏览网页
2. **只有 locator 失效时才允许局部扫描** — 用 Playwright 工具仅扫描失效元素所在的局部区域，禁止全 DOM 分析
3. **发现新元素时补充 YAML** — 浏览中发现未记录的元素，追加到对应 YAML 文件

YAML 格式：
```yaml
page: 页面名称

elements:

  元素名称:
    type: role | placeholder | label | text | testid | css
    role: button              # type=role 时必填
    name: 按钮文本             # type=role 时使用
    value: 属性值              # type=placeholder/label/text/testid/css 时使用
```

type 优先级：`role` > `testid` > `label` > `placeholder` > `text` > `css`（最后手段）

### Locator best practices

定位优先级：**get_by_role 最优先**，然后 testid、label、placeholder，最后才用 CSS。绝对禁用 `nth-child`、xpath、深层 CSS、`locator("..")` 等依赖 DOM 结构的脆弱选择器。

1. **`get_by_role()`** — 第一优先级，语义化、稳定、可访问性优先
2. **`get_by_test_id()`** — 第二优先级（页面有 data-testid 时优先）
3. **`get_by_label()`** — 第三优先级
4. **`get_by_placeholder()`** — 第四优先级
5. **`get_by_text()` + `filter(has_text=)` / `css`** — 仅当以上均不可用

```python
# BAD — 依赖 DOM 顺序，字段调整即失败
SEARCH_URGENCY = ".search-form .el-form-item:nth-child(2) .el-select"

# GOOD — role + name 文本定位
self.page.get_by_role("button", name="查询")
self.page.get_by_role("menuitem", name="采购申请")
self.page.get_by_role("dialog", name="新增项目")

# GOOD — placeholder 定位
self.page.get_by_placeholder("请输入项目名称")

# GOOD — label 定位
self.page.get_by_label("省份")
```

- **Use `get_by_role("row"/"cell")` for table access** instead of CSS `:nth-child()` on `.el-table__row > td`
- **Prefer `get_cell_text_by_header(row, header)`** over numeric column indices — dynamically resolves column position from header text, so tests survive column reordering
- Page objects can use private `_prefixed` helper methods for reusable locator strategies (e.g., `_dialog_select_by_label`, `_body_table`)
