from django.forms import ModelForm
from django import forms
from .models import *


class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = '__all__'


class Room_TypeForm(forms.ModelForm):
    class Meta:
        model = Room_Type
        fields = '__all__'


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'
