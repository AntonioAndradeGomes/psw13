from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib import auth



# Create your views here.
def cadastro(request):
    if(request.method == 'GET'):
        # Render the registration form
        return render(request, 'cadastro.html')
    if(request.method == 'POST'):
        # Process the form data
        username = request.POST.get('username')
        password = request.POST.get('senha')
        confirm_password = request.POST.get('confirmar_senha')

        #validate data
        if(not password == confirm_password):
            messages.add_message(request, constants.ERROR, 'Senha e Confirmar senha devem ser iguais.')
            return redirect('/users/cadastro')
        if(len(password) < 6):
            messages.add_message(request, constants.ERROR, 'A senha deve ter 6 ou mais caracteres.')
            return redirect('/users/cadastro')
        
        users = User.objects.filter(username = username)

        if(users.exists()):
            messages.add_message(request, constants.ERROR, 'Já existe um usuário com esse username.')
            return redirect('/users/cadastro')
        
        User.objects.create_user(username=username, password=password)
        
        return redirect('/users/login')

def login(request):
    if(request.method == 'GET'):
        return render(request, 'login.html')
    if(request.method == "POST"):
        username = request.POST.get("username")
        password = request.POST.get("senha")
        user = authenticate(request, username=username, password=password)
        if(user):
            auth.login(request, user)
            return redirect('/mentorados/')
        messages.add_message(request, constants.ERROR, "Username ou senha inválidos.")
        return redirect('login')