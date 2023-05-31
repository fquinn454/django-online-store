from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views



urlpatterns = [
    path("register", views.register, name="register"),
    path("account-info", views.accountInfo, name="account-info"),
    path('login', LoginView.as_view(template_name='registration/login.html'), name="login"),
    

]