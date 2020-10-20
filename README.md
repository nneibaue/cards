# Cards
<h3>Simple library for simulating a deck of cards.</h3>

<br>

## What's included?
- Deck object
- Card object
- Joker object 

<br>

## Installation

**This library uses Python 3.7+**

To clone this repo, simply copy and paste the following into your terminal window

    git clone https://github.com/nneibaue/cards

At this point, this library requires no external libraries; however, it is still recommended to work within a virtual environment. To set this up, paste the following commands into your terminal:

    python3 -venv env
    source env/bin/activate
    pip install --upgrade pip

If you do not have `virtualenv` installed, it can be installed using the system python:

    pip3 install virtualenv

<br>

## Testing

All tests are found in test_cards.py. They can be run by executing test_cards.py in the terminal.

<br>

## How to use:

### Deck
The simplest way to get started is to create a Deck instance:
    
    >>>d = Deck()
    
This creates a deck with 52 Cards. The deck will be instantiated with cards in the order of 2 - Ace; Clubs, Spades, Hearts, Diamonds. To include exactly 2 Jokers, add the following condition:

    >>>d_j = Deck(include_jokers=True)

Deck objects can be manipulated with the following methods:
>`d.shuffle()` --> Shuffles the deck in-place

>`d.deal_card()` --> Removes and returns the top card

>`d.add_card(card)` --> Adds a Card to the top of the Deck

>`d.insert_card(card)` --> Inserts a Card randomly into the Deck

>`d.clear()` --> Removes all foreign Cards from the Deck 

Note: "Foreign" Cards are cards in the Deck that belong to another Deck. This will be explained in more detail below.

<br>

### Card

Cards are typically created by Decks, but may be created on their own:

    >>>import cards

    >>>four_of_hearts = cards.Card('4', 'H', deck=None)
    >>>king_of_spades = cards.Card('K', 'S', deck=None)

The `deck=None` argument specifies a Deck instance to assign a Card to. This argument is used by a Deck when creating cards and **should not be used** if creating standalone cards. 

>If this argument _is_ passed, a Deck most likely already has a copy of this type of Card and a `DuplicateCard` error will be raised. 

<br>

Cards have the following accessible properties:

>`c.id` --> Returns the Card's string id (e.g. '3S')

>`c.deck` --> Returns the Card's assigned Deck

<br>

Cards can be added together to get a final value:

    >>>four_of_hearts + king_of_spades
    >>>17

<br>

Cards can also be added to an integer:

    >>>four_of_hearts + 50
    >>>54

<br>

### Joker

A Joker is a stripped down version of a Card. It has an id of 'Joker', and cannot be added to other Cards, Jokers, or integers:

    >>>joker = cards.Joker()
    >>>isinstance(Joker, cards.Card)
    >>>True

<br>

### Using Multiple Decks

Decks, at any point, may contain _any_ number of cards from _any_ Deck. This will happen by calling `add_card` or `insert_card` with a Card from another Deck:

    >>>black_deck = cards.Deck()
    >>>black_deck.shuffle()

    >>>red_deck = cards.Deck()
    >>>red_deck.shuffle()

    >>>black_deck.add_card(red_deck.deal_card())

    >>>black_deck.size
    >>>53

    # The black deck's top card is still assigned to the red deck
    >>>black_deck.top_card.deck == red_deck
    >>>True

<br>

## Other Notes


- Aces can be set globally as high or low by modifying the `ACE_HIGH` bool in constants.py

- Convenient human-readable names are stored in the `NAMES` dict in constants.py

- Card images (as well as some deck backs) can be found in the images/ directory. These are not currently used, but may be helpful if creating playing-card based GUIs using this library. Future updates of this library will add modular PyQt5 elements for easy game creation.


