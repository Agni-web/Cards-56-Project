import random, re
import helpers, testCase

deck = {
    "points": {"8": 0, "9": 2, "10": 1, "A": 1, "J": 3, "Q": 0, "K": 0},
    "priority": {"8": 0, "9": 5, "10": 3, "A": 4, "J": 6, "Q": 1, "K": 2}
}
ranks = ["8", "9", "10", "A", "J", "Q", "K"]

deck = {
    outerLoopKey: {key.lower(): value for key, value in innerLoopValue.items()}
    for outerLoopKey, innerLoopValue in deck.items()
}
ranks = {rank.lower() for rank in ranks} # Making a set for efficient O(1) if rank in ranks lookups.

# Write all similar colours like black, and red, together.
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

globalValues = {
    "noOfCardsAtATime": 3,
    "maxPoints": (_maxPoints := 56),
    # 12/56 is ratio to loose, you can pick any.., or even a different way to calculate all this.
    "honoursMinCall": _maxPoints - round((12 / 56) * _maxPoints - 1),
    "currentBidStarter": 2,
    # Gets defined in bidding()
    "teamToBidStarter": None,
    "noOfPlayers": len(players),
    # Gets defined in bidding()
    "noOfCards": None
}
del _maxPoints

currentDeck = []

def bidding(players):
    # Sending things as a list so the original value changes..
    def playerCountAndConditionalValidityFn(playersTeamBidded, index1, validityBool, index2):
        if (playersTeamBidded[index1] < maxPlayersPerTeam):
            playersTeamBidded[index1] += 1
        else:
            validityBool[index2] = False

    def notPassing(bid):
        nonlocal bidPlayer, highestBidPlayer, highestBid, highestBidTeam, teamToBid

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

        if (bid > highestBid and bid < globalValues["maxPoints"] + 1):
            highestBidPlayer = bidPlayer
            highestBid = bid
            highestBidTeam = teamToBid
            otherTeamToBid = 1 - teamToBid
            if (ifValidity[otherTeamToBid]):
                if globalValues["teamToBidStarter"] == teamToBid:
                    bidPlayer = globalValues["currentBidStarter"] + playersTeamBidded[otherTeamToBid] * 2 + 1
                else:
                    bidPlayer = globalValues["currentBidStarter"] + playersTeamBidded[otherTeamToBid] * 2

                playerCountAndConditionalValidityFn(playersTeamBidded, teamToBid, ifValidity, teamToBid)
            else:
                whileValidity[0] = False

            if teamToBid == 0:
                teamToBid = 1
            else:
                teamToBid = 0

            if (bid + 1 > globalValues["maxPoints"]):
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
            bid, key = helpers.honoursFn(bid, globalValues["honoursMinCall"], globalValues["maxPoints"])
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
            bid = helpers.soloContractorFn(bid)
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

    def getTrump(player):
        while True:
            helpers.displayCards(player)
            trump = input(f"Select the trump player {player["name"]}: ").lower()
            value = helpers.sortSuitandRank(trump, suits=suits, ranks=ranks, rankNeeded=True)
            if value:
                if helpers.checkForSuitAndRank(player, trump, suits=suits, ranks=ranks, rankNeeded=True):
                    player["cards"].remove(trump)
                    return trump
                else:
                    print("Invalid trump selected")
            else:
                print("Invalid trump selection format (It should be suit rank, or rank suit, like J heart, hEaRT j , case insensitive)")

    teamToBid = helpers.playerToTeam(globalValues["currentBidStarter"])
    globalValues["teamToBidStarter"] = teamToBid

    playersTeamBidded = [0, 0]
    highestBid = globalValues["maxPoints"] // 2 - 1 # Start just before actual highest bid (14, 28, 42) -> (13, 27, 41)
    highestSpecialMode = {
        "honours": None,
        "solo": None
    }
    highestBidTeam = 0
    bidPlayer = globalValues["currentBidStarter"]
    highestBidPlayer = None
    maxPlayersPerTeam = globalValues["noOfPlayers"] // 2 - 1
    whileValidity = [True] # List for mutation by playerCountAndConditionalValidityFn()
    ifValidity = [True, True]
    specialModeBools = {
        "honours": False,
        "solo": False
    }

    bidText = "Pass or Make a bid higher (Player {}): "

    # Without this, the first player can mess up a bad special bid call, and then be able to pass the game
    while True:
        helpers.displayCards(players[bidPlayer])
        bid = input(f"Bid, the lowest you can bid is {globalValues["maxPoints"] // 2} (Player {players[bidPlayer]["name"]}): ").lower()
        if bid == "pass":
            print("The first player isn't allowed to pass")
        elif bid == "exit":
            return 0, 0, 0
        elif handleBids(bid):
            break

    while whileValidity[0]:
        helpers.displayCards(players[bidPlayer])
        bid = input(bidText.format(players[bidPlayer]["name"])).lower() # No concept as 0th player in game.
        if bid == "exit":
            return
        elif (bid == "pass"):
            playerCountAndConditionalValidityFn(playersTeamBidded, teamToBid, whileValidity, 0)
            bidPlayer += 2    
        else:
            handleBids(bid)

        bidPlayer = bidPlayer % globalValues["noOfPlayers"] # Let it build up till player 6 (so bidPlayer = 5), then round to player 1 (bidPlayer = 0)

    globalValues["noOfCards"] = len(players[0]["cards"])

    if (specialModeBools["solo"]):
        print("Player", highestSpecialMode["solo"], "has chosen SOLO CONTRACTOR mode")
        return [highestBid, highestBidPlayer, getTrump(players[highestBidPlayer])]
    elif (specialModeBools["honours"]):
        print("Team", highestBidTeam, "has called", highestSpecialMode["honours"])
        return [highestBid, highestBidPlayer, getTrump(players[highestBidPlayer])]
    else:
        print("The highest bid is", highestBid, "by team", highestBidTeam)
        return [highestBid, highestBidPlayer, getTrump(players[highestBidPlayer])]

