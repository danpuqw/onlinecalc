# Generated by Django 2.0.1 on 2018-05-10 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('online_calc', '0005_auto_20180510_1448'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='credit',
            name='term_modif',
        ),
    ]
