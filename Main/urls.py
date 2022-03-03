from django.urls import path

from . import views

# app_name = 'Website'

urlpatterns = [

    # HOME PAGE
    path('', views.home, name="Home"),
    path("About", views.about, name="About"),
    path("Contact", views.contact, name="Contact"),
    path("Rooms", views.rooms, name="Rooms"),
    path("CreateRoom", views.create_room, name="CreateRoom")
]
