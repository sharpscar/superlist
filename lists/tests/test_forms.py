from django.test import TestCase
from lists.forms import ItemForm

class ItemFormTest(TestCase):

    # 아이템폼 렌더링 확인
    def test_form_renders_item_text_input(self):
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
        
