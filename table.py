from cards import Deck
from cards import Hand
from players import Player
from players import Dealer
import re

class Table:
    def __init__(self):
        self.player_list = []
        self.dealer = Dealer("Dealy McDealerface")
        self._Table__create_players()
        self.discard_pile = []

    def __create_players(self):
        self.all_people = []
        print("This game will allow for a maximum of 3 players.")
        player_count = 0
        while player_count < 3:
            player_name = ''
            more_players = True
            while not player_name:
                player_name = input(f"Please input a player name: > ")
            player_count += 1
            self.player_list.append(Player(player_name))
            if player_count < 3:
                another_player = ''
                while another_player.strip().lower() not in ['y','n']:
                    another_player = input(f'Would you like register another player? Please enter y or n > ')
                if another_player.strip().lower() == 'n':
                    break
        for player in self.player_list:
            self.all_people.append(player)
        self.all_people.append(self.dealer) # dealer appended last because they go last in play order

    def get_bet(self, player):
        is_valid_bet = False
        player.current_bet = str('')
        if player.chips < 10:
            print(f"Looks like you've had a rough night, {player.person_name}! You don't have enough chips to play.")
            player.is_still_playing = False
        else:
            print(f"How much would you like to bet, {player.person_name}?")   
            while not is_valid_bet:
                player.current_bet = input(f"Minimum bet is 10, maximum bet is {player.chips}, or enter 'x' to leave the table. > ")
                while not re.match("[0-9xX]", player.current_bet):
                    player.current_bet = input(f"Invalid bet, {player.person_name}! Minimum bet is 10, maximum bet is {player.chips}, or enter 'x' to leave the table. > ")            
                if player.current_bet.strip().lower() == 'x':
                    player.is_still_playing = False
                    print(f"Thanks for playing, {player.person_name}!")
                    #### Do more stuff to dump the player and their cards from the game here
                    player.hand.discard_hand(self)
                    table.all_people.remove(player)
                    break
                elif int(player.current_bet) >= 10 and int(player.current_bet) <= player.chips:
                    is_valid_bet = True
                    player.current_bet = int(player.current_bet)
                else:
                    print(f"Invalid bet, {player.person_name}!")

    def play_hand(self, player):
        while player.is_still_choosing:
            if player.person_type == 'dealer':
                player._hit_or_stand()
            else:
                player._hit_or_stand(player)
            if player.is_still_choosing:
                incoming_card = table.dealer._deck.deal()
                print(f"{player.person_name} is dealt {incoming_card.__dict__()}")
                player.hand.add_card(incoming_card)
                player.hand.show_hand()
            else:
                player.is_still_choosing = True # resetting for next round
                break
            if player.hand.calc_score() > 21:
                print(player.hand.calc_score())
                print(f"{player.person_name} has more than 21 and they've busted!")
                player.is_bust = True
                if player.person_type == 'player':
                    player.losses += 1
                break

    def show_all_hands(self):
        for person in self.all_people:
            print(f"Cards in {person.person_name}'s hand:")
            person.hand.show_hand()

# init with player creation
table = Table()

# display player info
print(f"There are {len(table.player_list)} players at the table.")
for player in table.player_list:
    player._introduce_self()
    print()
table.dealer._introduce_self()

# loop while there are still players in the game
players_playing = 1
while players_playing > 0:

    # deal starting hands
    table.dealer.deal_starting_hands(table.player_list)

    # get post-deal bets
    print(f"There are {len(table.player_list)} players")
    for player in table.player_list:
        if player.is_still_playing:
            table.get_bet(player)

    # show starting hands
    for person in table.all_people:
        print(f"Cards in {person.person_name}'s hand:")
        person.hand.show_hand()

    # play each player hand still in game
    for player in table.player_list:
        if player.is_still_playing:
            table.play_hand(player)

    # play dealer hand
    table.play_hand(table.dealer)
    
    # compare scores and generate W/T/L against dealer, pay out chips, discard all hands to discard pile
    if table.dealer.is_bust:
        print("The dealer is bust! All remaining players win!")
        for player in table.player_list:
            if not player.is_bust:
                player.wins += 1
                player.chips += player.current_bet
            player.hand.discard_hand(table)
    else:
        dealer_score = table.dealer.hand.calc_score()
        for player in table.player_list:
            if player.is_still_playing:
                player_score = player.hand.calc_score()
                if player_score > dealer_score:
                    player.wins += 1
                    print(f"{player.person_name}'s hand beats the dealer's! {player.person_name} wins!")
                    player.chips += player.current_bet
                elif player_score == dealer_score:
                    player.ties += 1
                    print(f"{player.person_name} ties with the dealer!")
                else:
                    player.losses += 1
                    print(f"The dealer's hadn beats {player.person_name}'s. {player.person_name} loses!")
                    player.chips -= player.current_bet
            player.hand.discard_hand(table)
        table.dealer.hand.discard_hand(table)

    # find players at table
    players_playing = 0
    for player in table.player_list:
        if player.is_still_playing:
            players_playing +=1
#TODO: finish out the section for allowing individual player to quit, finish out game sequence and then incorporate it into a loop that can run until all players are broke or have left
