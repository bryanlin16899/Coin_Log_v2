
from .models import Website_users, user_trade_records
from binance.exceptions import BinanceAPIException
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from crypto_app.user import GetUserInfo # user.py use to get user status,trade records...etc

def home(request):
    return render(request, 'index.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = GetUserInfo()
                user.api_key = request.POST['api_key']
                user.secret_key = request.POST['secret_key']
                if user.get_user_status():
                    user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                    user.save()
                    user_id = User.objects.get(username=request.POST['username']).id
                    api_info = Website_users(user_id=user_id, api_key=request.POST['api_key'], secret_key=request.POST['secret_key'])
                    api_info.save()
                    login(request, user)
                    return redirect('dashboard')
                else:
                    return render(request, 'signup.html', {'error': 'Your API key or Secret key is invalid.'})
            except IntegrityError:
                return render(request, 'signup.html', {'error': 'That username has already been taken \n try another one.'})
        else:
            return render(request, 'signup.html', {'error': 'Password did not match.'})
    # Design from Bryan lin: https://github.com/bryanlin16899


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {'error': 'Username and password did not match.'})
        else:
            login(request, user)
            return redirect('dashboard')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def dashboard(request):
    user = GetUserInfo()
    try:
        user_info = Website_users.objects.get(user=request.user)
        user.api_key = user_info.api_key
        user.secret_key = user_info.secret_key
        user.user_id = user_info.id
        if request.method == 'GET':
            user.load_trades_info()
            
            return render(request, 'dashboard.html',{
                'trade_records': user.get_trade_records(),
                'trade_info': user.cur_coin_detail(),
                'user_asset': user.get_asset()
            })
        elif request.method == 'POST':
            new_symbol = request.POST.get('inputTicker')
            if new_symbol in user.ALL_TICKERS:
                user.load_trades_info(symbol=new_symbol)
                return render(request, 'dashboard.html',{
                    'trade_records': user.get_trade_records(symbol=new_symbol),
                    'trade_info': user.cur_coin_detail(symbol=new_symbol),
                    'user_asset': user.get_asset()
                })
            else:
                return render(request, 'dashboard.html',
                              {
                               'error': 'Invalid Ticker',
                              })
        # if request.method == 'GET':
        #     return render(request, 'dashboard.html',
        #                   {
        #                    'this_coin': user.load_trades_info(),
        #                    'user_asset': user.get_asset()
        #                   })
        # elif request.method == 'POST':
        #     new_symbol = request.POST.get('inputTicker')
        #     if new_symbol in user.ALL_TICKERS:
        #         return render(request, 'dashboard.html',
        #                       {
        #                        'this_coin': user.load_trades_info(symbol=new_symbol),
        #                        'user_asset': user.get_asset()
        #                       })
        #     else:
        #         return render(request, 'dashboard.html',
        #                       {
        #                        'error': 'Invalid Ticker',
        #                        'user_asset': user.get_asset()
        #                       })
        # else:
        #     return render(request, 'dashboard.html',
        #                   {
        #                    'this_coin': user.load_trades_info(),
        #                    'user_asset': user.get_asset()
        #                   })
    except BinanceAPIException:
        return render(request, 'dashboard.html',
                      {
                        'error': 'Your API KEY or SECRET KEY did not correct.',
                      })


@login_required
def change_api_key(request):
    user_key_info = Website_users.objects.get(user=request.user)
    api_key = user_key_info.api_key
    secret_key = user_key_info.secret_key
    if request.method == 'GET':
        return render(request, 'change_user_api_key.html', {'api_key': api_key, 'secret_key': secret_key})
    else:
        user_key_info.api_key = request.POST['api_key']
        user_key_info.secret_key = request.POST['secret_key']
        user_key_info.save()
        return redirect('dashboard')
