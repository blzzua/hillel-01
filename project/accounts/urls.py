"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from accounts.views import AccountsIndexView, LoginView, RegistrationView, PersonalInformationView, LogoutView

urlpatterns = [
    path('', AccountsIndexView.as_view(), name='accounts_index'),
    path('login', LoginView.as_view(), name='accounts_login'),
    path('logout', LogoutView.as_view(), name='accounts_logout'),
    path('registration', RegistrationView.as_view(), name='accounts_registration'),
    path('profile', PersonalInformationView.as_view(), name='accounts_personal_information'),
]