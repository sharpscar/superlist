from django.test import TestCase
from lists.forms import ItemForm
from lists.models import Item, List

class ItemFormTest(TestCase):

    # 아이템폼 렌더링 확인
    def test_form_renders_text_input(self):
        form = ItemForm()

        self.assertIn('placeholder="작업 아이템 입력"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())


    # 비어있는 아이템을 폼 유효성 검증은 어떻게 이루어지는가
    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            ["You can't have an empty list item."]
        )

    def test_form_save_handles_saving_to_a_list(self):
        list_ = List.objects.create()

        form = ItemForm(data={'text':'do me'})
        new_item = form.save(for_list= list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'do me')
        self.assertEqual(new_item.list, list_)
