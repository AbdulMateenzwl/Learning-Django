from django.urls import path
from home import views

from rest_framework.routers import DefaultRouter
from .views import ContactViewSet


router = DefaultRouter()
router.register('v4/contacts', ContactViewSet)

urlpatterns = router.urls


# urlpatterns = [
#     path("", views.index, name='home'),
#     path("about", views.about, name='about'),
#     path("contact", views.contact, name='contact'),
#     path("api/contact", views.get_contacts, name='api/contacts'),
#     path("api/hello", views.HelloWorld.as_view(), name='hello_world'),
#     path("api/contacts/", views.PostListCreateView.as_view(), name='post_list_create')
# ]
