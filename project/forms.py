from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField(required=True, label='Email')
    age = forms.IntegerField(min_value=18)

    class Meta:
        model = User
        fields = ['username', 'email', 'age', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''  
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = '' 
        self.fields['age'].help_text = '' 