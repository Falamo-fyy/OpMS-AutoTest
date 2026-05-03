import os
import allure
import pytest

from base.base_test import BaseTest
from page.audit_records_page import AuditRecordsPage
from utils.logger import Logger
from utils.config_reader import ConfigReader

logger = Logger.get("opms")

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "web", "test_audit_records_data.yaml")
audit_data = ConfigReader(DATA_PATH)


@allure.feature("审核记录")
@allure.story("搜索筛选")
class TestAuditRecordsSearch(BaseTest):
    """审核记录页面搜索筛选测试用例"""

    @pytest.fixture(autouse=True)
    def _setup_search(self, logged_in_page, request):
        """注入审核记录页面对象，导航到审核记录页面（共享已登录状态）"""
        self._audit_page = AuditRecordsPage(logged_in_page)
        self.page = logged_in_page
        self.base_page = self._audit_page
        self.logger = Logger.get("opms")
        self._test_name = request.node.name
        self._audit_page.navigate_to_audit_records()
        self._audit_page.wait_for_load_state("domcontentloaded")

    # -------- 单条件筛选：审核结果 --------

    @allure.title("按审核结果筛选-已批准")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_audit_result_approved(self):
        """筛选审核结果为"已批准"，验证所有结果审核结果均为已批准"""
        data = audit_data.get("search_audit_result_approved")
        logger.step(f"执行搜索: {data['description']}")

        self._audit_page.select_audit_result_filter(data["audit_result"])
        self._audit_page.click_search()

        count = self._audit_page.get_table_row_count()
        assert count > 0, "筛选结果不应为空"
        for i in range(count):
            cell_text = self._audit_page.get_cell_text_by_header(i, "审核结果")
            expected = data["audit_result"]
            assert cell_text == expected, (
                f"第{i + 1}行审核结果验证失败\n"
                f"期望: '{expected}'\n"
                f"实际: '{cell_text}'\n"
                f"原始值: '{repr(cell_text)}'"
            )

        total = self._audit_page.get_total_count()
        logger.success(f"{data['description']}验证通过，{total}")
        self._audit_page.click_reset()

    @allure.title("按审核结果筛选-已拒绝")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_audit_result_rejected(self):
        """筛选审核结果为"已拒绝"，验证所有结果审核结果均为已拒绝"""
        data = audit_data.get("search_audit_result_rejected")
        logger.step(f"执行搜索: {data['description']}")

        self._audit_page.select_audit_result_filter(data["audit_result"])
        self._audit_page.click_search()

        count = self._audit_page.get_table_row_count()
        assert count > 0, "筛选结果不应为空"
        for i in range(count):
            cell_text = self._audit_page.get_cell_text_by_header(i, "审核结果")
            expected = data["audit_result"]
            assert cell_text == expected, (
                f"第{i + 1}行审核结果验证失败\n"
                f"期望: '{expected}'\n"
                f"实际: '{cell_text}'\n"
                f"原始值: '{repr(cell_text)}'"
            )

        total = self._audit_page.get_total_count()
        logger.success(f"{data['description']}验证通过，{total}")
        self._audit_page.click_reset()

    @allure.title("按审核结果筛选-审核中")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_audit_result_pending(self):
        """筛选审核结果为"审核中"，验证所有结果审核结果均为审核中"""
        data = audit_data.get("search_audit_result_pending")
        logger.step(f"执行搜索: {data['description']}")

        self._audit_page.select_audit_result_filter(data["audit_result"])
        self._audit_page.click_search()

        count = self._audit_page.get_table_row_count()
        assert count > 0, "筛选结果不应为空"
        for i in range(count):
            cell_text = self._audit_page.get_cell_text_by_header(i, "审核结果")
            expected = data["audit_result"]
            assert cell_text == expected, (
                f"第{i + 1}行审核结果验证失败\n"
                f"期望: '{expected}'\n"
                f"实际: '{cell_text}'\n"
                f"原始值: '{repr(cell_text)}'"
            )

        total = self._audit_page.get_total_count()
        logger.success(f"{data['description']}验证通过，{total}")
        self._audit_page.click_reset()

    # -------- 单条件筛选：审核人 --------

    @allure.title("按审核人筛选")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_auditor(self):
        """筛选审核人，验证所有结果审核人匹配"""
        data = audit_data.get("search_auditor")
        logger.step(f"执行搜索: {data['description']}")

        self._audit_page.select_auditor_filter(data["auditor"])
        self._audit_page.click_search()

        count = self._audit_page.get_table_row_count()
        assert count > 0, "筛选结果不应为空"
        for i in range(count):
            cell_text = self._audit_page.get_cell_text_by_header(i, "审核人")
            expected = data["auditor"]
            assert cell_text == expected, (
                f"第{i + 1}行审核人验证失败\n"
                f"期望: '{expected}'\n"
                f"实际: '{cell_text}'\n"
                f"原始值: '{repr(cell_text)}'"
            )

        total = self._audit_page.get_total_count()
        logger.success(f"{data['description']}验证通过，{total}")
        self._audit_page.click_reset()

    # -------- 单条件筛选：申请状态 --------

    @allure.title("按申请状态筛选-已提交")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_apply_status_submitted(self):
        """筛选申请状态为"已提交"，验证所有结果申请状态均为已提交"""
        data = audit_data.get("search_apply_status_submitted")
        logger.step(f"执行搜索: {data['description']}")

        self._audit_page.select_apply_status_filter(data["apply_status"])
        self._audit_page.click_search()

        count = self._audit_page.get_table_row_count()
        assert count > 0, "筛选结果不应为空"
        for i in range(count):
            cell_text = self._audit_page.get_cell_text_by_header(i, "申请状态")
            expected = data["apply_status"]
            assert cell_text == expected, (
                f"第{i + 1}行申请状态验证失败\n"
                f"期望: '{expected}'\n"
                f"实际: '{cell_text}'\n"
                f"原始值: '{repr(cell_text)}'"
            )

        total = self._audit_page.get_total_count()
        logger.success(f"{data['description']}验证通过，{total}")
        self._audit_page.click_reset()

    @allure.title("按申请状态筛选-已批准")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_apply_status_approved(self):
        """筛选申请状态为"已批准"，验证所有结果申请状态均为已批准"""
        data = audit_data.get("search_apply_status_approved")
        logger.step(f"执行搜索: {data['description']}")

        self._audit_page.select_apply_status_filter(data["apply_status"])
        self._audit_page.click_search()

        count = self._audit_page.get_table_row_count()
        assert count > 0, "筛选结果不应为空"
        for i in range(count):
            cell_text = self._audit_page.get_cell_text_by_header(i, "申请状态")
            expected = data["apply_status"]
            assert cell_text == expected, (
                f"第{i + 1}行申请状态验证失败\n"
                f"期望: '{expected}'\n"
                f"实际: '{cell_text}'\n"
                f"原始值: '{repr(cell_text)}'"
            )

        total = self._audit_page.get_total_count()
        logger.success(f"{data['description']}验证通过，{total}")
        self._audit_page.click_reset()

    @allure.title("按申请状态筛选-审核中")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_apply_status_pending(self):
        """筛选申请状态为"审核中"，验证所有结果申请状态均为审核中"""
        data = audit_data.get("search_apply_status_pending")
        logger.step(f"执行搜索: {data['description']}")

        self._audit_page.select_apply_status_filter(data["apply_status"])
        self._audit_page.click_search()

        count = self._audit_page.get_table_row_count()
        assert count > 0, "筛选结果不应为空"
        for i in range(count):
            cell_text = self._audit_page.get_cell_text_by_header(i, "申请状态")
            expected = data["apply_status"]
            assert cell_text == expected, (
                f"第{i + 1}行申请状态验证失败\n"
                f"期望: '{expected}'\n"
                f"实际: '{cell_text}'\n"
                f"原始值: '{repr(cell_text)}'"
            )

        total = self._audit_page.get_total_count()
        logger.success(f"{data['description']}验证通过，{total}")
        self._audit_page.click_reset()

    # -------- 日期范围筛选 --------

    @allure.title("按申请日期范围筛选")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_apply_date_range(self):
        """设置申请日期范围筛选，验证有结果返回"""
        data = audit_data.get("search_apply_date_range")
        logger.step(f"执行搜索: {data['description']}")

        self._audit_page.fill_apply_date_start(data["start_date"])
        self._audit_page.fill_apply_date_end(data["end_date"])
        self._audit_page.click_search()

        count = self._audit_page.get_table_row_count()
        assert count > 0, "日期范围筛选结果不应为空"

        total = self._audit_page.get_total_count()
        logger.success(f"{data['description']}验证通过，{total}")
        self._audit_page.click_reset()

    @allure.title("按审批时间范围筛选")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_audit_date_range(self):
        """设置审批时间范围筛选，验证有结果返回"""
        data = audit_data.get("search_audit_date_range")
        logger.step(f"执行搜索: {data['description']}")

        self._audit_page.fill_audit_date_start(data["start_date"])
        self._audit_page.fill_audit_date_end(data["end_date"])
        self._audit_page.click_search()

        count = self._audit_page.get_table_row_count()
        assert count > 0, "日期范围筛选结果不应为空"

        total = self._audit_page.get_total_count()
        logger.success(f"{data['description']}验证通过，{total}")
        self._audit_page.click_reset()

    # -------- 组合筛选 --------

    @allure.title("审核结果+申请状态组合筛选")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.web
    @pytest.mark.smoke
    def test_search_by_audit_result_and_status(self):
        """同时筛选审核结果和申请状态，验证两个条件同时生效"""
        data = audit_data.get("search_audit_result_and_status")
        logger.step(f"执行搜索: {data['description']}")

        self._audit_page.select_audit_result_filter(data["audit_result"])
        self._audit_page.select_apply_status_filter(data["apply_status"])
        self._audit_page.click_search()

        count = self._audit_page.get_table_row_count()
        assert count > 0, "组合筛选结果不应为空"
        for i in range(count):
            result_cell = self._audit_page.get_cell_text_by_header(i, "审核结果")
            status_cell = self._audit_page.get_cell_text_by_header(i, "申请状态")
            assert result_cell == data["audit_result"], f"第{i + 1}行审核结果应为{data['audit_result']}"
            assert status_cell == data["apply_status"], f"第{i + 1}行申请状态应为{data['apply_status']}"
        logger.success(f"{data['description']}验证通过，共{count}条")

    # -------- 重置 --------

    @allure.title("重置按钮清空筛选条件")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_reset_clears_filters(self):
        """设置筛选条件后点击重置，验证条件被清空且恢复全部数据"""
        logger.step("设置筛选条件后点击重置")

        self._audit_page.select_audit_result_filter("已拒绝")
        self._audit_page.click_search()
        filtered_count = self._audit_page.get_table_row_count()

        self._audit_page.click_reset()
        reset_count = self._audit_page.get_table_row_count()

        assert reset_count >= filtered_count, f"重置后数据量({reset_count})应不少于筛选后数据量({filtered_count})"
        logger.success("重置按钮验证通过")


