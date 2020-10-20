import random
import time
import constants


class UnassignedCardError(Exception):
    '''Raised when trying to assign a Card's Deck post-instantiation.'''
    pass


class DuplicateCardError(Exception):
    '''Raised when trying to assign a Card's Deck to a Deck that alread has one of this card.'''
    pass


class Card:
    '''Class representing a single playing card'''

    # Ledger of all cards in memory. This ensures that no duplicate cards are added
    # to any Decks
    _cards_in_existance = []

    def __init__(self, value, suit, deck=None):
        '''Creates a card instance.

        Cards can be created inside or outside of a Deck instance. A card's Deck is
        reflected by the `deck` property, and can only be set upon instantiation.
        
        Args:
            value: str. Value of the card. Valid values are stored in constants.VALUES,
                and are: ['1', '2', '3', '4', '5', '6', '7', '8', '9''10', 'J', 'Q', 'K', 'A']
            suit: str. Suit of the card. Valid suits are stored in constants.SUITS,
                and are: ['C', 'S', 'H', 'D']
            deck: Deck or None. Deck that the card belongs to'''

        if value not in constants.VALUES:
            raise ValueError(f'"{value}" not a valid Card value!'
                             f'Valid Card values: {constants.VALUES}')

        if suit not in constants.SUITS:
            raise ValueError(f'"{suit}" not a valid suit!'
                             f'Valid suits: {constants.SUITS}')

        if value in constants.REDS:
            self.color = 'red'
        else:
            self.color = 'black'

        self.value = value
        self.suit = suit

        # Check all cards to avoid duplicating cards in a Deck
        if deck is not None:
            for card in Card._cards_in_existance:
                if self.id == card.id and deck == card.deck:
                        raise DuplicateCardError(f'An instance of {self.id} has already'
                                                 f'been assigned to this Deck!')

        self._deck = deck
        Card._cards_in_existance.append(self)

    @property
    def id(self):
        '''Returns this Card's id, e.g. '4H' (four of hearts).'''
        return f'{self.value}{self.suit}'

    @property
    def deck(self):
        '''Returns this Card's Deck instance, if any.'''
        return self._deck

    @deck.setter
    def deck(self, _):
        raise UnassignedCardError('Cannot assign a Deck! Decks are only assigned during'
                                  'instantiation')
    
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

    def id(self):
        return 'Joker'

    def __int__(self):
        raise ValueError('Jokers do not have a numeric value!')

    def __str__(self):
        return 'Joker'

    def __repr__(self):
        return 'Joker'
        

class Deck:
    '''Class representing a standard deck of cards.
    
    A Deck is responsible for creating 52 standard Cards (54 if a Joker is included).
    Decks may, at any point, hold cards that belong to a different deck (e.g. during the
    classic card game "War".
    
    The user is responsible for all cards dealt from the deck. If a card is dealt, but 
    not captured, then the card is lost and the Deck must be re-instantiated to
    "recover" the lost card.'''
    
    def __init__(self, include_jokers=False, shuffle=True):
        '''Creates a standard deck of 52 (or 54) cards.
        
        Args:
            include_jokers: bool. Whether to include exactly 2 jokers in the deck.
            shuffle: bool. Whether to perform an initial shuffle on the cards.
        '''
        self.cards = [Card(value, suit, deck=self)
                      for suit in constants.SUITS for value in constants.VALUES]

        if include_jokers:
            self.cards += [Joker(), Joker()]

    @property
    def size(self):
        '''Returns the current size of the Deck, including any foreign cards.'''
        return len(self.cards)

    @property
    def top_card(self):
        '''Look at the top card without dealing it.'''
        return self.cards[-1]

    def _random_index(self):
        random.seed(time.time())
        return random.randint(0, self.size - 1)

    def deal_card(self):
        '''Deals (returns) the top card of the deck.'''
        if not self.cards:
            print('Deck is empty!')
            return
        return self.cards.pop()

    def clear(self):
        '''Removes and returns all cards that do not belong to this deck.'''
        cards_removed = []
        for i, card in enumerate(self.cards):
            if card.deck != self:
                cards_removed.append(self.cards.pop(i))
        return cards_removed

    def add_card(self, card):
        '''Adds a card to the top of the deck.'''
        if not isinstance(card, Card):
            raise ValueError(f'{card} is not a Card!')
        self.cards.append(card)

    def insert_card(self, card):
        '''Inserts a card at random into the deck.'''

        if not isinstance(card, Card):
            raise ValueError(f'{card} is not a Card!')
        self.cards.insert(self._random_index(), card)
        
    def shuffle(self):
        '''Shuffles the deck'''
        random.seed(time.time())
        remaining = self.size
        new = []
        while remaining:
            new.append(self.cards.pop(self._random_index()))
            remaining -= 1
        self.cards = new

    def __repr__(self):
        return f'Deck(size={self.size})'