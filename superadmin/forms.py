# superadmin/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Client, SuperAdmin
# forms.py


class ClientAdminCreationForm(UserCreationForm):
    first_name = forms.CharField(label='First Name', max_length=30)
    last_name = forms.CharField(label='Last Name', max_length=30)
    email = forms.EmailField(label='Email', max_length=254)

    class Meta:
        model = SuperAdmin
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_clientadmin = True
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            Client.objects.create(
                name=f"{self.cleaned_data['first_name']} {self.cleaned_data['last_name']}",
                email=self.cleaned_data['email'],
                created_by=user
            )
        return user



# forms.py
# superadmin/forms.py

from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
