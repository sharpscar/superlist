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

    # home_page함수가 post요청을 처리, 저장할수 있도록 테스트
    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = '신규 작업 아이템'

        response = home_page(request)

        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, '신규 작업 아이템')

    # 포스트 요청 처리후 리다이렉트 처리 할수 있도록 테스트
    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = '신규 작업 아이템'

        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'],'/')

    #
    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)

        self.assertEqual(Item.objects.count(),0)


    def test_home_page_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        request = HttpRequest()
        response = home_page(request)

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())
