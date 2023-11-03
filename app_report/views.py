from django.shortcuts import render
from django.http import JsonResponse
from app_store.models import Product
from django.core import serializers


# Create your views here.
def report_with_flexmonster(request):
    return render(request, 'report_with_flexmonster.html', {

    })

def pivot_data(request):
    dataset = Product.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)