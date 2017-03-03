import engine

def printcardvalue(value):
    if value <= 9:
        return str(value)
    elif value == 10:
        return 'T'
    elif value == 11:
        return 'J'
    elif value == 12:
        return 'Q'
    elif value == 13:
        return 'K'
    elif value == 14:
        return 'A'
    return '?'

def printcard(card):
    return printcardvalue(card[1]) + card[0]

def printplayercards(cards):
    if len(cards) < 2:
        return ''
    return printcard(cards[0]) + ', ' + printcard(cards[1])

def printplayer(player, idx, currentplayer, dealer):
    s = '  '
    if currentplayer == idx:
        s = '+ '
    elif dealer == idx:
        s = '- '
    s += str(idx).ljust(2)
    s += player['name'].ljust(12)
    s += str(player['chipsleft']).ljust(12)
    s += str(player['chipsinplay']).ljust(12)
    s += printplayercards(player['cards']).ljust(12)
    print(s)

def printplayers(players, currentplayer, dealer):
    print('    ' + 'Name'.ljust(12) + 'ChipsLeft'.ljust(12) + 'ChipsInPlay'.ljust(12) + 'Cards')
    for i in range(len(players)):
        printplayer(players[i], i, currentplayer, dealer)

def printtableinfo(sb, bb, tablecards, pots):
    print('Blinds: ' + str(sb) + '/' + str(bb))
    printtablecards(tablecards)
    print('Main pot: ' + str(pots[0]['chips']))

def printtablecards(cards):
    s = 'Cards: '
    if len(cards) == 0:
        print(s)
        return
    s += printcard(cards[0]) + ', '
    for i in range(1, len(cards) - 1):
        s += printcard(cards[i]) + ', '
    s += printcard(cards[len(cards) - 1])
    print(s)

def printpokertable(players, currentplayer, dealer, sb, bb, tablecards, pots):
    for i in range(20):
        print()
    printtableinfo(sb, bb, tablecards, pots)
    print()
    printplayers(players, currentplayer, dealer)

game = engine.Game()
gamedata = game.start()

while gamedata['currentplayer'] != -1:
    printpokertable(gamedata['players'],
                    gamedata['currentplayer'],
                    gamedata['dealer'],
                    gamedata['sb'],
                    gamedata['bb'],
                    gamedata['tablecards'],
                    gamedata['pots'])
    command = input('Enter command: ')
    if command == 'fold':
        gamedata = game.fold()
    elif command == 'check':
        gamedata = game.check()
    elif command == 'call':
        gamedata = game.call()
    elif command == 'raise':
        amount = input('Amount: ')
        gamedata = game.bet(int(amount))

print('Game over')
