from django.contrib import admin
from django.urls import path
from dreamdiary.views import home, about, cadastro, dream, login, myDreams, newDream

urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('login/', login, name='login'),
    path('cadastro/', cadastro, name='cadastro'),
    path('sobre/', about, name='sobre'),
    path('sonho/', dream, name='sonho'),
    path('meus_sonhos/', myDreams, name='meus_sonhos'),
    path('novo_sonho/', newDream, name='novo_sonho'),

]
