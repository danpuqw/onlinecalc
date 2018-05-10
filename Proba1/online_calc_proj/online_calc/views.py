from django.shortcuts import render
from online_calc.forms import credit_form, DD_LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from online_calc.models import credit, pay_graf, credit_temp
from django.http import HttpResponseRedirect
from django.utils import timezone
import datetime


def my_count(all_cost, first_pay, term, term_modif, percent):
    if term_modif == 'лет':
        term = term * 12
    percent = percent / 12 / 100
    i = 1
    znam = 1
    while i < term:
        znam = znam + (1 + percent) ** i
        i = i + 1
    month_pay = ((all_cost - first_pay) * ((1 + percent) ** term)) / znam
    all_pay = month_pay * term
    over_pay = all_pay - all_cost
    i = 1
    now = timezone.now()
    cur_date = now
    pay_count = month_pay
    all_left = all_cost - first_pay
    while i < term + 1:
        old_count = all_left
        all_left = all_left * (1 + percent)
        all_left = all_left - pay_count
        pay_cred = old_count - all_left
        pay_percent = pay_count - pay_cred
        delta = datetime.timedelta(days=1)
        if cur_date.month == 3 or 5 or 8 or 10:
            delta = datetime.timedelta(days=30)
        if cur_date.month == 2 or 4 or 6 or 7 or 9 or 11 or 12:
            delta = datetime.timedelta(days=31)
        if cur_date.month == 1:
            delta = datetime.timedelta(days=28)
        cur_date = cur_date + delta
        new_str = pay_graf.objects.create(date=cur_date, pay_count=pay_count, all_left=all_left,
                                          pay_cred=pay_cred, pay_percent=pay_percent)
        new_str.save()
        i = i + 1
    y = pay_graf.objects.all().last()
    if term_modif == 'лет':
        term = term / 12
    new_credit = credit_temp.objects.create(all_cost=all_cost,term=term,term_modif=term_modif,first_pay=first_pay,percent=percent)
    new_credit.save()
    last_credit_temp = credit_temp.objects.last()
    temp_id = last_credit_temp.id
    result = {'pay_count': pay_count, 'all_pay': all_pay, 'over_pay': over_pay, 'temp_id': temp_id}
    return result


def portal_main(request):
    if request.method == 'POST':
        pay_graf.objects.all().delete()
        credit_temp.objects.all().delete()
        form = credit_form(request.POST)
        if form.is_valid():
            all_cost = form.cleaned_data['all_cost']
            first_pay = form.cleaned_data['first_pay']
            term = form.cleaned_data['term']
            term_modif = form.cleaned_data['term_modif']
            percent = form.cleaned_data['percent']
            counted = my_count(all_cost, first_pay, term, term_modif, percent)
            pay_count = counted['pay_count']
            all_pay = counted['all_pay']
            over_pay = counted['over_pay']
            temp_id = counted['temp_id']
            cur_pay_graf = pay_graf.objects.all()
            if request.user.username != "":
                u_name = request.user.username
            else:
                u_name = ""
            return render(request, 'main.html', {'form': form, 'pay_count': pay_count, 'all_pay': all_pay,
                                                 'over_pay': over_pay, 'cur_pay_graf': cur_pay_graf,
                                                 'temp_id': temp_id, 'u_name': u_name})
    else:
        if request.user.username != "":
            u_name = request.user.username
        else:
            u_name = ""
        form = credit_form()
        return render(request, 'main.html', {'form':form,'u_name':u_name})


def DD_login(request):
    if request.method == 'POST':
        form = DD_LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    print("User is valid, active and authenticated")
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    print("The password is valid, but the account has been disabled!")
            else:
                print("The username and password were incorrect.")
    else:
        form = DD_LoginForm()
    return render(request, 'login.html', {'form': form})


def DD_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            new_user = User.objects.create_user(username=username,
                                 email=email,
                                 password=password)
            new_user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    print("User is valid, active and authenticated")
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    print("The password is valid, but the account has been disabled!")
            else:
                print("The username and password were incorrect.")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form':form})


def save(request, id):
    if request.user.username != "":
        cur_credit_temp = credit_temp.objects.get(pk=id)
        user = request.user
        all_cost = cur_credit_temp.all_cost
        first_pay = cur_credit_temp.first_pay
        percent = cur_credit_temp.percent
        term = cur_credit_temp.term
        term_modif = cur_credit_temp.term_modif
        cur_left = cur_credit_temp.all_cost - cur_credit_temp.first_pay
        creation_date = datetime.datetime.now()
        new_credit = credit.objects.create(all_cost=all_cost, first_pay=first_pay, percent=percent, term=term, term_modif=term_modif, owner=user, cur_left=cur_left, creation_date=creation_date)
        new_credit.save()
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/login/')


def show_credits(request):
    user = request.user
    if request.user.username != "":
        u_name = request.user.username
    else:
        u_name = ""
    cur_credits = credit.objects.filter(owner=user.id)
    for cred in cur_credits:
        delta = timezone.now() - cred.creation_date
        if cred.term_modif == 'лет':
            term = cred.term * 12
        else:
            term = cred.term
        percent = cred.percent / 12 / 100
        i = 1
        znam = 1
        while i < term:
            znam = znam + (1 + percent) ** i
            i = i + 1
        month_pay = ((cred.all_cost - cred.first_pay) * ((1 + percent) ** term)) / znam
        k = 1
        payed = 0
        while k < delta.days:
            payed = payed + month_pay
            k = k + 30
        cur_left = cred.all_cost - cred.first_pay - payed
        cred.cur_left = cur_left
    return render(request, 'saved_credits.html', {'credits':cur_credits,'u_name':u_name})


def delete(request, id):
    cur_credit = credit.objects.get(pk=id)
    cur_credit.delete()
    return HttpResponseRedirect('/saved_credits/')


def show_all(request, id):
    cur_credit = credit.objects.get(pk=id)
    pay_graf.objects.all().delete()
    credit_temp.objects.all().delete()
    counted = my_count(cur_credit.all_cost, cur_credit.first_pay, cur_credit.term, cur_credit.term_modif, cur_credit.percent)
    pay_count = counted['pay_count']
    all_pay = counted['all_pay']
    over_pay = counted['over_pay']
    temp_id = counted['temp_id']
    cur_pay_graf = pay_graf.objects.all()
    if request.user.username != "":
        u_name = request.user.username
    else:
        u_name = ""
    return render(request, 'show.html', {'pay_count': pay_count, 'all_pay': all_pay,
                                         'over_pay': over_pay, 'cur_pay_graf': cur_pay_graf,
                                         'temp_id': temp_id, 'u_name': u_name})







