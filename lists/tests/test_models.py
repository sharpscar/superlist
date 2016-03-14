  # -*- coding: utf-8 -*-
from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError

# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')


class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()


        first_item = Item()
        first_item.text = '첫번째 아이템'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = '두번째 아이템'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()

        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, '첫번째 아이템')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, '두번째 아이템')
        self.assertEqual(second_saved_item.list, list_)

    # 비어있는 아이템은 저장할수 없도록 모델에서 유효성 체크를 한다.
    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()
