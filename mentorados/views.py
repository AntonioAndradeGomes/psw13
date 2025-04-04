from django.shortcuts import render, redirect
#from django.http import HttpResponse, Http404
from .models import Mentorado, Navigator, DisponibilidadeHorario, Reuniao
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime, timedelta
from .auth import validate_token


# Create your views here.
def mentorados(request):
    if(not request.user.is_authenticated):
        return redirect('login')
    if(request.method == "GET"):
        navigators = Navigator.objects.filter(user=request.user)
        mentorados = Mentorado.objects.filter(user=request.user)
        stages = Mentorado.stages_choices
        stages_flat = [i[1] for i in stages]
        qtd_stages = []
        for i, _ in stages:
            x = Mentorado.objects.filter(stage=i).filter(user=request.user).count()
            qtd_stages.append(x)
        
        return render(
                request,
                'mentorados.html', 
                        {
                            'stages':stages, 
                            'navigators' : navigators, 
                            'mentorados' : mentorados, 
                            'stages_flat' : stages_flat, 
                            'qtd_stages' : qtd_stages
                        }
        )

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
        messages.add_message(
            request, 
            constants.SUCCESS, 
            'Mentorado cadastrado com sucesso.'
        )
        return redirect('mentorados')


def reunioes(request):
    if(request.method == "GET"):
        return render(request, 'reunioes.html')
    if(request.method == "POST"):
        date = request.POST.get('data')
        date = datetime.strptime(date, '%Y-%m-%dT%H:%M')

        disps = DisponibilidadeHorario.objects.filter(mentor=request.user).filter(
            #gte -> maior ou igual
            init_date__gte=(date - timedelta(minutes=50)),
            init_date__lte=(date + timedelta(minutes=50))
        )

        if(disps.exists()):
            messages.add_message(
                request, 
                constants.ERROR, 
                'Você já possui uma reunião em aberto.'
            )
            return redirect('reunioes')
        
        disp = DisponibilidadeHorario(
            init_date = date,
            mentor = request.user
        )

        disp.save()
        messages.add_message(
            request, 
            constants.SUCCESS, 
            'Horário disponibilizado com sucesso.'
        )
        return redirect('reunioes')
    

def auth(request):
    if(request.method == "GET"):
        return render(request, 'auth_mentorado.html')
    if(request.method == "POST"):
        token = request.POST.get("token")
        mentorado = Mentorado.objects.filter(token=token)
        if (not Mentorado.objects.filter(token=token).exists()):
            messages.add_message(request, constants.ERROR, 'Token inválido')
            return redirect('auth_mentorado')
        
        response = redirect('escolher_dia')
        response.set_cookie('auth_token', token, max_age=3600)

        return response

def escolher_dia(request):
    if(not validate_token(request.COOKIES.get('auth_token'))):
        return redirect('auth_mentorado')
    if(request.method == "GET"):
        mentorado = validate_token(request.COOKIES.get('auth_token'))
        disp = DisponibilidadeHorario.objects.filter(
            init_date__gte=datetime.now(),
            is_scheduled = False,
            mentor=mentorado.user
        ).values_list('init_date', flat=True)
        dates = []
        for i in disp:
            dates.append(i.strftime('%d-%m-%Y'))
        dates = list(set(dates))

        #todo: ordenar e tornar o mes e dia da semana dinâmicos
        return render(request, 'escolher_dia.html',{'horarios': dates})

def agendar_reuniao(request):
    if (not validate_token(request.COOKIES.get('auth_token'))):
        return redirect('auth_mentorado')
    
    if(request.method == "GET"):
        data = request.GET.get('data')
        data = datetime.strptime(data, '%d-%m-%Y')
        mentorado = validate_token(request.COOKIES.get('auth_token'))
        hors = DisponibilidadeHorario.objects.filter(
            init_date__gte=data,
            init_date__lt=data + timedelta(days=1),
            is_scheduled=False,
            mentor=mentorado.user
        )
        print(hors.first().init_date.time())

        return render(request, 'agendar_reuniao.html', {'horarios': hors, 'tags' : Reuniao.tag_choices})
    
