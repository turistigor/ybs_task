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
            'price': 234,
            'type': 'OFFER'
        }

        cls._validation_failed = {
            "code": 400,
            "message": "Validation Failed"
        }

        cls._imports_url = 'http://127.0.0.1:8000/imports'

    def _send(self, data):
        return http.post(url=self._imports_url, 
                         data=json.dumps(data))

    def test_updateDate(self):
        # request without field
        data = {'items':[self.normal_item]}
        resp = self._send(data)

        self.assertEqual(resp.status_code, 400)
        self.assertDictEqual(
            json.loads(resp.content.decode()), self._validation_failed
        )

        # valid date from example"
        data = {'items':[self.normal_item], 'updateDate': '2022-05-28T21:12:01.000Z'}
        resp = self._send(data)

        self.assertEqual(resp.status_code, 200)

        # incorrect value"
        data = {'items':[self.normal_item], 'updateDate': 'asdasd2wef'}
        resp = self._send(data)

        self.assertEqual(resp.status_code, 400)
        self.assertDictEqual(
            json.loads(resp.content.decode()), self._validation_failed
        )

        # empty value
        data = {'items':[self.normal_item], 'updateDate': ''}
        resp = self._send(data)

        self.assertEqual(resp.status_code, 400)
        self.assertDictEqual(
            json.loads(resp.content.decode()), self._validation_failed
        )

        # short date-time format
        data = {'items':[self.normal_item], 'updateDate': '2006-10-25 14:30'}
        resp = self._send(data)

        self.assertEqual(resp.status_code, 200)

        # date-time with offset
        data = {'items':[self.normal_item], 'updateDate': '2006-10-25T14:30+02:00'}
        resp = self._send(data)

        self.assertEqual(resp.status_code, 200)


