# views.py
from dotenv import load_dotenv
import os, stripe
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
from .models import Profile

load_dotenv()
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        context = {"form":form}
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('account-info')
    else:
        form = RegisterForm()
        context = {"form": form}
    return render(request, "register.html", context)

def accountInfo(request):
    if request.user.is_authenticated:
        return render(request, 'account-info.html')
    else:
        return redirect('login')
   
