from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver  # Add this import statement


class GameState(models.Model):
    game_id = models.CharField(max_length=50)
    secret = models.CharField(max_length=100)
    game_started = models.DateTimeField(auto_now_add=True)
    pieces_available = models.IntegerField(default=0)

class WinOutcome(models.Model):
    game_state = models.ForeignKey(GameState, on_delete=models.CASCADE, related_name='win_outcomes')
    win_combination = models.TextField()  # JSON list of winning pieces



class OpponentMoves(models.Model):
    game_state = models.ForeignKey(GameState, on_delete=models.CASCADE, related_name='opponent_moves')
    moves_list = models.TextField()

@receiver(post_save, sender=GameState)
def create_win_outcome(sender, instance, created, **kwargs):
    if created:
        default_moves = [
            ['A1', 'A2', 'A3'],
            ['C1', 'C2', 'C3'],
            ['A1', 'B1', 'C1'],
            ['A3', 'B3', 'C3'],
            ['A2', 'B2', 'C2'],
            ['B1', 'B2', 'B3'],
            ['A1', 'B2', 'C3'],
            ['C1', 'B2', 'C3']
        ]
       