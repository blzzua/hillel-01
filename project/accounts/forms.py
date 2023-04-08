from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import models, CharField, TextInput, PasswordInput


User = get_user_model()


class LoginForm(models.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        username = CharField(label='login:', widget=TextInput(attrs={"autofocus": True}))
        password = CharField(label='Password', widget=PasswordInput)

    def clean(self):
        username = self.data.get('username')
        password = self.data.get('password')
        self.cleaned_data = {'username': username, 'password': password}
        return self.cleaned_data


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        print(self)
        user.username = self.cleaned_data.get('email').split('@')[0]
        user.save()
        return user


class PersonalInformationForm(models.ModelForm):
    class Meta:
        model = User
        exclude = ['password']
