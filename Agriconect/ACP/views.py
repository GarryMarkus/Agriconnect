from django.shortcuts import render


def start_template(request):
    return render(request, 'index.html')
def login(request):
    return render(request, 'login.html')