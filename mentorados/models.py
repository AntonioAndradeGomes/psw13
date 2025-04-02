from django.db import models
from django.contrib.auth.models  import User

class Navigator(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE) #mentor
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Mentorado(models.Model):
    stages_choices = (
        ('E1', '10-100k'),
        ('E2', '100-500k'),
        ('E3', '500-...')
    )
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='photos', null=True, blank=True)
    stage = models.CharField(max_length=2, choices=stages_choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE) #mentor
    navigator = models.ForeignKey(Navigator, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
