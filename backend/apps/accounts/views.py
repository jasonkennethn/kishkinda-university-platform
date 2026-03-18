from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponse
from .forms import LoginForm
from .decorators import role_required

def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('accounts:dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    return render(request, 'accounts/dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

def access_denied_view(request):
    return render(request, 'accounts/access_denied.html')

@role_required(allowed_roles=['super_admin'])
def super_admin_panel(request):
    return render(request, 'accounts/super_admin_panel.html')

@role_required(allowed_roles=['super_admin', 'university_admin', 'college_admin'])
def admin_zone(request):
    return render(request, 'accounts/admin_zone.html')
