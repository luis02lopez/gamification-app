from django.db import models

class Course(models.Model):
    id = models.CharField(max_length=60, primary_key=True)
    name = models.CharField(max_length=60)

class Company(models.Model):
    name = models.CharField(max_length=120)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Student(models.Model):
    full_name = models.CharField(max_length=60)
    email = models.EmailField
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Teacher(models.Model):
    name = models.CharField(max_length=60)

class Wallet(models.Model):
    owner = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.IntegerField

class Reward(models.Model):
    name = models.CharField(max_length=60)
    price = models.IntegerField

class Basket(models.Model):
    owner = models.ForeignKey(Student, on_delete=models.CASCADE)
    rewards = models.ManyToManyField(Reward)
