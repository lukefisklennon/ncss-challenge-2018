import itertools

rankOrder = "34567890JQKA2"
suitOrder = "DCHS"

class Card:
  def __init__(self, card):
    if type(card) is str:
      self.rank = rankOrder.find(card[0]);
      self.suit = suitOrder.find(card[1]);
    else:
      self.rank = card.rank
      self.suit = card.suit
  def __eq__(self, other):
    return self.rank == other.rank and self.suit == other.suit
  def __lt__(self, other):
    return self.rank < other.rank or (self.rank == other.rank and self.suit < other.suit)
  def __gt__(self, other):
    return self.rank > other.rank or (self.rank == other.rank and self.suit > other.suit)
  def __str__(self):
    return rankOrder[self.rank] + suitOrder[self.suit]
  __repr__ = __str__

class Meld(list):
  def __init__(self, cards):
    cards = toCards(cards)
    self += cards
    self.size = len(self)
    self.isValid = self.size > 0
    if self.isValid:
      ranks = [card.rank for card in self]
      self.isValid = ranks[1:] == ranks[:-1]
      if self.isValid:
        self.rank = self[0].rank
        self.suit = sorted([card.suit for card in self])[-1]
  def isLegal(self, trick):
    return self.size == trick.size and self > trick
  def strings(self):
    return toStrings(self)
  def __lt__(self, other):
    return self.size < other.size or (self.size == other.size and (self.rank < other.rank or (self.rank == other.rank and self.suit < other.suit)))
  def __gt__(self, other):
    return self.size > other.size or (self.size == other.size and (self.rank > other.rank or (self.rank == other.rank and self.suit > other.suit)))

def toCards(cards):
  return [Card(card) for card in cards]

def toMelds(melds):
  return [Meld(meld) for meld in melds]

def toStrings(cards):
  return [str(card) for card in cards]

def filterMelds(function, melds):
  melds = list(filter(function, melds))
  return melds

def findMelds(cards):
  melds = []
  for i in range(1, 4):
    melds += filterValid(toMelds(combinations(cards, i)))
  return melds

def filterValid(melds):
  return list(filter(lambda meld: meld.isValid, melds))

def filterLegal(melds, trick):
  return list(filter(lambda meld: meld.isLegal(trick), melds))

def combinations(cards, n):
  return [list(combination) for combination in list(itertools.combinations(cards, n))]
