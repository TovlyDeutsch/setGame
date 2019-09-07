from enum import Enum, auto, unique
from itertools import product, combinations
import random
import time

SET_SIZE = 3
FIELD_SIZE = 12


@unique
class Color(Enum):
    RED = auto()
    GREEN = auto()
    PURPLE = auto()


@unique
class Number(Enum):
    ONE = auto()
    TWO = auto()
    THREE = auto()


@unique
class Shape(Enum):
    PILL = auto()
    SQUIGGLE = auto()
    DIAMOND = auto()


@unique
class Fill(Enum):
    SOLID = auto()
    HASH = auto()
    HOLLOW = auto()


props = [Color, Number, Shape, Fill]

validCombos = set()


class Card:
    def __init__(self, color, number, shape, fill):
        self.Color = color
        self.Number = number
        self.Shape = shape
        self.Fill = fill

    def __key(self):
        return (self.Color, self.Number, self.Shape, self.Fill)

    def __hash__(self):
        return hash(self.__key())


def generateDeck():
    propCombos = list(product(*[list(prop) for prop in props]))
    return [Card(*combo) for combo in propCombos]


def generateField(deck, size):
    return random.sample(deck, k=size)


def isSet(combo):
    if len(combo) != 3:
        return False
    propsSeen = {Color: set(), Number: set(), Shape: set(), Fill: set()}
    for card in combo:
        for prop in props:
            propsSeen[prop].add(getattr(card, prop.__name__))
    for prop, seenSet in propsSeen.items():
        if len(seenSet) != 1 and len(seenSet) != len(prop):
            return False
    return True


def isSetLookup(combo):
    return combo in validCombos


def findSet(field):
    combos = combinations(field, SET_SIZE)
    return next(filter(isSetLookup, combos), None)


def memoizeCombos():
    global validCombos
    deck = generateDeck()
    allCombos = combinations(deck, 3)
    validCombos = set(filter(isSet, allCombos))


def main():
    memoizeCombos()
    deck = generateDeck()
    field = generateField(deck, FIELD_SIZE)
    start = time.time()
    for _i in range(1000):
        firstSet = findSet(field)
    end = time.time()
    print(f'time is {end - start:.10f}')
    for card in firstSet:
        print(card.__dict__)


if __name__ == "__main__":
    main()
