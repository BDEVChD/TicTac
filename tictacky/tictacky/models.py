from django.db import models
from django.db.models.signals import post_save
import json
import requests
from django.dispatch import receiver 
import random


class GameState(models.Model):
    team_name = models.CharField(max_length=50, default='frogs')
    game_id = models.CharField(max_length=50)
    secret = models.CharField(max_length=100)
    game_started = models.DateTimeField(auto_now_add=True)
    pieces_available = models.TextField(default=json.dumps(['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']))

    def get_pieces_available(self):
        return json.loads(self.pieces_available)

    def get_piece_by_index(self, index):
        pieces_available = self.get_pieces_available()
        if 0 <= index < len(pieces_available):
            return pieces_available[index]
        return None

    def make_move(self, game_state, state):
        if state[1] != 'Completed':
            if state[2] is None:
                print("It's our turn!")
                # print("pieces available", game_state.get_pieces_available())
                # # randomly choose a win strategy/option
                random_number = random.randint(0, len(game_state.get_pieces_available()) -1)
                move = game_state.get_piece_by_index(random_number)
                print("Move made: ", move)
                game_state.remove_piece(move)
                url = f"https://xo.fullyaccountable.com/game/{game_state.game_id}/move"
                print(url)
                payload = {
                    "GAME_ID": game_state.game_id,
                    "team_name": game_state.team_name,
                    "secret": game_state.secret,
                    "move": move, 
                }

                print(payload)

                response = requests.post(url, data=payload)
            #test 
            # win_outcome = WinOutcome.objects.get(pk=1)
            # print(len(json.loads(win_outcome.win_combination))) 
            # random_number = random.randint(0, len(game_state.get_pieces_available()))
            # move = game_state.get_piece_by_index(random_number)
            # print("Move made: ", move)
            else: 
                print("It's MY TURN NOW!", state[2])
                win_outcome = WinOutcome.objects.get(pk=1)
                  
                mywinindex = win_outcome.my_strategy
                my_strategy = json.loads(win_outcome.win_combination)
                for win_outcome in WinOutcome.objects.all():
                    allcombos = win_outcome.win_combination
                    for index, combo in enumerate(json.loads(allcombos)):
                        if combo:
                            print("combo", combo)
                            print(index)
                            test = win_outcome.my_strategy
                            test.pop()
                            test.append(index)
                            win_outcome.save()
                            break
                    
                    move = my_strategy[win_outcome.my_strategy[0]][random.randint(0, len(my_strategy[win_outcome.my_strategy[0]]) -1)]
                    print("Strategy folded: ", move)
                    
                    url = f"https://xo.fullyaccountable.com/game/{game_state.game_id}/move"
                
                    payload = {
                        "GAME_ID": game_state.game_id,
                        "team_name": game_state.team_name,
                        "secret": game_state.secret,
                        "move": move, 
                    }
                # all registering of opponent moves and removing from winoutcomes and available pieces

                for win_outcome in WinOutcome.objects.all():
                    win_combination_list = json.loads(win_outcome.default_wins)
                    item_to_find = state[2]

                    for combination in win_combination_list:
            
                        if item_to_find in combination:
                            for opponent_move in OpponentMoves.objects.all():
                                if item_to_find in opponent_move.moves_list:
                                    # Increment count by 1
                                    opponent_move.count += 1
                                    opponent_move.save()
                                    print('alert danger')

                                else: 
                                    print('whoo')
                                    # Create a new OpponentMoves object
                                    # opponent_moves = OpponentMoves.objects.create(moves_list=combination)
                                    # opponent_moves.count += 1
                                    # opponent_moves.save()
                                    # combination.clear()
                                    # win_outcome.win_combination = json.dumps(win_combination_list)
                                    # win_outcome.save()

                    
                    opponent_move = state[2]
                    pieces_available_list = json.loads(game_state.pieces_available)
                    # pieces_available_list.remove(opponent_move)
                    # game_state.pieces_available = json.dumps(pieces_available_list)
                    # game_state.save()

                    #end housekeeping

                # scan all opponent moves if any counts are at 2, if so block  
                opponent_moves_to_block = OpponentMoves.objects.filter(count=2)

