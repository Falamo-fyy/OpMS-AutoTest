import os
import allure
import pytest

from base.base_test import BaseTest
from page.purchase_request_page import PurchaseRequestPage
from utils.logger import Logger
from utils.config_reader import ConfigReader

logger = Logger.get("opms")

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "test_purchase_request_search_data.yaml")
search_data = ConfigReader(DATA_PATH)


@allure.feature("采购申请")
@allure.story("搜索筛选")
class TestPurchaseRequestSearch(BaseTest):
    """采购申请页面搜索筛选测试用例"""

    @pytest.fixture(autouse=True)
    def _setup_search(self, logged_in_page, request):
        """注入采购申请页面对象，导航到采购申请页面（共享已登录状态）"""
        self._purchase_page = PurchaseRequestPage(logged_in_page)
        self.page = logged_in_page
        self.base_page = self._purchase_page
        self.logger = Logger.get("opms")
        self._test_name = request.node.name
        self._purchase_page.navigate_to_purchase_request()
        self._purchase_page.wait_for_load_state("domcontentloaded")

    # -------- 单条件筛选 --------

    @allure.title("按紧急程度筛选-普通")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_urgency_normal(self):
        """筛选紧急程度为"普通"，验证所有结果紧急程度均为普通"""
        data = search_data.get("search_urgency_normal")
        logger.step(f"执行搜索: {data['description']}")

        self._purchase_page.select_urgency_filter(data["urgency"])
        self._purchase_page.click_search()

        count = self._purchase_page.get_table_row_count()
        assert count > 0, "筛选结果不应为空"
        for i in range(count):
            cell = self._purchase_page.get_cell_text(i, 2)
            assert cell == data["urgency"], f"第{i + 1}行紧急程度应为{data['urgency']}，实际为{cell}"
        logger.success(f"{data['description']}验证通过，共{count}条")

    @allure.title("按紧急程度筛选-紧急")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_urgency_urgent(self):
        """筛选紧急程度为"紧急"，验证所有结果紧急程度均为紧急"""
        data = search_data.get("search_urgency_urgent")
        logger.step(f"执行搜索: {data['description']}")

        self._purchase_page.select_urgency_filter(data["urgency"])
        self._purchase_page.click_search()

        count = self._purchase_page.get_table_row_count()
        assert count > 0, "筛选结果不应为空"
        for i in range(count):
            cell = self._purchase_page.get_cell_text(i, 2)
            assert cell == data["urgency"], f"第{i + 1}行紧急程度应为{data['urgency']}，实际为{cell}"
        logger.success(f"{data['description']}验证通过，共{count}条")

    @allure.title("按紧急程度筛选-非常紧急")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_urgency_very_urgent(self):
        """筛选紧急程度为"非常紧急"，验证所有结果紧急程度均为非常紧急"""
        data = search_data.get("search_urgency_very_urgent")
        logger.step(f"执行搜索: {data['description']}")

        self._purchase_page.select_urgency_filter(data["urgency"])
        self._purchase_page.click_search()

        count = self._purchase_page.get_table_row_count()
        assert count > 0, "筛选结果不应为空"
        for i in range(count):
            cell = self._purchase_page.get_cell_text(i, 2)
            assert cell == data["urgency"], f"第{i + 1}行紧急程度应为{data['urgency']}，实际为{cell}"
        logger.success(f"{data['description']}验证通过，共{count}条")

    @allure.title("按审核状态筛选-已提交")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_status_submitted(self):
        """筛选审核状态为"已提交"，验证所有结果审核状态均为已提交"""
        data = search_data.get("search_status_submitted")
        logger.step(f"执行搜索: {data['description']}")

        self._purchase_page.select_status_filter(data["status"])
        self._purchase_page.click_search()

        count = self._purchase_page.get_table_row_count()
        assert count > 0, "筛选结果不应为空"
        for i in range(count):
            cell = self._purchase_page.get_cell_text(i, 3)
            assert cell == data["status"], f"第{i + 1}行审核状态应为{data['status']}，实际为{cell}"
        logger.success(f"{data['description']}验证通过，共{count}条")

    @allure.title("按审核状态筛选-已拒绝")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_status_rejected(self):
        """筛选审核状态为"已拒绝"，验证所有结果审核状态均为已拒绝"""
        data = search_data.get("search_status_rejected")
        logger.step(f"执行搜索: {data['description']}")

        self._purchase_page.select_status_filter(data["status"])
        self._purchase_page.click_search()

        count = self._purchase_page.get_table_row_count()
        assert count > 0, "筛选结果不应为空"
        for i in range(count):
            cell = self._purchase_page.get_cell_text(i, 3)
            assert cell == data["status"], f"第{i + 1}行审核状态应为{data['status']}，实际为{cell}"
        logger.success(f"{data['description']}验证通过，共{count}条")

    @allure.title("按使用科室筛选")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_department(self):
        """筛选使用科室，验证所有结果科室匹配"""
        data = search_data.get("search_department")
        logger.step(f"执行搜索: {data['description']}")

        self._purchase_page.select_department_filter(data["department"])
        self._purchase_page.click_search()

        count = self._purchase_page.get_table_row_count()
        assert count > 0, "筛选结果不应为空"
        for i in range(count):
            cell = self._purchase_page.get_cell_text(i, 5)
            assert cell == data["department"], f"第{i + 1}行使用科室应为{data['department']}，实际为{cell}"
        logger.success(f"{data['description']}验证通过，共{count}条")

    # -------- 文本搜索 --------

    @allure.title("按申请编号精确搜索")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.web
    @pytest.mark.smoke
    def test_search_by_request_no_exact(self):
        """输入完整申请编号搜索，验证精确匹配"""
        data = search_data.get("search_by_request_no")
        logger.step(f"执行搜索: {data['description']}")

        self._purchase_page.search_by_request_no(data["request_no"])

        count = self._purchase_page.get_table_row_count()
        assert count >= 1, "精确搜索应至少返回1条结果"
        cell = self._purchase_page.get_cell_text(0, 1)
        assert cell == data["request_no"], f"申请编号应为{data['request_no']}，实际为{cell}"
        logger.success(f"{data['description']}验证通过")

    @allure.title("按申请编号模糊搜索")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_request_no_partial(self):
        """输入部分申请编号搜索，验证模糊匹配"""
        data = search_data.get("search_by_request_no_partial")
        logger.step(f"执行搜索: {data['description']}")

        self._purchase_page.search_by_request_no(data["request_no"])

        count = self._purchase_page.get_table_row_count()
        assert count >= 1, "模糊搜索应至少返回1条结果"
        for i in range(count):
            cell = self._purchase_page.get_cell_text(i, 1)
            assert data["request_no"] in cell, f"第{i + 1}行申请编号应包含{data['request_no']}，实际为{cell}"
        logger.success(f"{data['description']}验证通过，共{count}条")

    @allure.title("按项目名称模糊搜索")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_project_name(self):
        """输入项目名称关键词搜索，验证模糊匹配"""
        data = search_data.get("search_by_project_name")
        logger.step(f"执行搜索: {data['description']}")

        self._purchase_page.search_by_project_name(data["project_name"])

        count = self._purchase_page.get_table_row_count()
        assert count >= 1, "项目名称搜索应至少返回1条结果"
        for i in range(count):
            cell = self._purchase_page.get_cell_text(i, 4)
            assert data["project_name"] in cell, f"第{i + 1}行项目名称应包含{data['project_name']}，实际为{cell}"
        logger.success(f"{data['description']}验证通过，共{count}条")

    @allure.title("按申请人搜索")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_applicant(self):
        """输入申请人搜索，验证匹配"""
        data = search_data.get("search_by_applicant")
        logger.step(f"执行搜索: {data['description']}")

        self._purchase_page.search_by_applicant(data["applicant"])

        count = self._purchase_page.get_table_row_count()
        assert count >= 1, "申请人搜索应至少返回1条结果"
        for i in range(count):
            cell = self._purchase_page.get_cell_text(i, 7)
            assert data["applicant"] in cell, f"第{i + 1}行申请人应包含{data['applicant']}，实际为{cell}"
        logger.success(f"{data['description']}验证通过，共{count}条")

    # -------- 组合筛选 --------

    @allure.title("紧急程度+审核状态组合筛选")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.web
    @pytest.mark.smoke
    def test_search_by_urgency_and_status(self):
        """同时筛选紧急程度和审核状态，验证两个条件同时生效"""
        data = search_data.get("search_urgency_and_status")
        logger.step(f"执行搜索: {data['description']}")

        self._purchase_page.select_urgency_filter(data["urgency"])
        self._purchase_page.select_status_filter(data["status"])
        self._purchase_page.click_search()

        count = self._purchase_page.get_table_row_count()
        assert count > 0, "组合筛选结果不应为空"
        for i in range(count):
            urgency_cell = self._purchase_page.get_cell_text(i, 2)
            status_cell = self._purchase_page.get_cell_text(i, 3)
            assert urgency_cell == data["urgency"], f"第{i + 1}行紧急程度应为{data['urgency']}"
            assert status_cell == data["status"], f"第{i + 1}行审核状态应为{data['status']}"
        logger.success(f"{data['description']}验证通过，共{count}条")

    @allure.title("使用科室+审核状态组合筛选")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_department_and_status(self):
        """同时筛选使用科室和审核状态，验证两个条件同时生效"""
        data = search_data.get("search_department_and_status")
        logger.step(f"执行搜索: {data['description']}")

        self._purchase_page.select_department_filter(data["department"])
        self._purchase_page.select_status_filter(data["status"])
        self._purchase_page.click_search()

        count = self._purchase_page.get_table_row_count()
        assert count > 0, "组合筛选结果不应为空"
        for i in range(count):
            dept_cell = self._purchase_page.get_cell_text(i, 5)
            status_cell = self._purchase_page.get_cell_text(i, 3)
            assert dept_cell == data["department"], f"第{i + 1}行科室应为{data['department']}"
            assert status_cell == data["status"], f"第{i + 1}行审核状态应为{data['status']}"
        logger.success(f"{data['description']}验证通过，共{count}条")

    # -------- 重置 --------

    @allure.title("重置按钮清空筛选条件")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_reset_clears_filters(self):
        """设置筛选条件后点击重置，验证条件被清空且恢复全部数据"""
        logger.step("设置筛选条件后点击重置")

        self._purchase_page.select_urgency_filter("紧急")
        self._purchase_page.click_search()
        filtered_count = self._purchase_page.get_table_row_count()

        self._purchase_page.click_reset()
        reset_count = self._purchase_page.get_table_row_count()

        assert reset_count >= filtered_count, f"重置后数据量({reset_count})应不少于筛选后数据量({filtered_count})"
        logger.success("重置按钮验证通过")
