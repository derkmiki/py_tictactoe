'''
Created on 15 Jul 2017

@author: edward allan florindo
'''
import random 
from IPython.display import clear_output
import os


class Game(object):

    deck = (list(range(2, 11)) + ['A', 'J', 'Q', 'K']) * 4
    moves = ('hit', 'stand')
    bust = -1
    
    def __init(self):
        pass

    def reset_status(self):
        self.is_busted = False;
        self.is_blackjack = False;

    def ask_to_rematch(self):
        while True:
            yn = input('Continue playing? y/n: ').lower() 
            if yn in 'yn':
                if yn == 'y':
                    return True
                elif yn == 'n':
                    return False

    def reset_deck(self):
        Game.deck = (list(range(2, 11)) + ['A', 'J', 'Q', 'K']) * 4
    
    def distribute(self):
        random.shuffle(Game.deck)
        self.cards = [Game.deck.pop(), Game.deck.pop()];
    
    def hit(self):
        self.cards.append(Game.deck.pop())
    
    def get_card_sum(self):
        adds = [10 if x in ['J', 'Q', 'K'] else x  for x in self.cards]
        aces = adds.count('A')
        adds = [0 if x == 'A' else x for x in adds]        
        total = sum(adds)
        total_set = (self.bust_or_num(total), self.bust_or_num(total)) 
        if aces == 1:
            total_set = (total + 1, total + 11) 
        elif aces == 2:
            total_set = (self.bust_or_num(total + 2), self.bust_or_num(total + 12))        
        elif aces >= 3:
            total_set = (self.bust_or_num(total + aces), self.bust_or_num(total + aces)) 
        return total_set 
                    
    def bust_or_num(self, number):
        if number > 21:
            return Game.bust
        else:
            return number

    def check_busted(self):
        card_sum = self.get_card_sum()
        if min(card_sum) == Game.bust:
            self.is_busted = True
        else:
            self.is_busted = False
        return self.is_busted    
            
    def check_blackjack(self):
        result = False
        if len(self.cards) == 2 and self.cards.count('A') == 1 and len([x for x in self.cards if x in ('J', 'K', 'Q', 10) ]) == 1:
            result = True
        self.is_blackjack = result
        return self.is_blackjack

    def reveal_cards(self):
        if(len(self.cards)):            
            info = '';
            if self.is_busted == True:
                info = 'Busted!' 
            elif self.is_blackjack == True:
                info = 'Blackjack!'
            else:
                cards = self.get_card_sum()
                if min(cards) == max(cards):
                    info = min(cards)
                else:
                    info = '%s/%s' % cards
            
            print('%s cards are: %s --> %s' % (self.name, self.cards, info))
        else:
            print('%s has no card yet' % self.name)

    def payout(self, dealer, players):        
        dealer_sum = dealer.get_card_sum();
        for player in players:
            player_sum = player.get_card_sum();
            if player.is_busted == True:
                player.last_payout = player.bet * -1
            elif player.is_blackjack == True and dealer.is_blackjack == False:
                player.last_payout = player.bet * 1.5
            elif dealer.is_busted == True and player.is_busted == False:
                player.last_payout = player.bet * 1
            elif dealer.is_blackjack == True and player.is_blackjack == False:
                player.last_payout = player.bet * -1
            elif max(dealer_sum) > max(player_sum):                
                player.last_payout = player.bet * -1
            elif max(player_sum) > max(dealer_sum):
                player.last_payout = player.bet * 1
            else:
                player.last_payout = 0                
            player.money = player.money + player.last_payout

class Player(Game):
    
    def __init__(self, name):
        self.cards = []
        self.name = name
        self.money = 0
        self.is_busted = False
        self.is_blackjack = False;
        self.type = 'Player'
        self.last_payout = 0
    
    def set_name(self):
        while True:
            name = input('Please enter your name: ') 
            if name != '':
                self.name = name
                break
           
    def set_money(self):
        while True:
            try:
                money = int(input('Please enter your initial money( 100 to 10000): '))  
                if money in range(100, 10001):
                    self.money = money
                else:
                    continue                    
            except:
                continue
            else:
                break

    def next_move(self):
        if self.check_blackjack():
            return 
        while True:            
            move = input('%s what is your move? choose %s : ' % (self.name, Game.moves))
            if (move in Game.moves):
                getattr(self, move)()
                if self.check_busted():
                    break
                if self.check_blackjack():
                    break
                if(move != 'hit'):
                    break
                self.reveal_cards()

    def show_money(self):
        if self.money <= 0:
            print("%s is broke and can't continue." % self.name)
        else:
            print('%s cash at hand is %s' % (self.name, self.money))
        return self.money

    def set_bet(self):
        max_bet = 200
        if self.money < max_bet:  
            max_bet = self.money
        while True:
            try:
                bet = int(input('Please enter your bet (1 to %s): ' % max_bet))
                if bet in range(1, 201):
                    self.bet = bet
                else:
                    continue
            except:
                continue
            else:
                break
                
    def show_bet(self):
        print('%s bet is %s' % (self.name, self.bet))
    
    def stand(self):
        pass
    
    def show_payout(self):
        if self.last_payout > 0:
            print('%s won by %s :-)' % (self.name, self.last_payout))
        elif self.last_payout < 0:
            print('%s lost by %s :-(' % (self.name, abs(self.last_payout)))            
        else:
            print('%s draw in the last game :-|' % self.name)            
                
class Dealer(Game):
    def __init__(self):
        self.cards = []
        self.is_busted = False
        self.is_blackjack = False
        self.name = 'Dealer'
        self.type = 'Dealer'
        
    def show_cards(self):
        try:
            print('%s shown card is: %s' % (self.name, self.cards[0]))
        except:
            print('%s has no card yet' % self.name)    
    
    
    def next_move(self):
        card_sum = self.get_card_sum()
        while max(card_sum) < 17:            
            self.hit()
            card_sum = self.get_card_sum()        
            if self.check_busted():
                break
            if self.check_blackjack():
                break

#the game flow
clear_output()
os.system('cls||clear')
print('Welcome to BLACKJACK Simple(No split, no insurance, no double)')
print('A text-based game')
print('-----------------')
game = Game()
player = Player('Player')
player.set_name()  
dealer = Dealer()
player.set_money()
while True:
    game.reset_deck()
    player.reset_status()
    if player.show_money() <= 0:
        break
    player.set_bet()
    player.show_bet()
    player.distribute()
    dealer.distribute()    
    player.reveal_cards()
    dealer.show_cards()
    player.next_move()
    dealer.next_move()    
    player.reveal_cards()
    dealer.reveal_cards()
    game.payout(dealer, [player])
    player.show_payout()
    if  player.ask_to_rematch() == False:
        break
print('Thank you for playing the game!')