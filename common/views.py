from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .models import User
from .forms import UserForm

# Create your views here.
def main_page(request):
    return render(request, template_name='common/index.html')

def signup(request):
    if (request.method == 'POST'):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('common:main_page')
    else:
        form = UserForm()
    ctx = {
        'form': form
    }
    return render(request, 'common/signup.html', ctx)

def logout_page(request):
    logout(request)
    return redirect('common:main_page')