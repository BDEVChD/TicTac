# Generated by Django 5.0.2 on 2024-04-19 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tictacky', '0007_remove_opponentmoves_game_state_opponentmoves_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='winoutcome',
            name='default_wins',
            field=models.TextField(default='[["A1", "A2", "A3"], ["C1", "C2", "C3"], ["A1", "B1", "C1"], ["A3", "B3", "C3"], ["A2", "B2", "C2"], ["B1", "B2", "B3"], ["A1", "B2", "C3"], ["C1", "B2", "C3"]]'),
        ),
    ]
