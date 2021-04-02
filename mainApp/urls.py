from django.urls import path

from mainApp import views

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('create/about/', views.create_about, name="create_about"),
    path('contacts/', views.contacts, name="contacts"),
]