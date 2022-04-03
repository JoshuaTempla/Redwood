from urllib import request
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import*
from django.contrib import messages
from Main.models import Room
from Main.models import Applicant


#################################### Start of user pages ###################################

def home(response):
    return render(response, "Main/User/Home.html", {})

# About Us page


def about(response):
    return render(response, "Main/User/About.html", {})

# Contact Us page


def contact(response):
    return render(response, "Main/User/Contact.html", {})

# User choose room page


def rooms(response):
    room_types = Room_Type.objects.all()
    context = {"room_types": room_types}

    if response.method == "POST":
        if 'btnReserve' in response.POST:
            # Get the choice of room type ( A, B, C, D)
            current_room_type = response.POST.get("room_type")
            # Put it into session
            response.session['room_type'] = current_room_type
            print(response.session['room_type'])
            return redirect(applicant)
        else:
            return HttpResponse('You are in the wrong page')

    return render(response, "Main/User/Rooms.html", context)


# User fill up form 1 ( User/Applicant Details )
def applicant(response):

    applicants = Applicant.objects.all()
    current_room = response.session['room_type']
    context = {'applicants': applicants, 'current_room': current_room}

    # After filling up, the applicant details will be save into the database.
    if 'btnAddApplicant' in response.POST:
        if response.POST.get('name') and response.POST.get('address') and response.POST.get('phone') and response.POST.get('email'):
            add_applicant = Applicant()
            add_applicant.applicant_name = response.POST.get(
                'name')
            add_applicant.applicant_address = response.POST.get(
                'address')
            add_applicant.applicant_contactNo = response.POST.get(
                'phone')
            add_applicant.applicant_email = response.POST.get(
                'email')
            add_applicant.save()
            print('Successfully Added an applicant')
            return redirect(date)
    return render(response, "Main/User/Applicant.html", context)

# User fill up form 2 ( User/Applicant choose date and room)


def date(request):
    room_types = Room_Type.objects.all()
    room_type_in_rooms = Room.objects.all()
    current_room = request.session['room_type']
    context = {'room_types': room_types,
               'room_type_in_rooms': room_type_in_rooms, 'current_room': current_room}

    if request.method == "POST":
        if 'previousDate' in request.POST:
            return redirect(applicant)
        else:
            return HttpResponse('You are in the wrong page')

    return render(request, "Main/User/Date.html", context)

# User fill up form 3 ( User/Applicant fill up the remaining fields)


def reservation(request):

    room_types = Room_Type.objects.all()
    room_ledger = RoomLedger.objects.all()
    current_room = request.session['room_type']

    # From the form 2 where user/applicant choose room and date
    user_chosen_room = request.GET['room']
    user_chosen_date = request.GET['date']

<<<<<<< HEAD
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
=======
    reservation = RoomLedger.objects.raw('SELECT room_ledger_id, date_of_use, room_number, room_type, morning, afternoon, evening FROM main_roomledger WHERE date_of_use = %s AND room_number = %s AND room_type = %s', [
                                         user_chosen_date, user_chosen_room, current_room])

    # If the chosen date and room number is not in the database, then it will automatically added in the database
    if not reservation:
        add_Ledger = RoomLedger()
        add_Ledger.date_of_use = user_chosen_date
        add_Ledger.room_number = user_chosen_room
        add_Ledger.room_type = current_room
        add_Ledger.morning = 0
        add_Ledger.afternoon = 0
        add_Ledger.evening = 0
        add_Ledger.save()

    reservation = RoomLedger.objects.raw('SELECT room_ledger_id, date_of_use, room_number, room_type, morning, afternoon, evening FROM main_roomledger WHERE date_of_use = %s AND room_number = %s AND room_type = %s', [
        user_chosen_date, user_chosen_room, current_room])

    # Submit the reservation form
    if 'btnSubmit' in request.POST:
        if user_chosen_room and current_room and user_chosen_date and request.POST.get('timeslot') and request.POST.get('email'):
            add_reservation = Reservation()
            add_reservation.scheduled_date_of_use = user_chosen_date
            add_reservation.room_number = Room.objects.get(
                room_number=user_chosen_room)
            add_reservation.applicant_email = Applicant.objects.get(
                applicant_email=request.POST["email"])
            add_reservation.usage_fee = request.POST.get('timeslot')
            add_reservation.save()
            messages.success(request, "You have made a reservation!")
            print("request:::::::", request.POST.get('timeslot'))
            print(add_reservation.usage_fee)
            print('Successfully Added an RESERVATION!!!!!!!!!!!!!!!!!!!!!!!')

            room_types = Room_Type.objects.raw(
                'SELECT room_type, morning, afternoon, evening FROM main_room_type WHERE room_type = %s', [current_room])

            for room_type in room_types:
                print(room_type.morning)
                print(request.POST.get('timeslot'))
                print(room_type.afternoon)

                morning_str = str(room_type.morning)
                afternoon_str = str(room_type.afternoon)
                evening_str = str(room_type.evening)
                user_time_str = str(request.POST.get('timeslot'))

                user_morning = morning_str == user_time_str
                user_afternoon = afternoon_str == user_time_str
                user_evening = evening_str == user_time_str

                if morning_str == user_time_str:
                    print("The usage fee of morning =", user_morning)
                    print(room_type.morning)
                    RoomLedger.objects.filter(room_number=user_chosen_room, date_of_use=user_chosen_date).update(
                        morning=add_reservation.reservation_number)
                elif afternoon_str == user_time_str:
                    print("The usage fee of afternoon", user_afternoon)
                    print(room_type.afternoon)
                    RoomLedger.objects.filter(room_number=user_chosen_room, date_of_use=user_chosen_date).update(
                        afternoon=add_reservation.reservation_number)
                elif evening_str == user_time_str:
                    print("The usage fee of evening", user_evening)
                    print(room_type.evening)
                    RoomLedger.objects.filter(room_number=user_chosen_room, date_of_use=user_chosen_date).update(
                        evening=add_reservation.reservation_number)
                else:
                    print("No usage fee to be display")
