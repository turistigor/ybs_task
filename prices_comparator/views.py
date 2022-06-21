from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest

import json

from requests import JSONDecodeError

from prices_comparator.import_forms import ImportForm


class PricesComparatorView(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode())
        except JSONDecodeError:
            return HttpResponseBadRequest(json.dumps({
                "code": 400,
                "message": "Validation Failed"
            }))

        import_form = ImportForm(data)

        if import_form.is_valid():
            
            return HttpResponse()
        else:
            return HttpResponseBadRequest(json.dumps({
                "code": 400,
                "message": "Validation Failed"
            }))

    def get(self, request):
        return HttpResponse('It works!')