@allure.feature("审核记录")
@allure.story("查看详情")
class TestAuditRecordsView(BaseTest):
    """审核记录查看详情测试用例"""

    @pytest.fixture(autouse=True)
    def _setup_view(self, logged_in_page, request):
        """注入审核记录页面对象，导航到审核记录页面"""
        self._audit_page = AuditRecordsPage(logged_in_page)
        self.page = logged_in_page
        self.base_page = self._audit_page
        self.logger = Logger.get("opms")
        self._test_name = request.node.name
        self._audit_page.navigate_to_audit_records()
        self._audit_page.wait_for_load_state("domcontentloaded")

    @allure.title("查看审核记录详情")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.web
    @pytest.mark.smoke
    def test_view_audit_record_detail(self):
        """点击查看按钮，验证新标签页打开采购申请详情"""
        logger.step("点击第一行的查看按钮")

        count = self._audit_page.get_table_row_count()
        assert count > 0, "表格应有数据"

        with self.page.context.expect_page() as new_page_info:
            self._audit_page.click_view_button(0)
        detail_page = new_page_info.value
        detail_page.wait_for_load_state("domcontentloaded")

        assert detail_page.url, "详情页URL不应为空"
        logger.success(f"查看审核记录详情验证通过，详情页: {detail_page.url}")
        detail_page.close()


