from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser): 
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128) 
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50) 

    USERNAME_FIELD = "email"  # Login será pelo email
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Dream(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dreams") 
    title = models.CharField(max_length=200) 
    description = models.TextField() 
    interpretation = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True) 

    def __str__(self):
        return self.title

# 🔹 3. Modelo de Emoções (Emotion)
class Emotion(models.Model):
    category = models.CharField(max_length=100)  
    name = models.CharField(max_length=50, unique=True) 

    def __str__(self):
        return self.name


class DreamEmotion(models.Model):
    dream = models.ForeignKey(Dream, on_delete=models.CASCADE, related_name="dream_emotions") 
    emotion = models.ForeignKey(Emotion, on_delete=models.CASCADE, related_name="dream_emotions")  

    class Meta:
        unique_together = ("dream", "emotion")  

    def __str__(self):
        return f"{self.dream.title} - {self.emotion.name}"