# Check if any danger cases were found
                if opponent_moves_to_block.exists():
                    print("Found OpponentMoves to block:")
                    
                    win_outcome = WinOutcome.objects.get(pk=1)
                  
                    mywinindex = win_outcome.my_strategy
                    my_strategy = json.loads(win_outcome.win_combination)
                    for win_outcome in WinOutcome.objects.all():
                        allcombos = win_outcome.win_combination
                        for index, combo in enumerate(json.loads(allcombos)):
                            if combo:
                                print("combo", combo)
                                print(index)
                                test = win_outcome.my_strategy
                                test.pop()
                                test.append(index)
                                win_outcome.save()
                                break
                       
                        move = my_strategy[win_outcome.my_strategy[0]][random.randint(0, len(my_strategy[win_outcome.my_strategy[0]]) -1)]
                        print("Strategy folded: ", move)
                        
                        url = f"https://xo.fullyaccountable.com/game/{game_state.game_id}/move"
                    
                        payload = {
                            "GAME_ID": game_state.game_id,
                            "team_name": game_state.team_name,
                            "secret": game_state.secret,
                            "move": move, 
                        }
                        response = requests.post(url, data=payload)
                        game_state.remove_piece(move)
                    if not my_strategy[mywinindex[0]]:
                        #find a new strategy 
                        for win_outcome in WinOutcome.objects.all():
                            allcombos = win_outcome.win_combination
                            for index, combo in enumerate(json.loads(allcombos)):
                                if combo:
                                    print("combo", combo)
                                    print(index)
                                    test = win_outcome.my_strategy
                                    test.pop()
                                    test.append(index)
                                    win_outcome.save()
                                    break
                       
                        move = my_strategy[win_outcome.my_strategy[0]][0]
                        print("Strategy folded: ", move)
                        
                        url = f"https://xo.fullyaccountable.com/game/{game_state.game_id}/move"
                    
                        payload = {
                            "GAME_ID": game_state.game_id,
                            "team_name": game_state.team_name,
                            "secret": game_state.secret,
                            "move": move, 
                        }
                        response = requests.post(url, data=payload)
                        game_state.remove_piece(move)
                else:
               
                    return
                    print("No OpponentMoves to block")           

                    win_outcome = WinOutcome.objects.get(pk=1)
                  
                    mywinindex = win_outcome.my_strategy
                    my_strategy = json.loads(win_outcome.win_combination)
              
                    if not my_strategy[mywinindex[0]]:
                        #find a new strategy 
                        for win_outcome in WinOutcome.objects.all():
                            allcombos = win_outcome.win_combination
                            for index, combo in enumerate(json.loads(allcombos)):
                                if combo:
                                    print("combo", combo)
                                    print(index)
                                    test = win_outcome.my_strategy
                                    test.pop()
                                    test.append(index)
                                    win_outcome.save()
                                    break
                        move = my_strategy[win_outcome.my_strategy[0]][0]
                        print("Strategy folded: ", move)
                        
                        url = f"https://xo.fullyaccountable.com/game/{game_state.game_id}/move"
                    
                        payload = {
                            "GAME_ID": game_state.game_id,
                            "team_name": game_state.team_name,
                            "secret": game_state.secret,
                            "move": move, 
                        }
                        response = requests.post(url, data=payload)
                        game_state.remove_piece(move)
                       
                    else: 
                         
                        move = my_strategy[win_outcome.my_strategy[0]][0]
                        print("Move made: ", move)
                        
                        url = f"https://xo.fullyaccountable.com/game/{game_state.game_id}/move"
                    
                        payload = {
                            "GAME_ID": game_state.game_id,
                            "team_name": game_state.team_name,
                            "secret": game_state.secret,
                            "move": move, 
                        }
                        response = requests.post(url, data=payload)
                        game_state.remove_piece(move)
            
                    

    def remove_piece(self, piece):
        pieces_available = self.get_pieces_available()
        updated_pieces_available = [p for p in pieces_available if p != piece]
        self.pieces_available = json.dumps(updated_pieces_available)
        self.save()

    def check_game_state(self):
        # Construct the URL for the API endpoint with the game ID
        url = f'https://xo.fullyaccountable.com/game/{self.game_id}/status'
    
        # Make a GET request to the API endpoint
        response = requests.get(url)
  
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the response JSON
            data = response.json()

    
            current_team = data.get('current_team')
            status = data.get('status')
            last_move = data.get('last_move')
            
                
            return current_team, status, last_move
        else:
            # Request was not successful, handle error or return None
            return None

class WinOutcome(models.Model):
    game_state = models.ForeignKey(GameState, on_delete=models.CASCADE, related_name='win_outcomes')
    win_combination = models.TextField() 
    default_wins = models.TextField(default=json.dumps([
        ['A1', 'A2', 'A3'],
        ['C1', 'C2', 'C3'],
        ['A1', 'B1', 'C1'],
        ['A3', 'B3', 'C3'],
        ['A2', 'B2', 'C2'],
        ['B1', 'B2', 'B3'],
        ['A1', 'B2', 'C3'],
        ['C1', 'B2', 'C3']
    ]))
    opponent_strategy = models.JSONField(default=list)  
    my_strategy = models.JSONField(default=list)  #
    def create_win_outcome(game_state):
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

        default_moves_json = json.dumps(default_moves)
        
        WinOutcome.objects.create(game_state=game_state, win_combination=default_moves_json)

    def get_win_combination(self):
        return json.loads(self.win_combination)
    
class OpponentMoves(models.Model):
    count = models.IntegerField(default=0)
    moves_list = models.JSONField(default=list)


    