from contextlib import nullcontext
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as log_out
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Student, Teacher, Course, Company, Wallet, Reward, Basket

import json


def index(request):
    user = request.user
    if user.is_authenticated:
        username = user.get_username()
        try:
            is_teacher = Teacher.objects.get(user_id = username)
        except:
            is_teacher = None
            pass
        if is_teacher:
            return redirect(teacher)
        else:
            return redirect(student)
    else:  
        return render(request, 'index.html')

@login_required
def teacher(request):
    user = request.user
    username = user.get_username()
    context ={}
    context["dataset"] = Teacher.objects.get(user_id = username)
    return render(request, 'teacher_home.html', context)


@login_required
def student(request):
    user = request.user
    username = user.get_username()
    context ={}
    context["dataset"] = Student.objects.get(user_id = username)
    return render(request, 'student_home.html', context)

@login_required
def add_course(request):
    user = request.user
    username = user.get_username()
    context ={}
    context["dataset"] = Teacher.objects.get(user_id = username)
    return render(request, 'teacher_home.html', context)


# def register_student(request):  
#     if request.POST == 'POST':  
#         form = CustomUserCreationForm()  
#         if form.is_valid():  
#             form.save()
#     else:  
#         form = CustomUserCreationForm()  
#     context = {  
#         'form':form  
#     }  
#     return render(request, 'registration/signup.html', context)  

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'