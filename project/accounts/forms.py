import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import models, Form, CharField, TextInput, PasswordInput, NumberInput


User = get_user_model()


class LoginForm(Form):
    email = CharField(label='email or phone', widget=TextInput(attrs={"autofocus": True}))
    password = CharField(label='Password', widget=PasswordInput(attrs={"type": "password"}), required=False)
    otp_password = CharField(label='SMS code', widget=NumberInput(attrs={}), required=False)

    def clean_email(self):
        email = self.data.get('email')
        phone_regex = re.match('^\+?(?:38)?(0\d{9})$', email)
        if bool(phone_regex):
            # valid phone number
            phone = phone_regex.groups()[0]
            return phone

    def clean(self):
        email = self.data.get('email')
        password = self.data.get('password')
        otp_password = self.data.get('otp_password')
        self.cleaned_data = {'email': email}
        if password != '':
            self.cleaned_data['password'] = password
        elif otp_password != '':
            self.cleaned_data['password'] = otp_password
        else:
            self.add_error('password', 'Empty Password (and OTP)')
            self.add_error('otp_password', 'Empty OTP (and Password)')
            # raise ValidationError('Empty Password and OTP')
        return self.cleaned_data


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        print(self)
        user.email = self.cleaned_data.get('email').split('@')[0]
        user.save()
        return user


class PersonalInformationForm(models.ModelForm):
    class Meta:
        model = User
        exclude = ['password']


class OtpForm(Form):
    phone_number = CharField()
    def clean_email(self):
        email = self.data.get('phone_number')
        # TODO: implement cool phone number
        if email.isdigit():
            return email

