# Generated by Django 5.0.2 on 2024-04-17 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tictacky', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamestate',
            name='team_name',
            field=models.CharField(default='frogs', max_length=50),
        ),
    ]
