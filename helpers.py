import random
def honoursFn(bid, honoursMinCall, maxPoints):
    bidMapping = {}

    bidMapping[f"honours"] = honoursMinCall
    for i, point in enumerate(range(honoursMinCall + 3, maxPoints, 3), start=1):
        bidMapping[f"honours {i}"] = point

    value = bidMapping.get(bid)
    if value is not None:
        key = next(key for key, value in bidMapping.items() if value == bidMapping[bid])
        return bidMapping[bid], key
    else:
        return None, None

def soloContractorFn(bid):
    return 56

def makeCardTemplate(currentDeck, ranks, suits):
    bool8 = True
    for rank in ranks:
        for i in range(4):
            currentDeck.append(rank + ' ' + suits[i])

        if (rank == "8" and bool8):
            bool8 = False
            continue

        for i in range(4):
            currentDeck.append(rank + ' ' + suits[i])

    currentDeck.append('8' + ' ' + suits[1])
    currentDeck.append('8' + ' ' + suits[3])

def distributeCards(currentDeck, NoOfCardsAtATime, noOfPlayers, players):
    for _ in range(3):
        random.shuffle(currentDeck)

    for i in range(0, len(currentDeck), NoOfCardsAtATime):
        cardDealTurn = (i // NoOfCardsAtATime) % (noOfPlayers) # Integer floor division
        players[cardDealTurn]["cards"].extend(currentDeck[i:i+3])
    return

def sortingTheCards(player, suits, ranks, rankOrder):
    suitOrder = {suits[0]: 0, suits[2]: 1, suits[1]: 2, suits[3]: 3}

    playerCards = []
    for card in player["cards"]:
        playerCards.append(sortSuitandRank(card, suits=suits, ranks=ranks, rankNeeded=True))

    # cards[1] is the suit part of a card. I should have made this a dictionary...
    # - used for reversing just that one's order
    playerCards.sort(key=lambda card: (suitOrder[card[0]], -rankOrder[card[1]]))

    player["cards"] = [card[1] + ' ' + card[0] for card in playerCards]

def displayCards(player):

    noOfCards = len(player["cards"])
    def draw(corner, middle, seperation):
        template = corner
        # Stopping just one step before so I can add a corner afterwards outside the for loop for the final card.
        if noOfCards > 1:
            for i in range(noOfCards - 1):
                template += middle[i]
                template += seperation
            template += middle[i + 1]
            template += corner
        else:
            template += middle[0]
            template += corner

        print(template)

    maxLength = len("Diamonde") + 5

    draw('+', ['-' * maxLength for _ in range(noOfCards)], '.')
    # Convert the first letter to caps, combine all into a list called cards
    cards = []
    for card in player["cards"]:
        cardSplit = card.split(' ')
        cardSplit[0] = cardSplit[0][0].upper() + cardSplit[0][1:]
        cardSplit[1] = cardSplit[1][0].upper() + cardSplit[1][1:]
        card = cardSplit[0] + ' ' + cardSplit[1]
        cards.append(card.center(maxLength))
    draw('|', cards, '|')
    draw('+', ['-' * maxLength for _ in range(noOfCards)], '.')
    return

def playerToTeam(playerIndex):
    if (playerIndex % 2 == 0):
        return 0
    else:
        return 1

def sortSuitandRank(card, *, suits, ranks, rankNeeded):
    while True:
        try:
            rank, suit = card.split(" ")
            break
        except (ValueError):
            return None

    # Swap suit and rank if its mixed up
    if (rank in suits):
        temp = rank
        rank = suit
        suit = temp
    # Check if the card has a valid suit and rank
    if (suit not in suits or rank not in ranks):
        return None
    
    if rankNeeded == True:
        return suit, rank
    else:
        return suit
    
def checkForSuitAndRank(player, cardOrSuitToCompareTo, *, suits, ranks, rankNeeded):
    if rankNeeded:
        cardToCompareTo = cardOrSuitToCompareTo
        # Ensures the given card is valid not something like G Obsidian, and makes the order predictable
        suit, rank = sortSuitandRank(cardToCompareTo, suits=suits, ranks=ranks, rankNeeded=rankNeeded) # rankNeeded = True always
        cardToCompareTo = rank + ' ' + suit
        if cardToCompareTo in player["cards"]:
            return True
        else:
            return False
    else:
        suitToCompareTo = cardOrSuitToCompareTo
        suitsOfPlayer = []
        for card in player["cards"]:
            suitOfPlayer = sortSuitandRank(card, suits=suits, ranks=ranks, rankNeeded=rankNeeded) # rankNeeded = False always
            # The main deck always have a valid suit rank, but this is just for safety and being explicit in code.
            if suitOfPlayer:
                suitsOfPlayer.append(suitOfPlayer)
        if suitToCompareTo in suitsOfPlayer:
            return True
        else:
            return False
