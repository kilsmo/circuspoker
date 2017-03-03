def _findwinners(players):
    best = -1
    winners = []
    for i in range(len(players)):
        if players[i]:
            if best == -1 or players[i] > best:
                best = players[i]
                winners = [i]
            elif players[i] == best:
                winners.append(i)
    return winners

def _splitpot(winners, pot):
    amount = pot // len(winners)
    winnings = [amount] * len(winners)
    winningsamount = amount * len(winners)
    for i in range(len(winnings)):
        if winningsamount >= amount:
            break
        winnings[i] += 1
        winningsamount += 1
    return winnings

def payout(players, pots):
    payouts = [0] * len(players)
    for pot in pots:
        if pot['chips'] > 0:
            winners = _findwinners(players)
            if (len(winners) > 0):
                winnings = _splitpot(winners, pot['chips'])
                for i in range(len(winners)):
                    payouts[winners[i]] += winnings[i]
                for allin in pot['players']:
                    players[allin] = False
    return payouts

if __name__ == '__main__':
    payouts = payout([False, [8, 13], [7, 14], False], [{ 'chips': 100, 'players': [] }])
    if payouts != [0, 100, 0, 0]:
        print('Test1 failed')
    payouts = payout([False, [8, 13], [7, 14], False], [{ 'chips': 100, 'players': [1] }, { 'chips': 50, 'players': [] }])
    if payouts != [0, 100, 50, 0]:
        print('Test2 failed')
    payouts = payout([False, [8, 13], [7, 14], [8, 13]], [{ 'chips': 100, 'players': [] }])
    if payouts != [0, 50, 0, 50]:
        print('Test3 failed')
