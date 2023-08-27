from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.core.exceptions import ValidationError

class register_user(forms.Form):
    Username = forms.CharField( widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "INSERT YOUR USER"}))
    Email = forms.EmailField(widget=forms.EmailInput(attrs={'class': "form-control", 'placeholder': 'INSERT YOUR EMAIL'}))
    Password1 = forms.CharField(label="PASSWORD", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'INSERT YOUR PASS'}))
    Password2 = forms.CharField(label=" CONFIRM PASSWORD", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'INSERT YOUR PASS'}))

    def clean_Email(self):
        email = self.cleaned_data['Email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use. Please choose another one.")
        return email

    def clean_username(self):
        username = self.cleaned_data['Username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("This Username is already in use. Please choose another one.")

    def clean(self):
        cd= super().clean()
        p1 = cd.get("Password1")
        p2= cd.get("Password2")
        if p1 and p2 and p1 != p2:
           raise ValidationError("your Passwords are note match")


class LoginForm(forms.Form):
    Username = forms.CharField( widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "INSERT YOUR USER or Email"}))
    Password = forms.CharField(label="PASSWORD", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'INSERT YOUR PASS'}))


class EditForm(forms.ModelForm):
    email=forms.EmailField()

    class Meta:
        model= Profile
        fields=( "age", "bio")

