from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def login (request):
    return render(request, 'pages/login.html')

def cadastro (request):
    return render(request, 'pages/cadastro.html')

def home (request):
    return render(request, 'pages/home.html')

def myDreams (request):
    return render(request, 'pages/my_dreams.html')

def dream (request):
    return render(request, 'pages/dream.html')

def newDream (request):
    return render(request, 'pages/new_dream.html')

def about (request):
    return render(request, 'pages/about.html')