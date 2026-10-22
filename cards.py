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
    MAX_BID = noOfPlayers
    currentBidStarter = 1
    teamToBid = None # 0 for team 1, 1 for team 2
    playersTeamBidded = [0, 0]

    if (currentBidStarter % 2 == 0):
        teamToBidStarter = 0
        teamToBid = 0
    else:
        teamToBidStarter = 1
        teamToBid = 1

    highestBid = maxPoints / 2 - 1 # Start just before actual highest bid (14, 28, 42) -> (13, 27, 41)
    highestBidTeam = 0
    bidPlayer = currentBidStarter
    maxPlayersPerTeam = noOfPlayers / 2 - 1
    whileValidity = True
    ifValidity = [True, True]

    while whileValidity:
        bid = input(f"Pass or Make a bid higher (Player {bidPlayer}): ").lower() # No concept as 0th player in game.
        if (bid == "pass"):
            if (teamToBid == 0):
                if (playersTeamBidded[0] < maxPlayersPerTeam):
                    playersTeamBidded[0] += 1
                else:
                    whileValidity = False
            else:
                if (playersTeamBidded[1] < maxPlayersPerTeam):
                    playersTeamBidded[1] += 1
                else:
                    whileValidity = False

            bidPlayer += 2
            # I used pass statement to allow me to use the variable noOfPlayers directly, otherwise it would have to be, if (bidPlayer > noOfPlayers - 1)
            if (bidPlayer < noOfPlayers): 
                pass
            else:
                bidPlayer = bidPlayer % noOfPlayers # Let it build up till player 6 (so bidPlayer = 5), then round to player 1 (bidPlayer = 0)
        else:
            bid = int(bid)

            if (bid > highestBid and bid < 57):
                highestBid = bid
                if (bid + 1 > 56):
                    whileValidity = False
                if (teamToBid == 0):
                    highestBidTeam = 0
                    if (ifValidity[1]):
                        if teamToBidStarter == 0:
                            bidPlayer = currentBidStarter + playersTeamBidded[1] * 2 + 1
                        else:
                            bidPlayer = currentBidStarter + playersTeamBidded[1] * 2

                        if (playersTeamBidded[0] < maxPlayersPerTeam and ifValidity[0]):
                            playersTeamBidded[0] += 1
                        else:
                            ifValidity[0] = False
                    else:
                        whileValidity = False
                else:
                    highestBidTeam = 1
                    if (ifValidity[0]):
                        if teamToBidStarter == 0:
                            bidPlayer = currentBidStarter + playersTeamBidded[0] * 2
                        else:
                            bidPlayer = currentBidStarter + playersTeamBidded[0] * 2 + 1

                        if (playersTeamBidded[1] < maxPlayersPerTeam and ifValidity[1]):
                            playersTeamBidded[1] += 1
                        else:
                            ifValidity[1] = False
                    else:
                        whileValidity = False

                if (ifValidity[0] == False and ifValidity[1] == False):
                    whileValidity = False

                if teamToBid == 0:
                    teamToBid = 1
                else:
                    teamToBid = 0

                if (bidPlayer < noOfPlayers): 
                    pass
                else:
                    bidPlayer = bidPlayer % noOfPlayers
            else:
                print("Invalid bid")

    print("The highest bid is", highestBid, "by team", highestBidTeam)

bidding()    
# Force first player to bid, implement honers, fix weird letting 3rd player bid again before exiting
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

    
        

