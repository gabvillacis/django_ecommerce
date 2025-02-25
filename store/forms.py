# store/forms.py
from django import forms
from django.contrib.auth.models import User

class SignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput, 
        min_length=8, max_length=12, 
        label="Contraseña"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, 
        min_length=8, max_length=12, 
        label="Confirmar Contraseña"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")
