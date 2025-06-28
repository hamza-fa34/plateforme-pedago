from django.shortcuts import render

def not_found(request):
    return render(request, '404.html')

def not_found_404(request, exception):
    return render(request, '404.html')