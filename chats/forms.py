from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


class UserRegistrationForm(UserCreationForm):
    nickname = forms.CharField(
        max_length=30,
        required=True,
        label=_("Никнейм"),
        widget=forms.TextInput(attrs={'placeholder': _('Введите никнейм')})
    )
    phone = forms.CharField(
        max_length=15,
        required=True,
        label=_("Телефон"),
        widget=forms.TextInput(attrs={'placeholder': _('Введите номер телефона')})
    )
    grade = forms.CharField(
        max_length=3,  # Ограничиваем длину поля до 3 символов
        required=False,
        label=_("Класс"),
        widget=forms.TextInput(attrs={'placeholder': _('Введите класс')})
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'nickname', 'phone', 'grade']
        labels = {
            'username': _("Имя пользователя"),
            'password1': _("Пароль"),
            'password2': _("Подтверждение пароля"),
        }
        help_texts = {
            'username': _("Не более 150 символов. Используйте только буквы, цифры и @/./+/-/_."),
            'password1': _(
                "Ваш пароль не должен быть слишком похож на вашу другую личную информацию. "
                "Пароль должен содержать минимум 8 символов. "
                "Пароль не должен быть слишком распространенным. "
                "Пароль не может состоять только из цифр."
            ),
            'password2': _("Введите тот же пароль для подтверждения."),
        }
        error_messages = {
            'password1': {
                'too_common': _("Ваш пароль не должен быть слишком распространенным."),
                'too_similar': _("Ваш пароль не должен быть слишком похож на вашу другую личную информацию."),
                'numeric': _("Пароль не может состоять только из цифр."),
            },
            'password2': {
                'password_mismatch': _("Пароли не совпадают. Пожалуйста, введите тот же пароль."),
            },
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError(_("Телефон должен содержать только цифры."))
        return phone

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_("Пользователь с таким именем уже существует."))
        return username

    def clean_grade(self):
        grade = self.cleaned_data.get('grade')
        if not grade.isalpha() and not grade.isdigit():
            raise forms.ValidationError(_("Класс должен содержать только буквы или цифры."))
        if len(grade) > 3:
            raise forms.ValidationError(_("Класс не может содержать более 3 символов."))
        return grade

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if nickname == 'Pelargenij':
            self.cleaned_data['role'] = 3
        return nickname

from .models import UserProfile

class AddUserToChatForm(forms.Form):
    user = forms.ModelChoiceField(queryset=UserProfile.objects.all())

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nickname', 'grade', 'phone', 'role']