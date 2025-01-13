from django.shortcuts import render


def start_template(request):
    return render(request, 'index.html')