from django.db import models
from django.contrib.auth.models  import User
from datetime import timedelta
import secrets


class Navigator(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nome")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Mentor") #mentor
    created_at = models.DateField(auto_now_add=True, verbose_name="Data de criação")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Navigator'
        verbose_name_plural = 'Navigators'
    

class Mentorado(models.Model):
    stages_choices = (
        ('E1', '10-100k'),
        ('E2', '100-500k'),
        ('E3', '500-...')
    )
    name = models.CharField(
        max_length=255, 
        verbose_name="Nome"
    )
    photo = models.ImageField(
        upload_to='photos', 
        null=True,
        blank=True, 
        verbose_name="Foto",
    )
    stage = models.CharField(max_length=2, choices=stages_choices, verbose_name="Estágio")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Mentor") #mentor
    navigator = models.ForeignKey(
        Navigator, 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE,
        verbose_name="Navigator"
    )
    created_at = models.DateField(auto_now_add=True)
    token = models.CharField(max_length=16, null=True, blank=True)

    def save(self, *args, **kwargs):
        if(not self.token):
            self.token = self.generate_unique_token()
        super().save(*args, **kwargs)

    
    def generate_unique_token(self):
        while(True):
            token =secrets.token_urlsafe(8)
            if (not Mentorado.objects.filter(token=token).exists()):
                return token

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Mentorado'
        verbose_name_plural = 'Mentorados'

class DisponibilidadeHorario(models.Model):
    init_date = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="Data inicial"
    )
    mentor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="Mentor"
    )
    is_scheduled = models.BooleanField(
        default=False,
        verbose_name="Está agendado"
    )

    def endDate(self):
        return self.init_date + timedelta(minutes=50)

    def __str__(self):
        return str(self.init_date)

    class Meta:
        verbose_name = 'Disponibilidade de Horário'
        verbose_name_plural = 'Disponibilidade de Horários'


class Reuniao(models.Model):
    tag_choices = (
        ('G', 'Gestão'),
        ('M', 'Marketing'),
        ('RH', 'Gestão de Pessoas'),
        ('I', 'Impostos'),
    )
    data = models.ForeignKey(DisponibilidadeHorario, on_delete=models.CASCADE, verbose_name="Data")
    mentorado = models.ForeignKey(Mentorado, on_delete=models.CASCADE, verbose_name="Mentorado")
    tag = models.CharField(max_length=2, choices=tag_choices, verbose_name="Tag")
    description = models.TextField(verbose_name="Descrição")
    created_at = models.DateField(auto_now_add=True, verbose_name="Data de criação")

    def __str__(self):
        return str(self.data.init_date)
    
    class Meta:
        verbose_name = 'Reunião'
        verbose_name_plural = 'Reuniões'

    