def handleRound(players, highestBid, highestBidPlayer, trump):

    def getPlayerMove():
        while True:
            helpers.displayCards(players[index["currentPlayerToPlay"]])
            selectedCard = input(f"{players[index["currentPlayerToPlay"]]["name"]}'s turn: ").lower()

            if selectedCard == "exit":
                return False
            if selectedCard == "show trump":
                fakePlayer = {
                    "name": "heeeheee",
                    "cards": [trump]
                }
                print("Trump revealed!")
                helpers.displayCards(fakePlayer)
                players[highestBidPlayer]["cards"].append(trump)
                helpers.sortingTheCards(players[highestBidPlayer], suits, ranks, deck["priority"])
                continue
            
            # Sorting things like Heart 10, to 10 Heart
            tempValueHolder = helpers.sortSuitandRank(selectedCard, suits=suits, ranks=ranks, rankNeeded=True)

            if tempValueHolder:
                suit, rank = tempValueHolder
                return suit, rank
            else:
                print("Invalid card format (It should be suit rank, or rank suit, like J heart, hEaRT j , case insensitive or type in Show Trump)")    ###

    temp = helpers.sortSuitandRank(trump, suits=suits, ranks=ranks, rankNeeded=True)
    currentGame = {
        # Holder team will be evaluated on the fly
        "roundHolderPlayer": globalValues["currentBidStarter"],
        # Since only 2 teamsn (core part of the game), we will base things off of the game starting team.
        "starterTeamPoints": 0,
        "trumpSuite": temp[0],
        "trumpRank": temp[1],
        "trumpRevealed": False
    }
    for _ in range(globalValues["noOfCards"]):
        index = {
            "roundStarter": currentGame["roundHolderPlayer"],
            "currentPlayerToPlay": None
        }
        currentHighestRank = None
        currentHighestTrumpRank = None
        firstSuit = True
        points = 0
        # i is important as players that is starting the round can be anyone
        print("NEW ROUND \n \n")
        for i in range(len(players)):
            index["currentPlayerToPlay"] = (index["roundStarter"] + i) % globalValues["noOfPlayers"]
            while True:
                temp = getPlayerMove()
                if temp:
                    suit, rank = temp
                else:
                    continue

                selectedCard = rank + ' ' + suit

                # This already ensures suit and rank are correct.
                if (selectedCard not in players[index["currentPlayerToPlay"]]["cards"]):
                    print("You do not have this card")
                    continue

                if (suit == currentGame["trumpSuite"] and currentGame["trumpRevealed"] is False and index["currentPlayerToPlay"] == highestBidPlayer):
                    print("The person who has selected the trump cannot start with it until its revealed")
                    continue
                
                if (firstSuit):
                    currentSuit = suit
                    firstSuit = False

                if(suit != currentSuit and helpers.checkForSuitAndRank(players[index["currentPlayerToPlay"]], currentSuit, suits=suits, ranks=ranks, rankNeeded=False)):
                    print(f"Play a card of the suit {currentSuit}")
                else:
                    #if currentSuit is not trump and suit == trump: -> If a player doesn't have trump, obviously their current card can't be trump
                    if suit == currentGame["trumpSuite"] and deck["priority"][rank] > deck["priority"].get(currentHighestTrumpRank, -1):
                        currentGame["roundHolderPlayer"] = index["currentPlayerToPlay"]
                        currentHighestTrumpRank = rank
                    # Get is used for avoiding error on the first run
                    elif (suit == currentSuit and deck["priority"][rank] > deck["priority"].get(currentHighestRank, -1)
                          and currentHighestTrumpRank is None):
                        currentGame["roundHolderPlayer"] = index["currentPlayerToPlay"]
                        currentHighestRank = rank

                    players[index["currentPlayerToPlay"]]["cards"].remove(selectedCard)
                    points += deck["points"][rank]
                    print(f"Points collected {points}")
                    break
                    
            print(f"Player having the round {players[currentGame["roundHolderPlayer"]]["name"]}")

        print(f"Team that bid's points {currentGame["starterTeamPoints"]}")
        if (helpers.playerToTeam(currentGame["roundHolderPlayer"]) == globalValues["teamToBidStarter"]):
            currentGame["starterTeamPoints"] += points
            print(f"Points successfully collected by team {globalValues["teamToBidStarter"]}")

def main():
    helpers.makeCardTemplate(currentDeck, ranks, suits)
    helpers.distributeCards(currentDeck, globalValues["noOfCardsAtATime"], globalValues["noOfPlayers"], players)
    for player in players:
        helpers.sortingTheCards(player, suits, ranks, deck["priority"])
    highestBid, highestBidPlayer, trump = bidding(players)
    if highestBid == 0:
        return

    handleRound(players, highestBid, highestBidPlayer, trump)
    #handleRound(*testCase.test())

main()
# implement mvp, then clean up the variable names
# In solo, they start the round,
# implement winning and loosing, implement overall winning and loosing using files
# many scenerios, u can be playing, and as the person who kept trump, u now have to play that trump
# You can be the player who kept the trump and now start with it if you got no other cards
# Trump should be removed from the player but that will mess with the loops
# If a person asks for trump, the main guy gets it back
"""
"""
