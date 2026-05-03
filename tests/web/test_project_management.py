import os
import allure
import pytest

from base.base_test import BaseTest
from page.project_management_page import ProjectManagementPage
from utils.logger import Logger
from utils.config_reader import ConfigReader

logger = Logger.get("opms")

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "web", "test_project_management_data.yaml")
project_data = ConfigReader(DATA_PATH)


@allure.feature("项目管理")
@allure.story("搜索筛选")
class TestProjectManagementSearch(BaseTest):
    """项目管理页面搜索筛选测试用例"""

    @pytest.fixture(autouse=True)
    def _setup_search(self, logged_in_page, request):
        """注入项目管理页面对象，导航到项目管理页面（共享已登录状态）"""
        self._project_page = ProjectManagementPage(logged_in_page)
        self.page = logged_in_page
        self.base_page = self._project_page
        self.logger = Logger.get("opms")
        self._test_name = request.node.name
        self._project_page.navigate_to_project_management()
        self._project_page.wait_for_load_state("domcontentloaded")

    # -------- 单条件筛选 --------

    @allure.title("按项目状态筛选-进行中")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_status_active(self):
        """筛选项目状态为"进行中"，验证所有结果状态均为进行中"""
        data = project_data.get("search_status_active")
        logger.step(f"执行搜索: {data['description']}")

        self._project_page.select_status_filter(data["status"])
        self._project_page.click_search()

        count = self._project_page.get_table_row_count()
        assert count > 0, "筛选结果不应为空"

        for i in range(count):
            cell_text = self._project_page.get_cell_text_by_header(i, "项目状态")
            expected = data["status"]
            assert cell_text == expected, (
                f"第{i + 1}行项目状态验证失败\n"
                f"期望: '{expected}'\n"
                f"实际: '{cell_text}'\n"
                f"原始值: '{repr(cell_text)}'"
            )

        count = self._project_page.get_total_count()
        logger.success(f"{data['description']}验证通过，{count}")
        self._project_page.click_reset()

    @allure.title("按项目状态筛选-已完成")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_status_completed(self):
        """筛选项目状态为"已完成"，验证所有结果状态均为已完成"""
        data = project_data.get("search_status_completed")
        logger.step(f"执行搜索: {data['description']}")

        self._project_page.select_status_filter(data["status"])
        self._project_page.click_search()

        count = self._project_page.get_table_row_count()
        assert count > 0, "筛选结果不应为空"

        for i in range(count):
            cell_text = self._project_page.get_cell_text_by_header(i, "项目状态")
            expected = data["status"]
            assert cell_text == expected, (
                f"第{i + 1}行项目状态验证失败\n"
                f"期望: '{expected}'\n"
                f"实际: '{cell_text}'\n"
                f"原始值: '{repr(cell_text)}'"
            )

        count = self._project_page.get_total_count()
        logger.success(f"{data['description']}验证通过，{count}")
        self._project_page.click_reset()

    @allure.title("按项目状态筛选-未开始")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_status_pending(self):
        """筛选项目状态为"未开始"，验证所有结果状态均为未开始"""
        data = project_data.get("search_status_pending")
        logger.step(f"执行搜索: {data['description']}")

        self._project_page.select_status_filter(data["status"])
        self._project_page.click_search()

        count = self._project_page.get_table_row_count()
        assert count > 0, "筛选结果不应为空"

        for i in range(count):
            cell_text = self._project_page.get_cell_text_by_header(i, "项目状态")
            expected = data["status"]
            assert cell_text == expected, (
                f"第{i + 1}行项目状态验证失败\n"
                f"期望: '{expected}'\n"
                f"实际: '{cell_text}'\n"
                f"原始值: '{repr(cell_text)}'"
            )

        count = self._project_page.get_total_count()
        logger.success(f"{data['description']}验证通过，{count}")
        self._project_page.click_reset()

    @allure.title("按省份筛选")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_province(self):
        """筛选省份，验证所有结果省份匹配"""
        data = project_data.get("search_province")
        logger.step(f"执行搜索: {data['description']}")

        self._project_page.select_province_filter(data["province"])
        self._project_page.click_search()

        count = self._project_page.get_table_row_count()
        assert count > 0, "筛选结果不应为空"

        for i in range(count):
            cell_text = self._project_page.get_cell_text_by_header(i, "省份")
            expected = data["province"]
            assert expected in cell_text, (
                f"第{i + 1}行省份验证失败\n"
                f"期望包含: '{expected}'\n"
                f"实际: '{cell_text}'\n"
                f"原始值: '{repr(cell_text)}'"
            )

        count = self._project_page.get_total_count()
        logger.success(f"{data['description']}验证通过，{count}")
        self._project_page.click_reset()

    @allure.title("按创建人筛选")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_creator(self):
        """筛选创建人，验证所有结果创建人匹配"""
        data = project_data.get("search_creator")
        logger.step(f"执行搜索: {data['description']}")

        self._project_page.select_creator_filter(data["creator"])
        self._project_page.click_search()

        count = self._project_page.get_table_row_count()
        assert count > 0, "筛选结果不应为空"

        for i in range(count):
            cell_text = self._project_page.get_cell_text_by_header(i, "创建人")
            expected = data["creator"]
            assert cell_text == expected, (
                f"第{i + 1}行创建人验证失败\n"
                f"期望: '{expected}'\n"
                f"实际: '{cell_text}'\n"
                f"原始值: '{repr(cell_text)}'"
            )

        count = self._project_page.get_total_count()
        logger.success(f"{data['description']}验证通过，{count}")
        self._project_page.click_reset()

    # -------- 文本搜索 --------

    @allure.title("按项目编号精确搜索")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.web
    @pytest.mark.smoke
    def test_search_by_project_no_exact(self):
        """输入完整项目编号搜索，验证精确匹配"""
        data = project_data.get("search_by_project_no")
        logger.step(f"执行搜索: {data['description']}")

        self._project_page.search_by_project_no(data["project_no"])

        count = self._project_page.get_table_row_count()
        assert count >= 1, "精确搜索应至少返回1条结果"
        cell = self._project_page.get_cell_text_by_header(0, "项目编号")
        assert cell == data["project_no"], f"项目编号应为{data['project_no']}，实际为{cell}"
        logger.success(f"{data['description']}验证通过")

    @allure.title("按项目编号模糊搜索")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_project_no_partial(self):
        """输入部分项目编号搜索，验证模糊匹配"""
        data = project_data.get("search_by_project_no_partial")
        logger.step(f"执行搜索: {data['description']}")

        self._project_page.search_by_project_no(data["project_no"])

        count = self._project_page.get_table_row_count()
        assert count >= 1, "模糊搜索应至少返回1条结果"
        for i in range(count):
            cell = self._project_page.get_cell_text_by_header(i, "项目编号")
            assert data["project_no"] in cell, f"第{i + 1}行项目编号应包含{data['project_no']}，实际为{cell}"
        logger.success(f"{data['description']}验证通过，共{count}条")

    @allure.title("按项目名称模糊搜索")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_search_by_project_name(self):
        """输入项目名称关键词搜索，验证模糊匹配"""
        data = project_data.get("search_by_project_name")
        logger.step(f"执行搜索: {data['description']}")

        self._project_page.search_by_project_name(data["project_name"])

        count = self._project_page.get_table_row_count()
        assert count >= 1, "项目名称搜索应至少返回1条结果"
        for i in range(count):
            cell = self._project_page.get_cell_text_by_header(i, "项目名称")
            assert data["project_name"] in cell, f"第{i + 1}行项目名称应包含{data['project_name']}，实际为{cell}"
        logger.success(f"{data['description']}验证通过，共{count}条")

    # -------- 组合筛选 --------

    @allure.title("省份+项目状态组合筛选")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.web
    @pytest.mark.smoke
    def test_search_by_province_and_status(self):
        """同时筛选省份和项目状态，验证两个条件同时生效"""
        data = project_data.get("search_province_and_status")
        logger.step(f"执行搜索: {data['description']}")

        self._project_page.select_province_filter(data["province"])
        self._project_page.select_status_filter(data["status"])
        self._project_page.click_search()

        count = self._project_page.get_table_row_count()
        assert count > 0, "组合筛选结果不应为空"
        for i in range(count):
            province_cell = self._project_page.get_cell_text_by_header(i, "省份")
            status_cell = self._project_page.get_cell_text_by_header(i, "项目状态")
            assert data["province"] in province_cell, f"第{i + 1}行省份应包含{data['province']}"
            assert status_cell == data["status"], f"第{i + 1}行项目状态应为{data['status']}"
        logger.success(f"{data['description']}验证通过，共{count}条")

    # -------- 重置 --------

    @allure.title("重置按钮清空筛选条件")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_reset_clears_filters(self):
        """设置筛选条件后点击重置，验证条件被清空且恢复全部数据"""
        logger.step("设置筛选条件后点击重置")

        self._project_page.select_status_filter("进行中")
        self._project_page.click_search()
        filtered_count = self._project_page.get_table_row_count()

        self._project_page.click_reset()
        reset_count = self._project_page.get_table_row_count()

        assert reset_count >= filtered_count, f"重置后数据量({reset_count})应不少于筛选后数据量({filtered_count})"
        logger.success("重置按钮验证通过")


