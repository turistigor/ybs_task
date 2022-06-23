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

            local_ids = getattr(import_form.fields.get('items', None), 'local_ids', {})
            all_ids = getattr(import_form.fields.get('items', None), 'all_ids', {})
            update_date = import_form.cleaned_data['updateDate']

            with transaction.atomic():
                models = self._get_models_by_ids(all_ids)

                while local_ids:
                    __, item = local_ids.popitem()
                    self._save_model_with_parents(item, local_ids, models, update_date)

        except (JSONDecodeError, IntegrityError, ValidationError, KeyError) as ex:
            return self._http_resp_bad_request

        return HttpResponse()

    def get(self, request, *args, **kwargs):
        return self._process_node(request.method, kwargs['id'])

    def delete(self, request, *args, **kwargs):
        return self._process_node(request.method, kwargs['id'])

    @staticmethod
    def _get_models_by_ids(ids):
        return {
            str(m.id): m for m in ImportModel.objects.filter(
                id__in=ids
            )
        }

    def _save_model_with_parents(self, item, ids, db_ids, update_date):
        parent_model = self._get_parent_model(item, ids, db_ids, update_date)
        model_type = getattr(db_ids[item['id']], 'type') if item['id'] in db_ids else None
        self._check_item_integrity(parent_model, item['type'], model_type)

        m = ImportModel(
            id=item['id'], name=item['name'], parent_id=parent_model, 
            type=item['type'], price=item.get('price', None), date=update_date
        )
        m.save()

        db_ids[item['id']] = m
        ids.pop(item['id'], None)

        return m

    def _get_parent_model(self, item, ids, db_ids, update_date):
        parent_id = item.get('parentId', None)
        if parent_id in ids:
            return self._save_model_with_parents(
                ids[parent_id], ids, db_ids, update_date
            )
        return db_ids.get(parent_id, None)

    @staticmethod
    def _check_item_integrity(parent_model, item_type, model_type):
        if parent_model and parent_model.type != 'CATEGORY':
            raise IntegrityError('Only CATEGORY can be a parent')
        if model_type and item_type != model_type:
            raise IntegrityError('You can\'t change item type')

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

    @staticmethod
    def _get_node_id(node_id):
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

    @staticmethod
    def _get_node_children(node):
        return (child for child in node.importmodel_set.all())

    @staticmethod
    def _stringify(d, children):
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

    @staticmethod
    def _delete_node(node_id):
        res = ImportModel.objects.filter(id=node_id).delete()
        if not res[0]:
            raise ImportModel.DoesNotExist()

