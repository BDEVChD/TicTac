# Generated by Django 5.0.2 on 2024-04-19 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tictacky', '0004_alter_gamestate_pieces_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='winoutcome',
            name='my_strategy',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='winoutcome',
            name='opponent_strategy',
            field=models.JSONField(default=list),
        ),
    ]
