  # -*- coding: utf-8 -*-


from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page
from lists.models import Item
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'it is  a first item'
        first_item.save()
        second_item = Item()
        second_item.text = 'that is a second item'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(),2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'it is  a first item')
        self.assertEqual(second_saved_item.text, 'that is a second item')


class HomePageTest(TestCase):

    # URL의 사이트 루트를 해석해서 특정 뷰 기능에 매칭시킬수 있는가
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    # 올바른 html형식의 실제 응답을 반환하는 함수를 위한 테스트
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html  =  render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

class NewListTest(TestCase):
        # home_page함수가 post요청을 처리, 저장할수 있도록 테스트
        def test_saving_a_POST_request(self):
            self.client.post('/lists/new', data={'item_text':'신규 작업 아이템'})
            self.assertEqual(Item.objects.count(), 1)
            new_item = Item.objects.first()
            self.assertEqual(new_item.text, '신규 작업 아이템')


        # 포스트 요청 처리후 리다이렉트 처리 할수 있도록 테스트
        def test_redirect_after_POST(self):

            response = self.client.post('/lists/new', data={'item_text':'신규 작업 아이템'})
            self.assertRedirects(response,'/lists/the-only-list-in-the-world/')



class ListViewTest(TestCase):

    def test_displys_all_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

    # 서로 다른(리스트, 홈페이지) 템플릿을 사용하는지 테스트
    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')
