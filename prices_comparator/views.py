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

            ids = getattr(import_form.fields.get('items', None), 'ids', {})
            update_date = import_form.cleaned_data['updateDate']

            with transaction.atomic():
                while len(ids):
                    item = ids[list(ids)[0]]
                    self._check_db_consistency(item)
                    _, used_ids = self._save_model_rec(item, ids, update_date)
                    for used_id in used_ids:
                        del ids[used_id]

        except (JSONDecodeError, IntegrityError, ValidationError):
            return self._http_resp_bad_request

        return HttpResponse()

    def get(self, request, *args, **kwargs):
        return self._process_node(request.method, kwargs['id'])

    def delete(self, request, *args, **kwargs):
        return self._process_node(request.method, kwargs['id'])

    def _check_db_consistency(self, item):
        try:
            m = ImportModel.objects.get(id=item['id'])
        except ImportModel.DoesNotExist:
            pass
        else:
            if m.type != item['type']:
                raise ValidationError(message="You can't change item type")

    def _save_model_rec(self, item, ids, update_date, used_ids=None):
        parent_id = item.get('parentId', None)
        used_ids = used_ids or set()
        if parent_id in ids:
            parent_model, used_ids = self._save_model_rec(
                ids[parent_id], ids, update_date, used_ids
            )
        else:
            try:
                parent_model = ImportModel.objects.get(id=parent_id)
            except ImportModel.DoesNotExist:
                parent_model = None

        m = ImportModel(
            id=item['id'], name=item['name'], parent_id=parent_model, 
            type=item['type'], price=item.get('price', None), date=update_date
        )
        used_ids.add(item['id'])
        m.save()
        return m, used_ids

    def _process_node(self, request_method, node_id):
        try:
            node_id = self._get_node_id(node_id)

            with transaction.atomic():
                if request_method == 'GET':
                    resp_content = self._get_node_json(node_id)
                    return HttpResponse(resp_content)
                elif request_method == 'DELETE':
                    self._delete_node(node_id)
                    return HttpResponse()

        except ValidationError:
            return self._http_resp_bad_request

        except ImportModel.DoesNotExist:
            return self._http_resp_not_found

    def _get_node_id(self, node_id):
        node_form = NodeForm({'id': node_id})
        if not node_form.is_valid():
            raise ValidationError(message='Validation error')

        return node_form.cleaned_data['id']

    def _get_node_json(self, node_id):
        node_model = ImportModel.objects.get(id=node_id)
        item = self._model_to_dict(node_model)
        return json.dumps(item)

    def _model_to_dict(self, node):
        children = [
            self._model_to_dict(child) for child in self._get_node_children(node)
        ]

        d = model_to_dict(node)

        return self._stringify(d, children)

    def _get_node_children(self, node):
        return (child for child in node.importmodel_set.all())

    def _stringify(self, d, children):
        ''' some fields are converted to strings to become jsonable '''

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

    def _delete_node(self, node_id):
        res = ImportModel.objects.filter(id=node_id).delete()
        if not res[0]:
            raise ImportModel.DoesNotExist()