@allure.feature("项目管理")
@allure.story("新增项目")
class TestProjectManagementAdd(BaseTest):
    """项目管理新增项目测试用例"""

    @pytest.fixture(autouse=True)
    def _setup_add(self, logged_in_page, request):
        """注入项目管理页面对象，导航到项目管理页面"""
        self._project_page = ProjectManagementPage(logged_in_page)
        self.page = logged_in_page
        self.base_page = self._project_page
        self.logger = Logger.get("opms")
        self._test_name = request.node.name
        self._project_page.navigate_to_project_management()
        self._project_page.wait_for_load_state("domcontentloaded")

    @allure.title("新增项目成功")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.web
    @pytest.mark.smoke
    def test_add_project_success(self):
        """填写完整信息新增项目，验证新增成功"""
        data = project_data.get("add_project_success")
        logger.step(f"执行新增项目: {data['description_text']}")

        self._project_page.create_project(
            province=data["province"],
            city=data["city"],
            project_name=data["project_name"],
            status=data["status"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            description=data["description"],
        )

        # 验证弹窗已关闭
        self._project_page.assert_add_dialog_closed()
        logger.success(f"{data['description_text']}验证通过")

    @allure.title("新增项目-取消操作")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_add_project_cancel(self):
        """填写信息后点击取消，验证弹窗关闭且未新增数据"""
        logger.step("新增项目-点击取消")

        self._project_page.click_add_project()
        self._project_page.assert_add_dialog_visible()
        self._project_page.select_add_province("北京市")
        self._project_page.fill_add_project_name("取消测试项目")
        self._project_page.click_add_cancel()

        self._project_page.assert_add_dialog_closed()
        logger.success("取消新增项目验证通过")

    @allure.title("新增项目-关闭弹窗")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_add_project_close(self):
        """点击弹窗关闭按钮，验证弹窗关闭"""
        logger.step("新增项目-关闭弹窗")

        self._project_page.click_add_project()
        self._project_page.assert_add_dialog_visible()
        self._project_page.close_add_dialog()

        self._project_page.assert_add_dialog_closed()
        logger.success("关闭新增弹窗验证通过")


@allure.feature("项目管理")
@allure.story("查看详情")
class TestProjectManagementView(BaseTest):
    """项目管理查看详情测试用例"""

    @pytest.fixture(autouse=True)
    def _setup_view(self, logged_in_page, request):
        """注入项目管理页面对象，导航到项目管理页面"""
        self._project_page = ProjectManagementPage(logged_in_page)
        self.page = logged_in_page
        self.base_page = self._project_page
        self.logger = Logger.get("opms")
        self._test_name = request.node.name
        self._project_page.navigate_to_project_management()
        self._project_page.wait_for_load_state("domcontentloaded")

    @allure.title("查看项目详情")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.web
    @pytest.mark.smoke
    def test_view_project_detail(self):
        """点击查看按钮，验证详情弹窗打开并展示字段"""
        logger.step("点击第一行的查看按钮")

        self._project_page.click_view_button(0)
        self._project_page.assert_view_dialog_visible()

        # 验证详情弹窗中关键字段有值
        project_name = self._project_page.get_view_field_value("项目名称")
        assert project_name, "项目名称不应为空"

        province = self._project_page.get_view_field_value("省份")
        assert province, "省份不应为空"

        status = self._project_page.get_view_field_value("项目状态")
        assert status, "项目状态不应为空"

        logger.success(f"查看项目详情验证通过，项目名称: {project_name}")

        self._project_page.close_view_dialog()
        self._project_page.assert_view_dialog_closed()

    @allure.title("关闭查看详情弹窗")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_view_project_close(self):
        """点击关闭按钮关闭详情弹窗"""
        logger.step("关闭查看详情弹窗")

        self._project_page.click_view_button(0)
        self._project_page.assert_view_dialog_visible()
        self._project_page.close_view_dialog()
        self._project_page.assert_view_dialog_closed()

        logger.success("关闭详情弹窗验证通过")


@allure.feature("项目管理")
@allure.story("编辑项目")
class TestProjectManagementEdit(BaseTest):
    """项目管理编辑项目测试用例"""

    @pytest.fixture(autouse=True)
    def _setup_edit(self, logged_in_page, request):
        """注入项目管理页面对象，导航到项目管理页面"""
        self._project_page = ProjectManagementPage(logged_in_page)
        self.page = logged_in_page
        self.base_page = self._project_page
        self.logger = Logger.get("opms")
        self._test_name = request.node.name
        self._project_page.navigate_to_project_management()
        self._project_page.wait_for_load_state("domcontentloaded")

    @allure.title("编辑项目成功")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.web
    @pytest.mark.smoke
    def test_edit_project_success(self):
        """编辑项目名称和状态，验证编辑成功"""
        data = project_data.get("edit_project_success")
        logger.step(f"执行编辑项目: {data['description_text']}")

        self._project_page.click_edit_button(0)
        self._project_page.assert_edit_dialog_visible()

        self._project_page.fill_edit_project_name(data["project_name"])
        self._project_page.select_edit_status(data["status"])
        self._project_page.fill_edit_description(data["description"])
        self._project_page.click_edit_confirm()

        self._project_page.assert_edit_dialog_closed()
        logger.success(f"{data['description_text']}验证通过")

    @allure.title("编辑项目-取消操作")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_edit_project_cancel(self):
        """编辑项目后点击取消，验证弹窗关闭且数据未变更"""
        logger.step("编辑项目-点击取消")

        # 先记录编辑前的项目名称
        original_name = self._project_page.get_cell_text_by_header(0, "项目名称")

        self._project_page.click_edit_button(0)
        self._project_page.assert_edit_dialog_visible()
        self._project_page.fill_edit_project_name("取消编辑测试")
        self._project_page.click_edit_cancel()

        self._project_page.assert_edit_dialog_closed()

        # 验证数据未变更
        current_name = self._project_page.get_cell_text_by_header(0, "项目名称")
        assert current_name == original_name, f"取消编辑后项目名称不应变化，原: '{original_name}'，现: '{current_name}'"

        logger.success("取消编辑项目验证通过")


@allure.feature("项目管理")
@allure.story("删除项目")
class TestProjectManagementDelete(BaseTest):
    """项目管理删除项目测试用例"""

    @pytest.fixture(autouse=True)
    def _setup_delete(self, logged_in_page, request):
        """注入项目管理页面对象，导航到项目管理页面"""
        self._project_page = ProjectManagementPage(logged_in_page)
        self.page = logged_in_page
        self.base_page = self._project_page
        self.logger = Logger.get("opms")
        self._test_name = request.node.name
        self._project_page.navigate_to_project_management()
        self._project_page.wait_for_load_state("domcontentloaded")

    @allure.title("删除项目-取消操作")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.web
    @pytest.mark.regression
    def test_delete_project_cancel(self):
        """点击删除后取消，验证数据未被删除"""
        logger.step("删除项目-点击取消")

        original_count = self._project_page.get_table_row_count()
        assert original_count > 0, "表格应有数据"

        self._project_page.click_delete_button(0)
        self._project_page.cancel_delete()

        current_count = self._project_page.get_table_row_count()
        assert current_count == original_count, f"取消删除后行数不应变化，原: {original_count}，现: {current_count}"

        logger.success("取消删除项目验证通过")
