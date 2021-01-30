'''
* Grupo 1363
* Pareja 8
* File: forms.py
'''

from django import forms
from django.contrib.auth.models import User
from datamodel.models import Move
from django.core.validators import MaxValueValidator, MinValueValidator


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


class MoveForm(forms.ModelForm):
    origin = forms.IntegerField(widget=forms.HiddenInput(), validators=[MinValueValidator(0),
                                MaxValueValidator(63)], required=False)
    target = forms.IntegerField(widget=forms.HiddenInput(), validators=[MinValueValidator(0),
                                MaxValueValidator(63)], required=False)

    class Meta:
        model = Move
        fields = ('origin', 'target')


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')
