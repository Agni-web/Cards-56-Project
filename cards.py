import random
deck = {"8": 0, "9": 2, "10": 1, "A": 1, "J": 3, "Q": 0, "K": 0}
numbers = ["8", "9", "10", "A", "J", "Q", "K"]
NoOfCardsAtATime = 3
maxPoints = 56

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
    def notPassing(bid):
        nonlocal bidPlayer, highestBid, highestBidTeam, teamToBid, teamToBidStarter

        try:
            bid = int(bid)
        except ValueError:
            print("Input shouldn't contain characters")
            return

        if (bid > highestBid and bid < maxPoints + 1):
            highestBid = bid
            if (bid + 1 > maxPoints):
                return

            otherTeamToBid = 1 - teamToBid
            highestBidTeam = teamToBid
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
        else:
            print("Invalid bid")

    bid = input(f"Bid, the lowest you can bid is {maxPoints // 2} (Player {bidPlayer}): ").lower()
    notPassing(bid)

    while whileValidity[0]:
        bid = input(f"Pass or Make a bid higher (Player {bidPlayer}): ").lower() # No concept as 0th player in game.
        if (bid == "pass"):
            playerCountAndConditionalValidityFn(playersTeamBidded, teamToBid, whileValidity, 0)

            bidPlayer += 2
        else:
            notPassing(bid)
        # I used pass statement to allow me to use the variable noOfPlayers directly, otherwise it would have to be, if (bidPlayer > noOfPlayers - 1)
        if (bidPlayer < noOfPlayers): 
            pass
        else:
            bidPlayer = bidPlayer % noOfPlayers # Let it build up till player 6 (so bidPlayer = 5), then round to player 1 (bidPlayer = 0)

    print("The highest bid is", highestBid, "by team", highestBidTeam)
    return [highestBid, highestBidTeam]

bidding()
#implement honers, max bid doesnt end the game
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

    
        

