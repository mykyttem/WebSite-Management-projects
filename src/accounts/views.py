from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password

from .forms import AccountsForm_SignUp, AccountsForm_SignIn
from .models import Accounts


#FIXME: don't save photo user
def sign_up(request):
    """
    Get data for fields
    Hashing password
    Save and redirect for page sign in
    """
    form = AccountsForm_SignUp(request.POST)

    if request.method == "POST":
        if form.is_valid():
            # Get model form, but don't save 
            account = form.save(commit=False)
            login = form.cleaned_data['login']

            # Hashing password
            encrypted_password = make_password(form.cleaned_data['password'])

            # Accept hashing password for model
            account.password = encrypted_password

            # checking duplicate login in DB
            if Accounts.objects.filter(login=login).exists():
                messages.success(request, f'Логін "{login}" вже зайнятий, оберіть інший')
            else:
                form.save()
                return redirect('/sign-in')

    
    return render(request, 'sign_up.html', {'form': form})


def sign_in(request):
    form = AccountsForm_SignIn(request.GET)

    if request.method == 'GET':
        if form.is_valid():
            login = form.cleaned_data['login']       
            password = form.cleaned_data['password']
            

            if Accounts.objects.filter(login=login).exists():
                user_account = Accounts.objects.get(login=login)

                if check_password(password, user_account.password):
                    request.session['user-login'] = login
                    return redirect(f'/my-profile/{login}')
                else:

                    messages.success(request, 'Пароль не вірний')
                    return redirect('/sign-in')
            else:
                messages.success(request, 'Акаунт не знайдений, перевірьте коректні дані')
                return redirect('/sign-in')


    return render(request, 'sign_in.html', {'form': form})


def my_profile(request, login):
    return HttpResponse(f'Профіль користувача {login}')