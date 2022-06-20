from django.test import TestCase

import requests as http
import json


class ImportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.normal_item = {
            'id': '3fa85f64-5717-4562-b3fc-2c963f66a444',
            'name': 'Оффер',
            'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
            'type': 'OFFER',
            'price': 234,
        }

        cls.normal_update_date = '2022-05-28T21:12:01.000Z'

        cls._validation_failed = {
            "code": 400,
            "message": "Validation Failed"
        }

        cls._imports_url = 'http://127.0.0.1:80/imports'

    def _send(self, data):
        return http.post(url=self._imports_url, 
                         data=json.dumps(data))

    def check_validation_failed(self, resp):
        self.assertEqual(resp.status_code, 400)
        self.assertDictEqual(
            json.loads(resp.content.decode()), self._validation_failed
        )

    def test_updateDate(self):
        # request without field
        data = {'items':[self.normal_item]}
        resp = self._send(data)
        self.check_validation_failed(resp)

        # incorrect value"
        data = {'items':[self.normal_item], 'updateDate': 'asdasd2wef'}
        resp = self._send(data)
        self.check_validation_failed(resp)

        # empty value
        data = {'items':[self.normal_item], 'updateDate': ''}
        resp = self._send(data)
        self.check_validation_failed(resp)

        # None value
        data = {'items':[self.normal_item], 'updateDate': None}
        resp = self._send(data)
        self.check_validation_failed(resp)

        # short date-time format
        data = {'items':[self.normal_item], 'updateDate': '2006-10-25 14:30'}
        resp = self._send(data)
        self.assertEqual(resp.status_code, 200)

        # date-time with offset
        data = {'items':[self.normal_item], 'updateDate': '2006-10-25T14:30+02:00'}
        resp = self._send(data)
        self.assertEqual(resp.status_code, 200)

    def test_items(self):
        # request without field
        data = {'updateDate': self.normal_update_date}
        resp = self._send(data)
        self.check_validation_failed(resp)

    def test_item_id(self):
        # request without field
        data = {'updateDate': self.normal_update_date, 'items': [{
            'name': 'Оффер',
            'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
            'type': 'OFFER',
            'price': 234,
        },]}
        resp = self._send(data)
        self.check_validation_failed(resp)

        # id is not valid uuid
        data = {
            'updateDate': self.normal_update_date,
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
        resp = self._send(data)
        self.check_validation_failed(resp)

        # id is empty
        data = {
            'updateDate': self.normal_update_date,
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
        resp = self._send(data)
        self.check_validation_failed(resp)

        # id is None
        data = {
            'updateDate': self.normal_update_date,
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
        resp = self._send(data)
        self.check_validation_failed(resp)

        # there are two identical id
        data = {
            'updateDate': self.normal_update_date, 
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
        resp = self._send(data)
        self.check_validation_failed(resp)

    def test_parent_id(self):
        # parentId is not valid uuid
        data = {
            'updateDate': self.normal_update_date, 
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
        resp = self._send(data)
        self.check_validation_failed(resp)

    def test_name(self):
        # request without field
        data = {'updateDate': self.normal_update_date, 'items': [{
            'id': '3fa85f64-5717-4562-b3fc-2c963f66a333',
            'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
            'type': 'OFFER',
            'price': 234,
        },]}
        resp = self._send(data)
        self.check_validation_failed(resp)

        # name is to long
        data = {
            'updateDate': self.normal_update_date,
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
        resp = self._send(data)
        self.check_validation_failed(resp)

        # name is empty
        data = {
            'updateDate': self.normal_update_date,
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
        resp = self._send(data)
        self.check_validation_failed(resp)

        # name is None
        data = {
            'updateDate': self.normal_update_date,
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
        resp = self._send(data)
        self.check_validation_failed(resp)

    def test_type(self):
        # request without field
        data = {'updateDate': self.normal_update_date, 'items': [{
            'id': '3fa85f64-5717-4562-b3fc-2c963f66a333',
            'name': 'Оффер',
            'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
            'price': 234,
        },]}
        resp = self._send(data)
        self.check_validation_failed(resp)

        # type is not valid
        data = {
            'updateDate': self.normal_update_date, 
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
        resp = self._send(data)
        self.check_validation_failed(resp)

        # type is empty
        data = {
            'updateDate': self.normal_update_date,
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
        resp = self._send(data)
        self.check_validation_failed(resp)

        # type is None
        data = {
            'updateDate': self.normal_update_date,
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
        resp = self._send(data)
        self.check_validation_failed(resp)

    def test_price(self):
        # price is nan
        data = {
            'updateDate': self.normal_update_date,
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
        resp = self._send(data)
        self.check_validation_failed(resp)

        # price is negative
        data = {
            'updateDate': self.normal_update_date,
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
        resp = self._send(data)
        self.check_validation_failed(resp)

        # price is None for offer
        data = {
            'updateDate': self.normal_update_date,
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
        resp = self._send(data)
        self.check_validation_failed(resp)

        # price is empty for offer
        data = {
            'updateDate': self.normal_update_date,
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
        resp = self._send(data)
        self.check_validation_failed(resp)

        # price is not null for category
        data = {
            'updateDate': self.normal_update_date,
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
        resp = self._send(data)
        self.check_validation_failed(resp)

    def test_all_fields_correct(self):
        data = {
            'updateDate': self.normal_update_date, 
            'items': [
                {
                    'id': '3fa85f64-5717-4562-b3fc-2c963f66a332',
                    'name': 'Фрукт',
                    'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'type': 'CATEGORY'
                }, {
                    'id': '3fa85f64-5717-4562-b3fc-2c963f66a334',
                    'name': 'Фрукт',
                    'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'type': 'CATEGORY',
                    'price': None
                }, {
                    'id': '3fa85f64-5717-4562-b3fc-2c963f66a335',
                    'name': 'Фрукт',
                    'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                    'type': 'OFFER',
                    'price': 0
                },
                self.normal_item
            ]
        }
        resp = self._send(data)
        self.assertEqual(resp.status_code, 200)
