  # -*- coding: utf-8 -*-


from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from lists.models import Item, List
from lists.views import home_page
from django.utils.html import escape
from lists.forms import ItemForm, EMPTY_LIST_ERROR
from unittest import skip
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')



class HomePageTest(TestCase):

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

class NewListTest(TestCase):
        # home_page함수가 post요청을 처리, 저장할수 있도록 테스트
        def test_saving_a_POST_request(self):
            self.client.post('/lists/new', data={'text':'신규 작업 아이템'})
            self.assertEqual(Item.objects.count(), 1)
            new_item = Item.objects.first()
            self.assertEqual(new_item.text, '신규 작업 아이템')


        # 포스트 요청 처리후 리다이렉트 처리 할수 있도록 테스트
        def test_redirect_after_POST(self):

            response = self.client.post('/lists/new', data={'text':'신규 작업 아이템'})
            new_list  = List.objects.first()
            self.assertRedirects(response,'/lists/%d/' % (new_list.id,))

        # # 빈 아이템을 등록할때에 1.200 코드로 응답 2. home.html을 템플릿으로 사용  3. 해당 에러메시지 발생하는지
        # def test_validation_errors_are_sent_back_to_home_page_template(self):
        #     response = self.client.post('/lists/new', data={'text':''})
        #     self.assertEqual(response.status_code, 200)
        #     self.assertTemplateUsed(response, 'home.html')
        #     expected_error = escape("You can't have an empty list item.")
        #     self.assertContains(response, expected_error)

        # 잘못된 입력이 홈페이지 템플릿에 렌더링 되는지
        def test_for_invalid_input_renders_home_template(self):
            response = self.client.post('/lists/new', data={'text':''})
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'home.html')

        #유효성 검증 실패가 홈페이지에 드러나는지
        def test_validation_errors_are_show_on_home_page(self):
            response = self.client.post('/lists/new', data={'text':''})
            # self.fail(response.content.decode())
            self.assertContains(response, escape(EMPTY_LIST_ERROR))

        # 잘못된 폽 입력이 템플릿에 전달 되는지
        def test_for_invalid_input_passes_form_to_template(self):
            response = self.client.post('/lists/new', data={'text':''})
            self.assertIsInstance(response.context['form'], ItemForm)


        # 유효성 체크를 실패했는데도 객체를 생성하고 있는 문제
        def test_invalid_list_items_arent_saved(self):
            self.client.post('/lists/new', data={'text':''})
            self.assertEqual(List.objects.count(),0)
            self.assertEqual(Item.objects.count(),0)




class ListViewTest(TestCase):

    #아이템에 해당하는 리스트만 표시되도록 테스트
    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='다른목록 아이템 1', list=other_list)
        Item.objects.create(text='다른목록 아이템 2', list=other_list)


        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

        self.assertNotContains(response, '다른목록 아이템 1')
        self.assertNotContains(response, '다른목록 아이템 2')

    # 서로 다른(리스트, 홈페이지) 템플릿을 사용하는지 테스트
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'list.html')

    # 뷰가 템플릿에 목록을 넘기기
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)

    # 기존 목록에 아이템을 추가하면 저장되는지
    def test_can_save_a_POST_request_to_an_exisint_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post('/lists/%d/' % (correct_list.id,),
            data={'text': '기존 목록에 신규 아이템'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, '기존 목록에 신규 아이템')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post('/lists/%d/' % (correct_list.id,),
            data={'text': '기존 목록에 신규 아이템'}
        )
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))

    # def test_validation_errors_end_up_on_lists_page(self):
    #     list_= List.objects.create()
    #     response = self.client.post('/lists/%d/' % (list_.id,), data={'text':''})
    #
    #     self.assertEqual(response.status_code,200)
    #     self.assertTemplateUsed(response, 'list.html')
    #     expected_error = escape("You can't have an empty list item.")
    #     self.assertContains(response, expected_error)


    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')

    # 잘못된 입력
    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post('/lists/%d/' % (list_.id,), data={'text':''})

    #잘못된 입력을 보냈을때 저장하지 않도록 확인
    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(),0)

    # 잘못된 입력을 리스트 템플릿으로 렌더링한다.
    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    # 잘못된 입력을보냈을때 응답객체가 아이템 폼 인스턴스인지 확인
    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)


    #잘못된 입력이 페이지에 에러를 표시하는지 확인
    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        # self.fail(response.content.decode())
        self.assertContains(response, escape(EMPTY_LIST_ERROR))

    # 리스트객체와 아이템의 텍스트 내용이 중복된다.
    #sqlite3.IntegrityError: UNIQUE constraint failed: lists_item.list_id, lists_item.text
    @skip
    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='textey')
        response = self.client.post(
            '/lists/%d/' % (list1.id,),
            data= {'text':'textey'}
        )
        expected_error = escape("이미 리스트에 해당 아이템이 있습니다.")
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.all().count, 1)
