# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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
```

Pytest is configured via `pytest.ini` with auto-flags: `-v -s --tb=short --reruns 2 --reruns-delay 1 --alluredir=./temps --clean-alluredir`. Failed tests are automatically retried twice with 1s delay.

No linter/formatter is configured. No `requirements.txt` exists; dependencies include: `playwright`, `pytest`, `pytest-rerunfailures`, `allure-pytest`, `PyYAML`, `python-dotenv`.

## Architecture

Playwright-based web UI test framework using Page Object Model, testing a Chinese-language operations management platform (OpMS).

### Four-layer structure

1. **Config** — `config/config.yaml` holds all runtime settings (base URL, browser, headless, timeouts, logging, reports). `utils/config_reader.py` provides a singleton `config` object with `get(*keys, default)`, `get_int()`, `get_bool()` for nested key access. Credentials live in `.env` (gitignored) loaded via `python-dotenv`.

2. **Base classes** — `base/base_page.py` (`BasePage`) wraps all Playwright Page interactions with `logger.info()` calls before/after each action. `base/base_test.py` (`BaseTest`) uses `@pytest.fixture(autouse=True)` to inject `self.page`, `self.base_page`, `self.logger`, and `self._test_name` into every test. Also provides `save_screenshot()` and `save_screenshot_on_failure()`.

3. **Page objects** — `page/` directory. Each page class inherits from `BasePage`, defines locators as class attributes, and exposes business-action methods (navigate, input, click, assert).

4. **Tests** — `tests/` directory, organized by type (`tests/web/`). Test classes inherit from `BaseTest`, use page objects to perform actions and assertions. Allure decorators for reporting.

### Fixture lifecycle (`conftest.py`)

- `pytest_configure` / `pytest_unconfigure` — session-scoped browser launch/teardown
- `context` fixture — creates a browser context per test (1920x1080 viewport, configured timeouts)
- `page` fixture — creates a new page per test from the context
- `pytest_runtest_makereport` hook — auto-screenshots on failure to `image/`

### Logging (`utils/logger.py`)

`Logger.get(name)` returns a singleton. Convenience methods with prefixes: `step()` → `[STEP]`, `data()` → `[DATA]`, `success()` → `[PASS]`, `fail()` → `[FAIL]`. All `BasePage` methods log at INFO level. Configuration (level, format, dir) comes from `config.yaml` `log` section.

## Conventions

- All code comments, log messages, and docstrings are in Chinese
- Page object locators are defined as class-level constants (e.g., `USERNAME_INPUT = "input[placeholder='请输入用户名']"`)
- Every `BasePage` method must log its action before (and after for getters that return values)
- Test credentials are accessed from `.env` via `os.getenv()`, never hardcoded
- Custom pytest markers: `smoke`, `critical`, `slow`, `regression`, `api`, `web`
