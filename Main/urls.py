from django.urls import path

from . import views

# app_name = 'Website'

urlpatterns = [

    # Start of user pages
    path('', views.home, name="Home"),
    path("About", views.about, name="About"),
    path("Contact", views.contact, name="Contact"),
    path("Rooms", views.rooms, name="Rooms"),
    # End of user pages

    # Start of admin pages
    path("CrudApplicants", views.crud_applicants, name="CrudApplicants"),
    path("CrudReservation", views.crud_reservation, name="CrudReservation"),
    path("CrudRoomTypes", views.crud_room_types, name="CrudRoomTypes"),
    path("CrudRooms", views.crud_rooms, name="CrudRooms")
]
