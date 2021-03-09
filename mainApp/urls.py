from django.urls import path

from mainApp import views

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('contacts/', views.contacts, name="contacts"),
]