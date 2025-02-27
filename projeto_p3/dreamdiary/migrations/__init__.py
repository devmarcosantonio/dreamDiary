from django.db import migrations

def populate_emotions(apps, schema_editor):
    Emotion = apps.get_model("dreamdiary", "Emotion")  # Ajuste conforme necessário
    emotions = [
        {"category": "emocao-boa", "name": "Alegria"},
        {"category": "emocao-boa", "name": "Euforia"},
        {"category": "emocao-boa", "name": "Paz"},
        {"category": "emocao-boa", "name": "Paixão"},
        {"category": "emocao-boa", "name": "Surpresa"},
        {"category": "emocao-boa", "name": "Nostalgia"},
        {"category": "emocao-ruim", "name": "Vergonha"},
        {"category": "emocao-ruim", "name": "Confusão"},
        {"category": "emocao-ruim", "name": "Constrangimento"},
        {"category": "emocao-ruim", "name": "Tristeza"},
        {"category": "emocao-ruim", "name": "Medo"},
        {"category": "emocao-ruim", "name": "Ansiedade"},
        {"category": "emocao-ruim", "name": "Raiva"},
        {"category": "emocao-ruim", "name": "Frustração"},
    ]

    for emotion in emotions:
        Emotion.objects.get_or_create(category=emotion["category"], name=emotion["name"])

class Migration(migrations.Migration):

    dependencies = [
        ("dreamdiary", "0001_initial"),  # Substitua pela última migration existente
    ]

    operations = [
        migrations.RunPython(populate_emotions),
    ]
