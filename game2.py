import math
import collections
import itertools

rankOrder = "34567890JQKA2"
suitOrder = "DCHS"
fives = ["straight", "flush", "fullHouse", "four", "straightFlush"]
compLimit = 5

class Card:
  def __init__(self, card):
    if type(card) is str:
      self.rank = rankOrder.find(card[0]);
      self.suit = suitOrder.find(card[1]);
    else:
      self.rank = card.rank
      self.suit = card.suit

  def toTuple(self):
    return (self.rank, self.suit)

  def __eq__(self, other):
    return self.rank == other.rank and self.suit == other.suit

  def __lt__(self, other):
    return self.toTuple() < other.toTuple()

  def __gt__(self, other):
    return not self == other and not self < other

  def __str__(self):
    return rankOrder[self.rank] + suitOrder[self.suit]

  __repr__ = __str__

class Meld(list):
  def __init__(self, cards):
    self += sorted(toCards(cards))
    self.size = len(self)
    self.rank = None
    self.suit = None
    self.level = None
    self.isValid = self.size > 0
    if self.isValid:
      result = quickMeld(self)
      self.isValid = result["isValid"]
      self.rank = result["rank"]
      self.suit = result["suit"]
      self.level = result["level"]

  def straight(self):
    first = self[0]
    i = 0
    for card in self:
      if card.rank != first.rank + i:
        return False
      i += 1
    return (self[-1].rank, self[-1].suit)

  def flush(self):
    suits = [card.suit for card in self]
    if suits[1:] == suits[:-1]:
      return (self[-1].rank, self[-1].suit)
    return False

  def fullHouse(self):
    counts = countRanks(self)
    if counts[0][1] == 3 and counts[1][1] == 2:
      return (counts[0][0], None)
    return False

  def four(self):
    counts = countRanks(self)
    if counts[0][1] == 4 and counts[1][1] == 1:
      return (counts[0][0], None)
    return False

  def straightFlush(self):
    if Meld.straight(self) != False and Meld.flush(self) != False:
      return Meld.straight(self)
    return False

  def isLegal(self, trick):
    return self.size == trick.size and self > trick

  def breaking(self, melds):
    breaks = []
    for meld in melds:
      if self == meld: continue
      if self.size >= meld.size: continue
      for card in self:
        if card in meld:
          breaks.append(len(meld))
          break
    return breaks

  def winChance(self, hand, trick, roundHistory):
    cards = remainingCards(hand, trick, roundHistory)
    print(len(findMelds(cards)))

  def strings(self):
    return toStrings(self)

  def toTuple(self):
    return (self.rank, self.suit)

  def __eq__(self, other):
    return self.size == other.size and self.level == other.level and self.suit == other.suit and self.rank == other.rank

  def __lt__(self, other):
    if self.size < other.size: return True
    if self.size > other.size: return False
    if self.size <= 3:
      return self.toTuple() < other.toTuple()
    else:
      if self.level < other.level: return True
      if self.level > other.level: return False
      if fives[self.level] == "straight" or fives[self.level] == "straightFlush":
        return self.toTuple() < other.toTuple()
      elif fives[self.level] == "flush":
        return self.toTuple()[::-1] < other.toTuple()[::-1]
      elif fives[self.level] == "fullHouse" or fives[self.level] == "four":
        return self.rank < other.rank

  def __gt__(self, other):
    return not self == other and not self < other

def quickMeld(cards):
  self = {"isValid": True, "rank": None, "suit": None, "level": None}
  fives = [Meld.straightFlush, Meld.four, Meld.fullHouse, Meld.flush, Meld.straight]
  if len(cards) <= 3:
    ranks = [card.rank for card in cards]
    self["isValid"] = ranks[1:] == ranks[:-1]
    if self["isValid"]:
      self["rank"] = cards[0].rank
      self["suit"] = sorted([card.suit for card in cards])[-1]
  else:
    level = len(fives) - 1
    for five in fives:
      result = five(cards)
      if result != False:
        self["rank"], self["suit"] = result
        self["level"] = level
        break
      level -= 1
    if self["rank"] == None and self["suit"] == None:
      self["isValid"] = False
      level = None
  return self

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
  for i in [1, 2, 3, 5]:
    combinations = itertools.combinations(cards, i)
    j = 0
    for combination in combinations:
      quick = quickMeld(list(combination))
      # meld = Meld(list(combination))
      # if meld.isValid and meld.size <= compLimit: melds.append(meld)
      if j % 5000 == 0: print(str(math.ceil((j / 575757) * 100)) + "%")
      j += 1
  return melds

def filterLegal(melds, trick):
  return list(filter(lambda meld: meld.isLegal(trick), melds))

def countRanks(cards):
  return collections.Counter([card.rank for card in cards]).most_common()

def remainingCards(hand, trick, roundHistory):
  cards = allCards()
  history = flattenHistory(roundHistory)
  def removeCards(lists):
    for list in lists:
      for card in list:
        if card in cards: cards.remove(card)
  removeCards([hand, trick, history])
  return cards

def allCards():
  cards = []
  for rank in rankOrder:
    for suit in suitOrder:
      cards.append(Card(rank + suit))
  return cards

def flattenHistory(roundHistory):
  cards = []
  for trickHistory in roundHistory:
    for trick in trickHistory:
      cards += toCards(trick[1])
  return sorted(cards)
