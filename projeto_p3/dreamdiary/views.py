from django.http import HttpResponse
from django.shortcuts import render, redirect
from dreamdiary.models import User
from django.contrib import messages

# Create your views here.

def login (request):
    return render(request, 'pages/login.html')

def cadastro(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Verifica se o usuário já existe
        if User.objects.filter(username=username).exists():
            messages.error(request, "Usuário já cadastrado!")
            return redirect("cadastro")

        # Criar o usuário
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, "Cadastro realizado com sucesso! Faça login.")
        return redirect("login")

    return render(request, "pages/cadastro.html")

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