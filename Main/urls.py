from django.urls import include, path
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.conf import settings


# app_name = 'Website'

urlpatterns = [

    # Start of user pages
    path('', views.home, name="Home"),
    path("Redwood-About", views.about, name="About"),
    path("Redwood-Contact", views.contact, name="Contact"),
    path("Redwood-Rooms", views.rooms, name="Rooms"),
    path("Redwood-ApplicantDetails", views.applicant, name="Applicant"),
    path("Redwood-Date", views.date, name="Date"),
    path("Redwood-Reservation", views.reservation, name="Reservation"),

    # End of user pages

    # icon browser tab
    path("favicon.ico", RedirectView.as_view(
        url=staticfiles_storage.url("favicon.ico"))),


    # Start of admin pages
    path("Admin-crudapplicants", views.crud_applicants, name="CrudApplicants"),
    path("Admin-crudreservation", views.crud_reservation, name="CrudReservation"),
    path("Admin-crudroomledger", views.crud_room_ledger, name="CrudRoomLedger"),
    path("Admin-crudrooms", views.crud_rooms, name="CrudRooms")
]
