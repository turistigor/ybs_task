from django.test import TestCase
from django.utils.dateparse import parse_datetime

import requests as http
import json
import os
from datetime import datetime


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


DATE_TIME_WITH_TZ = '2022-05-28T21:12:01.000Z'
DATE_TIME_WITH_OFFSET = '20022-10-25T14:30+02:00'


class ImportTest(TestCase, HttpMixin):
    @classmethod
    def setUpTestData(cls):
        cls.normal_item = {
            'id': '3fa85f64-5717-4562-b3fc-2c963f66a444',
            'name': 'Оффер',
            'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
            'type': 'OFFER',
            'price': 234,
        }

        cls._validation_failed = {
            "code": 400,
            "message": "Validation Failed"
        }

        cls._imports_url = cls._get_imports_url()

    def check_validation_failed(self, resp):
        self.assertEqual(resp.status_code, 400)
        self.assertDictEqual(
            json.loads(resp.content.decode()), self._validation_failed
        )

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
        data = {'updateDate': DATE_TIME_WITH_TZ}
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

    def test_item_id(self):
        # request without field
        data = {'updateDate': DATE_TIME_WITH_OFFSET, 'items': [{
            'name': 'Оффер',
            'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
            'type': 'OFFER',
            'price': 234,
        },]}
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

        # id is not valid uuid
        data = {
            'updateDate': DATE_TIME_WITH_TZ,
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
            'updateDate': DATE_TIME_WITH_OFFSET,
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
            'updateDate': DATE_TIME_WITH_TZ,
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
            'updateDate': DATE_TIME_WITH_OFFSET, 
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
            'updateDate': DATE_TIME_WITH_TZ, 
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
        data = {'updateDate': DATE_TIME_WITH_TZ, 'items': [{
            'id': '3fa85f64-5717-4562-b3fc-2c963f66a333',
            'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
            'type': 'OFFER',
            'price': 234,
        },]}
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

        # name is to long
        data = {
            'updateDate': DATE_TIME_WITH_OFFSET,
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
            'updateDate': DATE_TIME_WITH_TZ,
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
            'updateDate': DATE_TIME_WITH_OFFSET,
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
        data = {'updateDate': DATE_TIME_WITH_TZ, 'items': [{
            'id': '3fa85f64-5717-4562-b3fc-2c963f66a333',
            'name': 'Оффер',
            'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
            'price': 234,
        },]}
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

        # type is not valid
        data = {
            'updateDate': DATE_TIME_WITH_OFFSET, 
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
            'updateDate': DATE_TIME_WITH_OFFSET,
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
            'updateDate': DATE_TIME_WITH_OFFSET,
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
        # price is nan
        data = {
            'updateDate': DATE_TIME_WITH_OFFSET,
            'items': [{
                    'id': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'name': 'Фрукт',
                    'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'type': 'CATEGORY',
                    'price': 'sd',
                },
                self.normal_item
            ]
        }
        resp = self._send_imports_post(data)
        self.check_validation_failed(resp)

        # price is negative
        data = {
            'updateDate': DATE_TIME_WITH_OFFSET,
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
            'updateDate': DATE_TIME_WITH_OFFSET,
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
            'updateDate': DATE_TIME_WITH_OFFSET,
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
            'updateDate': DATE_TIME_WITH_OFFSET,
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


class IntegratedTest(TestCase, HttpMixin):

    @classmethod
    def setUpTestData(cls):
        cls._imports_url = cls._get_imports_url()
        cls._nodes_url = cls._get_nodes_url()

    def _get_crud_data(self):
        return {
            'updateDate': DATE_TIME_WITH_TZ, 
            'items': [
                {
                    'id': '11111111-1111-1111-1111-111111111111',
                    'name': 'Продукты',
                    'parentId': None,
                    'type': 'CATEGORY'
                }
            ]
        }

    def _create(self, data):
        resp = self._send_imports_post(data)
        self.assertEqual(resp.status_code, 200)

    def _assert_node(self, item, update_date, resp):
        saved_obj = json.loads(resp.content.decode())
        self.assertEqual(saved_obj['id'], item['id'])
        self.assertEqual(saved_obj['name'], item['name'])
        self.assertEqual(saved_obj['parentId'], item['parentId'])
        self.assertEqual(saved_obj['type'], item['type'])
        self.assertEqual(saved_obj['price'], item.get('price', None))
        self.assertEqual(
            parse_datetime(saved_obj['date']), parse_datetime(update_date)
        )

    def _read(self, data, expected_found=True):
        resp = self._send_nodes_get(data['items'][0]['id'])
        if expected_found:
            self.assertEqual(resp.status_code, 200)
            self._assert_node(data['items'][0], data['updateDate'], resp)
        else:
            self.assertEqual(resp.status_code, 404)

    def _update(self, data):
        resp = self._send_imports_post(data)
        self.assertEqual(resp.status_code, 200)

    def _delete(self, data, expected_found=True):
        resp = self._send_nodes_delete(data['items'][0]['id'])
        if expected_found:
            self.assertEqual(resp.status_code, 200)
        else:
            self.assertEqual(resp.status_code, 404)

    def test_CRUD(self):
        data = self._get_crud_data()

        #create
        self._create(data)
        self._read(data)

        #update
        data['items'][0].update(name='Продукты питания')
        self._create(data)
        self._read(data)

        #delete
        self._delete(data)
        self._read(data, expected_found=False)
        self._delete(data, expected_found=False)


