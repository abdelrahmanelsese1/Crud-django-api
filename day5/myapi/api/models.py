from django.db import models

# Create your models here.


class Intake(models.Model):
    intake_name = models.CharField(max_length=50)


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    email = models.CharField(max_length=100)
    # intakeId = models.ForeignKey('Intake', on_delete=models.CASCADE)
