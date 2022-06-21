from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest

import json

from prices_comparator.import_forms import ImportForm


class PricesComparatorView(View):
    def post(self, request):
        data = json.loads(request.body.decode())
        import_form = ImportForm(data)

        if import_form.is_valid():
            #TODO: create db models, validate and save
            return HttpResponse()
        else:
            return HttpResponseBadRequest(json.dumps({
                "code": 400,
                "message": "Validation Failed"
            }))

    def get(self, request):
        return HttpResponse('It works!')
