from django.shortcuts import render
from .forms import*
from django.contrib import messages


# Start of user pages.

def home(response):
    return render(response, "Main/User/Home.html", {})


def about(response):
    return render(response, "Main/User/About.html", {})


def contact(response):
    return render(response, "Main/User/Contact.html", {})


def rooms(response):
    return render(response, "Main/User/Rooms.html", {})

# End of user pages


# Start of Admin Pages


def crud_applicants(response):
    return render(response, "Main/Admin/CrudApplicants.html", {})


def crud_reservation(response):
    return render(response, "Main/Admin/CrudReservation.html", {})


def crud_room_types(response):
    return render(response, "Main/Admin/CrudRoomTypes.html", {})


def crud_rooms(response):

    rooms = Room.objects.all()
    context = {"rooms": rooms}

    if response.method == "POST":
        if 'btnUpdate' in response.POST:
            room_number = response.POST.get("room_number")
            room_type = response.POST.get("room_type")
            room_description = response.POST.get("room_description")
            Room.objects.filter(room_number=room_number).update(
                room_type=room_type, room_description=room_description)

        elif 'btnDelete' in response.POST:
            room_number = response.POST.get("room_number")
            Room.objects.filter(room_number=room_number).delete()

        elif 'btnAddRoom' in response.POST:
            if response.POST.get('room_number') and response.POST.get('room_type') and response.POST.get('room_description'):
                add_room = Room()
                add_room.room_number = response.POST.get('room_number')
                add_room.room_description = response.POST.get(
                    'room_description')
                add_room.room_type = Room_Type.objects.get(
                    room_type=response.POST["room_type"])
                add_room.save()
                messages.success(response, "Room Successfully Added!!!")

    return render(response, "Main/Admin/CrudRooms.html", context)
