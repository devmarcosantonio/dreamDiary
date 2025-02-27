from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from dreamdiary.models import User, Dream, Emotion, DreamEmotion
from datetime import datetime, timedelta
import calendar
from django.contrib import messages


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

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

def home(request):
    # Data atual para exibir o calendário do mês correto
    hoje = datetime.today()
    ano_atual = hoje.year
    mes_atual = hoje.month

    # Buscar os últimos 5 sonhos cadastrados
    ultimos_sonhos = Dream.objects.filter(user=request.user).order_by("-date")[:5]

    # Buscar os dias em que os sonhos foram cadastrados no mês atual
    sonhos_no_mes = Dream.objects.filter(
        user=request.user, date__year=ano_atual, date__month=mes_atual
    ).values_list("date", flat=True)

    # Criar um conjunto com os dias onde há sonhos registrados
    dias_com_sonho = {data.day for data in sonhos_no_mes}

    # Gerar a lista de dias do mês atual
    _, total_dias_mes = calendar.monthrange(ano_atual, mes_atual)
    dias_do_mes = list(range(1, total_dias_mes + 1))  # Exemplo: [1, 2, 3, ..., 30]

    return render(
        request,
        "pages/home.html",
        {
            "ultimos_sonhos": ultimos_sonhos,
            "dias_com_sonho": dias_com_sonho,
            "dias_do_mes": dias_do_mes,
            "mes_atual": hoje.strftime("%B"),  # Nome do mês por extenso
            "ano_atual": ano_atual,
        },
    )

def myDreams(request):
    # Captura a data enviada pelo usuário (se existir)
    data_filtrada = request.GET.get("data", "")

    # Filtra os sonhos do usuário logado
    sonhos = Dream.objects.filter(user=request.user).prefetch_related("dream_emotions__emotion")

    # Se o usuário forneceu uma data, filtramos os sonhos para essa data específica
    if data_filtrada:
        try:
            data_formatada = datetime.strptime(data_filtrada, "%Y-%m-%d").date()
            sonhos = sonhos.filter(date=data_formatada)
        except ValueError:
            pass  # Caso a data seja inválida, simplesmente ignoramos o filtro

    return render(request, "pages/my_dreams.html", {"sonhos": sonhos, "data_filtrada": data_filtrada})

def dream(request, id):
    # Busca o sonho pelo ID ou retorna 404 se não encontrado
    sonho = get_object_or_404(Dream, id=id)

    # Exibe o sonho e as emoções associadas a ele
    print("Sonho:", sonho.title)
    print("Emoções associadas ao sonho:")
    for dream_emotion in sonho.dream_emotions.all():
        print(f"Categoria: {dream_emotion.emotion.category}, Nome: {dream_emotion.emotion.name}")

    # Passa o sonho para o template
    return render(request, 'pages/dream.html', {'sonho': sonho})

def newDream(request):
    emotions = Emotion.objects.all().order_by('category')  # Pega todas as emoções do banco ordenadas por categoria
    return render(request, "pages/new_dream.html", {"emotions": emotions})

def newDream(request):
    if request.method == 'POST':
        # Captura os dados do formulário
        title = request.POST.get('title')
        description = request.POST.get('description')
        emotions = request.POST.getlist('emotions')

        # Cria o novo sonho e salva
        dream = Dream.objects.create(
            user=request.user,
            title=title,
            description=description
        )

        # Associa as emoções ao sonho
        for emotion_id in emotions:
            try:
                emotion = Emotion.objects.get(id=emotion_id)
                DreamEmotion.objects.create(dream=dream, emotion=emotion)
            except Emotion.DoesNotExist:
                continue  # Caso a emoção não exista, ignoramos

        # Redireciona para a página de "Meus Sonhos"
        return redirect('meus_sonhos')

    else:
        # Se o método não for POST, apenas mostra o formulário vazio
        emotions = Emotion.objects.all()
        return render(request, 'pages/new_dream.html', {'emotions': emotions})

def about (request):
    return render(request, 'pages/about.html')
    


# CRUD SONHOS
def saveDream(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        emotions_ids = request.POST.getlist("emotions")  # Lista de IDs das emoções selecionadas
        user = request.user  # Usuário logado

        dream = Dream.objects.create(user=user, title=title, description=description)

        # Associar emoções ao sonho
        for emotion_id in emotions_ids:
            emotion = Emotion.objects.get(id=emotion_id)
            DreamEmotion.objects.create(dream=dream, emotion=emotion)

        return redirect("meus_sonhos")  # Redireciona para a página de sonhos do usuário

    return render(request, "pages/new_dream.html")


def deleteDream(request, id):
    # Busca o sonho pelo ID ou retorna 404 se não encontrado
    sonho = get_object_or_404(Dream, id=id)

    # Verifica se o usuário logado é o dono do sonho
    if sonho.user == request.user:
        sonho.delete()  # Exclui o sonho
      
    return redirect('meus_sonhos')  # Redireciona de volta para a lista de sonhos


import google.generativeai as genai
from django.http import JsonResponse

genai.configure(api_key="AIzaSyCTwlnep5--qk4HeWA-VIf6DLO8XnuVeTk")

import logging
logger = logging.getLogger(__name__)  # Para registrar os erros no log do Django

def generate_interpretation(request, id):
    if request.method == "POST":
        try:
            sonho = get_object_or_404(Dream, id=id)

            # Obtém as emoções associadas ao sonho
            emotions = sonho.dream_emotions.all()
            emotion_texts = [f"{de.emotion.name} ({de.emotion.category})" for de in emotions]
            emotion_list = ", ".join(emotion_texts) if emotion_texts else "Nenhuma emoção associada"

            # Constrói o prompt
            modo = request.POST.get('modo', 'formal')  # Padrão: formal
            prompt = f"""
            Você é um especialista em interpretação de sonhos. Analise o sonho abaixo e forneça uma interpretação profunda:

            **Título:** {sonho.title}
            **Descrição:** {sonho.description}
            **Emoções associadas:** {emotion_list}

            Interprete o sonho de forma {modo}, considerando as emoções e possíveis significados psicológicos e simbólicos.

            deve ser organizado em formado de texto normal, e no máximo 3 páragrafos
            """

            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt)

            if not response or not hasattr(response, 'text'):
                raise ValueError("Resposta inválida da API Gemini")

            interpretation = response.text

            # Atualiza o sonho no banco de dados
            sonho.interpretation = interpretation
            sonho.save()

            return JsonResponse({"interpretation": interpretation})

        except Exception as e:
            logger.error(f"Erro ao gerar interpretação: {str(e)}")
            return JsonResponse({"error": f"Erro interno: {str(e)}"}, status=500)

    return JsonResponse({"error": "Método inválido"}, status=400)