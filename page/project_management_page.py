from playwright.sync_api import expect

from base.base_page import BasePage


class ProjectManagementPage(BasePage):
    """项目管理页面对象，封装项目管理列表、新增/编辑/查看/删除的元素定位与操作方法"""

    # -------- 页面路由 --------
    PAGE_URL = "/#/link/project-management"

    # -------- 列表页 - 搜索区域 --------
    SEARCH_PROJECT_NO = "input[placeholder='请输入项目编号']"
    SEARCH_PROJECT_NAME = "input[placeholder='请输入项目名称']"
    SEARCH_BTN = "button:has-text('查询')"
    RESET_BTN = "button:has-text('重置')"


    # -------- 列表页 - 操作按钮 --------
    ADD_BTN = "button:has-text('新增项目')"
    BATCH_DELETE_BTN = "button:has-text('批量删除')"
    EXPORT_BTN = "button:has-text('导出Excel')"

    # -------- 列表页 - 表格 --------
    TABLE_ROW = ".el-table__body-wrapper .el-table__row"
    CHECKBOX_ALL = ".el-table__header .el-checkbox"

    # -------- 新增/编辑弹窗 --------
    ADD_DIALOG = "[aria-label='新增项目']"
    EDIT_DIALOG = "[aria-label='编辑项目']"
    DIALOG_CLOSE = ".el-dialog__headerbtn"

    # 新增弹窗 - 表单输入框
    FORM_PROJECT_NAME = "input[placeholder='请输入项目名称']"
    FORM_DESCRIPTION = "textarea[placeholder='请输入项目描述']"

    # 弹窗底部按钮
    CANCEL_BTN = "button:has-text('取消')"
    CONFIRM_BTN = "button:has-text('确定')"

    # -------- 查看详情弹窗 --------
    VIEW_DIALOG = "[aria-label='项目详情']"

    # -------- 内部辅助方法 --------

    def _search_select_by_label(self, label: str):
        """根据标签文本在搜索区域定位对应的 el-select 下拉框"""
        return self.page.locator(".search-form .el-col").filter(has_text=label).locator(".el-select")

    def _dialog_select_by_label(self, label: str, dialog_aria_label: str = "新增项目"):
        """根据标签文本在弹窗表单中定位对应的 el-select 下拉框"""
        return self.page.get_by_role("dialog", name=dialog_aria_label).locator(".el-form-item").filter(has_text=label).locator(".el-select")

    def _dialog_date_by_label(self, label: str, dialog_aria_label: str = "新增项目"):
        """根据标签文本在弹窗表单中定位对应的日期选择器"""
        return self.page.get_by_role("dialog", name=dialog_aria_label).locator(".el-form-item").filter(has_text=label).locator("input")

    def _body_table(self):
        """获取表格主体区域"""
        return self.page.locator(".el-table__body-wrapper").get_by_role("table")

    def _header_table(self):
        """获取表格表头区域"""
        return self.page.locator(".el-table__header-wrapper").get_by_role("table")

    # -------- 导航 --------

    def navigate_to_project_management(self):
        """导航到项目管理页面"""
        self.goto(self.PAGE_URL)

    def navigate_via_menu(self):
        """通过左侧菜单导航：信息管理 -> 项目管理"""
        self.page.get_by_role("menuitem", name="信息管理").click()
        self.page.get_by_role("menuitem", name="项目管理").click()
        self.wait_for_load_state("domcontentloaded")

    # -------- 列表页 - 搜索操作 --------

    def search_by_project_no(self, project_no: str):
        """按项目编号搜索"""
        self.fill(self.SEARCH_PROJECT_NO, project_no)
        self.click(self.SEARCH_BTN)

    def search_by_project_name(self, project_name: str):
        """按项目名称搜索"""
        self.fill(self.SEARCH_PROJECT_NAME, project_name)
        self.click(self.SEARCH_BTN)

    def _wait_loading_gone(self):
        """等待页面 loading 遮罩消失"""
        loading = self.page.locator(".el-loading-mask")
        if loading.count() > 0:
            loading.last.wait_for(state="hidden", timeout=10000)

    def select_province_filter(self, province: str):
        """选择省份筛选"""
        self._wait_loading_gone()
        self._search_select_by_label("省份").click()
        self.page.get_by_role("option", name=province, exact=True).click()

    def select_city_filter(self, city: str):
        """选择市县筛选（需先选择省份）"""
        self._wait_loading_gone()
        self._search_select_by_label("市县").click()
        self.page.get_by_role("option", name=city, exact=True).click()

    def select_creator_filter(self, creator: str):
        """选择创建人筛选"""
        self._wait_loading_gone()
        self._search_select_by_label("创建人").click()
        self.page.get_by_role("option", name=creator, exact=True).click()

    def select_status_filter(self, status: str):
        """选择项目状态筛选"""
        self._wait_loading_gone()
        self._search_select_by_label("项目状态").click()
        self.page.get_by_role("option", name=status, exact=True).click()

    def fill_start_date_filter(self, date: str):
        """填写搜索区域开始时间"""
        self.page.get_by_placeholder("选择开始日期").fill(date)
        self.page.keyboard.press("Enter")

    def fill_end_date_filter(self, date: str):
        """填写搜索区域结束时间"""
        self.page.get_by_placeholder("选择结束日期").fill(date)
        self.page.keyboard.press("Enter")

    def click_search(self):
        """点击查询按钮"""
        self.click(self.SEARCH_BTN)
        self.wait_for_load_state("networkidle")

    def click_reset(self):
        """点击重置按钮"""
        self.click(self.RESET_BTN)

    # -------- 列表页 - 表格操作 --------

    def get_table_row_count(self) -> int:
        """获取当前页面表格行数"""
        return self._body_table().get_by_role("row").count()

    def get_cell_text(self, row: int, col: int) -> str:
        """获取表格指定行列的文本内容

        Args:
            row: 行索引，从0开始
            col: 列索引，从0开始（含复选框列）
        """
        return self._body_table().get_by_role("row").nth(row).get_by_role("cell").nth(col).inner_text()

    def get_cell_text_by_header(self, row: int, header: str) -> str:
        """根据列标题获取表格指定行的单元格文本"""
        headers = self._header_table().locator("th .cell")
        header_count = headers.count()

        col_index = -1
        for i in range(header_count):
            header_text = headers.nth(i).inner_text().strip()
            if header == header_text or header in header_text:
                col_index = i
                break

        if col_index == -1:
            raise ValueError(
                f"未找到列标题: '{header}'，可用标题: {[headers.nth(i).inner_text().strip() for i in range(header_count)]}")

        target_row = self._body_table().locator("tbody tr").nth(row)
        expect(target_row).to_be_visible(timeout=5000)

        target_cell = target_row.locator("td").nth(col_index)
        expect(target_cell).not_to_have_text("", timeout=5000)

        return target_cell.inner_text().strip()

    def click_row_checkbox(self, row: int):
        """勾选指定行的复选框"""
        self._body_table().get_by_role("row").nth(row).get_by_role("checkbox").click()

    def click_select_all_checkbox(self):
        """点击表头全选复选框"""
        self.page.locator(self.CHECKBOX_ALL).click()

    def click_view_button(self, row: int):
        """点击指定行的查看按钮"""
        self._body_table().get_by_role("row").nth(row).get_by_role("button", name="查看").click()

    def click_edit_button(self, row: int):
        """点击指定行的编辑按钮"""
        self._body_table().get_by_role("row").nth(row).get_by_role("button", name="编辑").click()

    def click_delete_button(self, row: int):
        """点击指定行的删除按钮"""
        self._body_table().get_by_role("row").nth(row).get_by_role("button", name="删除").click()

    # -------- 列表页 - 分页操作 --------

    def click_next_page(self):
        """点击下一页"""
        self.page.get_by_role("button", name="下一页").click()

    def click_prev_page(self):
        """点击上一页"""
        self.page.get_by_role("button", name="上一页").click()

    def click_page_number(self, page_num: int):
        """点击指定页码"""
        self.page.get_by_role("listitem", name=f"第 {page_num} 页").click()

    def get_total_count(self) -> str:
        """获取总记录数文本"""
        return self.page.locator(".el-pagination__total").inner_text()

    # -------- 列表页 - 顶部按钮操作 --------

    def click_add_project(self):
        """点击新增项目按钮"""
        self.click(self.ADD_BTN)

    def click_batch_delete(self):
        """点击批量删除按钮"""
        self.click(self.BATCH_DELETE_BTN)

    def click_export_excel(self):
        """点击导出Excel按钮"""
        self.click(self.EXPORT_BTN)

    # -------- 新增项目弹窗操作 --------

    def select_add_province(self, province: str):
        """在新增弹窗中选择省份"""
        self._dialog_select_by_label("省份").click()
        self.page.get_by_role("option", name=province, exact=True).click()

    def select_add_city(self, city: str):
        """在新增弹窗中选择市县（需先选择省份）"""
        self._dialog_select_by_label("市县").click()
        self.page.get_by_role("option", name=city, exact=True).click()

    def fill_add_project_name(self, project_name: str):
        """在新增弹窗中填写项目名称"""
        self.page.get_by_role("dialog", name="新增项目").get_by_placeholder("请输入项目名称").fill(project_name)

    def select_add_status(self, status: str):
        """在新增弹窗中选择项目状态"""
        self._dialog_select_by_label("项目状态").click()
        self.page.get_by_role("option", name=status, exact=True).click()

    def fill_add_start_date(self, date: str):
        """在新增弹窗中填写开始时间"""
        self._dialog_date_by_label("开始时间").click()
        self._dialog_date_by_label("开始时间").fill(date)
        self.page.keyboard.press("Enter")

    def fill_add_end_date(self, date: str):
        """在新增弹窗中填写结束时间"""
        self._dialog_date_by_label("结束时间").click()
        self._dialog_date_by_label("结束时间").fill(date)
        self.page.keyboard.press("Enter")

    def fill_add_description(self, description: str):
        """在新增弹窗中填写项目描述"""
        self.page.get_by_role("dialog", name="新增项目").get_by_placeholder("请输入项目描述").fill(description)

    def click_add_confirm(self):
        """在新增弹窗中点击确定"""
        self.page.get_by_role("dialog", name="新增项目").get_by_role("button", name="确定").click()

    def click_add_cancel(self):
        """在新增弹窗中点击取消"""
        self.page.get_by_role("dialog", name="新增项目").get_by_role("button", name="取消").click()

    def close_add_dialog(self):
        """关闭新增弹窗"""
        self.page.get_by_role("dialog", name="新增项目").get_by_role("button", name="关闭此对话框").click()

    # -------- 编辑项目弹窗操作 --------

    def select_edit_province(self, province: str):
        """在编辑弹窗中选择省份"""
        self._dialog_select_by_label("省份", "编辑项目").click()
        self.page.get_by_role("option", name=province, exact=True).click()

    def select_edit_city(self, city: str):
        """在编辑弹窗中选择市县"""
        self._dialog_select_by_label("市县", "编辑项目").click()
        self.page.get_by_role("option", name=city, exact=True).click()

    def fill_edit_project_name(self, project_name: str):
        """在编辑弹窗中填写项目名称"""
        self.page.get_by_role("dialog", name="编辑项目").get_by_placeholder("请输入项目名称").fill(project_name)

    def select_edit_status(self, status: str):
        """在编辑弹窗中选择项目状态"""
        self._dialog_select_by_label("项目状态", "编辑项目").click()
        self.page.get_by_role("option", name=status, exact=True).click()

    def fill_edit_start_date(self, date: str):
        """在编辑弹窗中填写开始时间"""
        self._dialog_date_by_label("开始时间", "编辑项目").click()
        self._dialog_date_by_label("开始时间", "编辑项目").fill(date)
        self.page.keyboard.press("Enter")

    def fill_edit_end_date(self, date: str):
        """在编辑弹窗中填写结束时间"""
        self._dialog_date_by_label("结束时间", "编辑项目").click()
        self._dialog_date_by_label("结束时间", "编辑项目").fill(date)
        self.page.keyboard.press("Enter")

    def fill_edit_description(self, description: str):
        """在编辑弹窗中填写项目描述"""
        self.page.get_by_role("dialog", name="编辑项目").get_by_placeholder("请输入项目描述").fill(description)

    def click_edit_confirm(self):
        """在编辑弹窗中点击确定"""
        self.page.get_by_role("dialog", name="编辑项目").get_by_role("button", name="确定").click()

    def click_edit_cancel(self):
        """在编辑弹窗中点击取消"""
        self.page.get_by_role("dialog", name="编辑项目").get_by_role("button", name="取消").click()

    def close_edit_dialog(self):
        """关闭编辑弹窗"""
        self.page.get_by_role("dialog", name="编辑项目").get_by_role("button", name="关闭此对话框").click()

    # -------- 查看详情弹窗操作 --------

    def get_view_field_value(self, field_name: str) -> str:
        """在查看详情弹窗中获取指定字段的值"""
        return self.page.get_by_role("dialog", name="项目详情").get_by_role("textbox", name=field_name).input_value()

    def close_view_dialog(self):
        """关闭查看详情弹窗"""
        self.page.get_by_role("dialog", name="项目详情").get_by_role("button", name="关闭").click()

    # -------- 删除确认操作 --------

    def confirm_delete(self):
        """确认删除（点击 MessageBox 确定按钮）"""
        self.page.get_by_role("button", name="确定").click()

    def cancel_delete(self):
        """取消删除（点击 MessageBox 取消按钮）"""
        self.page.get_by_role("button", name="取消").click()

    # -------- 新增项目完整流程 --------

    def create_project(self, province: str, city: str, project_name: str,
                       status: str, start_date: str = None, end_date: str = None,
                       description: str = None):
        """新增项目完整流程

        Args:
            province: 省份
            city: 市县
            project_name: 项目名称
            status: 项目状态
            start_date: 开始时间
            end_date: 结束时间
            description: 项目描述
        """
        self.click_add_project()
        self.page.get_by_role("dialog", name="新增项目").wait_for(state="visible")
        self.select_add_province(province)
        self.select_add_city(city)
        self.fill_add_project_name(project_name)
        self.select_add_status(status)
        if start_date:
            self.fill_add_start_date(start_date)
        if end_date:
            self.fill_add_end_date(end_date)
        if description:
            self.fill_add_description(description)
        self.click_add_confirm()

    # -------- 断言方法 --------

    def assert_on_project_management_page(self):
        """断言当前在项目管理页面"""
        self.assert_url(f"*{self.PAGE_URL}*")

    def assert_table_has_data(self):
        """断言表格有数据"""
        self.assert_visible(self.TABLE_ROW)

    def assert_add_dialog_visible(self):
        """断言新增弹窗可见"""
        expect(self.page.get_by_role("dialog", name="新增项目")).to_be_visible()

    def assert_add_dialog_closed(self):
        """断言新增弹窗已关闭"""
        expect(self.page.get_by_role("dialog", name="新增项目")).to_be_hidden()

    def assert_edit_dialog_visible(self):
        """断言编辑弹窗可见"""
        expect(self.page.get_by_role("dialog", name="编辑项目")).to_be_visible()

    def assert_edit_dialog_closed(self):
        """断言编辑弹窗已关闭"""
        expect(self.page.get_by_role("dialog", name="编辑项目")).to_be_hidden()

    def assert_view_dialog_visible(self):
        """断言查看详情弹窗可见"""
        expect(self.page.get_by_role("dialog", name="项目详情")).to_be_visible()

    def assert_view_dialog_closed(self):
        """断言查看详情弹窗已关闭"""
        expect(self.page.get_by_role("dialog", name="项目详情")).to_be_hidden()

    def assert_search_result_contains(self, header: str, expected: str):
        """断言搜索结果中第一行指定列包含预期文本"""
        actual = self.get_cell_text_by_header(0, header)
        assert expected in actual, f"列'{header}'预期包含'{expected}'，实际为'{actual}'"
