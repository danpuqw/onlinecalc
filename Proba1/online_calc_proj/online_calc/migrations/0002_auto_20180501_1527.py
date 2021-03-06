# Generated by Django 2.0.1 on 2018-05-01 12:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('online_calc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='credit_temp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('all_cost', models.IntegerField()),
                ('first_pay', models.IntegerField()),
                ('term', models.IntegerField()),
                ('term_modif', models.CharField(max_length=20)),
                ('percent', models.DecimalField(decimal_places=2, max_digits=14)),
            ],
        ),
        migrations.AddField(
            model_name='credit',
            name='owner',
            field=models.ForeignKey(default=1, on_delete='cascade', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
