
from unittest import skip
from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):


    def test_cannot_add_empty_list_items(self):
        # 에디스는 메인 페이지에 접속해서 빈 아이템을 실수로 등록하려고 한다
        #입력상자가 비어있는 상태에서 엔터키를 누른다
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')

        #페이지가 새로고침되고, 빈아이템을 등록할수 없다는 에러메시지가 표시된다
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an empty list item.")

        #다른 아이템을 입력하고 이번에는 정상 처리된다
        self.get_item_input_box().send_keys('우유 사기\n')
        self.check_for_row_in_list_table('1: 우유 사기')
        #그녀는 고의적으로 다시 빈 아이템을 등록한다
        self.get_item_input_box().send_keys('\n')
        # 리스트 페이지에 다시 에러메시지가 표시된다.
        self.check_for_row_in_list_table('1: 우유 사기')
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an empty list item.")


        # 아이템을 입력하면 정상 동작한다.
        self.get_item_input_box().send_keys('tea 만들기\n')
        self.check_for_row_in_list_table('1: 우유 사기')
        self.check_for_row_in_list_table('2: tea 만들기')


    def test_cannot_add_duplicate_items(self):
        # 에디스는 메인 페이지로 돌아가서 신규 목록을 시작한다
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('콜라 사기\n')
        self.check_for_row_in_list_table('1: 콜라 사기')

        #실수로 중복 아이템을 입력한다.
        self.get_item_input_box().send_keys('콜라 사기\n')

        #도움이 되는 에러 메시지를 본다
        self.check_for_row_in_list_table('1: 콜라 사기')
        error = self.get_error_element()
        self.assertEqual(error.text, "이미 리스트에 해당 아이템이 있습니다.")

    def get_error_element(self):

        return self.browser.find_element_by_css_selector('.has-error')

    def test_error_messages_are_cleared_on_input(self):
        #에디스는 검증 에러를 발생시키도록 신규 목록을 시작한다.
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')
        error = self.get_error_element()
        self.assertTrue(error.is_displayed())

        #에러를 제거하기 위해 입력 상자에 타이핑하기 시작한다.
        self.get_item_input_box().send_keys('a')

        #에러메시지가 사라진것을 보고 기뻐한다
        error = self.get_error_element()
        self.assertFalse(error.is_displayed())
