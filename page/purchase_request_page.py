from base.base_page import BasePage


class PurchaseRequestPage(BasePage):
    """采购申请页面对象，封装采购申请列表和新增申请的元素定位与操作方法"""

    # -------- 页面路由 --------
    PAGE_URL = "/#/demo/purchase-request"

    # -------- 列表页 - 搜索区域（文本输入框，placeholder定位） --------
    SEARCH_REQUEST_NO = "input[placeholder='请输入申请编号']"
    SEARCH_PROJECT_NAME = "input[placeholder='请输入项目名称']"
    SEARCH_APPLICANT = "input[placeholder='请输入申请人']"
    SEARCH_START_DATE = "input[placeholder='选择开始日期']"
    SEARCH_END_DATE = "input[placeholder='选择结束日期']"
    SEARCH_BTN = "button:has-text('查询')"
    RESET_BTN = "button:has-text('重置')"

    # -------- 列表页 - 操作按钮 --------
    ADD_BTN = "button:has-text('新增申请')"
    DEPARTMENT_BTN = "button:has-text('科室管理')"
    AUDIT_BTN = "button:has-text('开始审核')"
    BATCH_DELETE_BTN = "button:has-text('批量删除')"
    EXPORT_BTN = "button:has-text('导出Excel')"

    # -------- 列表页 - 表格 --------
    TABLE_ROW = ".el-table__body-wrapper .el-table__row"
    CHECKBOX_ALL = ".el-table__header .el-checkbox"

    # -------- 新增/编辑弹窗 --------
    DIALOG = "[aria-label='新增采购申请']"
    EDIT_DIALOG = "[aria-label='编辑采购申请']"
    DIALOG_CLOSE = ".el-drawer__close-btn"
    DIALOG_TITLE = ".el-drawer__title"

    # 新增申请 - 申请信息表单（基于placeholder定位的输入框）
    FORM_APPLICANT = "[aria-label='新增采购申请'] input[disabled]"
    FORM_REQUEST_NO = "input[placeholder='请输入申请编号']"
    FORM_REASON = "textarea[placeholder='请详细说明采购原因及物品用途...']"

    # 新增申请 - 采购物品
    ADD_ITEM_BTN = "button:has-text('添加物品')"
    ITEM_EMPTY_TEXT = "text=尚未添加采购物品"

    # 新增申请 - 附件上传
    UPLOAD_AREA = ".el-upload-dragger"

    # 新增申请 - 底部按钮
    CANCEL_BTN = "button:has-text('取消')"
    SUBMIT_BTN = "button:has-text('提交申请')"

    # -------- 内部辅助方法 --------

    def _search_select_by_label(self, label: str):
        """根据标签文本在搜索区域定位对应的 el-select 下拉框

        替代 nth-child 选择器，通过标签文本（如"紧急程度"）精确匹配
        """
        return self.page.locator(".search-form .el-form-item").filter(has_text=label).locator(".el-select")

    def _dialog_select_by_label(self, label: str):
        """根据标签文本在新增弹窗表单中定位对应的 el-select 下拉框

        替代 :has-text() 选择器，通过标签文本（如"科室"、"经办人"）精确匹配
        """
        return self.page.locator(self.DIALOG).locator(".el-form-item").filter(has_text=label).locator(".el-select")

    def _dialog_date_by_label(self, label: str):
        """根据标签文本在新增弹窗表单中定位对应的日期选择器 input"""
        return self.page.locator(self.DIALOG).locator(".el-form-item").filter(has_text=label).locator("input")

    def _body_table(self):
        """获取表格主体区域"""
        return self.page.locator(".el-table__body-wrapper").get_by_role("table")

    def _header_table(self):
        """获取表格表头区域"""
        return self.page.locator(".el-table__header-wrapper").get_by_role("table")

    # -------- 导航 --------
    def navigate_to_purchase_request(self):
        """导航到采购申请页面"""
        self.goto(self.PAGE_URL)

    def navigate_via_menu(self):
        """通过左侧菜单导航：申请提交 -> 采购申请"""
        self.page.get_by_role("menuitem", name="申请提交").click()
        self.page.get_by_role("menuitem", name="采购申请").click()
        self.wait_for_load_state("domcontentloaded")

    # -------- 列表页 - 搜索操作 --------
    def search_by_request_no(self, request_no: str):
        """按申请编号搜索"""
        self.fill(self.SEARCH_REQUEST_NO, request_no)
        self.click(self.SEARCH_BTN)

    def search_by_project_name(self, project_name: str):
        """按项目名称搜索"""
        self.fill(self.SEARCH_PROJECT_NAME, project_name)
        self.click(self.SEARCH_BTN)

    def search_by_applicant(self, applicant: str):
        """按申请人搜索"""
        self.fill(self.SEARCH_APPLICANT, applicant)
        self.click(self.SEARCH_BTN)

    def select_urgency_filter(self, urgency: str):
        """选择紧急程度筛选"""
        self._search_select_by_label("紧急程度").click()
        self.page.get_by_role("listitem").filter(has_text=urgency).click()

    def select_department_filter(self, department: str):
        """选择使用科室筛选"""
        self._search_select_by_label("使用科室").click()
        self.page.get_by_role("listitem").filter(has_text=department).click()

    def select_status_filter(self, status: str):
        """选择审核状态筛选"""
        self._search_select_by_label("审核状态").click()
        self.page.get_by_role("listitem").filter(has_text=status).click()

    def click_search(self):
        """点击查询按钮"""
        self.click(self.SEARCH_BTN)

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
        """根据列标题获取表格指定行的单元格文本

        Args:
            row: 行索引，从0开始
            header: 列标题名称，如"申请编号"、"紧急程度"等
        """
        headers = self._header_table().get_by_role("columnheader")
        col_index = -1
        for i in range(headers.count()):
            if header in headers.nth(i).inner_text():
                col_index = i
                break
        if col_index == -1:
            raise ValueError(f"未找到列标题: {header}")
        return self._body_table().get_by_role("row").nth(row).get_by_role("cell").nth(col_index).inner_text()

    def click_row_checkbox(self, row: int):
        """勾选指定行的复选框

        Args:
            row: 行索引，从0开始
        """
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
    def click_add_request(self):
        """点击新增申请按钮"""
        self.click(self.ADD_BTN)

    def click_department_manage(self):
        """点击科室管理按钮"""
        self.click(self.DEPARTMENT_BTN)

    def click_start_audit(self):
        """点击开始审核按钮"""
        self.click(self.AUDIT_BTN)

    def click_batch_delete(self):
        """点击批量删除按钮"""
        self.click(self.BATCH_DELETE_BTN)

    def click_export_excel(self):
        """点击导出Excel按钮"""
        self.click(self.EXPORT_BTN)

    # -------- 新增申请弹窗操作 --------
    def select_handler(self, handler: str):
        """在新增弹窗中选择经办人"""
        self._dialog_select_by_label("经办人").click()
        self.page.get_by_role("listitem").filter(has_text=handler).click()

    def fill_request_no(self, request_no: str):
        """在新增弹窗中填写申请编号"""
        self.page.locator(self.DIALOG).locator(self.FORM_REQUEST_NO).fill(request_no)

    def select_department(self, department: str):
        """在新增弹窗中选择科室"""
        self._dialog_select_by_label("科室").click()
        self.page.get_by_role("listitem").filter(has_text=department).click()

    def select_project(self, project: str):
        """在新增弹窗中选择使用项目"""
        self._dialog_select_by_label("使用项目").click()
        self.page.get_by_role("listitem").filter(has_text=project).click()

    def fill_expected_date(self, date: str):
        """在新增弹窗中填写期望到货日期"""
        self._dialog_date_by_label("期望到货").click()
        self._dialog_date_by_label("期望到货").fill(date)
        self.page.keyboard.press("Enter")

    def select_urgency(self, urgency: str):
        """在新增弹窗中选择紧急程度"""
        self._dialog_select_by_label("紧急程度").click()
        self.page.get_by_role("listitem").filter(has_text=urgency).click()

    def fill_reason(self, reason: str):
        """在新增弹窗中填写采购原因"""
        self.page.locator(self.DIALOG).locator(self.FORM_REASON).fill(reason)

    def click_add_item(self):
        """在新增弹窗中点击添加物品"""
        self.click(self.ADD_ITEM_BTN)

    def click_submit_request(self):
        """在新增弹窗中点击提交申请"""
        self.click(self.SUBMIT_BTN)

    def click_cancel_request(self):
        """在新增弹窗中点击取消"""
        self.click(self.CANCEL_BTN)

    def close_dialog(self):
        """关闭弹窗"""
        self.page.locator(self.DIALOG_CLOSE).click()

    # -------- 新增申请完整流程 --------
    def create_purchase_request(self, department: str, project: str, urgency: str,
                                handler: str = None, expected_date: str = None,
                                reason: str = None):
        """新增采购申请完整流程

        Args:
            department: 使用科室
            project: 使用项目
            urgency: 紧急程度
            handler: 经办人
            expected_date: 期望到货日期
            reason: 采购原因
        """
        self.click_add_request()
        self.page.locator(self.DIALOG).wait_for(state="visible")
        if handler:
            self.select_handler(handler)
        self.select_department(department)
        self.select_project(project)
        if expected_date:
            self.fill_expected_date(expected_date)
        self.select_urgency(urgency)
        if reason:
            self.fill_reason(reason)
        self.click_submit_request()

    # -------- 断言方法 --------
    def assert_on_purchase_request_page(self):
        """断言当前在采购申请页面"""
        self.assert_url(f"*{self.PAGE_URL}*")

    def assert_table_has_data(self):
        """断言表格有数据"""
        self.assert_visible(self.TABLE_ROW)

    def assert_dialog_visible(self):
        """断言新增弹窗可见"""
        self.assert_visible(self.DIALOG)

    def assert_dialog_closed(self):
        """断言新增弹窗已关闭"""
        self.assert_hidden(self.DIALOG)

    def assert_search_result_contains(self, header: str, expected: str):
        """断言搜索结果中第一行指定列包含预期文本

        Args:
            header: 列标题名称，如"申请编号"、"紧急程度"等
            expected: 预期文本
        """
        actual = self.get_cell_text_by_header(0, header)
        assert expected in actual, f"列'{header}'预期包含'{expected}'，实际为'{actual}'"
