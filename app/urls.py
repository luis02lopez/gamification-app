"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import SignUpView

urlpatterns = [
    path('', views.index),
    path('teacher', views.teacher),
    path('student', views.student),
    path('student/list-courses-to-join', views.student_list_courses_to_join),
    path('student/manage-courses', views.student_manage_courses),
    path('student/manage-course/<str:course>/', views.student_manage_course),
    path('student/manage-company/<str:course>/', views.student_manage_company),
    path('student/manage-company/<str:course>/create', views.student_create_company),
    path('teacher/add-course', views.add_course),
    path('teacher/manage-courses', views.teacher_manage_courses),
    path('teacher/manage-course/<str:course>/', views.teacher_manage_course),
    path('teacher/manage-awards', views.teacher_manage_awards),
    path('teacher/manage-prizes', views.teacher_manage_prizes),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', SignUpView.as_view(), name='signup'),
]
