# views.py
from dotenv import load_dotenv
import os, stripe
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from .models import Profile

load_dotenv()
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        context = {"form":form}
        if form.is_valid():
            form.save()
        return redirect('account-info')
    else:
        form = RegisterForm()
        context = {"form":form}
    return render(response, "register.html", context)

def accountInfo(request):
    if request.user.is_authenticated:
        return render(request, 'account-info.html')
    else:
        return redirect('login')
   
