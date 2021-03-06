import email
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, primary_key=True, unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=True)
    full_name = models.CharField(max_length=60)
    USERNAME_FIELD = 'email'
    def __str__(self):
        return self.email
    
    objects = UserManager()

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    objects =  UserManager()

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    objects =  UserManager()

class Course(models.Model):
    id = models.CharField(max_length=60, primary_key=True)
    name = models.CharField(max_length=60)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True)

class Company(models.Model):
    name = models.CharField(max_length=120)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Student_Course(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    is_accepted = models.BooleanField(blank=True, null=True)

class Student_Company(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    is_accepted = models.BooleanField(blank=True, null=True)

class Wallet(models.Model):
    owner = models.OneToOneField(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    points = models.IntegerField(blank=True, null=True)

class Award(models.Model):
    name = models.CharField(max_length=60)
    points = models.IntegerField(blank=True, null=True)

class Prize(models.Model):
    name = models.CharField(max_length=60)
    price = models.IntegerField(blank=True, null=True)

class Bucket(models.Model):
    owner = models.ForeignKey(Student, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE, null=True)
    is_approved = models.BooleanField(blank=True, null=True)
