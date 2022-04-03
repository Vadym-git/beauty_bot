from django.shortcuts import render, HttpResponse
from django.http import JsonResponse


# Create your views here.

def index(request):
    response = JsonResponse({'text': 'hello'})
    return response
