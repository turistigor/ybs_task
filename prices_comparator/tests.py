from django.test import TestCase
from django.utils.dateparse import parse_datetime

import requests as http
import json
import os
import copy


class HttpMixin:
    def _send_imports_post(self, data):
        return http.post(url=self._imports_url, 
                         data=json.dumps(data))

    def _send_nodes_get(self, id):
        return http.get(url=f'{self._get_nodes_url()}{id}')

    def _send_nodes_delete(self, id):
        return http.delete(url=f'{self._get_nodes_url()}{id}')

    @classmethod
    def _get_host(self):
        host = os.environ.get('WEB_HOST', 'http://127.0.0.1')
        port = os.environ.get('WEB_PORT', '80')
        return f'{host}:{port}'

    @classmethod
    def _get_imports_url(cls):
        host = cls._get_host()
        return f'{host}/imports'

    @classmethod
    def _get_nodes_url(cls):
        host = cls._get_host()
        return f'{host}/nodes/'

    @classmethod
    def _get_delete_url(cls):
        host = cls._get_host()
        return f'{host}/delete/'


class TestCommonMixin:
    DATE_TIME_WITH_TZ = '2022-05-28T21:12:01.000Z'

    normal_item = {
        'id': '3fa85f64-5717-4562-b3fc-2c963f66a444',
        'name': 'Оффер',
        'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
        'type': 'OFFER',
        'price': 234,
    }

    _validation_failed = {
        'code': 400,
        'message': 'Validation Failed'
    }

    _item_not_found = {
        'code': 404,
        'message': 'Item not found'
    }

    def check_validation_failed(self, resp):
        self.assertEqual(resp.status_code, 400)
        self.assertDictEqual(
            json.loads(resp.content.decode()), self._validation_failed
        )

    def check_item_not_found(self, resp):
        self.assertEqual(resp.status_code, 404)
        self.assertDictEqual(
            json.loads(resp.content.decode()), self._item_not_found
        )


