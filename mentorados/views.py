from django.shortcuts import render, redirect
#from django.http import HttpResponse, Http404
from .models import Mentorado, Navigator
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.
def mentorados(request):
    if(not request.user.is_authenticated):
        return redirect('login')
    if(request.method == "GET"):
        navigators = Navigator.objects.filter(user=request.user)
        mentorados = Mentorado.objects.filter(user=request.user)
        return render(request, 'mentorados.html', {'stages': Mentorado.stages_choices, 'navigators' : navigators, 'mentorados' : mentorados})

    if(request.method == "POST"):
        nome = request.POST.get('nome')
        foto = request.FILES.get('foto')
        estagio = request.POST.get("estagio")
        navigator = request.POST.get('navigator')

        mentorado = Mentorado(
                        name=nome,
                        photo=foto,
                        stage=estagio,
                        navigator_id=navigator,
                        user = request.user,
        )

        mentorado.save()
        messages.add_message(request, constants.SUCCESS, 'Mentorado cadastrado com sucesso.')
        return redirect('mentorados')
