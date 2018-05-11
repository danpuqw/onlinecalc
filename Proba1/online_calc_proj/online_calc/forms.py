from django import forms
from django.forms import ModelForm
from online_calc.models import credit

class credit_form(ModelForm):
    class Meta:
        model = credit
        fields = ['all_cost','first_pay','term','term_modif','percent']
        labels = {
            'all_cost': 'Общая сумма',
            'first_pay': 'Первоначальный взнос',
            'term': 'Срок выплат',
            'percent': 'Процентная ставка',
            'term_modif': '',
        }
        widgets = {

        }


class DD_LoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя", max_length=64)
    password = forms.CharField(label="Пароль",widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    username = forms.CharField(label="Имя пользователя", max_length=64)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    email = forms.EmailField(label="Электронная почта", widget=forms.EmailInput())