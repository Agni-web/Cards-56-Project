import random, re
deck = {"8": 0, "9": 2, "10": 1, "A": 1, "J": 3, "Q": 0, "K": 0}
ranks = ["8", "9", "10", "A", "J", "Q", "K"]
ranks = [rank.lower() for rank in ranks]
NoOfCardsAtATime = 3
maxPoints = 56
 # 11/56 is ratio to loose, you can pick any.., or even a different way to calculate all this.
honoursMinCall = maxPoints - round((12 / 56) * maxPoints - 1)
currentBidStarter = 2

suits = ["Spade", "Clubs", "Heart", "Diamonde"]
suits = [suit.lower() for suit in suits]
players = [
    {"name": "Alice", "cards": []},
    {"name": "Bob", "cards": []},
    {"name": "Charlie", "cards": []},
    {"name": "David", "cards": []},
    {"name": "Advait", "cards": []},
    {"name": "Akash", "cards": []}
]

noOfPlayers = len(players)

currentDeck = []

def honoursFn(bid):
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

def makeCardTemplate(currentDeck):
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

def distributeCards(currentDeck):
    for _ in range(3):
        random.shuffle(currentDeck)

    for i in range(0, len(currentDeck), NoOfCardsAtATime):
        cardDealTurn = (i // NoOfCardsAtATime) % (noOfPlayers) # Integer floor division
        players[cardDealTurn]["cards"].extend(currentDeck[i:i+3])
    return

def displayCards(player):

    noOfCards = len(player["cards"])
    def draw(corner, middle, seperation):
        parameters = [corner]
        for i in range(noOfCards - 1):
            parameters.append(middle[i])
            parameters.append(seperation)
        parameters.append(middle[i + 1])
        parameters.append(corner)
        lengthOfParameters = len(parameters)
        template = '{}' * lengthOfParameters
        print(template.format(*parameters))

    maxLength = len("Diamonde") + 5

    draw('+', ['-' * maxLength for i in range(noOfCards)], '.')
    # Convert the first letter to caps, combine all into a list called cards
    cards = []
    for card in player["cards"]:
        cardSplit = card.split(' ')
        cardSplit[0] = cardSplit[0][0].upper() + cardSplit[0][1:]
        cardSplit[1] = cardSplit[1][0].upper() + cardSplit[1][1:]
        card = cardSplit[0] + ' ' + cardSplit[1]
        cards.append(card.center(maxLength))
    draw('|', cards, '|')
    draw('+', ['-' * maxLength for i in range(noOfCards)], '.')

    return

def bidding(players):
    # Sending things as a list so the original value changes..
    def playerCountAndConditionalValidityFn(playersTeamBidded, index1, validityBool, index2):
        if (playersTeamBidded[index1] < maxPlayersPerTeam):
            playersTeamBidded[index1] += 1
        else:
            validityBool[index2] = False

    def notPassing(bid):
        nonlocal bidPlayer, highestBidPlayer, highestBid, highestBidTeam, teamToBid, teamToBidStarter

        # if (honours):
        #     pass
        # elif (soloContractor):
        #     pass
        # else:
        try:
            bid = int(bid)
        except ValueError:
            print("Input shouldn't contain characters")
            return

        if (bid > highestBid and bid < maxPoints + 1):
            highestBidPlayer = bidPlayer
            highestBid = bid
            highestBidTeam = teamToBid
            otherTeamToBid = 1 - teamToBid
            if (ifValidity[otherTeamToBid]):
                if teamToBidStarter == teamToBid:
                    bidPlayer = currentBidStarter + playersTeamBidded[otherTeamToBid] * 2 + 1
                else:
                    bidPlayer = currentBidStarter + playersTeamBidded[otherTeamToBid] * 2

                playerCountAndConditionalValidityFn(playersTeamBidded, teamToBid, ifValidity, teamToBid)
            else:
                whileValidity[0] = False

            if teamToBid == 0:
                teamToBid = 1
            else:
                teamToBid = 0

            if (bid + 1 > maxPoints):
                whileValidity[0] = False
                return True
            
            if (not any(ifValidity)):
                whileValidity[0] = False
            return True
        else:
            print("Invalid bid")
            return False

    def handleBids(bid):
        nonlocal bidText
        returnValue = None

        if (re.fullmatch(r"honours( \d+)?", bid)):
            bid, key = honoursFn(bid)
            if bid is None:
                print("Invalid honours call")
                returnValue = False
            else:
                bidText = "Honours have been called, call higher? (Honours 1, honours 2, etc.) (Player {}): "
                specialModeBools["honours"] = True
                returnValue = notPassing(bid)
                # This would be true if it was a successful higher honers call
                if returnValue:
                    highestSpecialMode["honours"] = key
            return returnValue
        
        elif (bid == "solo"):
            bid = soloContractorFn(bid)
            specialModeBools["solo"] = True
            highestSpecialMode["solo"] = bidPlayer
            returnValue = notPassing(bid)
            return returnValue
        
        elif not any(specialModeBools.values()):
            returnValue = notPassing(bid)
            return returnValue
        
        else:
            # After honours is called, players should only be able to call higher honours, not raw numbers like 49, so deliberately passing 0.
            returnValue = notPassing(0)
            print("You are only allowed to perform higher honours calls or solo")
        
    teamToBid = None # 0 for team 1, 1 for team 2

    if (currentBidStarter % 2 == 0):
        teamToBidStarter = 0
        teamToBid = 0
    else:
        teamToBidStarter = 1
        teamToBid = 1

    playersTeamBidded = [0, 0]
    highestBid = maxPoints // 2 - 1 # Start just before actual highest bid (14, 28, 42) -> (13, 27, 41)
    highestSpecialMode = {
        "honours": None,
        "solo": None
    }
    highestBidTeam = 0
    bidPlayer = currentBidStarter
    highestBidPlayer = None
    maxPlayersPerTeam = noOfPlayers // 2 - 1
    whileValidity = [True] # List for mutation by playerCountAndConditionalValidityFn()
    ifValidity = [True, True]
    specialModeBools = {
        "honours": False,
        "solo": False
    }

    bidText = "Pass or Make a bid higher (Player {}): "

    # Without this, the first player can mess up a bad special bid call, and then be able to pass the game
    while True:
        displayCards(players[bidPlayer])
        bid = input(f"Bid, the lowest you can bid is {maxPoints // 2} (Player {bidPlayer}): ").lower()
        if bid == "pass":
            print("The first player isn't allowed to pass")
        elif bid == "exit":
            return 0, 0, 0
        elif handleBids(bid):
            break

    while whileValidity[0]:
        displayCards(players[bidPlayer])
        bid = input(bidText.format(bidPlayer)).lower() # No concept as 0th player in game.
        if bid == "exit":
            return
        elif (bid == "pass"):
            playerCountAndConditionalValidityFn(playersTeamBidded, teamToBid, whileValidity, 0)
            bidPlayer += 2    
        else:
            handleBids(bid)

        bidPlayer = bidPlayer % noOfPlayers # Let it build up till player 6 (so bidPlayer = 5), then round to player 1 (bidPlayer = 0)

    if (specialModeBools["solo"]):
        print("Player", highestSpecialMode["solo"], "has chosen SOLO CONTRACTOR mode")
        return [highestBid, highestBidTeam, highestBidPlayer]
    elif (specialModeBools["honours"]):
        print("Team", highestBidTeam, "has called", highestSpecialMode["honours"])
        return [highestBid, highestBidTeam, highestBidPlayer]
    else:
        print("The highest bid is", highestBid, "by team", highestBidTeam)
        return [highestBid, highestBidTeam, highestBidPlayer]

def handleRound(players, highestBid, highestBidTeam, highestBidPlayer):

    def sortSuitandRank(card, *, rankNeeded):
        while True:
            try:
                rank, suit = card.split(" ")
                break
            except (ValueError):
                return None

        if (rank in ("heart", "spade", "club", "diamonde")):
            temp = rank
            rank = suit
            suit = temp
        
        if rankNeeded == True:
            return suit, rank
        else:
            return suit

    def checkForSuit(player, *, suit, currentSuit):
        if(suit != currentSuit):
            suitsOfPlayer = []
            for card in player["cards"]:
                value = sortSuitandRank(card, rankNeeded=False)
                # The main deck always have a valid suit rank, but this is just for safety and being explicit in code.
                if value:
                    suitsOfPlayer.append(value)
            if currentSuit in suitsOfPlayer:
                return True
            else:
                return False

    round = {
        "starter": currentBidStarter,
        "holder": currentBidStarter
    }
    while True:
        firstSuit = True
        # i is important as players that is starting the round can be anyone
        print("NEW ROUND \n \n")
        for i in range(len(players)): 
            index = (round["starter"] + i) % noOfPlayers
            while True:
                while True:
                    displayCards(players[index])
                    selectedCard = input(f"{players[index]["name"]}'s turn: ").lower()
                    if input == 'exit':
                        return
                    tempValueHolder = sortSuitandRank(selectedCard, rankNeeded=True)
                    if tempValueHolder:
                        suit, rank = tempValueHolder
                        break
                    else:
                        print("Incorrect format, try typing in the way it is displayed above (not case sensitive):")    

                # Sorting things like Heart 10, to 10 Heart
                selectedCard = rank + ' ' + suit

                if (selectedCard not in players[index]["cards"]):
                    print("You do not have this card")
                    continue

                if (firstSuit):
                    currentSuit = suit
                    firstSuit = False

                if(suit != currentSuit and checkForSuit(players[index], suit=suit, currentSuit=currentSuit)):
                    print(f"Play a card of the suit {currentSuit}")
                else:
                    players[index]["cards"].remove(selectedCard)
                    break
                



            #print(rank)
            #print(suit) Code now distributes cards, and has seperated rank and suit
def main():
    makeCardTemplate(currentDeck)
    distributeCards(currentDeck)
    highestBid, highestBidTeam, highestBidPlayer = bidding(players)
    if highestBid == 0:
        return
    #print(highestBid, highestBidTeam, highestBidPlayer)
    handleRound(players, highestBid, highestBidTeam, highestBidPlayer)

main()
# implement mvp, then clean up the variable names
# Implement trump card
# Implemented card display fixes (unable to scale according to player's cards), forcing player to deck suit if they have it + more
# Generalised player % noOfPlayers to both the main round function and the bidding function
