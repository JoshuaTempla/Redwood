from urllib import request
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import*
from django.contrib import messages
from Main.models import Room
from Main.models import Applicant


# Start of user pages.

def home(response):
    return render(response, "Main/User/Home.html", {})


def about(response):
    return render(response, "Main/User/About.html", {})


def contact(response):
    return render(response, "Main/User/Contact.html", {})


def rooms(response):

    room_types = Room_Type.objects.all()
    context = {"room_types": room_types}

    if response.method == "POST":
        if 'btnReserve' in response.POST:
            current_room_type = response.POST.get("room_type")
            response.session['room_type'] = current_room_type
            return redirect(date)
        else:
            return HttpResponse('You are in the wrong page')

    return render(response, "Main/User/Rooms.html", context)


def date(response):
    room_types = Room_Type.objects.all()
    room_type_in_rooms = Room.objects.all()
    current_room = response.session['room_type']

    context = {'room_types': room_types,
               'room_type_in_rooms': room_type_in_rooms, 'current_room': current_room}

    if response.method == "POST":
        if 'btnReserve' in response.POST:
            chosen_room = response.POST.get("room")
            response.session['room'] = chosen_room
            used_date = response.POST.get("date")
            response.session['date'] = used_date
            return redirect(reservation)
        else:
            return HttpResponse('You are in the wrong page')
    return render(response, "Main/User/Date.html", context)


def reservation(response):

    room_types = Room_Type.objects.all()
    # room_type_in_rooms = Room.objects.all()
    # current_room = request.session['room_type']

    # # selected_day = request.GET.get('format_date', None)
    # # room = request.GET.get('room', None)
    # # print("Date selected: ", selected_day)
    # # print("Room selected: ", room)

    # # available_time_slot = RoomLedger.objects.raw(
    # #     'SELECT * FROM main_roomledger WHERE date_of_use = %s AND room_number = %s', [selected_day, room])
    # # print("Available timeslots: ", available_time_slot)

    room_ledger = RoomLedger.objects.all()
    reservation = Reservation.objects.all()
    current_room = response.session['room_type']
    used_date = response.session['date']
    chosen_room = response.session['room']
    context = {'current_room': current_room, 'room_types': room_types,
               'used_date': used_date, 'reservation': reservation, 'room_ledger': room_ledger, 'chosen_room': chosen_room}

    if response.method == "POST":
        if 'previousDate' in response.POST:
            return redirect(date)
        else:
            return HttpResponse('You are in the wrong page')
    return render(response, 'Main/User/Reservation.html', context)

    # def reservation(response):

    # # view data from database
    # room_types = Room_Type.objects.all()
    # room_type_in_rooms = Room.objects.all()
    # current_room = response.session['room_type']
    # #selected_day = response.session['selectedDay']
    # #selected_day = request.GET.get
    # #available_time_slot = RoomLedger.objects.filter(date_of_use = selected_day)

    # context = {'current_room': current_room, 'room_types': room_types,
    #            'room_type_in_rooms': room_type_in_rooms}
    # # end of view

    # return render(response, "Main/User/Reservation.html", context)

# End of user pages


# Start of Admin Pages


def crud_applicants(response):

    applicants = Applicant.objects.all()
    context = {"applicants": applicants}

    if response.method == "POST":
        if 'btnUpdate' in response.POST:
            applicant_name = response.POST.get("applicant_name")
            applicant_address = response.POST.get("applicant_address")
            applicant_contactNo = response.POST.get("applicant_contactNo")
            applicant_email = response.POST.get("applicant_email")
            Applicant.objects.filter(applicant_email=applicant_email).update(
                applicant_name=applicant_name, applicant_address=applicant_address, applicant_contactNo=applicant_contactNo)

        elif 'btnDelete' in response.POST:
            applicant_email = response.POST.get("applicant_email")
            Applicant.objects.filter(applicant_email=applicant_email).delete()

        elif 'btnAddApplicant' in response.POST:
            if response.POST.get('applicant_name') and response.POST.get('applicant_address') and response.POST.get('applicant_contactNo') and response.POST.get('applicant_email'):
                add_applicant = Applicant()
                add_applicant.applicant_name = response.POST.get(
                    'applicant_name')
                add_applicant.applicant_address = response.POST.get(
                    'applicant_address')
                add_applicant.applicant_contactNo = response.POST.get(
                    'applicant_contactNo')
                add_applicant.applicant_email = response.POST.get(
                    'applicant_email')
                add_applicant.save()
                messages.success(response, "Applicant Successfully Added!!!")

    return render(response, "Main/Admin/CrudApplicants.html", context)


def crud_reservation(response):

    reservations = Reservation.objects.all()
    context = {"reservations": reservations}

    if response.method == "POST":
        if 'btnUpdate' in response.POST:
            reservation_number = response.POST.get("reservation_number")
            applicant_email = response.POST.get("applicant_email")
            room_number = response.POST.get("room_number")
            scheduled_date_of_use = response.POST.get("scheduled_date_of_use")
            usage_fee = response.POST.get("usage_fee")
            Reservation.objects.filter(reservation_number=reservation_number).update(
                applicant_email=applicant_email, room_number=room_number, scheduled_date_of_use=scheduled_date_of_use, usage_fee=usage_fee)

        elif 'btnDelete' in response.POST:
            reservation_number = response.POST.get("reservation_number")
            Reservation.objects.filter(
                reservation_number=reservation_number).delete()

        elif 'btnAddReservation' in response.POST:
            if response.POST.get('applicant_email') and response.POST.get('room_number') and response.POST.get('scheduled_date_of_use') and response.POST.get('usage_fee'):
                add_reservation = Reservation()
                add_reservation.applicant_email = Applicant.objects.get(
                    applicant_email=response.POST["applicant_email"])
                add_reservation.room_number = Room.objects.get(
                    room_number=response.POST["room_number"])
                add_reservation.scheduled_date_of_use = response.POST.get(
                    'scheduled_date_of_use')
                add_reservation.usage_fee = response.POST.get('usage_fee')
                add_reservation.save()
                messages.success(response, "Reservation Successfully Added!!!")

    return render(response, "Main/Admin/CrudReservation.html", context)


def crud_room_types(response):

    room_types = Room_Type.objects.all()
    context = {"room_types": room_types}

    if response.method == "POST":
        if 'btnUpdate' in response.POST:
            room_type = response.POST.get("room_type")
            morning = response.POST.get("morning")
            afternoon = response.POST.get("afternoon")
            evening = response.POST.get("evening")
            Room_Type.objects.filter(room_type=room_type).update(
                morning=morning, afternoon=afternoon, evening=evening)

        elif 'btnDelete' in response.POST:
            room_type = response.POST.get("room_type")
            Room_Type.objects.filter(room_type=room_type).delete()

        elif 'btnAddRoomType' in response.POST:
            if response.POST.get('room_type') and response.POST.get('morning') and response.POST.get('afternoon') and response.POST.get('evening'):
                add_room_type = Room_Type()
                add_room_type.room_type = response.POST.get('room_type')
                add_room_type.morning = response.POST.get('morning')
                add_room_type.afternoon = response.POST.get('afternoon')
                add_room_type.evening = response.POST.get('evening')
                add_room_type.save()
                messages.success(
                    response, "A Different Kind of Room has Successfully Added!!!")

    return render(response, "Main/Admin/CrudRoomTypes.html", context)


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
