import os
import allure
import pytest

from base.base_test import BaseTest
from page.receiving_records_page import ReceivingRecordsPage
from utils.logger import Logger
from utils.config_reader import ConfigReader

logger = Logger.get("opms")

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "web", "test_receiving_records_data.yaml")
receiving_data = ConfigReader(DATA_PATH)


@allure.feature("收货记录")
@allure.story("搜索筛选")
class TestReceivingRecordsSearch(BaseTest):
    """收货记录页面搜索筛选测试用例"""

    @pytest.fixture(autouse=True)
    def _setup_search(self, logged_in_page, request):
        """注入收货记录页面对象，导航到收货记录页面（共享已登录状态）"""
        self._receiving_page = ReceivingRecordsPage(logged_in_page)
        self.page = logged_in_page
        self.base_page = self._receiving_page
        self.logger = Logger.get("opms")
        self._test_name = request.node.name
        self._receiving_page.navigate_to_receiving_records()
        self._receiving_page.wait_for_load_state("domcontentloaded")

    # -------- 单条件筛选：采购状态 --------

    @allure.title("按采购状态筛选-未发货")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_purchase_status_unshipped(self):
        """筛选采购状态为"未发货"，验证所有结果采购状态均为未发货"""
        data = receiving_data.get("search_purchase_status_unshipped")
        logger.step(f"执行搜索: {data['description']}")

        self._receiving_page.select_purchase_status_filter(data["purchase_status"])
        self._receiving_page.click_search()

        count = self._receiving_page.get_table_row_count()
        assert count > 0, "筛选结果不应为空"
        for i in range(count):
            cell_text = self._receiving_page.get_cell_text_by_header(i, "采购状态")
            expected = data["purchase_status"]
            assert cell_text == expected, (
                f"第{i + 1}行采购状态验证失败\n"
                f"期望: '{expected}'\n"
                f"实际: '{cell_text}'\n"
                f"原始值: '{repr(cell_text)}'"
            )

        total = self._receiving_page.get_total_count()
        logger.success(f"{data['description']}验证通过，{total}")
        self._receiving_page.click_reset()

    @allure.title("按采购状态筛选-部分发货")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_purchase_status_partial(self):
        """筛选采购状态为"部分发货"，验证所有结果采购状态均为部分发货"""
        data = receiving_data.get("search_purchase_status_partial")
        logger.step(f"执行搜索: {data['description']}")

        self._receiving_page.select_purchase_status_filter(data["purchase_status"])
        self._receiving_page.click_search()

        count = self._receiving_page.get_table_row_count()
        assert count > 0, "筛选结果不应为空"
        for i in range(count):
            cell_text = self._receiving_page.get_cell_text_by_header(i, "采购状态")
            expected = data["purchase_status"]
            assert cell_text == expected, (
                f"第{i + 1}行采购状态验证失败\n"
                f"期望: '{expected}'\n"
                f"实际: '{cell_text}'\n"
                f"原始值: '{repr(cell_text)}'"
            )

        total = self._receiving_page.get_total_count()
        logger.success(f"{data['description']}验证通过，{total}")
        self._receiving_page.click_reset()

    # -------- 单条件筛选：收货状态 --------

    @allure.title("按收货状态筛选-未收货")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_receiving_status_unreceived(self):
        """筛选收货状态为"未收货"，验证所有结果收货状态均为未收货"""
        data = receiving_data.get("search_receiving_status_unreceived")
        logger.step(f"执行搜索: {data['description']}")

        self._receiving_page.select_receiving_status_filter(data["receiving_status"])
        self._receiving_page.click_search()

        count = self._receiving_page.get_table_row_count()
        assert count > 0, "筛选结果不应为空"
        for i in range(count):
            cell_text = self._receiving_page.get_cell_text_by_header(i, "收货状态")
            expected = data["receiving_status"]
            assert cell_text == expected, (
                f"第{i + 1}行收货状态验证失败\n"
                f"期望: '{expected}'\n"
                f"实际: '{cell_text}'\n"
                f"原始值: '{repr(cell_text)}'"
            )

        total = self._receiving_page.get_total_count()
        logger.success(f"{data['description']}验证通过，{total}")
        self._receiving_page.click_reset()

    @allure.title("按收货状态筛选-已收货")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_receiving_status_received(self):
        """筛选收货状态为"已收货"，验证所有结果收货状态均为已收货"""
        data = receiving_data.get("search_receiving_status_received")
        logger.step(f"执行搜索: {data['description']}")

        self._receiving_page.select_receiving_status_filter(data["receiving_status"])
        self._receiving_page.click_search()

        count = self._receiving_page.get_table_row_count()
        assert count > 0, "筛选结果不应为空"
        for i in range(count):
            cell_text = self._receiving_page.get_cell_text_by_header(i, "收货状态")
            expected = data["receiving_status"]
            assert cell_text == expected, (
                f"第{i + 1}行收货状态验证失败\n"
                f"期望: '{expected}'\n"
                f"实际: '{cell_text}'\n"
                f"原始值: '{repr(cell_text)}'"
            )

        total = self._receiving_page.get_total_count()
        logger.success(f"{data['description']}验证通过，{total}")
        self._receiving_page.click_reset()

    # -------- 单条件筛选：入库状态 --------

    @allure.title("按入库状态筛选-未入库")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_storage_status_unstored(self):
        """筛选入库状态为"未入库"，验证所有结果入库状态均为未入库"""
        data = receiving_data.get("search_storage_status_unstored")
        logger.step(f"执行搜索: {data['description']}")

        self._receiving_page.select_storage_status_filter(data["storage_status"])
        self._receiving_page.click_search()

        count = self._receiving_page.get_table_row_count()
        assert count > 0, "筛选结果不应为空"
        for i in range(count):
            cell_text = self._receiving_page.get_cell_text_by_header(i, "入库状态")
            expected = data["storage_status"]
            assert cell_text == expected, (
                f"第{i + 1}行入库状态验证失败\n"
                f"期望: '{expected}'\n"
                f"实际: '{cell_text}'\n"
                f"原始值: '{repr(cell_text)}'"
            )

        total = self._receiving_page.get_total_count()
        logger.success(f"{data['description']}验证通过，{total}")
        self._receiving_page.click_reset()

    # -------- 日期范围筛选 --------

    @allure.title("按收货日期范围筛选")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_receiving_date_range(self):
        """设置收货日期范围筛选，验证有结果返回"""
        data = receiving_data.get("search_receiving_date_range")
        logger.step(f"执行搜索: {data['description']}")

        self._receiving_page.fill_receiving_date_start(data["start_date"])
        self._receiving_page.fill_receiving_date_end(data["end_date"])
        self._receiving_page.click_search()

        count = self._receiving_page.get_table_row_count()
        assert count > 0, "日期范围筛选结果不应为空"

        total = self._receiving_page.get_total_count()
        logger.success(f"{data['description']}验证通过，{total}")
        self._receiving_page.click_reset()

    # -------- 组合筛选 --------

    @allure.title("采购状态+收货状态组合筛选")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.web
    @pytest.mark.smoke
    def test_search_by_purchase_and_receiving_status(self):
        """同时筛选采购状态和收货状态，验证两个条件同时生效"""
        data = receiving_data.get("search_purchase_and_receiving_status")
        logger.step(f"执行搜索: {data['description']}")

        self._receiving_page.select_purchase_status_filter(data["purchase_status"])
        self._receiving_page.select_receiving_status_filter(data["receiving_status"])
        self._receiving_page.click_search()

        count = self._receiving_page.get_table_row_count()
        assert count > 0, "组合筛选结果不应为空"
        for i in range(count):
            purchase_cell = self._receiving_page.get_cell_text_by_header(i, "采购状态")
            receiving_cell = self._receiving_page.get_cell_text_by_header(i, "收货状态")
            assert purchase_cell == data["purchase_status"], f"第{i + 1}行采购状态应为{data['purchase_status']}"
            assert receiving_cell == data["receiving_status"], f"第{i + 1}行收货状态应为{data['receiving_status']}"
        logger.success(f"{data['description']}验证通过，共{count}条")

    # -------- 重置 --------

    @allure.title("重置按钮清空筛选条件")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_reset_clears_filters(self):
        """设置筛选条件后点击重置，验证条件被清空且恢复全部数据"""
        logger.step("设置筛选条件后点击重置")

        self._receiving_page.select_receiving_status_filter("未收货")
        self._receiving_page.click_search()
        filtered_count = self._receiving_page.get_table_row_count()

        self._receiving_page.click_reset()
        reset_count = self._receiving_page.get_table_row_count()

        assert reset_count >= filtered_count, f"重置后数据量({reset_count})应不少于筛选后数据量({filtered_count})"
        logger.success("重置按钮验证通过")


