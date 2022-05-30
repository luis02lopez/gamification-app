from contextlib import nullcontext
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as log_out
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, CreateCourse
from django.urls import reverse_lazy
from django.views import generic
from .models import Student, Teacher, Course, Company, Wallet, Reward, Basket, Student_Course

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
    return render(request, 'teacher/home.html', context)


@login_required
def student(request):
    user = request.user
    username = user.get_username()
    context ={}
    context["dataset"] = Student.objects.get(user_id = username)
    return render(request, 'student/home.html', context)

@login_required
def student_list_courses_to_join(request):
    user = request.user
    context ={}
    context["dataset"] = Course.objects.raw('SELECT * FROM public.app_course as course FULL JOIN public.app_student_course as student_course on course.id = student_course.course_id')
    if(request.POST.get('course_to_join')):
        student = Student.objects.get(user_id = user.get_username())
        course = Course.objects.get(id = request.POST.get('course_to_join'))
        student_course = Student_Course(student=student, course=course, is_accepted=False)
        student_course.save()
    return render(request, 'student/list_courses_to_join.html', context)

@login_required
def student_manage_courses(request):
    user = request.user
    username = user.get_username()
    context ={}
    context["dataset"] = Course.objects.filter(student_course__student = username, student_course__is_accepted = True)
    return render(request, 'student/manage_courses.html', context)

@login_required
def student_manage_course(request, course):
    user = request.user
    username = user.get_username()
    context ={}
    context["dataset"] = Student_Course.objects.all().filter(course_id=course)
    if(request.POST.get('student_to_join')):
        student = Student.objects.get(user_id = request.POST.get('student_to_join'))
        course = Course.objects.get(id = course)
        student_course = Student_Course.objects.get(student=student, course=course, is_accepted=False)
        student_course.is_accepted = True
        student_course.save()
    return render(request, 'student/manage_course.html', context)

@login_required
def add_course(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    form = CreateCourse(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(manage_courses)
         
    context['form']= form
    return render(request, "teacher/add_course.html", context)

@login_required
def teacher_manage_courses(request):
    user = request.user
    username = user.get_username()
    context ={}
    context["dataset"] = Course.objects.all()
    return render(request, 'teacher/manage_courses.html', context)

@login_required
def teacher_manage_course(request, course):
    user = request.user
    username = user.get_username()
    context ={}
    context["dataset"] = Student_Course.objects.all().filter(course_id=course)
    if(request.POST.get('student_to_join')):
        student = Student.objects.get(user_id = request.POST.get('student_to_join'))
        course = Course.objects.get(id = course)
        student_course = Student_Course.objects.get(student=student, course=course, is_accepted=False)
        student_course.is_accepted = True
        student_course.save()
    return render(request, 'teacher/manage_course.html', context)

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

# from django.views.generic.edit import CreateView

# class AddCourse(CreateView):
#     model = Course
#     fields = ['name', 'teacher']
#     success_url = 'manage-courses'
#     template_name = 'teacher/add_course.html'
