from django import forms
from django.contrib.auth.forms import SetPasswordForm as DjangoSetPasswordForm
from .models import *
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.forms import SetPasswordForm
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.contrib import messages
class regiform(forms.Form):
    name=forms.CharField(max_length=30)
    username=forms.CharField(max_length=20)
    email = forms.EmailField()
    phone = forms.IntegerField()
    bio = forms.CharField(max_length=100)
    password = forms.CharField(max_length=30)
    cfpassword=forms.CharField(max_length=30)
    photo = forms.FileField()
class loginform(forms.Form):
    email=forms.EmailField()
    password=forms.CharField(max_length=29)

class employregisterform(forms.Form):
    name=forms.CharField(max_length=20)
    bio=forms.CharField(max_length=100)
    phone=forms.IntegerField()
    photo=forms.FileField()
    email=forms.EmailField()
    city = forms.CharField(max_length=50)
    rate=forms.IntegerField()
    password=forms.CharField(max_length=30)


class RequestResetForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)
class ShopSearchForm(forms.Form):
    services = forms.CharField(max_length=100, required=False)

class employeesearchform(forms.Form):
    location = forms.CharField(max_length=100, required=False)

class appoimentform(forms.Form):
    location = forms.CharField(max_length=100, required=False)
    date=forms.DateTimeField()
class PaymentForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

class RequestResetForm(forms.Form):
    email = forms.EmailField()

class SetPasswordForm(DjangoSetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="New password")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm new password")