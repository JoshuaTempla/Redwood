from asyncio.windows_events import NULL
from urllib import request, response
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
            print(response.session['room_type'])
            return redirect(date)
        else:
            return HttpResponse('You are in the wrong page')

    return render(response, "Main/User/Rooms.html", context)


def date(request):
    room_types = Room_Type.objects.all()
    room_type_in_rooms = Room.objects.all()
    current_room = request.session['room_type']
    context = {'room_types': room_types,
               'room_type_in_rooms': room_type_in_rooms, 'current_room': current_room}
    return render(request, "Main/User/Date.html", context)


def reservation(request):

    room_types = Room_Type.objects.all()
    room_ledger = RoomLedger.objects.all()
    current_room = request.session['room_type']

    user_chosen_room = request.GET['room']
    user_chosen_date = request.GET['date']

    reservation = RoomLedger.objects.filter(date_of_use = user_chosen_date).filter(room_number = user_chosen_room).filter(room_type = current_room)
    room_prices = Room_Type.objects.filter(room_type = current_room)
    print(reservation)

    if not reservation :
        Ledger = RoomLedger()
        Ledger.date_of_use = user_chosen_date
        Ledger.room_number = user_chosen_room
        Ledger.room_type = current_room
        Ledger.morning = 0                                         
        Ledger.afternoon= 0
        Ledger.evening = 0
        Ledger.save()   

        print('Added')
        reservation = RoomLedger.objects.filter(date_of_use = user_chosen_date).filter(room_number = user_chosen_room).filter(room_type = current_room)
        room_prices = Room_Type.objects.filter(room_type = current_room)
        
    else:
        print('Hatdog')

    context = {'current_room': current_room, 'room_types': room_types,
               'date': user_chosen_date,  'room_ledger': room_ledger,
                'room': user_chosen_room, 'reservation': reservation,
                'room_prices':room_prices}
                
    if request.method == "POST":
        if 'previousDate' in request.POST:
            return redirect(date)

        elif 'submit' in request.POST:
           
            if request.POST.get('timeslots') and request.POST.get('name') and request.POST.get('email') and request.POST.get('phone') and request.POST.get('address'):
                add_Reservation = Reservation()
                add_Reservation.applicant_email = request.POST.get('email')
                add_Reservation.room_number = user_chosen_room
                add_Reservation.scheduled_date_of_use = user_chosen_date
                add_Reservation.time_slot = request.POST.get('timeslots')

                if request.POST.get('timeslots') == 'morning':
                    add_Reservation.usage_fee = room_prices.morning
                elif request.POST.get('timeslots') == 'afternoon':
                    add_Reservation.usage_fee = room_prices.afternoon
                else:
                    add_Reservation.usage_fee = room_prices.evening 
                
                add_Reservation.save()
                print('Reservation Added')
        else:
            return HttpResponse('You are in the wrong page')

           
    return render(request, 'Main/User/Reservation.html', context)
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
