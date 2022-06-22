from datetime import datetime
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.forms import ValidationError
from django.forms.models import model_to_dict
from django.db import IntegrityError, transaction

import json
from json.decoder import JSONDecodeError

from prices_comparator.import_forms import ImportForm, NodeForm
from prices_comparator.models import ImportModel


class PricesComparatorView(View):

    _http_resp_bad_request = HttpResponseBadRequest(json.dumps({
        'code': 400,
        'message': 'Validation Failed'
    }))

    _http_resp_not_found = HttpResponseNotFound(json.dumps({
        'code': 404,
        'message': 'Item not found'
    }))

    def post(self, request):
        try:
            data = json.loads(request.body.decode())

            import_form = ImportForm(data)
            if not import_form.is_valid():
                raise ValidationError(message='Validation error')
            items = import_form.cleaned_data.get('items', [])

            with transaction.atomic():
                for item in items:
                    ids = getattr(import_form.fields.get('items', None), 'ids', {})
                    self._save_model_rec(item, ids, import_form.cleaned_data['updateDate'])

        except (JSONDecodeError, IntegrityError, ValidationError):
            return self._http_resp_bad_request

        return HttpResponse()

    def _save_model_rec(self, item, ids, update_date):
        parent_id = item.get('parent_id', None)
        if parent_id in ids:
            parent_model = self._save_model_rec(ids[item.parent_id], ids, update_date)
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

    def _get_node_children(self, node):
        qs = node.importmodel_set.all().values()
        return (model_to_dict(child) for child in qs)

    def _stringify(self, node, children):
        # some fields are converted to strings to become jsonable
        d = model_to_dict(node)

        d['children'] = children
        d['id'] = str(d['id'])
        try:
            parent_id = d['parent_id']
            d['parentId'] = str(d['parent_id']) if parent_id else None
            del d['parent_id']
        except KeyError:
            pass
        d['date'] = datetime.isoformat(d['date'])
        return d

    def _model_to_dict(self, node):
        #TODO: try to use generator here
        children = [
            self._model_to_dict(child) for child in self._get_node_children(node)
        ]
        #TODO: price of category is the average price of all offers in it
        #TODO: children for empty cat is an empty list; for offer is null

        return self._stringify(node, children)

    def get(self, request, *args, **kwargs):
        node_form = NodeForm({'id': kwargs['id']})

        try:
            if not node_form.is_valid():
                raise ValidationError(message='Validation error')

            node_id = node_form.cleaned_data['id']

            with transaction.atomic():
                node_model = ImportModel.objects.get(id=node_id)
                item = self._model_to_dict(node_model)

        except ValidationError:
            return self._http_resp_bad_request

        except ImportModel.DoesNotExist:
            return self._http_resp_not_found

        return HttpResponse(json.dumps(item))
