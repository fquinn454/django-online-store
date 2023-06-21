# views.py
from dotenv import load_dotenv
import os, stripe
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
from .models import Profile
from address.models import Address
from order.models import Order

load_dotenv()
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('showcart')
        else:
            form = RegisterForm()
            context = {"form": form}
    else:
        form = RegisterForm()
        context = {"form": form}
    return render(request, "register.html", context)

def accountInfo(request):
    if request.user.is_authenticated:

        addresses=Address.objects.filter(profile = Profile.objects.get(user = request.user))
        orders=Order.objects.filter(profile = Profile.objects.get(user = request.user)).order_by('-id')

        return render(request, 'account-info.html', {'addresses':addresses, 'orders':orders})
    else:
        return redirect('login')

