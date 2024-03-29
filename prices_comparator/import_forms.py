import django.forms as forms
from django.core.exceptions import ValidationError

import prices_comparator.common as const
from prices_comparator.common import ItemType


class ImportItemForm(forms.Form):
    id = forms.UUIDField()
    name = forms.CharField(max_length=const.IMPORT_UNIT_NAME_MAX_LENGTH)
    parentId = forms.UUIDField(required=False)
    type = forms.ChoiceField(
        choices=const.IMPORT_UNIT_TYPE_CHOICES
    )
    price = forms.IntegerField(min_value=0, required=False)

    def clean(self):
        item_type = self.cleaned_data.get('type', None)
        price = self.cleaned_data.get('price', None)

        if item_type == ItemType.CATEGORY.value:
            if isinstance(price, int):
                raise ValidationError(message='price for category isn\'t null')
        elif item_type == ItemType.OFFER.value:
            if not isinstance(price, int) or price < 0:
                raise ValidationError(message='invalid offer price')

        return super().clean()


class ListField(forms.MultipleChoiceField):
    def __init__(self, *args, item_form_class=None, **kwargs):
        self.form_class = item_form_class
        super().__init__()

    def to_python(self, values):
        if not values:
            return []
        elif not isinstance(values, (list, tuple)):
            raise ValidationError('items field is not a sequence')
        return values

    def validate(self, value):
        if self.required and not value:
            raise ValidationError(
                self.error_messages["required"], code="required"
            )

        self.local_ids = {}
        for val in value:
            form = self.form_class(val)
            if not form.is_valid():
                raise ValidationError(message = f'There is an error at \'{val}\'')
            else:
                new_id = str(form.cleaned_data['id'])
                if new_id in self.local_ids.keys():
                    raise ValidationError('id is not unique in the imported set')
                else:
                    self.local_ids[new_id] = val

        self.all_ids = set(self.local_ids)
        for item in self.local_ids.values():
            try:
                parent_id = item.get('parentId', None)
                parent = self.local_ids.get(parent_id, None)
                if parent and parent['type'] != ItemType.CATEGORY.value:
                    raise ValidationError(f'Only {ItemType.CATEGORY.value} can be a parent')
                if parent_id:
                    self.all_ids.add(parent_id)
            except KeyError:
                continue


class ImportForm(forms.Form):
    items = ListField(item_form_class=ImportItemForm)
    updateDate = forms.DateTimeField()


class NodeForm(forms.Form):
    id = forms.UUIDField()
