from contextlib import nullcontext
from unicodedata import name
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as log_out
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, CreateCourse, CreateCompany
from django.urls import reverse_lazy
from django.views import generic
from .models import Student, Teacher, Course, Company, Wallet, Award, Prize, Bucket, Student_Course, Student_Company

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
    context["course"] = Course.objects.get(id = course)
    if(request.POST.get('student_to_join')):
        student = Student.objects.get(user_id = request.POST.get('student_to_join'))
        course = Course.objects.get(id = course)
        student_course = Student_Course.objects.get(student=student, course=course, is_accepted=False)
        student_course.is_accepted = True
        student_course.save()
    return render(request, 'student/manage_course.html', context)

@login_required
def student_manage_company(request, course):
    user = request.user
    username = user.get_username()
    context ={}
    try:
        context["company"] = Student_Company.objects.raw('SELECT * FROM public.app_company INNER JOIN public.app_student_company ON public.app_company.id = public.app_student_company.company_id')
        context["company"][0]
    except:
        context["company"] = None
    context["course"] = course
    if(request.POST.get('member_to_remove')):
        student = Student.objects.get(user_id = request.POST.get('member_to_remove'))
        student_company = Student_Company.objects.get(student=student)
        student_company.delete()
        return redirect(student_manage_company, course)
    return render(request, 'student/manage_company.html', context)

@login_required
def student_create_company(request, course):
    user = request.user
    username = user.get_username()
    context ={}
    context["course"] = course
    form = CreateCompany(request.POST or None)
    if form.is_valid():
        company = form.save()
        student = Student.objects.get(user_id = username)
        company = Company.objects.get(id = company.id)
        student_company = Student_Company(student=student, company=company, is_accepted = True)
        student_company.save()
        return redirect(student_manage_company, course)
    context['form']= form
    return render(request, 'student/create_company.html', context)

@login_required
def add_course(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    form = CreateCourse(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(teacher_manage_courses)
         
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

@login_required
def teacher_manage_awards(request):
    user = request.user
    username = user.get_username()
    context ={}
    context["awards"] = Award.objects.all()
    if(request.POST.get('create_award_name')):
        award = Award(name = request.POST.get('create_award_name'), points = request.POST.get('create_award_points'))
        award.save()
        return redirect(teacher_manage_awards)
    if(request.POST.get('edit_award_id')):
        award = Award(id = request.POST.get('edit_award_id'), name = request.POST.get('edit_award_name'), points = request.POST.get('edit_award_points'))
        award.save()
        return redirect(teacher_manage_awards)
    if(request.POST.get('delete_award_id')):
        award = Award.objects.get(id = request.POST.get('delete_award_id'))
        award.delete()
        return redirect(teacher_manage_awards)
    return render(request, 'teacher/manage_awards.html', context)

@login_required
def teacher_manage_prizes(request):
    user = request.user
    username = user.get_username()
    context ={}
    context["prizes"] = Prize.objects.all()
    if(request.POST.get('create_prize_name')):
        prize = Prize(name = request.POST.get('create_prize_name'), price = request.POST.get('create_prize_price'))
        prize.save()
        return redirect(teacher_manage_prizes)
    if(request.POST.get('edit_prize_id')):
        prize = Prize(id = request.POST.get('edit_prize_id'), name = request.POST.get('edit_prize_name'), price = request.POST.get('edit_prize_price'))
        prize.save()
        return redirect(teacher_manage_prizes)
    if(request.POST.get('delete_prize_id')):
        prize = Prize.objects.get(id = request.POST.get('delete_prize_id'))
        prize.delete()
        return redirect(teacher_manage_prizes)
    return render(request, 'teacher/manage_prizes.html', context)

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
