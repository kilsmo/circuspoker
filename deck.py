from random import shuffle

class Deck:
    def __init__(self):
        suites = ['s', 'h', 'd', 'c']
        self.cards = [(i,j) for j in range(2, 15) for i in suites]
        shuffle(self.cards)
        self.nextcard = 0

    def dealcard(self):
        card = self.cards[self.nextcard]
        self.nextcard += 1
        return card

if __name__ == '__main__':
    deck = Deck()
    print(len(deck.cards))
