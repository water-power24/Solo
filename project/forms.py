from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField(required=True, label='Email')
    age = forms.IntegerField(min_value=18)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'age', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].help_text = ''
    


class FitnessForm(forms.ModelForm):
    max_pushups = forms.IntegerField(required=True, label="Максимум в отжиманиях")
    max_pullups = forms.IntegerField(required=True, label="Максимум в подтягиваниях")
    max_run_1km = forms.FloatField(required=True, label="Время на 1 км (минуты)")

    class Meta:
        model = CustomUser
        fields = ['max_pushups', 'max_pullups', 'max_run_1km']