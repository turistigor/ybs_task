from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
import django.forms as forms
from django.core.exceptions import ValidationError

import json


class ImportItemForm(forms.Form):
    id = forms.UUIDField()
    name = forms.CharField(max_length=200)
    parentId = forms.UUIDField()
    type = forms.ChoiceField(
        choices=(('OFFER', 'OFFER'), ('CATEGORY', 'CATEGORY'))
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
        if self.required and not value:
            raise ValidationError(
                self.error_messages["required"], code="required"
            )

        ids = set()

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
                if new_id in ids:
                    raise ValidationError('id is not unique in the imported set')
                else:
                    ids.add(new_id)


class ImportForm(forms.Form):
    items = ListField(item_form_class=ImportItemForm)
    updateDate = forms.DateTimeField()


class PricesComparatorView(View):
    def post(self, request):
        data = json.loads(request.body.decode())
        import_form = ImportForm(data)

        if import_form.is_valid():
            #TODO: create db models, validate and save
            return HttpResponse()
        else:
            return HttpResponseBadRequest(json.dumps({
                "code": 400,
                "message": "Validation Failed"
            }))

    def get(self, request):
        return HttpResponse('It works!')
