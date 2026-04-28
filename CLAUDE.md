# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

```bash
# Install dependencies (no requirements.txt exists)
pip install playwright pytest pytest-rerunfailures allure-pytest PyYAML python-dotenv

# Install Playwright browsers
playwright install

# Create .env from example and fill in credentials
cp .env.example .env
# Edit .env: set TEST_USER and TEST_PASSWORD
```

## Common Commands

```bash
# Run all tests
pytest

# Run a single test file
pytest tests/web/test_login.py

# Run a single test method
pytest tests/web/test_login.py::TestLogin::test_login_success

# Run by marker
pytest -m smoke
pytest -m web

# Generate Allure report (after test run)
allure serve ./temps

# Script runner (alternative entry point)
python scripts/run_tests.py                        # run all
python scripts/run_tests.py -t web                 # run web tests only
python scripts/run_tests.py -m smoke               # run by marker
python scripts/run_tests.py -l                     # list tests without running
python scripts/run_tests.py --no-report            # skip Allure report

# Allure report script
python scripts/allure_report.py                    # run tests + generate report
python scripts/allure_report.py --skip-test        # generate report from existing data
python scripts/allure_report.py --open             # open report in browser
```

Pytest is configured via `pytest.ini` with auto-flags: `-v -s --tb=short --reruns 2 --reruns-delay 1 --alluredir=./temps --clean-alluredir`. Failed tests are automatically retried twice with 1s delay.

No linter/formatter is configured.

## Architecture

Playwright-based web UI test framework using Page Object Model, testing a Chinese-language operations management platform (OpMS).

### Four-layer structure

1. **Config** — `config/config.yaml` holds all runtime settings (base URL, browser, headless, timeouts, logging, reports). `utils/config_reader.py` provides a singleton `config` object with `get(*keys, default)`, `get_int()`, `get_bool()` for nested key access. Also used to load test data YAML files: `ConfigReader("data/test_login_data.yaml")`.

2. **Base classes** — `base/base_page.py` (`BasePage`) wraps all Playwright Page interactions with `logger.info()` calls before/after each action; assertion methods auto-screenshot on failure to `image/`. `base/base_test.py` (`BaseTest`) uses `@pytest.fixture(autouse=True)` to inject `self.page`, `self.base_page`, `self.logger`, and `self._test_name` into every test. Also provides `save_screenshot()` and `save_screenshot_on_failure()`.

3. **Page objects** — `page/` directory. Each page class inherits from `BasePage`, defines locators as class attributes, and exposes business-action methods (navigate, input, click, assert).

4. **Tests** — `tests/` directory, organized by type (`tests/web/`, `tests/api/`). Test classes inherit from `BaseTest`, use page objects to perform actions and assertions. Allure decorators for reporting. Test data is loaded from `data/*.yaml` via `ConfigReader`.

### Fixture lifecycle (`conftest.py`)

- `pytest_configure` / `pytest_unconfigure` — session-scoped browser launch/teardown; `pytest_configure` sets run-level log file and cleans expired logs/traces
- `context` fixture — creates a browser context per test (1920x1080 viewport, configured timeouts)
- `page` fixture — creates a new page per test from the context
- `pytest_runtest_makereport` hook — auto-screenshots on failure to `image/`
- Tracing: when `tracing.enabled=true` in config, Playwright traces are saved to `reports/traces/YYYY-MM-DD/test_name.zip` and auto-cleaned after `tracing.cleanup_days` days
- Logging: each pytest run produces a single log file `logs/run_YYYYMMDD_HHMMSS.log`; expired logs auto-cleaned after `log.cleanup_days` days

### Output directories

| Directory | Purpose |
|-----------|---------|
| `image/` | Failure screenshots (auto) and manual screenshots |
| `logs/` | Test execution logs |
| `temps/` | Allure raw results (cleaned each run) |
| `reports/` | Allure HTML reports and Playwright traces |

### Logging (`utils/logger.py`)

`Logger.get(name)` returns a singleton. Convenience methods with prefixes: `step()` → `[STEP]`, `data()` → `[DATA]`, `success()` → `[PASS]`, `fail()` → `[FAIL]`. All `BasePage` methods log at INFO level. Configuration (level, format, dir) comes from `config.yaml` `log` section.

During pytest runs, `Logger.set_run_log()` is called in `pytest_configure` to create a shared log file `logs/run_YYYYMMDD_HHMMSS.log`. All loggers write to this single file instead of per-name files. Expired logs are auto-cleaned by `clean_logs()` based on `log.cleanup_days` in config.

## Conventions

- All code comments, log messages, and docstrings are in Chinese
- Page object locators are defined as class-level constants (e.g., `USERNAME = "input[placeholder='请输入用户名']"`)
- Every `BasePage` method must log its action before (and after for getters that return values)
- Test credentials are accessed from `.env` via `os.getenv()`, never hardcoded
- Test data for parameterized/negative cases lives in `data/*.yaml`, loaded via `ConfigReader(path)`, not inline in test files
- Custom pytest markers: `smoke`, `critical`, `slow`, `regression`, `api`, `web`
- New page objects follow the `LoginPage` pattern: class-level locator constants, business-action methods, assertion methods that delegate to `BasePage.assert_*`
- API 测试用例必须引入 `json` 库处理接口返回的 JSON 数据：字符串处理用 `json.loads()` / `json.dumps()`，文件处理用 `json.load()` / `json.dump()`
