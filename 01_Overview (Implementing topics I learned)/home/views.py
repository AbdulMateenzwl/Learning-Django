from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    context = {
        'variable': 'this is sent'
    }
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')
