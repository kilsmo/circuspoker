def movebutton(players, bb, sb, dealer):
    nextbb = _findnextplayer(players, bb)
    second = _findnextplayer(players, nextbb)
    third = _findnextplayer(players, second)
    if third == nextbb:
        return nextbb, second, second
    nextsb = -1
    if players[bb]:
        nextsb = bb
    nextdealer = dealer
    if players[sb]:
        nextdealer = sb
    return nextbb, nextsb, nextdealer

def _addone(players, value):
    ret = value + 1
    if ret >= len(players):
        return 0
    return ret

def _findnextplayer(players, pos):
    nextplayer = _addone(players, pos)
    while nextplayer != pos:
        if players[nextplayer]:
            return nextplayer
        nextplayer = _addone(players, nextplayer)
    return -1 # should never happen

if __name__ == '__main__':
    bb, sb, dealer = movebutton([True, True, True, True, True, True], 2, 1, 0)
    if (bb != 3 or sb != 2 or dealer != 1):
        print('test1 failed')
    bb, sb, dealer = movebutton([True, True, True, True, True, True], 0, 5, 4)
    if (bb != 1 or sb != 0 or dealer != 5):
        print('test2 failed')
    bb, sb, dealer = movebutton([True, True, True, True, True, True], 1, 0, 5)
    if (bb != 2 or sb != 1 or dealer != 0):
        print('test3 failed')
    bb, sb, dealer = movebutton([True, True, True, False, True, True], 2, 1, 0)
    if (bb != 4 or sb != 2 or dealer != 1):
        print('test4 failed')
    bb, sb, dealer = movebutton([True, True, False, True, True, True], 2, 1, 0)
    if (bb != 3 or sb != -1 or dealer != 1):
        print('test5 failed')
    bb, sb, dealer = movebutton([True, False, True, True, True, True], 2, 1, 0)
    if (bb != 3 or sb != 2 or dealer != 0):
        print('test6 failed')
    bb, sb, dealer = movebutton([True, False, False, False, True, False], 2, 1, 0)
    if (bb != 4 or sb != 0 or dealer != 0):
        print('test7 failed')
    bb, sb, dealer = movebutton([False, False, False, True, True, True], 2, 1, 0)
    if (bb != 3 or sb != -1 or dealer != 0):
        print('test8 failed')
    bb, sb, dealer = movebutton([False, False, True, True, True, True], 2, 1, 0)
    if (bb != 3 or sb != 2 or dealer != 0):
        print('test9 failed')
    bb, sb, dealer = movebutton([False, True, False, True, True, True], 2, 1, 0)
    if (bb != 3 or sb != -1 or dealer != 1):
        print('test10 failed')
    bb, sb, dealer = movebutton([False, True, True, True, True, True], 2, 1, 0)
    if (bb != 3 or sb != 2 or dealer != 1):
        print('test11 failed')
