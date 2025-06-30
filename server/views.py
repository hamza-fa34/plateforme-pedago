from django.shortcuts import render

def csrf_failure(request, reason=''):
    return render(request, 'csrf_error.html', {'reason': reason}, status=403) 