from django.shortcuts import render, HttpResponse, redirect
from models import *
from datetime import datetime 
from django.contrib import messages
import bcrypt


def index(request):
    return render(request, 'users/index.html')

def verify(request):
    if len(request.POST['name']) == 0 or len(request.POST['dob']) == 0 or len(request.POST['alias']) == 0 or len(request.POST['email']) == 0 or len(request.POST['password']) == 0:
        messages.error(request, 'All fields must be filled out!')
        return redirect ('/')
    if not request.POST['name'].replace(' ','').isalpha():
        messages.error(request,'Name can only contain letters!')
        return redirect ('/')
    if request.POST['password'] != request.POST['confirm_pw']:
        messages.error(request,'Passwords must match!')
        return redirect ('/')
    if len(request.POST['password']) < 8:
        messages.error(request,'Passwords must be at least 8 characters long!')
        return redirect ('/')
    if datetime.now() <= datetime.strptime(request.POST['dob'], "%Y-%m-%d"):
        messages.error(request,'Date of birth must be in the past')
        return redirect ('/')

    password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    new_user = User.objects.create(name= request.POST['name'], alias = request.POST['alias'], email = request.POST['email'], password = password_hash, dob = request.POST['dob'])
    request.session['id'] = new_user.id
    request.session['name'] = new_user.name
    return redirect('/quotes')

def login(request):
    user = User.objects.filter(email = request.POST['email'])
    if len(user) > 0:
        user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['name'] = user.name
            request.session['id'] = user.id
            return redirect('/quotes')
        else:
            messages.error(request, 'Email/Password invalid')
            return redirect('/')
    else:
        messages.error(request, 'User not found') 
    return redirect('/') 

def quotes(request):
    quotes = Quote.objects.exclude(quotes = request.session['id'])
    favs = Quote.objects.filter(quotes = request.session['id'])
    context = {
        "quotes": quotes,
        "favs": favs
    }
    return render(request,'users/quotes.html', context)

def process(request):
    if len(request.POST['person']) == 0 or len(request.POST['message']) == 0:
        messages.error(request, 'All fields must be filled out!')
        return redirect ('/quotes')
    if len(request.POST['person']) < 3:
        messages.error(request, 'Person must be at least 3 characters!')
        return redirect ('/quotes')
    if len(request.POST['message']) < 10:
        messages.error(request, 'Message must be more that 10 characters!')
        return redirect ('/quotes')
    new_quote = Quote.objects.create(quoted_by = request.POST['person'], message = request.POST['message'], poster = User.objects.get(id = request.session['id']))
    return redirect('/quotes')

def user_page(request, number):   
    user_quote = User.objects.filter(id = number)
    quote = Quote.objects.filter(poster = user_quote)
    length = len(Quote.objects.filter(poster = user_quote))
    count = str(length)
    context = {
        "user_quote": user_quote,
        "quote": quote,
        "count": count
    }
    return render (request, 'users/user_page.html', context)

def add(request, number):
    user = User.objects.get(id = request.session['id'])
    quote = Quote.objects.get(id = number)
    quote.quotes.add(user)
    return redirect('/quotes')

def remove(request, number):
    user = User.objects.get(id = request.session['id'])
    quote = Quote.objects.get(id = number)
    quote.quotes.remove(user)
    return redirect('/quotes')

def logout(request):
    del request.session  
    return redirect('/')