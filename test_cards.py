import unittest
import cards
import constants

class TestCard(unittest.TestCase):
    
    def test_instantiation_no_deck(self):
        c = cards.Card('4', 'D')
        self.assertIsInstance(c, cards.Card)
        self.assertEqual(c.deck, None)


    def test_instatiation_from_deck(self):
        d = cards.Deck()
        c = d.cards[0]
        self.assertIsInstance(c.deck, cards.Deck)
        self.assertEqual(c.deck, d)


    def test_setting_deck_raises_exception(self):
        c = cards.Card('4', 'D')
        with self.assertRaises(cards.UnassignedCardError):
            c.deck = cards.Deck()


    def test_invalid_value(self):
        with self.assertRaisesRegex(ValueError,
                                     'not a valid Card value'):
            c = cards.Card('12', 'D')


    def test_invalid_suit(self):
        with self.assertRaisesRegex(ValueError,
                                    'not a valid suit'):
            c = cards.Card('8', 'Hearts')


    def test_cast_to_int(self):
        c = cards.Card('Q', 'D')
        self.assertEqual(12, int(c))

    
    def test_str(self):
        c = cards.Card('4', 'S')
        self.assertEqual(str(c), '4 of spades')


class TestJoker(unittest.TestCase):

    def setUp(self):
        self.j = cards.Joker()


    def test_instantiation(self):
        self.assertIsInstance(self.j, cards.Card)
        self.assertIsInstance(self.j, cards.Joker)


    def test_cast_to_int_raises_exception(self):
        with self.assertRaisesRegex(ValueError,
                                    'Jokers do not have a numeric value'):
            int(self.j)
                                

        
class TestDeck(unittest.TestCase):
    
    def test_instantiation_no_jokers(self):
        d = cards.Deck(include_jokers=False)
        self.assertIsInstance(d, cards.Deck)
        self.assertEqual(constants.STANDARD_DECK_SIZE_WITHOUT_JOKERS, len(d.cards))

    def test_instatiation_with_jokers(self):
        d = cards.Deck(include_jokers=True)
        self.assertIsInstance(d, cards.Deck)
        self.assertEqual(constants.STANDARD_DECK_SIZE_WITH_JOKERS, len(d.cards))


    def test_deal_card(self):
        d = cards.Deck(include_jokers=False)
        c = d.deal_card()
        
    def test_shuffle(self):
        d = cards.Deck()
        old = d.cards[:]
        d.shuffle()
        self.assertNotEqual(old, d.cards)

        
    def test_shuffle_after_dealing_10(self):
        d = cards.Deck()
        for _ in range(10):
            d.deal_card()

        d.shuffle()
        self.assertEqual(42, d.size)
            


    def test_shuffle_is_not_deterministic(self):
        decks = [cards.Deck(), cards.Deck(), cards.Deck()]
        
        # Check each deck's cards against one another
        def check_decks():
            self.assertNotEqual(decks[0].cards, decks[1].cards)
            self.assertNotEqual(decks[0].cards, decks[2].cards)
            self.assertNotEqual(decks[1].cards, decks[2].cards)

        # Shuffle each deck 3 times and check cards after each
        for _ in range(3):
            for d in decks:
                d.shuffle()
            check_decks()

            
        
        
            


if __name__ == '__main__':
    unittest.main()