import random
from IPython.display import clear_output

playing = True

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return(f'{self.rank} of {self.suit}')

class Deck:
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))    
                
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n '+ card.__str__()
        return 'The deck has: ' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        single_card = self.deck.pop()
        return single_card
        
class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces > 0:
            self.value = self.value - 10
            self.aces -= 1
              
class Chips:
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet 
        
def take_bet(chips):
    while True:
        print(f'You have {chips.total} chips')
        try:
            bet = int(input('Place your bet: '))
        except:
            print('Error occurred, please type a number')
        else:
            if bet > chips.total:
                print('You cannot bet more than you have in your pocket!')
                continue
            else:
                clear_output()
                player_chips.bet = bet
                print(f'Your bet is {bet}, good luck!')
                break
                
def hit(deck,hand):
    clear_output()
    hand.add_card(deck.deal())
    print(f'Player hit! New hand value: {player_hand.value}')
    hand.adjust_for_ace() 

def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    while playing == True:
        choice = input('Hit or Stand?')
        if choice[0].lower() == 'h':
            hit(deck,hand)
            show_some(player_hand, dealer_hand)
            if player_hand.value > 21:
                print('value is over 21')
                clear_output() #try here
                playing = False
        else:
            clear_output()
            print('Player stands')
            playing = False

def show_some(player,dealer):
    print('Dealer hand:')
    print('*Card Hidden*')
    print(f'{dealer.cards[1]}')
    print('Player Hand:', *player.cards, sep='\n ')
    
def show_all(player,dealer):
    print('Dealer Hand:', *dealer.cards, sep='\n ')
    print('Dealer Score:', dealer.value)
    print('Player Hand:', *player.cards, sep='\n ')
    print('Player Score:', player.value)
    
def player_busts(chips):
    print('Player Busts!!!')
    chips.lose_bet()

def player_wins(chips):
    print('Player Wins!!!')
    chips.win_bet()

def dealer_busts(chips):
    print('Dealer Busts!!!')
    chips.win_bet()

def dealer_wins(chips):
    print('Dealer Wins!!!')
    chips.lose_bet()

def push():
    print("It's a push!")
    
    
# Set up the Player's chips
player_chips = Chips()
while True:
    # Print an opening statement
    print('Welcome to BlackJack!')
    
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
        
    
    # Prompt the Player for their bet
    take_bet(player_chips)

    
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player_hand)
        
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_chips)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
        if player_hand.value <= 21:
            while dealer_hand.value < 17:
                hit(deck, dealer_hand)
    
        # Show all cards
        show_all(player_hand, dealer_hand)
    
        # Run different winning scenarios
        if dealer_hand.value > 21:
            print('dealer hand greater than 21')
            dealer_busts(player_chips)
        elif dealer_hand.value > player_hand.value:
            print('dealer hand greater than player hand')
            dealer_wins(player_chips)
        elif dealer_hand.value < player_hand.value:
            print('dealer hand less than than player hand')
            player_wins(player_chips)
        else:
            push()
        
    
    # Inform Player of their chips total 
    print(f"You're new chip total is: {player_chips.total}")
    
    # Ask to play again
    play_again = input('Do you want to play again? (yes / no)')
    if play_again[0].lower() == 'y' and player_chips.total == 0:
        player_chips = Chips()
        playing = True
        clear_output()
        continue
    elif play_again[0].lower() == 'y':
        playing = True
        clear_output()
        continue
    else:
        print('Thanks for playing!!')
        break
