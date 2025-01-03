from django.contrib.auth import logout
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request,'users/home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, you have successfully created an account.')
            return redirect('home')

    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required()
def profile(request):
    return render(request, 'users/profile.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def index(request):
    return render(request,'users/index.html')
