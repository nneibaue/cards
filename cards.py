import constants
from random import randint

class UnassignedCardError(Exception):
    pass

class Card:
    '''Class representing a single playing card'''
    def __init__(self, value, suit, deck=None):
        '''Creates a card instance. Cards typically belong to a deck, but may be created outside of a deck.
        
        Args:
            value: str. Value of the card. Valid values are stored in constants.VALUES, and are:
                ['1', '2', '3', '4', '5', '6', '7', '8', '9' '10', 'J', 'Q', 'K', 'A']
            suit: str. Suit of the card. Valid suits are stored in constants.SUITS, and are:
                ['C', 'S', 'H', 'D']
            deck: Deck or None. Deck that the card belongs to'''
        
        if value not in constants.VALUES:
            raise ValueError(f'"{value}" not a valid Card value! Valid Card values: {constants.VALUES}')

        if suit not in constants.SUITS:
            raise ValueError(f'"{suit}" not a valid suit! Valid suits: {constants.SUITS}')

        if value in constants.REDS:
            self.color = 'red'
        else:
            self.color = 'black'

        self.value = value
        self.suit = suit
        
        self._deck = deck

    @property
    def deck(self):
        return self._deck

    @deck.setter
    def deck(self, _):
        raise UnassignedCardError('Cannot assign a Deck! Decks are only assigned when Cards are created by a Deck instance')
    
            
    def __int__(self):
        '''Returns the numeric card value'''
        if self.value == 'A':
            if constants.ACE_HIGH:
                return 14
            else:
                return 1
        else:
            return 2 + constants.VALUES.index(self.value)
            

    def __add__(self, other):
        '''Adds two cards or a card to an integer'''
        return int(self) + int(other)

    def __str__(self):
        '''Returns the conventional name of the card, e.g. "jack of diamonds".'''
        if self.value not in constants.NAMES:
            name = self.value
        else:
            name = constants.NAMES[self.value]
        return f'{name} of {constants.NAMES[self.suit]}'
        
    def __repr__(self):
        return f'Card({self.value}, {self.suit})'


class Joker(Card):
    def __init__(self):
        '''Create a Joker instance. This takes no arguments'''
        pass

    def __int__(self):
        raise ValueError('Jokers do not have a numeric value!')

    def __str__(self):
        return 'Joker'

    def __repr__(self):
        return 'Joker'
        

class Deck:
    '''Class representing a standard deck of cards'''
    def __init__(self, include_jokers=False, shuffle=True):
        '''Creates a standard deck of 52 (or 54) cards.
        
        Args:
            include_jokers: bool. Whether to include exactly 2 jokers in the deck.
            shuffle: bool. Whether to perform an initial shuffle on the cards.
        '''
        self.cards = [Card(value, suit, deck=self) for suit in constants.SUITS for value in constants.VALUES]

        if include_jokers:
            self.cards += [Joker(), Joker()]


    @property
    def size(self):
        return len(self.cards)


    def _random_index(self):
        return randint(0, self.size - 1)


    def deal_card(self):
        '''Deals (returns) the top card of the deck.'''

        return self.cards.pop()


    def insert_card(self, card):
        '''Inserts a card at random into the deck.'''

        if not isinstance(card, Card):
            raise ValueError(f'{card} is not a Card!')
        self.cards.insert(self._random_index(), card)

        
    def shuffle(self):
        '''Shuffles the deck'''
        remaining = self.size
        new = []
        while remaining:
            new.append(self.cards.pop(self._random_index()))
            remaining -= 1
        self.cards = new