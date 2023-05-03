from django.http import HttpResponse
from django.shortcuts import render
import requests

def index(request):
    return render(request, "index.html")

def welcome(request):
    return render(request, "welcome.html")

def products(request):
    response = requests.get('https://dummyjson.com/products?limit=10')
    context = response.json()
    
    return render(request, "products.html", context)