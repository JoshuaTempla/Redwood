from pyexpat import model
from django.db import models
from django.db.models.base import Model


# Create your models here.

#Applicant Class
class Applicant(models.Model):
    applicant_contactNo = models.CharField(max_length = 11, primary_key= True)
    applicant_name = models.CharField(max_length=40)
    applicant_address = models.CharField(max_length=40)

    def __str__(self):
        return self.applicant_name

    class meta:
        db_table = 'tblapplicant'

class Reservation(models.Model):
    reservation_number = models.AutoField(primary_key=True)
    scheduled_date_of_use = models.DateField()