class ImportTest(TestCase, HttpMixin, TestCommonMixin):
    @classmethod
    def setUpTestData(cls):
        cls._imports_url = cls._get_imports_url()

    def test_updateDate(self):
        # request without field
        data = {'items':[self.normal_item]}
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

        # incorrect value"
        data = {'items':[self.normal_item], 'updateDate': 'asdasd2wef'}
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

        # empty value
        data = {'items':[self.normal_item], 'updateDate': ''}
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

        # None value
        data = {'items':[self.normal_item], 'updateDate': None}
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

    def test_items(self):
        # request without field
        data = {'updateDate': self.DATE_TIME_WITH_TZ}
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

    def test_item_id(self):
        # request without field
        data = {'updateDate': self.DATE_TIME_WITH_TZ, 'items': [{
            'name': 'Оффер',
            'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
            'type': 'OFFER',
            'price': 234,
        },]}
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

        # id is not valid uuid
        data = {
            'updateDate': self.DATE_TIME_WITH_TZ,
            'items': [{
                    'id': 'asdew83rnf c',
                    'name': 'Фрукт',
                    'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'type': 'OFFER',
                    'price': 100,
                },
                self.normal_item
            ]
        }
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

        # id is empty
        data = {
            'updateDate': self.DATE_TIME_WITH_TZ,
            'items': [{
                    'id': '',
                    'name': 'Фрукт',
                    'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'type': 'OFFER',
                    'price': 100,
                },
                self.normal_item
            ]
        }
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

        # id is None
        data = {
            'updateDate': self.DATE_TIME_WITH_TZ,
            'items': [{
                    'id': None,
                    'name': 'Фрукт',
                    'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'type': 'OFFER',
                    'price': 100,
                },
                self.normal_item
            ]
        }
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

        # there are two identical id
        data = {
            'updateDate': self.DATE_TIME_WITH_TZ, 
            'items': [{
                    'id': self.normal_item['id'],
                    'name': 'Фрукт',
                    'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'type': 'OFFER',
                    'price': 100,
                },
                self.normal_item
            ]
        }
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

    def test_parent_id(self):
        # parentId is not valid uuid
        data = {
            'updateDate': self.DATE_TIME_WITH_TZ, 
            'items': [{
                    'id': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'name': 'Фрукт',
                    'parentId': 'asdew83rnf c',
                    'type': 'OFFER',
                    'price': 100,
                },
                self.normal_item
            ]
        }
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

    def test_name(self):
        # request without field
        data = {'updateDate': self.DATE_TIME_WITH_TZ, 'items': [{
            'id': '3fa85f64-5717-4562-b3fc-2c963f66a333',
            'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
            'type': 'OFFER',
            'price': 234,
        },]}
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

        # name is to long
        data = {
            'updateDate': self.DATE_TIME_WITH_TZ,
            'items': [{
                    'id': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'name': 201*'a',
                    'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'type': 'OFFER',
                    'price': 100,
                },
                self.normal_item
            ]
        }
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

        # name is empty
        data = {
            'updateDate': self.DATE_TIME_WITH_TZ,
            'items': [{
                    'id': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'name': '',
                    'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'type': 'OFFER',
                    'price': 100,
                },
                self.normal_item
            ]
        }
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

        # name is None
        data = {
            'updateDate': self.DATE_TIME_WITH_TZ,
            'items': [{
                    'id': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'name': None,
                    'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'type': 'OFFER',
                    'price': 100,
                },
                self.normal_item
            ]
        }
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

    def test_type(self):
        # request without field
        data = {'updateDate': self.DATE_TIME_WITH_TZ, 'items': [{
            'id': '3fa85f64-5717-4562-b3fc-2c963f66a333',
            'name': 'Оффер',
            'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
            'price': 234,
        },]}
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

        # type is not valid
        data = {
            'updateDate': self.DATE_TIME_WITH_TZ, 
            'items': [{
                    'id': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'name': 'Фрукт',
                    'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'type': ';wlmf;klw',
                    'price': 100,
                },
                self.normal_item
            ]
        }
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

        # type is empty
        data = {
            'updateDate': self.DATE_TIME_WITH_TZ,
            'items': [{
                    'id': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'name': 'Фрукт',
                    'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'type': '',
                    'price': 100,
                },
                self.normal_item
            ]
        }
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

        # type is None
        data = {
            'updateDate': self.DATE_TIME_WITH_TZ,
            'items': [{
                    'id': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'name': 'Фрукт',
                    'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'type': None,
                    'price': 100,
                },
                self.normal_item
            ]
        }
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

    def test_price(self):
        # price is nan for offer
        data = {
            'updateDate': self.DATE_TIME_WITH_TZ,
            'items': [{
                    'id': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'name': 'Фрукт',
                    'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'type': 'OFFER',
                    'price': 'sd',
                },
                self.normal_item
            ]
        }
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

        # price is negative for offer
        data = {
            'updateDate': self.DATE_TIME_WITH_TZ,
            'items': [{
                    'id': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'name': 'Фрукт',
                    'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'type': 'OFFER',
                    'price': -3,
                },
                self.normal_item
            ]
        }
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

        # price is None for offer
        data = {
            'updateDate': self.DATE_TIME_WITH_TZ,
            'items': [{
                    'id': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'name': 'Фрукт',
                    'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'type': 'OFFER',
                    'price': None,
                },
                self.normal_item
            ]
        }
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

        # price is empty for offer
        data = {
            'updateDate': self.DATE_TIME_WITH_TZ,
            'items': [{
                    'id': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'name': 'Фрукт',
                    'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'type': 'OFFER',
                    'price': '',
                },
                self.normal_item
            ]
        }
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

        # price is not null for category
        data = {
            'updateDate': self.DATE_TIME_WITH_TZ,
            'items': [{
                    'id': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'name': 'Фрукт',
                    'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'type': 'CATEGORY',
                    'price': 11,
                },
                self.normal_item
            ]
        }
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

    def test_parents_only_groups(self):
        data = {
            'updateDate': self.DATE_TIME_WITH_TZ,
            'items': [{
                'id': '21111111-1111-1111-1111-111111111111',
                'name': 'car',
                'type': 'OFFER',
                'price': 1002,
            },{
                'id': '31111111-1111-1111-1111-111111111111',
                'parentId': '21111111-1111-1111-1111-111111111111',
                'name': 'wheel',
                'type': 'OFFER',
                'price': 10,
            }]
        }
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)


