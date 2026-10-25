import random, re
deck = {"8": 0, "9": 2, "10": 1, "A": 1, "J": 3, "Q": 0, "K": 0}
numbers = ["8", "9", "10", "A", "J", "Q", "K"]
NoOfCardsAtATime = 3
maxPoints = 56
 # 11/56 is ratio to loose, you can pick any.., or even a different way to calculate all this.
honoursMinCall = maxPoints - round((12 / 56) * maxPoints - 1)

suits = ["Spade", "Clubs", "Heart", "Diamonde"]
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
bool8 = True

def honoursFn(bid):
    bidMapping = {}

    bidMapping[f"honours"] = honoursMinCall
    for i, point in enumerate(range(honoursMinCall + 3, maxPoints, 3), start=1):
        bidMapping[f"honours {i}"] = point
    bidMapping[f"honours {i + 1}"] = maxPoints
    # I have allowed maxPoints honour call, if a player really wants to flex that they don't need extra point for winning solo contractor mode.

    value = bidMapping.get(bid)
    if value is not None:
        return bidMapping[bid]
    else:
        return None

def soloContractorFn(bid):
    pass


for number in numbers:

    currentDeck.append(number + ' ' + suits[0])
    currentDeck.append(number + ' ' + suits[1])
    currentDeck.append(number + ' ' + suits[2])
    currentDeck.append(number + ' ' + suits[3])

    if (number == "8" and bool8):
        bool8 = False
        continue

    currentDeck.append(number + ' ' + suits[0])
    currentDeck.append(number + ' ' + suits[1])
    currentDeck.append(number + ' ' + suits[2])
    currentDeck.append(number + ' ' + suits[3])

currentDeck.append('8' + ' ' + suits[1])
currentDeck.append('8' + ' ' + suits[3])

for _ in range(3):
    random.shuffle(currentDeck)

for i in range(0, len(currentDeck), NoOfCardsAtATime):
    cardDealTurn = (i // NoOfCardsAtATime) % (noOfPlayers) # Integer floor division
    players[cardDealTurn]["cards"].extend(currentDeck[i:i+3])


def bidding():
    # Sending things as a list so the original value changes..
    def playerCountAndConditionalValidityFn(playersTeamBidded, index1, validityBool, index2):
        if (playersTeamBidded[index1] < maxPlayersPerTeam):
            playersTeamBidded[index1] += 1
        else:
            validityBool[index2] = False

    def notPassing(bid):
        nonlocal bidPlayer, highestBid, highestBidTeam, teamToBid, teamToBidStarter

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
            highestBid = bid
            highestBidTeam = teamToBid
            if (bid + 1 > maxPoints):
                whileValidity[0] = False
                return True

            otherTeamToBid = 1 - teamToBid
            if (ifValidity[otherTeamToBid]):
                if teamToBidStarter == teamToBid:
                    bidPlayer = currentBidStarter + playersTeamBidded[otherTeamToBid] * 2 + 1
                else:
                    bidPlayer = currentBidStarter + playersTeamBidded[otherTeamToBid] * 2

                playerCountAndConditionalValidityFn(playersTeamBidded, teamToBid, ifValidity, teamToBid)
            else:
                whileValidity[0] = False

            if (not any(ifValidity)):
                whileValidity[0] = False

            if teamToBid == 0:
                teamToBid = 1
            else:
                teamToBid = 0
            return True
        else:
            print("Invalid bid")
            return False

    def handleBids(bid):
        nonlocal bidText
        returnValue = None

        if (re.fullmatch(r"honours( \d+)?", bid)):
            bid = honoursFn(bid)
            if bid is None:
                print("Invalid honours call")
                returnValue = False
            else:
                returnValue = notPassing(bid)
            return returnValue
        elif (bid == "solo"):
            bid = soloContractorFn(bid)
            if bid is None:
                print("Invalid solo contractor call")
                returnValue = False
            else:
                returnValue = notPassing(bid)
            return returnValue
        else:
            returnValue = notPassing(bid)
            return returnValue
        
    currentBidStarter = 2
    teamToBid = None # 0 for team 1, 1 for team 2
    playersTeamBidded = [0, 0]

    if (currentBidStarter % 2 == 0):
        teamToBidStarter = 0
        teamToBid = 0
    else:
        teamToBidStarter = 1
        teamToBid = 1

    highestBid = maxPoints // 2 - 1 # Start just before actual highest bid (14, 28, 42) -> (13, 27, 41)
    highestBidTeam = 0
    bidPlayer = currentBidStarter
    maxPlayersPerTeam = noOfPlayers // 2 - 1
    whileValidity = [True] # List for mutation by playerCountAndConditionalValidityFn()
    ifValidity = [True, True]
    bidText = "Pass or Make a bid higher (Player {}): "

    # Without this, the first player can mess up a bad special bid call, and then be able to pass the game
    while True:
        bid = input(f"Bid, the lowest you can bid is {maxPoints // 2} (Player {bidPlayer}): ").lower()
        if bid == "pass":
            print("The first player isn't allowed to pass")
        elif bid == "exit":
            return
        elif handleBids(bid):
            break

    while whileValidity[0]:
        bid = input(bidText.format(bidPlayer)).lower() # No concept as 0th player in game.
        if bid == "exit":
            return
        elif (bid == "pass"):
            playerCountAndConditionalValidityFn(playersTeamBidded, teamToBid, whileValidity, 0)
            bidPlayer += 2    
        else:
            handleBids(bid)
        # I used this statement to allow me to use the variable noOfPlayers directly, otherwise it would have to be, if (bidPlayer > noOfPlayers - 1)
        if not (bidPlayer < noOfPlayers): 
            bidPlayer = bidPlayer % noOfPlayers # Let it build up till player 6 (so bidPlayer = 5), then round to player 1 (bidPlayer = 0)

    print("The highest bid is", highestBid, "by team", highestBidTeam)
    return [highestBid, highestBidTeam]

bidding()
#implement solo contractor, change the bid text after an honours, prevent ppl from simply betting the points higher, and actually using the honours 1 system
while False:
    firstSuit = True

    
    for i in range(len(players)):
        for card in players[i]["cards"]:
            print(f"{card} ", end="")
        print()
        selectedCard = input(f"Player {i+1}'s turn \n")

        if input == 0:
            break

        if (selectedCard in ("king", "k", "queen", "q", "jack", "j", "ace", "a")):
            pass
        value, suit = selectedCard.lower().split(" ")
        if (value in ("heart", "spade", "club", "diamonde")):
            temp = value
            value = suit
            suit = temp

        if (firstSuit):
            currentSuit = suit
        if(suit != firstSuit):
            continue


        #print(value)
        #print(suit) Code now distributes cards, and has seperated value and suit

    
        

