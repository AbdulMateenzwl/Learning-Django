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

@csrf_exempt
def get_contacts(request):

    if request.method == "GET":
        # contacts = Contact.objects.all()
        # contacts = Contact.objects.filter(name="mateen")
        # contacts = Contact.objects.filter(name__contains="mat")
        # contacts = Contact.objects.filter(date__year=2025)

        # Get one contact
        # contact = Contact.objects.get(id=1)

        # .values and values_list
        # contacts = Contact.objects.values('name', 'date')
        # contacts = Contact.objects.values_list('name')

        # Chaining
        contacts =Contact.objects.filter(name="test").exclude(date__year=2024).order_by('-date')


        print(contacts)
        return HttpResponse(contacts)