from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def no_access(request):
    return render(request, 'no_access.html')