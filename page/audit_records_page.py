from playwright.sync_api import expect

from base.base_page import BasePage


class AuditRecordsPage(BasePage):
    """审核记录页面对象，封装审核记录列表的搜索筛选、查看申请页、删除的元素定位与操作方法"""

    # -------- 页面路由 --------
    PAGE_URL = "/#/link/audit-records"

    # -------- 列表页 - 搜索区域 --------
    SEARCH_BTN = "button:has-text('查询')"
    RESET_BTN = "button:has-text('重置')"

    # -------- 列表页 - 表格 --------
    TABLE_ROW = ".el-table__body-wrapper .el-table__row"

    # -------- 内部辅助方法 --------

    def _search_select_by_label(self, label: str):
        """根据标签文本在搜索区域定位对应的 el-select 下拉框"""
        return self.page.locator(".search-form .el-col").filter(has_text=label).locator(".el-select")

    def _search_date_by_label(self, label: str):
        """根据标签文本在搜索区域定位对应的日期选择器 combobox"""
        return self.page.locator(".search-form .el-col").filter(has_text=label).get_by_role("combobox")

    def _body_table(self):
        """获取表格主体区域"""
        return self.page.locator(".el-table__body-wrapper").get_by_role("table")

    def _header_table(self):
        """获取表格表头区域"""
        return self.page.locator(".el-table__header-wrapper").get_by_role("table")

    # -------- 导航 --------

    def navigate_to_audit_records(self):
        """导航到审核记录页面"""
        self.goto(self.PAGE_URL)

    def navigate_via_menu(self):
        """通过左侧菜单导航：信息管理 -> 审核记录"""
        self.page.get_by_role("menuitem", name="信息管理").click()
        self.page.get_by_role("menuitem", name="审核记录").click()
        self.wait_for_load_state("domcontentloaded")

    # -------- 列表页 - 搜索操作 --------

    def select_purchase_no_filter(self, purchase_no: str):
        """选择采购编号筛选"""
        self._search_select_by_label("采购编号").click()
        self.page.get_by_role("option", name=purchase_no, exact=True).click()

    def select_project_name_filter(self, project_name: str):
        """选择项目名称筛选"""
        self._search_select_by_label("项目名称").click()
        self.page.get_by_role("option", name=project_name, exact=True).click()

    def fill_apply_date_start(self, date: str):
        """填写搜索区域申请日期-开始"""
        self._search_date_by_label("申请日期").first.fill(date)
        self.page.keyboard.press("Enter")

    def fill_apply_date_end(self, date: str):
        """填写搜索区域申请日期-结束（至）"""
        self._search_date_by_label("至").first.fill(date)
        self.page.keyboard.press("Enter")

    def fill_audit_date_start(self, date: str):
        """填写搜索区域审核日期-开始"""
        self._search_date_by_label("审核日期").first.fill(date)
        self.page.keyboard.press("Enter")

    def fill_audit_date_end(self, date: str):
        """填写搜索区域审核日期-结束（至）"""
        self._search_date_by_label("至").last.fill(date)
        self.page.keyboard.press("Enter")

    def select_audit_result_filter(self, result: str):
        """选择审核结果筛选"""
        self._search_select_by_label("审核结果").click()
        self.page.get_by_role("option", name=result, exact=True).click()

    def select_auditor_filter(self, auditor: str):
        """选择审核人筛选"""
        self._search_select_by_label("审核人").click()
        self.page.get_by_role("option", name=auditor, exact=True).click()

    def select_apply_status_filter(self, status: str):
        """选择申请状态筛选"""
        self._search_select_by_label("申请状态").click()
        self.page.get_by_role("option", name=status, exact=True).click()

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

    def click_view_button(self, row: int):
        """点击指定行的查看按钮"""
        self._body_table().get_by_role("row").nth(row).get_by_role("button", name="查看").click()

    def click_application_page_button(self, row: int):
        """点击指定行的申请页按钮"""
        self._body_table().get_by_role("row").nth(row).get_by_role("button", name="申请页").click()

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

    # -------- 删除确认操作 --------

    def confirm_delete(self):
        """确认删除（点击 MessageBox 确定按钮）"""
        self.page.get_by_role("button", name="确定").click()

    def cancel_delete(self):
        """取消删除（点击 MessageBox 取消按钮）"""
        self.page.get_by_role("button", name="取消").click()
