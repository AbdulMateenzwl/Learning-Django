from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from home.models import Contact
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages


def index(request):
    context = {
        'variable': 'this is sent'
    }
    messages.success(request, "this is test messages")
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')


@csrf_exempt
def contact(request):

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')

        contact = Contact(name=name, email=email, phone=phone,
                          desc=desc, date=datetime.today())
        contact.save()
        print(contact)
        messages.success(request, 'Profile Created')

    return render(request, 'contact.html')
