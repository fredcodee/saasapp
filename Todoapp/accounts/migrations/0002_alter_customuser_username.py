# Generated by Django 4.0.4 on 2022-05-31 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(default='', max_length=40),
        ),
    ]
