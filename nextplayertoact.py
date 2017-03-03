def _nextplayer(players, value):
    ret = value + 1
    if ret >= len(players):
        return 0
    return ret

def _findnextplayer(players, pos, dealer):
    wrap = pos == dealer
    nextplayer = _nextplayer(players, pos)
    while nextplayer != pos:
        if players[nextplayer]:
            return nextplayer, wrap
        if nextplayer == dealer:
            wrap = True
        nextplayer = _nextplayer(players, nextplayer)
    return pos, wrap

def nextplayertoact(players, bb, dealer, startbet, amounttocall, currentplayer):
    count = 0
    for player in players:
        if player and player[0] > 0:
            count += 1
    if count == 0:
        return -1
    nextplayer, wrap = _findnextplayer(players, currentplayer, dealer)
    while nextplayer != currentplayer:
        if amounttocall == 0 and wrap:
            return -1
        if players[nextplayer][0] > 0:
            if amounttocall == 0:
                return nextplayer
            if amounttocall > 0 and amounttocall == startbet and nextplayer == bb:
                return nextplayer
            if amounttocall == players[nextplayer][1]:
                return -1
            return nextplayer
        nextplayer, wrap = _findnextplayer(players, nextplayer, dealer)
    return -1

if __name__ == '__main__':
    if nextplayertoact([(100, 0), (100, 0), (100, 0), (100, 0), (100, 0), (100, 0)], 2, 0, 0, 0, 5) != 0:
        print('Test1 failed')
    if nextplayertoact([(100, 0), (100, 0), (100, 0), (100, 0), (100, 0), (100, 0)], 2, 0, 0, 0, 4) != 5:
        print('Test2 failed')
    if nextplayertoact([(100, 0), (100, 0), (100, 0), (100, 0), (100, 0), (100, 0)], 2, 0, 0, 0, 0) != -1:
        print('Test3 failed')
    if nextplayertoact([(100, 50), (100, 50), (100, 50), (100, 50), (100, 50), (100, 50)], 2, 0, 50, 50, 1) != 2:
        print('Test4 failed')
    if nextplayertoact([(100, 50), (100, 50), (100, 50), (100, 50), (100, 50), (100, 50)], 2, 0, 50, 50, 2) != -1:
        print('Test5 failed')
    if nextplayertoact([(100, 50), (100, 50), (100, 50), (100, 50), (100, 50), (100, 50)], 2, 0, 0, 50, 3) != -1:
        print('Test6 failed')
    if nextplayertoact([(100, 50), (100, 50), (100, 50), (100, 50), (100, 0), (100, 50)], 2, 0, 0, 50, 3) != 4:
        print('Test7 failed')
    if nextplayertoact([(100, 50), (100, 50), (100, 50), (100, 50), (100, 50), (100, 50)], 2, 0, 50, 50, 1) != 2:
        print('Test8 failed')
