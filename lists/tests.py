from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page




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

    # home_page함수가 post요청을 처리할수 있도록 테스트
    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = '신규 작업 아이템'
        response = home_page(request)
        self.assertIn('신규 작업 아이템', response.content.decode())
        expected_html = render_to_string(
        'home.html',
        {'new_item_text':'신규 작업 아이템'}
        )
        self.assertEqual(response.content.decode(), expected_html)
