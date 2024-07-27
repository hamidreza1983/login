from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import *
from django.core.mail import send_mail
from django.contrib.auth import login, password_validation
from rest_framework.authtoken.models import Token
from django.contrib.auth.forms import UserCreationForm
import uuid

# Create your views here.


def login_user(request):
    global redirection

    form = LoginForm()
    context = {
            'form': form,
        }
    if request.method == "GET" : 
        return render(request, 'registrations/login.html', context=context)
    elif request.method == "POST" :
        try : 
            user = User.objects.get(email=request.POST.get('email'))
            redirection = 0
        except:
            user = User.objects.create(email=request.POST.get('email'), username = uuid.uuid4 )
            redirection = 1
        token, create = Token.objects.get_or_create(user=user)
        send_mail(
        "confirmation email",
        f"please confirm your email \n\n http://127.0.0.1:8000/accounts/email-confirmation/{token.key}",
        "admin@admin.com",
        [request.POST.get('email')],
        fail_silently=True,
    )
        return render(request, 'registrations/fine.html', context=context)

def signup(request, token):
    user = Token.objects.get(key=token).user
    if redirection == 0:
        login(request, user)
        print ('login')
        return redirect('root:home')
    else:
        form = UserCreationForm()
        context = {
                'form': form,
            }
        if request.method == "GET" : 
            return render(request, 'registrations/signup.html', context=context)
        elif request.method == "POST" :
            form = UserCreationForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if password1 == password2:
                    user.username = username
                    password_validation.validate_password(password1)
                    user.set_password(password1)
                    user.save()
                    login(request, user)
                    return redirect('root:home')




