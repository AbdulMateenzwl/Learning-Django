from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.index, name = 'home'),
    path('login', views.loginUser, name = "login"),
    path('logout', views.logoutUser, name = "logout"),
    path('jwt-demo', views.jwt_demo, name = "jwt_demo"),
]
