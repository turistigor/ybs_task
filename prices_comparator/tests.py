from django.test import TestCase

import requests as http
import uuid


class PriceComparatorTest(TestCase):
    def test_loop(self):
        data = {
            'id': uuid.uuid1(), 
            'name': 'soft',
            # 'parentId': None
            'type': 'CATEGORY',
            'price': 0
        }

        url = 'http://127.0.0.1:8000/imports'
        resp = http.post(url=url, data=data)


