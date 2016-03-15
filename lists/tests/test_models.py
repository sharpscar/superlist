  # -*- coding: utf-8 -*-
from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError

# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

class ItemModelTest(TestCase):

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text,'')

class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/lists/%d/' % (list_.id,))


class ListAndItemModelsTest(TestCase):

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())


    # 비어있는 아이템은 저장할수 없도록 모델에서 유효성 체크를 한다.
    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()



    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='bla')
            item.full_clean()

    def test_CAN_save_same_item_to_different_lists(self):
        list1  = List.objects.create()
        list2  = List.objects.create()

        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean() #에러를 발생시키지 않는다.

    def test_list_ordering(self):
        list1  = List.objects.create()
        item1 = Item.objects.create(list=list1, text='i1')
        item2 = Item.objects.create(list=list1, text='item 2')
        item3 = Item.objects.create(list=list1, text='3')
        self.assertEqual(
        list(Item.objects.all()), [item1, item2, item3])

    def test_string_representation(self):
        item = Item(text='어떤텍스트')
        self.assertEqual(str(item), '어떤텍스트')
