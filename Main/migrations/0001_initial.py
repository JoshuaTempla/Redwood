# Generated by Django 3.2.6 on 2022-03-03 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('applicant_email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('applicant_contactNo', models.CharField(max_length=11)),
                ('applicant_name', models.CharField(max_length=40)),
                ('applicant_address', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Room_Type',
            fields=[
                ('room_type', models.CharField(max_length=1, primary_key=True, serialize=False)),
                ('morning', models.IntegerField()),
                ('afternoon', models.IntegerField()),
                ('evening', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room_number', models.IntegerField(primary_key=True, serialize=False)),
                ('room_description', models.TextField()),
                ('room_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.room_type')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('reservation_number', models.AutoField(primary_key=True, serialize=False)),
                ('scheduled_date_of_use', models.DateField()),
                ('usage_fee', models.IntegerField()),
                ('applicant_email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.applicant')),
                ('room_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.room')),
            ],
        ),
    ]