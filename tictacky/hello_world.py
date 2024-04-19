
import schedule
import time
import requests
import os
import django
import json
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tictacky.settings')
django.setup()
from tictacky.models import GameState
from tictacky.models import WinOutcome

def job():

    if GameState.objects.filter(game_id__isnull=False).exists():
        print("Game already exists in the database." ) 


        game_states = GameState.objects.all()

        for game_state in game_states:
            status = game_state.check_game_state()
            if (status[0] == 'frogs'):
                # Make a move
        
                game_state.make_move(game_state, status)
            else:
                if status[2] is not None:
                    print("It's the opponent's turn!")
                    moves = status[2]
                    print(moves)
                    win_outcome = WinOutcome.objects.get(pk=1)
        

                    test = random.randint(0, len(json.loads(win_outcome.win_combination)) -1)
                    win_outcome = WinOutcome.objects.get(pk=1)
             
                    win_outcome.my_strategy = [test]
                    win_outcome.save()
                    print('my strategy', win_outcome.my_strategy)

                    my_strategy = json.loads(win_outcome.win_combination)[win_outcome.my_strategy[0]]

                    opponent_strategy = win_outcome.opponent_strategy
                    if not opponent_strategy:
                        print('opponent_strategy is empty')
                        if my_strategy:
            
                            move = my_strategy[0]
                        
                            if(move in game_state.get_pieces_available()):
                            
                                game_state.remove_piece(move)
                                url = f"https://xo.fullyaccountable.com/game/{game_state.game_id}/move"
                                payload = {
                                    "GAME_ID": game_state.game_id,
                                    "team_name": game_state.team_name,
                                    "secret": game_state.secret,
                                    "move": move, 
                                }
                                response = requests.post(url, data=payload)
                                # break
                                # print('mystrategy', my_strategy)

                                myindexstrategy = win_outcome.my_strategy[0]

                                win_combination_list = json.loads(win_outcome.win_combination)
                                

                                if move in my_strategy:
                              
                                    #removes from winoutcomes
                                    win_combination_list[myindexstrategy].remove(move)
                                    win_outcome.win_combination = json.dumps(win_combination_list)
                                    win_outcome.save()
                                    del win_combination_list[move_index]

                                    #removes from available pieces
                                    pieces_available_list = json.loads(game_state.pieces_available) 
                                    pieces_available_list.remove(move)
                                    game_state.pieces_available = json.dumps(pieces_available_list)
                                    game_state.save()


                    else: 
                        print('opponent_strategy is not empty')
            
                 
                        
                       


           
                    # print(json.loads(win_outcome.win_combination)[0]) 
                    # random_number = random.randint(0, len(game_state.get_pieces_available()))
                    # move = game_state.get_piece_by_index(random_number)
                    # print("Move made: ", move)
      
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

                default_moves = [['A1', 'A2', 'A3'],
                            ['C1', 'C2', 'C3'],
                            ['A1', 'B1', 'C1'],
                            ['A3', 'B3', 'C3'],
                            ['A2', 'B2', 'C2'],
                            ['B1', 'B2', 'B3'],
                            ['A1', 'B2', 'C3'],
                            ['C1', 'B2', 'C3']]

                default_moves_json = json.dumps(default_moves)
                
                WinOutcome.objects.create(game_state=game_state, win_combination=default_moves_json, default_wins=default_moves_json)
                print("Game registered successfully! Game ID:", game_id)
                
            else:
                print('hi')

        except Exception as e:
            print("An error occurred while registering the game:", e)




schedule.every(1).seconds.do(job)  # Adjust frequency as needed

while True:
    schedule.run_pending()
    time.sleep(1)


    
# def register_game(request):


