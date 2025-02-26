from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from dreamdiary.models import User, Emotion
from django.contrib import messages


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)  # Usa 'auth_login' para evitar conflito
            return redirect("home")  # Redireciona para a página inicial após login
        else:
            messages.error(request, "Usuário ou senha inválidos.")  # Exibe erro se as credenciais forem inválidas

    return render(request, "pages/login.html")

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

def newDream(request):
    emotions = Emotion.objects.all().order_by('category')  # Pega todas as emoções do banco ordenadas por categoria
    return render(request, "pages/new_dream.html", {"emotions": emotions})

def about (request):
    return render(request, 'pages/about.html')