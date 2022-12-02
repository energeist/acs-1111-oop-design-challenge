from cards import Deck
from cards import Hand
from players import Player
from players import Dealer

class Table:
    def __init__(self):
        self.player_list = []
        self.dealer = Dealer("Dealy McDealerface")
        self._Table__create_players()

    def __create_players(self):
        self.all_people = []
        print("This game will allow for a maximum of 3 players.")
        player_count = 0
        while player_count < 3:
            player_name = ''
            while not player_name:
                player_name = input(f"Please input a player name: > ")
            player_count += 1
            self.player_list.append(Player(player_name))
            if player_count < 3:
                another_player = ''
                while another_player.strip().lower() not in ['y','n']:
                    another_player = input(f'Would you like register another player? Please enter y or n > ')
                if another_player.strip().lower() == 'n':
                    return self.player_list
        self.all_people.append(self.dealer)
        for player in self.player_list:
            self.all_people.append(player)

    def get_bet(self, player):
        player.current_bet = 0
        if player.chips < 10:
            print("Looks like you've had a rough night. You don't have enough chips to play!")
            player.still_playing = False
        else:   
            player.current_bet = int(input(f"How much would you like to bet, {player.person_name}? Minimum bet is 10, maximum bet is {player.chips} > "))
            while player.current_bet < 10 or player.current_bet > player.chips:
                player.current_bet = int(input(f"Invalid bet, {player.person_name}! Minimum bet is 10, maximum bet is {player.chips} > "))

    def play_hand(self, player):
        while player.is_still_choosing:
            player._hit_or_stand(player)
            if player.is_still_choosing:
                player.hand.add_card(table.dealer._deck.deal())
            else:
                break

table = Table()
print(f"There are {len(table.player_list)} players")
for player in table.player_list:
    player._introduce_self()
table.dealer._introduce_self()
table.dealer.deal_starting_hands(table.player_list)

for person in table.all_people:
    print(f"Cards in {person.person_name}'s hand:")
    person.hand.show_hand()

print(f"There are {len(table.player_list)} players")
for player in table.player_list:
    if player.is_still_playing:
        table.get_bet(player)

for player in table.player_list:
    table.play_hand(player)
