from django.contrib import admin
from .models import Navigator, Mentorado, DisponibilidadeHorario, Reuniao
# Register your models here.

admin.site.register(Navigator)
admin.site.register(Mentorado)
admin.site.register(DisponibilidadeHorario)
admin.site.register(Reuniao)
# admin.site.register(Mentorado)