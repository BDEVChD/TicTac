
import schedule
import time
import requests
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tictacky.settings')
django.setup()
from tictacky.models import GameState

def job():

    if GameState.objects.filter(game_id__isnull=False).exists():
        print("Game already exists in the database.")
    else:
        # If no game exists, register a new game
        game_registration_url = "https://xo.fullyaccountable.com/game/register"
        payload = {"team_name": "frogs"}
        try:
            response = requests.post(game_registration_url, json=payload)
            if response.status_code == 200:
                game_data = response.json()
                game_id = game_data.get("game_id")
                secret = game_data.get("secret")
                # Save game_id and secret to the database
                GameState.objects.create(team_name='frogs', game_id=game_id, secret=secret)
                print("Game registered successfully! Game ID:", game_id)
            else:
                print("Failed to register the game:", response.text)
        except Exception as e:
            print("An error occurred while registering the game:", e)


    #   game_id = "YOUR_GAME_ID_HERE"  # Replace with the actual game ID
    # url = f"https://xo.fullyaccountable.com/{game_id}/status"
    # try:
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         game_status = response.json()
    #         current_team = game_status.get("current_team")
    #         status = game_status.get("status")
    #         last_move = game_status.get("last_move")

    #         print("Current Team:", current_team)
    #         print("Status:", status)
    #         print("Last Move:", last_move)

    #         # If last_move is NULL, make a first move and set game_started to true
    #         if last_move is None:
    #             # Make your first move here
    #             # For example:
    #             # first_move_url = f"https://xo.fullyaccountable.com/game/{game_id}/move"
    #             # first_move_payload = {"move": "A1"}  # Make your move here
    #             # response = requests.post(first_move_url, json=first_move_payload)
    #             # Handle response and update game state accordingly

    # except Exception as e:
    #     print("An error occurred while fetching game status:", e)
    # print("Game Registered Successfully! Game ID: ")

schedule.every(10).seconds.do(job)  # Adjust frequency as needed

while True:
    schedule.run_pending()
    time.sleep(1)


def register_game(request):
    # Generate game_id
    game_id = ''

    # Generate secret
    secret = ''
    # Initial pieces available
    pieces_available = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']

    # Save to database
    game_state = tictacky_gamestate.objects.create(game_id=game_id, secret=secret, pieces_available=pieces_available)

    serializer = GameStateSerializer(game_state)