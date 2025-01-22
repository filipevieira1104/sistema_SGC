from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from .models import UserProfile

# View registro ajustada
def registro(request):
    if request.method == "GET":
        return render(request, 'registro.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        whatsapp = request.POST.get('whatsapp')

        if not all([username.strip(), email.strip(), whatsapp.strip(), password.strip()]):
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('registro')

        if User.objects.filter(email=email).exists():
            messages.add_message(request, constants.ERROR, 'E-mail já cadastrado')
            return redirect('registro')

        # Criação do usuário
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.profile.whatsapp = whatsapp  # Atualiza o campo whatsapp no UserProfile
            user.profile.save()  # Salva o perfil
            login(request, user)
            messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso!')
            return redirect('login')
        except Exception as e:
            messages.add_message(request, constants.ERROR, 'Erro ao registrar usuário')
            return redirect('registro')


def login_view(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('criar_solicitacao')
        else:
            messages.add_message(request, constants.ERROR, 'Credenciais Inválidas')
    return redirect('login')        

def logout_view(request):
    logout(request)
    messages.add_message(request, constants.INFO, 'Para acessar o sistema novamente, realize seu login!')
    return redirect('login')  