class IntegratedTest(TestCase, HttpMixin, TestCommonMixin):

    @classmethod
    def setUpTestData(cls):
        cls._imports_url = cls._get_imports_url()
        cls._nodes_url = cls._get_nodes_url()

        cls._items = [{
            'id': '11111111-1111-1111-1111-111111111111',
            'name': 'Продукты',
            'parentId': None,
            'type': 'CATEGORY',
            'price': 52,
            'date': cls.DATE_TIME_WITH_TZ,
            'children': [{
                'id': '11111111-1111-1111-1111-111111111112',
                'parentId': '11111111-1111-1111-1111-111111111111',
                'name': 'Овощи',
                'price': 52,
                'type': 'CATEGORY',
                'date': cls.DATE_TIME_WITH_TZ,
                'children': [{
                    'id': '11111111-1111-1111-1111-111111111113',
                    'parentId': '11111111-1111-1111-1111-111111111112',
                    'name': 'Огурцы',
                    'price': 11,
                    'type': 'OFFER',
                    'date': cls.DATE_TIME_WITH_TZ,
                    'children': [],
                },{
                    'id': '11111111-1111-1111-1111-111111111114',
                    'parentId': '11111111-1111-1111-1111-111111111112',
                    'name': 'Подовощи',
                    'price':  72,
                    'type': 'CATEGORY',
                    'date': cls.DATE_TIME_WITH_TZ,
                    'children': [{
                        'id': '11111111-1111-1111-1111-111111111115',
                        'parentId': '11111111-1111-1111-1111-111111111114',
                        'name': 'Помидоры',
                        'price': 114,
                        'type': 'OFFER',
                        'date': cls.DATE_TIME_WITH_TZ,
                        'children': [],
                    }, {
                        'id': '11111111-1111-1111-1111-111111111116',
                        'parentId': '11111111-1111-1111-1111-111111111114',
                        'name': 'Морковь',
                        'price': 31,
                        'type': 'OFFER',
                        'date': cls.DATE_TIME_WITH_TZ,
                        'children': [],
                    }],
                }],
            }]
        }]

    def flatten(self, items, res=None):
        res = res or []
        for item in items:
            citem = copy.deepcopy(item)

            if citem['type'] == 'CATEGORY':
                citem['price'] = None

            if 'children' in citem:
                res = self.flatten(citem['children'], res)
                citem.pop('children')

            res.append(citem)
        return res

    def _get_crud_data(self):
        return {
            'updateDate': self.DATE_TIME_WITH_TZ, 
            'items': self.flatten(self._items)
        }

    def _create(self, data):
        resp = self._send_imports_post(data)
        self.assertEqual(resp.status_code, 200)

    def _assert_node(self, item, saved_obj):
        self.assertEqual(saved_obj['id'], item['id'])
        self.assertEqual(saved_obj['name'], item['name'])
        self.assertEqual(saved_obj['parentId'], item['parentId'])
        self.assertEqual(saved_obj['type'], item['type'])
        self.assertEqual(saved_obj['price'], item.get('price', None))
        self.assertEqual(
            parse_datetime(saved_obj['date']), parse_datetime(item['date'])
        )
        self.assertEqual('children' in saved_obj, 'children' in item)
        if item.get('children', None):
            for saved_child in saved_obj['children']:
                for item_child in item['children']:
                    if item_child['id'] == saved_child['id']:
                        self._assert_node(item_child, saved_child)
                        break
                else:
                    self.assertEqual(True, False, f"{saved_child['id']}")

    def _read(self, item, expected_found=True):
        resp = self._send_nodes_get(item['id'])
        if expected_found:
            self.assertEqual(resp.status_code, 200)
            saved_obj = json.loads(resp.content.decode())
            self._assert_node(item, saved_obj)
        else:
            self.check_item_not_found(resp)

    def _delete(self, item_id, expected_found=True):
        resp = self._send_nodes_delete(item_id)
        if expected_found:
            self.assertEqual(resp.status_code, 200)
        else:
            self.check_item_not_found(resp)

    def test_CRUD(self):
        data = self._get_crud_data()

        #create
        self._create(data)
        self._read(self._items[0])

        #update
        self._items[0].update(name=self._items[0]['name'] + '!!!')
        data['items'] = self.flatten(self._items)
        self._create(data)
        self._read(self._items[0])

        #delete
        deleted_item = self._items[0]['children'][0]['children'].pop(0)
        self._delete(deleted_item['id'])
        self._items[0]['price'] = 72
        self._items[0]['children'][0]['price'] = 72
        self._read(deleted_item, expected_found=False)
        self._read(self._items[0])

        deleted_item = self._items[0]['children'][0]['children'].pop(0)
        self._delete(deleted_item['id'])
        self._items[0]['price'] = None
        self._items[0]['children'][0]['price'] = None
        self._read(deleted_item, expected_found=False)
        self._read(deleted_item['children'][0], expected_found=False)
        self._read(deleted_item['children'][1], expected_found=False)
        self._read(self._items[0])

        deleted_item = self._items.pop(0)
        self._delete(deleted_item['id'])
        self._read(deleted_item, expected_found=False)
        self._read(deleted_item['children'][0], expected_found=False)

    def test_update_type(self):
        # can't change type for existing item
        data = {
            'updateDate': self.DATE_TIME_WITH_TZ,
            'items': [{
                'id': '1fa85f64-5717-4562-b3fc-2c963f66a333',
                'name': 'Фрукт',
                'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                'type': 'OFFER',
                'price': 100,
            }]
        }
        resp = self._send_imports_post(data)
        self.assertEqual(resp.status_code, 200)

        data['items'][0]['type'] = 'CATEGORY'
        data['items'][0]['price'] = None
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

        self._delete(data['items'][0]['id'])

    def test_parents_only_groups(self):
        data = {
            'updateDate': self.DATE_TIME_WITH_TZ,
            'items': [{
                'id': '21111111-1111-1111-1111-111111111111',
                'name': 'car',
                'type': 'OFFER',
                'price': 1002,
            }]
        }
        resp = self._send_imports_post(data)
        self.assertEqual(resp.status_code, 200)

        data = {
            'updateDate': self.DATE_TIME_WITH_TZ,
            'items':[{
                'id': '31111111-1111-1111-1111-111111111111',
                'parentId': '21111111-1111-1111-1111-111111111111',
                'name': 'wheel',
                'type': 'OFFER',
                'price': 10,
            }]
        }
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

        self._delete('21111111-1111-1111-1111-111111111111')

    def test_update_to_null_parent(self):
        data = {
            'updateDate': self.DATE_TIME_WITH_TZ,
            'items': [{
                'id': '21111111-1111-1111-1111-111111111111',
                'name': 'car',
                'type': 'CATEGORY',
                'price': None
            }, {
                'id': '31111111-1111-1111-1111-111111111111',
                'parentId': '21111111-1111-1111-1111-111111111111',
                'name': 'wheel',
                'type': 'OFFER',
                'price': 10,
            }]
        }
        resp = self._send_imports_post(data)
        self.assertEqual(resp.status_code, 200)

        data = {
            'updateDate': self.DATE_TIME_WITH_TZ,
            'items': [{
                'id': '31111111-1111-1111-1111-111111111111',
                'parentId': None,
                'name': 'whEEl',
                'type': 'OFFER',
                'price': 11,
            }]
        }

        resp = self._send_imports_post(data)
        self.assertEqual(resp.status_code, 200)

        resp = self._send_nodes_get('31111111-1111-1111-1111-111111111111')
        saved = json.loads(resp.content.decode())
        self.assertIsNone(saved['parentId'])

        self._delete('21111111-1111-1111-1111-111111111111')
        self._delete('31111111-1111-1111-1111-111111111111')