@allure.feature("收货记录")
@allure.story("查看详情")
class TestReceivingRecordsView(BaseTest):
    """收货记录查看详情测试用例"""

    @pytest.fixture(autouse=True)
    def _setup_view(self, logged_in_page, request):
        """注入收货记录页面对象，导航到收货记录页面"""
        self._receiving_page = ReceivingRecordsPage(logged_in_page)
        self.page = logged_in_page
        self.base_page = self._receiving_page
        self.logger = Logger.get("opms")
        self._test_name = request.node.name
        self._receiving_page.navigate_to_receiving_records()
        self._receiving_page.wait_for_load_state("domcontentloaded")

    @allure.title("查看收货记录详情")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.web
    @pytest.mark.smoke
    def test_view_receiving_record_detail(self):
        """点击查看按钮，验证新标签页打开收货详情"""
        logger.step("点击第一行的查看按钮")

        count = self._receiving_page.get_table_row_count()
        assert count > 0, "表格应有数据"

        with self.page.context.expect_page() as new_page_info:
            self._receiving_page.click_view_button(0)
        detail_page = new_page_info.value
        detail_page.wait_for_load_state("domcontentloaded")

        assert detail_page.url, "详情页URL不应为空"
        logger.success(f"查看收货记录详情验证通过，详情页: {detail_page.url}")
        detail_page.close()
