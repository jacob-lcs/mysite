from django.shortcuts import render
from django.template import loader
from .qcwy_text.predict import pre

from django.http import HttpResponse, JsonResponse


def index(request):
    data = {'info': ''}
    data['info'] = pre(request.GET["intro"])
    if request.method == 'GET':
        return JsonResponse(data)
    else:
        template = loader.get_template('predict/index.html')
        return HttpResponse(template.render())
