from django.shortcuts import render
from django.views import View
from django.http import HttpResponse


class PricesComparatorView(View):
    def post(self, request):
        return HttpResponse(request.POST)