@allure.feature("审核记录")
@allure.story("申请页跳转")
class TestAuditRecordsApplicationPage(BaseTest):
    """审核记录申请页跳转测试用例"""

    @pytest.fixture(autouse=True)
    def _setup_app_page(self, logged_in_page, request):
        """注入审核记录页面对象，导航到审核记录页面"""
        self._audit_page = AuditRecordsPage(logged_in_page)
        self.page = logged_in_page
        self.base_page = self._audit_page
        self.logger = Logger.get("opms")
        self._test_name = request.node.name
        self._audit_page.navigate_to_audit_records()
        self._audit_page.wait_for_load_state("domcontentloaded")

    @allure.title("从审核记录跳转到申请页")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_navigate_to_application_page(self):
        """点击申请页按钮，验证跳转到对应采购申请详情页"""
        logger.step("点击第一行的申请页按钮")

        count = self._audit_page.get_table_row_count()
        assert count > 0, "表格应有数据"

        with self.page.context.expect_page() as new_page_info:
            self._audit_page.click_application_page_button(0)
        app_page = new_page_info.value
        app_page.wait_for_load_state("domcontentloaded")

        assert app_page.url, "申请页URL不应为空"
        logger.success(f"跳转申请页验证通过，目标页: {app_page.url}")
        app_page.close()


@allure.feature("审核记录")
@allure.story("删除记录")
class TestAuditRecordsDelete(BaseTest):
    """审核记录删除测试用例"""

    @pytest.fixture(autouse=True)
    def _setup_delete(self, logged_in_page, request):
        """注入审核记录页面对象，导航到审核记录页面"""
        self._audit_page = AuditRecordsPage(logged_in_page)
        self.page = logged_in_page
        self.base_page = self._audit_page
        self.logger = Logger.get("opms")
        self._test_name = request.node.name
        self._audit_page.navigate_to_audit_records()
        self._audit_page.wait_for_load_state("domcontentloaded")

    @allure.title("删除审核记录-取消操作")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_delete_audit_record_cancel(self):
        """点击删除后取消，验证数据未被删除"""
        logger.step("删除审核记录-点击取消")

        original_count = self._audit_page.get_table_row_count()
        assert original_count > 0, "表格应有数据"

        self._audit_page.click_delete_button(0)
        self._audit_page.cancel_delete()

        current_count = self._audit_page.get_table_row_count()
        assert current_count == original_count, f"取消删除后行数不应变化，原: {original_count}，现: {current_count}"

        logger.success("取消删除审核记录验证通过")
