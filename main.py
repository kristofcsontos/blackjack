import random, sys

# Színek/Jelek 
HEARTS   = chr(9829) # Kőr
DIAMONDS = chr(9830) # Káró
SPADES   = chr(9824) # Pikk
CLUBS    = chr(9827) # Treff
BACKSIDE = 'backside'


def main():
    money = betMoney()
    
    while True: 
        # Addig tart a játék még van pénz
        # Vizsgálat
        if money <= 0:
            print("Elfogyott a pénzed. Vége!")
            sys.exit()
        #Fogadás
        print('Money:', money)
        bet = BetMoney(money)

        #Kártyaosztás
        deck = getDeck()
        dealerHand = [deck.pop(), deck.pop()] 
        playerHand = [deck.pop(), deck.pop()]

        print('Fogadás:', bet)
        while True: 
            displayHands(playerHand, dealerHand, False)
            print()
            
            if getHandValue(playerHand) > 21:
                break

            #Játékos lépés választás
            move = getMove(playerHand, money - bet)

            if move in ('H', 'D'):
                # Új kártya
                #newCard = deck.pop()
                #rank, suit = newCard
                #print(rank, suit)
                playerHand.append(deck.pop())
                if getHandValue(playerHand) > 21:
                    #Bust
                    continue

            # Játékos lépés választás kezelése:
            if move == 'D':
                # Ha duplázik akkor növelheti a tétet 
                plusBet = BetMoney(min(bet, (money - bet)))
                bet += plusBet
                print('Tétet megemelte: {}.'.format(bet))
                print('Bet:', bet)


            if move in ('S', 'D'):
                # megáll ha Stop vagy double van
                break

        # Dealer
        if getHandValue(playerHand) <= 21:
            while getHandValue(dealerHand) < 17:
                print('Dealer húz...')
                dealerHand.append(deck.pop())
                displayHands(playerHand, dealerHand, False)
                if getHandValue(dealerHand) > 21:
                    break 
                input('Press Enter to continue...')
                print('\n\n')

        #Felfordított dealer lapok
        displayHands(playerHand, dealerHand, True)
        playerValue = getHandValue(playerHand)
        dealerValue = getHandValue(dealerHand)
        if dealerValue > 21:
            print('Dealer bust! Te nyetél: ${}!'.format(bet))
            money += bet
        elif (playerValue > 21) or (playerValue < dealerValue):
            print('Vesztettél!')
            money -= bet
        elif playerValue > dealerValue:
            print('Te nyertél: ${}!'.format(bet))
            money += bet
        elif playerValue == dealerValue:
            print('Döntetlen!')

        input('Press Enter to continue...')
        print('\n')


def BetMoney(maxBet):
    while True:  
            print('Mennyivel szeretnél fogadni? (1-{}, or QUIT)'.format(maxBet))
            bet = input('> ').upper().strip()
            if bet == 'QUIT':
                print('Vége')
                sys.exit()
            try:
                bet = int(bet)
                if 1 <= bet <= maxBet:
                    return bet  
            except:
                print('(1-{}, or QUIT)'.format(maxBet))
                print()
        

def getDeck():
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))  
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))  #  Hozzáadja ('2', '♥')
    random.shuffle(deck)
    return deck

def displayHands(playerHand, dealerHand, showDealerHand):
    print()
    if showDealerHand:
        print('DEALER:', getHandValue(dealerHand))
        displayCards(dealerHand)
    else:
        print('DEALER:')
        # dealer első kártyája rejtett
        displayCards([BACKSIDE] + dealerHand[1:])

    print('Játékos:', getHandValue(playerHand))
    displayCards(playerHand)


def getHandValue(cards):
    #Kártya érték 
    value = 0
    numberOfAces = 0

    for card in cards:
        rank = card[0]  
        if rank == 'A':
            numberOfAces += 1
        elif rank in ('K', 'Q', 'J'):  
            value += 10
        else:
            value += int(rank) 
    value = numberOfAces + value 
    for i in range(numberOfAces):   
        if value + 10 <= 21:
            value += 10
    return value


def displayCards(cards):
    rows = ['', '', '', '', '']  # sorokban megjelenítendő szöveg.
    for i, card in enumerate(cards):
        rows[0] += ' ___  '  # Felső sor a kártyában
        if card == BACKSIDE:
            # Dealer kártya hátoldala
            rows[1] += '|## | '
            rows[2] += '|###| '
            rows[3] += '|_##| '
        else:
            rank, suit = card
            rows[1] += '|{} | '.format(rank.ljust(2))
            rows[2] += '| {} | '.format(suit)
            rows[3] += '|_{}| '.format(rank.rjust(2, '_'))
    for row in rows:
        print(row)

def getMove(playerHand, money):
    """Bekéri hogy a következő lépést és vissza adja H vagy S vagy D"""
    while True:  
        moves = ['H(úzás)', 'S(top)']  
        # A kártya húzás plusszban +
        # A megállj -

        # Ha két kártyája van és van még pénze tudja bővíteni a fogadás pénzét
        if len(playerHand) == 2 and money > 0:
            moves.append('D(upla)')
        movesPrint = ', '.join(moves)+": "
        move = input(movesPrint).upper()
        if move in ('H', 'S'):
            return move  # megáll vagy hit
        if move == 'D' and 'D(upla)' in moves:
            return move  # duplázás
def betMoney():
    while True:
        try:
            print("\n\nMekkora téttel szeretne fogadni?")
            money = int(input('> '))
            return money
        except:
            print("Hiba, számot írjon be")
main()