>>>>>>> main

    if request.method == "POST":
        if 'previousDate' in request.POST:
            return redirect(date)

    context = {'current_room': current_room, 'room_types': room_types,
               'date': user_chosen_date,  'room_ledger': room_ledger, 'room': user_chosen_room, 'reservation': reservation}

<<<<<<< HEAD
           
=======
>>>>>>> main
    return render(request, 'Main/User/Reservation.html', context)

################################### End of user pages ###################################


#################################### Start of Admin Pages ###################################
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
    sql_reservations = Reservation.objects.raw(
        'SELECT reservation_number, room_number_id AS MostBookedRoom, COUNT(room_number_id) as TotalOfReservation FROM main_reservation GROUP BY room_number_id ORDER BY TotalOfReservation DESC LIMIT 1')

    sql_days = Reservation.objects.raw(
        'SELECT reservation_number, scheduled_date_of_use AS DateOfUse, COUNT(room_number_id) AS NumberOfReservation FROM main_reservation GROUP BY scheduled_date_of_use')

    context = {"reservations": reservations,
               "sql_reservations": sql_reservations, "sql_days": sql_days}

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


def crud_room_ledger(response):

    room_ledgers = RoomLedger.objects.all()
    sql_ledgers = RoomLedger.objects.raw(
        'SELECT room_ledger_id, date_of_use, room_number, morning, afternoon, evening FROM `main_roomledger` WHERE morning = 0 OR afternoon = 0 OR evening = 0')
    context = {"room_ledgers": room_ledgers, "sql_ledgers": sql_ledgers}

    if response.method == "POST":
        if 'btnUpdate' in response.POST:
            room_ledger_id = response.POST.get("room_ledger_id")
            date_of_use = response.POST.get("date_of_use")
            room_number = response.POST.get("room_number")
            room_type = response.POST.get("room_type")
            morning = response.POST.get("morning")
            afternoon = response.POST.get("afternoon")
            evening = response.POST.get("evening")
            RoomLedger.objects.filter(room_ledger_id=room_ledger_id).update(
                date_of_use=date_of_use, room_number=room_number, room_type=room_type, morning=morning, afternoon=afternoon, evening=evening)

        elif 'btnDelete' in response.POST:
            room_ledger_id = response.POST.get("room_ledger_id")
            RoomLedger.objects.filter(room_ledger_id=room_ledger_id).delete()

        elif 'btnAddRoomLedger' in response.POST:
            if response.POST.get('date_of_use') and response.POST.get('room_number') and response.POST.get('room_type') and response.POST.get('morning') and response.POST.get('afternoon') and response.POST.get('evening'):
                add_room_ledger = RoomLedger()
                add_room_ledger.date_of_use = response.POST.get('date_of_use')
                add_room_ledger.room_number = response.POST.get('room_number')
                add_room_ledger.room_type = response.POST.get('room_type')
                add_room_ledger.morning = response.POST.get('morning')
                add_room_ledger.afternoon = response.POST.get('afternoon')
                add_room_ledger.evening = response.POST.get('evening')
                add_room_ledger.save()
                messages.success(
                    response, "A Room Ledger has Successfully Added!!!")

    return render(response, "Main/Admin/CrudRoomLedger.html", context)


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
