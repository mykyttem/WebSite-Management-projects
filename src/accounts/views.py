from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password

from .forms import AccountsForm_SignUp, AccountsForm_SignIn, UpdateAccount
from .models import Accounts

def auth_user(f):
    def wrapper(request, *args, **kwargs):
        idUser_session = request.session.get('user-id')
        user_account = Accounts.objects.filter(id=idUser_session).values()

        # checking for auth user
        if 'user-id' not in request.session:
            return redirect('/sign-up')  
        return f(request, user_account, *args, **kwargs)
    return wrapper


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
    """
    Get data for fields
    Checking hashing password
    Checking correct data account
    Redirect page profile
    """

    form = AccountsForm_SignIn(request.GET)

    if request.method == 'GET':
        if form.is_valid():
            login = form.cleaned_data['login']       
            password = form.cleaned_data['password']
            

            if Accounts.objects.filter(login=login).exists():
                user_account = Accounts.objects.get(login=login)

                if check_password(password, user_account.password):
                    request.session['user-login'] = login
                    request.session['user-id'] = user_account.id
                    return redirect(f'/my-profile/{login}')
                else:
                    messages.success(request, 'Пароль не вірний')
                    return redirect('/sign-in')
            else:
                messages.success(request, 'Акаунт не знайдений, перевірьте коректні дані')
                return redirect('/sign-in')


    return render(request, 'sign_in.html', {'form': form})


@auth_user
def my_profile(request, user_account, login):
    if 'logout' in request.POST:
        # get hidden element
        request.session.flush()
        return redirect('/sign-in')

    return render(request, 'profile.html')


#FIXME: don't save photo user
@auth_user
def settings(request, user_account, login):
    if request.method == "GET":
        id_user = request.session.get('user-id')
        form = UpdateAccount(request.GET)


        if form.is_valid():
            update_account = Accounts.objects.get(id=id_user)
            if update_account:

                # get input user
                name = form.cleaned_data['name']
                i_login = form.cleaned_data['login']
                email = form.cleaned_data['email']
                new_password = form.cleaned_data['password']

                # update data
                update_account.name = name
                update_account.login = i_login
                update_account.email = email
                update_account.password = make_password(new_password)

                update_account.save()
                request.session.flush()
                messages.success(request, 'Увійдіть знову')
                return redirect('/sign-in')


    return render(request, 'settings.html', {'form': form})