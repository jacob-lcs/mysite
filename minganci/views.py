from django.shortcuts import render
from django.template import loader

from django.http import HttpResponse, JsonResponse

import importlib, sys

importlib.reload(sys)


def minganci(f1):
    # coding=utf-8
    f = open('/home/ubuntu/django_project/mysite/minganci/filtered_words.txt', 'r', encoding="utf-8")
    for line in f:
        if line.strip() in f1:
            f1 = f1.replace(line.strip(), '**')
    f.close()
    return f1


# Create your views here.
def index(request):
    data = {'sentence': ''}
    data['sentence'] = minganci(request.GET["sentence"])
    if request.method == 'GET':
        return JsonResponse(data)
