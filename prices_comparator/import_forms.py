import django.forms as forms
from django.core.exceptions import ValidationError

import prices_comparator.common as const


class ImportItemForm(forms.Form):
    id = forms.UUIDField()
    name = forms.CharField(max_length=const.IMPORT_UNIT_NAME_MAX_LENGTH)
    parentId = forms.UUIDField()
    type = forms.ChoiceField(
        choices=const.IMPORT_UNIT_TYPE_CHOICES
    )
    price = forms.IntegerField(min_value=0, required=False)

    def clean(self):
        item_type = self.cleaned_data.get('type', None)
        price = self.cleaned_data.get('price', None)

        if item_type == 'CATEGORY':
            if isinstance(price, int):
                raise ValidationError(message='price for category isn\'t null')
        elif item_type == 'OFFER':
            if not isinstance(price, int) or price < 0:
                raise ValidationError(message='price for category isn\'t null')

        return super().clean()


class ListField(forms.MultipleChoiceField):
    def __init__(self, *args, item_form_class=None, **kwargs):
        self.form_class = item_form_class
        super().__init__()

    def to_python(self, values):
        if not values:
            return []
        elif not isinstance(values, (list, tuple)):
            raise ValidationError(
                self.error_messages["invalid_list"], code="invalid_list"
            )
        return values

    def validate(self, value):
        self.ids = {}
        if self.required and not value:
            raise ValidationError(
                self.error_messages["required"], code="required"
            )

        for val in value:
            form = self.form_class(val)
            if not form.is_valid():
                raise ValidationError(
                    self.error_messages["invalid_choice"],
                    code="invalid_choice",
                    params={"value": val},
                )
            else:
                new_id = form.cleaned_data['id']
                if new_id in self.ids.keys():
                    raise ValidationError('id is not unique in the imported set')
                else:
                    self.ids[new_id] = val


class ImportForm(forms.Form):
    items = ListField(item_form_class=ImportItemForm)
    updateDate = forms.DateTimeField()

