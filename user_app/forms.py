from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm, \
    PasswordChangeForm
from django.contrib.auth.models import User

from blog.models import PostModel, CategoryModel, PostFilesModel
from user_app import models


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя'
        })
    )
    password = forms.CharField(
        max_length=128,
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль',
            "autocomplete": "password"
        })
    )

    class Meta:
        model = User
        fields = ['username', 'password']


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email'
        })
    )
    password1 = forms.CharField(
        max_length=128,
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )
    password2 = forms.CharField(
        max_length=128,
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', ]


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Введите Email',
                   "autocomplete": "email"}
        )
    )


class CustomSetPasswordForm(SetPasswordForm):
    error_messages = {
        "password_mismatch": "Пароли не совпадают"
    }
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Введите новый пароль',
                   "autocomplete": "new-password"}
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='Подтверждение нового пароля',
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Подтвердите новый пароль',
                   "autocomplete": "new-password"}
        ),
    )


class UserInfoForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        label='Имя пользователя (username)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email'
        })
    )
    first_name = forms.CharField(
        max_length=150,
        label='Имя',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше имя'
        })
    )
    last_name = forms.CharField(
        max_length=150,
        label='Фамилия',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите вашу фамилию'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class UserPasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        max_length=128,
        label='Старый пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите старый пароль'
        })
    )
    new_password1 = forms.CharField(
        max_length=128,
        label='Новый пароль',
        help_text=password_validation.password_validators_help_text_html(),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите новый пароль'
        })
    )
    new_password2 = forms.CharField(
        max_length=128,
        label='Подтверждение нового пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите новый пароль'
        })
    )


class ProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(
        label='Пол',
        choices=models.ProfileModel.Genders.choices,
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-select',
            }
        )
    )
    dob = forms.DateField(
        label='Дата рождения',
        required=False,
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control',
            }
        )
    )
    site_link = forms.CharField(
        label='Личный сайт',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'https://...'
            }
        )
    )
    telegram_link = forms.CharField(
        label='Профиль в Telegram',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'https://t.me/...'
            }
        )
    )
    user_avatar = forms.FileField(
        label='Аватарка',
        required=False,
        widget=forms.FileInput(
            attrs={
                'type': 'file',
                'class': 'form-control',
            }
        )
    )

    show_last_name = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input mt-0',
            }
        )
    )
    show_email = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input mt-0',
            }
        )
    )
    show_telegram = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input mt-0'
            }
        )
    )

    class Meta:
        model = models.ProfileModel
        fields = ['gender', 'dob', 'site_link', 'telegram_link', 'user_avatar', 'show_last_name', 'show_email',
                  'show_telegram']

class AddPostByAuthorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autofocus': ''})

        self.fields['short_body'].widget.attrs.update({'class': 'django_ckeditor_5'})
        self.fields['full_body'].widget.attrs.update({'class': 'django_ckeditor_5'})
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.fields["short_body"].required = False
        self.fields["full_body"].required = False

    class Meta:
        model = PostModel
        fields = ('title', 'image', 'category', 'short_body', 'full_body', 'status', 'telegram_link',
                  'file', 'tags')


class AddCategoryByAuthorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autofocus': ''})

        self.fields['description'].widget.attrs.update({'class': 'django_ckeditor_5'})

    class Meta:
        model = CategoryModel
        fields = ('title', 'parent', 'description')


class AddFileByAuthorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autofocus': ''})

    class Meta:
        model = PostFilesModel
        fields = ('title', 'file')

