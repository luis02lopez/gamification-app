from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError  
from django.forms.fields import EmailField  
from django.forms.forms import Form  
from django import forms  
from .models import User, Student, Teacher, Course, Company, Wallet, Reward, Basket


class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'full_name')


class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'full_name')


class CustomUserCreationForm(UserCreationForm):  
    email = forms.EmailField(label='Correo institucional')
    full_name = forms.CharField(label='Nombre completo')
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)  
  
    def email_clean(self):  
        username = self.cleaned_data['email'].lower()  
        new = User.objects.filter(username = username)
        if new.count():  
            raise ValidationError("Este correo ya se encuentra registrado.")  
        return username
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  
  
    def save(self, commit = True):  
        user = User.objects.create_user( 
            self.cleaned_data['email'],  
            full_name=self.cleaned_data['full_name'], 
            password=self.cleaned_data['password1']  
        )
        username = self.cleaned_data['email'].lower()
        student = Student.objects.create_user( 
            email=username,
            password=self.cleaned_data['password1'] 
        )
        return user 

class CreateCourse(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Course
 
        # specify fields to be used
        fields = [
            "id",
            "name",
            "teacher",
        ]
