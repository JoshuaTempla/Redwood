from pyexpat import model
from statistics import mode
from tkinter import CASCADE
from tkinter.tix import Tree
from django.db import models
from django.db.models.base import Model
from sklearn import model_selection
#from pyrsistent import T


# Create your models here.

# Applicant Class
class Applicant(models.Model):
    applicant_email = models.EmailField(max_length=254, primary_key=True)
    applicant_contactNo = models.CharField(max_length=11)
    applicant_name = models.CharField(max_length=40)
    applicant_address = models.CharField(max_length=40)

   # def __str__(self):
        #return self.applicant_name

    class meta:
        db_table = 'tblapplicant'


class Room_Type(models.Model):
    room_type = models.CharField(max_length=1, primary_key=True)
    morning = models.FloatField()
    afternoon = models.FloatField()
    evening = models.FloatField()

    def __str__(self):
        return self.room_type

    class meta:
        db_table = 'tblroomtype'


class Room(models.Model):
    room_number = models.IntegerField(primary_key=True)
    room_type = models.ForeignKey(Room_Type, on_delete=models.CASCADE)
    room_description = models.TextField()

    class meta:
        db_table = 'tblroom'


class Reservation(models.Model):
    reservation_number = models.AutoField(primary_key=True)
    applicant_email = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    room_number = models.ForeignKey(Room, on_delete=models.CASCADE)
    scheduled_date_of_use = models.DateField()
    usage_fee = models.FloatField()

    class meta:
        db_table = 'tblreservation'



class RoomLedger(models.Model):
    room_ledger_id = models.AutoField(primary_key= True)
    date_of_use = models.DateField()
    room_number = models.IntegerField()
    room_type = models.IntegerField()
    morning = models.IntegerField()
    afternoon = models.IntegerField()
    evening = models.IntegerField()
