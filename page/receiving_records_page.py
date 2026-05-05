from playwright.sync_api import expect

from base.base_page import BasePage


class ReceivingRecordsPage(BasePage):
    """收货记录页面对象，封装收货记录列表的搜索筛选、查看详情、收货操作的元素定位与操作方法"""

    # -------- 页面路由 --------
    PAGE_URL = "/#/demo/receiving-records"

    # -------- 列表页 - 搜索区域 --------
    SEARCH_APPLICATION_NO = "input[placeholder='请输入申请编号']"
    SEARCH_ORDER_NO = "input[placeholder='请输入采购编号']"
    SEARCH_PROJECT_NAME = "input[placeholder='请输入项目名称']"
    SEARCH_RECIPIENT = "input[placeholder='请输入收件人姓名']"
    SEARCH_BTN = "button:has-text('搜索')"
    RESET_BTN = "button:has-text('重置')"

    # -------- 下拉选择框 --------
    SELECT_DEPARTMENT_TEXT = "请选择所属科室"
    SELECT_PURCHASE_STATUS_TEXT = "请选择采购状态"
    SELECT_RECEIVING_STATUS_TEXT = "请选择收货状态"
    SELECT_STORAGE_STATUS_TEXT = "请选择入库状态"

    # -------- 列表页 - 操作按钮 --------
    EXPORT_BTN = "button:has-text('导出Excel')"

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

    def navigate_to_receiving_records(self):
        """导航到收货记录页面"""
        self.goto(self.PAGE_URL)

    def navigate_via_menu(self):
        """通过左侧菜单导航：申请提交 -> 收货记录"""
        self.page.get_by_role("menuitem", name="申请提交").click()
        self.page.get_by_role("menuitem", name="收货记录").click()
        self.wait_for_load_state("domcontentloaded")

    # -------- 列表页 - 搜索操作 --------

    def search_by_application_no(self, application_no: str):
        """按申请编号搜索"""
        self.fill(self.SEARCH_APPLICATION_NO, application_no)
        self.click(self.SEARCH_BTN)

    def search_by_order_no(self, order_no: str):
        """按采购编号搜索"""
        self.fill(self.SEARCH_ORDER_NO, order_no)
        self.click(self.SEARCH_BTN)

    def search_by_project_name(self, project_name: str):
        """按项目名称搜索"""
        self.fill(self.SEARCH_PROJECT_NAME, project_name)
        self.click(self.SEARCH_BTN)

    def search_by_recipient(self, recipient: str):
        """按收件人搜索"""
        self.fill(self.SEARCH_RECIPIENT, recipient)
        self.click(self.SEARCH_BTN)

    def select_department_filter(self, department: str):
        """选择所属科室筛选"""
        self.get_by_text(self.SELECT_DEPARTMENT_TEXT).click()
        self.page.get_by_role("option", name=department, exact=True).click()

    def select_purchase_status_filter(self, status: str):
        """选择采购状态筛选"""
        self.get_by_text(self.SELECT_PURCHASE_STATUS_TEXT).click()
        self.page.get_by_role("option", name=status, exact=True).click()

    def select_receiving_status_filter(self, status: str):
        """选择收货状态筛选"""
        self.get_by_text(self.SELECT_RECEIVING_STATUS_TEXT).click()
        self.page.get_by_role("option", name=status, exact=True).click()

    def select_storage_status_filter(self, status: str):
        """选择入库状态筛选"""
        self.get_by_text(self.SELECT_STORAGE_STATUS_TEXT).click()
        self.page.get_by_role("option", name=status, exact=True).click()

    def fill_receiving_date_start(self, date: str):
        """填写搜索区域收货日期范围-开始"""
        self._search_date_by_label("收货日期范围").first.fill(date)
        self.page.keyboard.press("Enter")

    def fill_receiving_date_end(self, date: str):
        """填写搜索区域收货日期范围-结束"""
        self._search_date_by_label("收货日期范围").last.fill(date)
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

    def click_receive_button(self, row: int):
        """点击指定行的收货按钮"""
        self._body_table().get_by_role("row").nth(row).get_by_role("button", name="收货").click()

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

    def click_export_excel(self):
        """点击导出Excel按钮"""
        self.click(self.EXPORT_BTN)

    # -------- 断言方法 --------

    def assert_on_receiving_records_page(self):
        """断言当前在收货记录页面"""
        self.assert_url(f"*{self.PAGE_URL}*")

    def assert_table_has_data(self):
        """断言表格有数据"""
        self.assert_visible(self.TABLE_ROW)

    def assert_search_result_contains(self, header: str, expected: str):
        """断言搜索结果中第一行指定列包含预期文本"""
        actual = self.get_cell_text_by_header(0, header)
        assert expected in actual, f"列'{header}'预期包含'{expected}'，实际为'{actual}'"
