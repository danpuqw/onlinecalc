from django.db import models
from django.contrib.auth.models import User

class credit(models.Model):
    all_cost = models.IntegerField()
    first_pay = models.IntegerField()
    term = models.IntegerField()
    term_modif = models.IntegerField(choices=(
        (1, 'месяцев'),
        (2, 'лет')
    ), default=2)
    percent = models.DecimalField(max_digits=14, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    cur_left = models.DecimalField(max_digits=14, decimal_places=2, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True)

class pay_graf(models.Model):
    date = models.DateField()
    pay_count = models.DecimalField(max_digits=14, decimal_places=2)
    pay_cred = models.DecimalField(max_digits=14, decimal_places=2)
    pay_percent = models.DecimalField(max_digits=14, decimal_places=2)
    all_left = models.DecimalField(max_digits=14, decimal_places=2)

class credit_temp(models.Model):
    all_cost = models.IntegerField()
    first_pay = models.IntegerField()
    term = models.IntegerField()
    term_modif = models.CharField(max_length=20)
    percent = models.DecimalField(max_digits=14, decimal_places=2)


