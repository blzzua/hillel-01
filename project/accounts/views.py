import logging

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, RedirectView, FormView
from django.views.generic.edit import FormMixin
from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.decorators import login_required
from django.urls import reverse
from accounts.forms import RegistrationForm, LoginForm
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.
class LoginView(FormView):
    template_name = 'accounts/login.html'
    get_redirect_url = 'accounts_personal_information'
    form_class = LoginForm

    def post(self, request):
        context = super().get_context_data()
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request, email=form.cleaned_data.get('email'),
                password=form.cleaned_data.get('password')
            )
            if user:
                login(request, user)
                return redirect('accounts_personal_information')
            else:
                form.add_error('password', 'LOGIN FAILED')
                context['form'] = form

        logging.error(form.errors)
        #   request, template_name, context=None, content_type=None, status=None, using=None
        return render(request, template_name=self.get_template_names(), context=context)


class RegistrationView(TemplateView, FormMixin):
    template_name = 'accounts/registration.html'
    get_redirect_url = 'accounts_personal_information'
    form_class = RegistrationForm

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('accounts_personal_information')
        else:
            #   request, template_name, context=None, content_type=None, status=None, using=None
            return render(request=request, template_name=self.template_name)


class LogoutView(RedirectView):
    def get(self, reqeust, *args, **kwargs):
        logout(reqeust)
        # return super().get(reqeust, *args, **kwargs)
        return redirect(reverse('accounts_index'))


class AccountsIndexView(TemplateView):
    template_name = 'accounts/personal_information.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = {f.name: getattr(self.request.user, f.name, None) for f in User._meta.get_fields()
                           if f.name in ("id", "last_login", "is_superuser", "first_name", "last_name",
                                         "email", "phone", "is_staff", "is_active", "date_joined")}
        return context


class PersonalInformationView(AccountsIndexView):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super().get(*args, **kwargs)
        else:
            return redirect(reverse('accounts_login'))
