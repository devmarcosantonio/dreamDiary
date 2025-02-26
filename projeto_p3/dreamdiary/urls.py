from django.contrib import admin
from django.urls import path
from dreamdiary.views import home, about, cadastro, dream, login_view, myDreams, newDream, deleteDream
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('login'), name='index'),  # Redireciona para login
    path('home/', home, name='home'),
    path('login/', login_view, name='login'),
    path('cadastro/', cadastro, name='cadastro'),
    path('sobre/', about, name='sobre'),
    path('sonho/<int:id>/', dream, name='sonho'),
    path('meus_sonhos/', myDreams, name='meus_sonhos'),
    path('novo_sonho/', newDream, name='novo_sonho'),
    path('excluir_sonho/<int:id>/', deleteDream, name='excluir_sonho'),  # URL de exclusão de sonho
]

