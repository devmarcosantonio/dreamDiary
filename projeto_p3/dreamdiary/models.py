from django.db import models
from django.contrib.auth.models import AbstractUser

# 🔹 1. Modelo de Usuário (User)
class User(AbstractUser):  # Extende o User padrão do Django
    email = models.EmailField(unique=True)  # E-mail único
    password = models.CharField(max_length=128)  # Senha segura
    first_name = models.CharField(max_length=50)  # Nome
    last_name = models.CharField(max_length=50)  # Sobrenome

    USERNAME_FIELD = "email"  # Login será pelo email
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# 🔹 2. Modelo de Sonho (Dream)
class Dream(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dreams")  # Ligação com usuário
    title = models.CharField(max_length=200)  # Título do sonho
    description = models.TextField()  # Descrição do sonho
    interpretation = models.TextField(blank=True, null=True)  # Interpretação do sonho
    date = models.DateField(auto_now_add=True)  # Data do sonho

    def __str__(self):
        return self.title

# 🔹 3. Modelo de Emoções (Emotion)
class Emotion(models.Model):
    category = models.CharField(max_length=100)  # Categoria da emoção (exemplo: positiva, negativa)
    name = models.CharField(max_length=50, unique=True)  # Nome da emoção (exemplo: felicidade, medo)

    def __str__(self):
        return self.name

# 🔹 4. Tabela intermediária (DreamEmotion)
class DreamEmotion(models.Model):
    dream = models.ForeignKey(Dream, on_delete=models.CASCADE, related_name="dream_emotions")  # Sonho
    emotion = models.ForeignKey(Emotion, on_delete=models.CASCADE, related_name="dream_emotions")  # Emoção

    class Meta:
        unique_together = ("dream", "emotion")  # Garante que a mesma emoção não seja repetida no mesmo sonho

    def __str__(self):
        return f"{self.dream.title} - {self.emotion.name}"
