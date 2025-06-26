from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def not_found(request):
    return render(request, '404.html')

def not_found_404(request, exception):
    return render(request, '404.html')