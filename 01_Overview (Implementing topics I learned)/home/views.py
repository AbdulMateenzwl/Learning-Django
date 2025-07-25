from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from home.models import Contact
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .serializers import ContactSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view


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
@api_view(['GET'])
def get_contacts(request):

    if request.method == "GET":
        contacts = Contact.objects.all()
        # contacts = Contact.objects.filter(name="mateen")
        # contacts = Contact.objects.filter(name__contains="mat")
        # contacts = Contact.objects.filter(date__year=2025)

        # Get one contact
        # contact = Contact.objects.get(id=1)

        # .values and values_list
        # contacts = Contact.objects.values('name', 'date')
        # contacts = Contact.objects.values_list('name')

        # Chaining
        # contacts =Contact.objects.filter(name="test").exclude(date__year=2024).order_by('-date')

        # print(contacts)
        # return HttpResponse(contacts)
    

        serializer = ContactSerializer(contacts, many = True)

        return Response(serializer.data)

from rest_framework.views import APIView

class HelloWorld(APIView):
    def get(self, request):
        return Response({"message": "Hello from class view!"})


from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin

class PostListCreateView(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


from rest_framework.viewsets import ModelViewSet

class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer