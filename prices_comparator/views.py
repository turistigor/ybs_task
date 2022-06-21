from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
from django.forms import ValidationError
from django.db import IntegrityError, transaction

import json
from json.decoder import JSONDecodeError

from prices_comparator.import_forms import ImportForm
from prices_comparator.models import ImportModel


class PricesComparatorView(View):

    _http_resp_bad_request = HttpResponseBadRequest(json.dumps({
        "code": 400,
        "message": "Validation Failed"
    }))

    @transaction.atomic
    def post(self, request):
        try:
            data = json.loads(request.body.decode())

            import_form = ImportForm(data)
            if not import_form.is_valid():
                raise ValidationError(message='Validation error')
            items = import_form.cleaned_data.get('items', [])

            for item in items:
                ids = getattr(import_form.fields.get('items', None), 'ids', {})
                self.save_model_rec(item, ids, import_form.cleaned_data['updateDate'])

        except (JSONDecodeError, IntegrityError, ValidationError):
            return self._http_resp_bad_request

        return HttpResponse()
            

    def save_model_rec(self, item, ids, update_date):
        parent_id = item.get('parent_id', None)
        if parent_id in ids:
            parent_model = self.save_model_rec(ids[item.parent_id], ids, update_date)
            del ids[item.parent_id]
            parent_model.save()
        else:
            try:
                parent_model = ImportModel.objects.get(id=parent_id)
            except ImportModel.DoesNotExist:
                parent_model = None

        m = ImportModel(
            id=item['id'], name=item['name'], parent_id=parent_model, 
            type=item['type'], price=item.get('price', None), date=update_date
        )
        m.save()

    def get(self, request):
        return HttpResponse('It works!')
