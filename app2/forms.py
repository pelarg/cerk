from django import forms
from .models import CustomUser

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

from django import forms
from .models import Ank

class AnkForm(forms.ModelForm):
    class Meta:
        model = Ank
        fields = ['event_name', 'user_name', 'event_photo']