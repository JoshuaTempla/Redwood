from django.urls import include, path
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.conf import settings


# app_name = 'Website'

urlpatterns = [

    # Start of user pages
    path('', views.home, name="Home"),
    path("About", views.about, name="About"),
    path("Contact", views.contact, name="Contact"),
    path("Rooms", views.rooms, name="Rooms"),
    # End of user pages

    # icon browser tab
    path("favicon.ico", RedirectView.as_view(
        url=staticfiles_storage.url("favicon.ico"))),


    # Start of admin pages
    path("CrudApplicants", views.crud_applicants, name="CrudApplicants"),
    path("CrudReservation", views.crud_reservation, name="CrudReservation"),
    path("CrudRoomTypes", views.crud_room_types, name="CrudRoomTypes"),
    path("CrudRooms", views.crud_rooms, name="CrudRooms")
]
