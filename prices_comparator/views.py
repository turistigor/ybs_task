from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest
import django.forms as forms

import json 


class ImportForm(forms.Form):
    # items = forms.CharField()
    updateDate = forms.DateTimeField()


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
