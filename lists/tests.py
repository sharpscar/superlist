from django.core.urlresolvers import resolve
from django.test import TestCase
from lists.views import home_page

class HomePageTest(TestCase):

    # URL의 사이트 루트를 해석해서 특정 뷰 기능에 매칭시킬수 있는가
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
