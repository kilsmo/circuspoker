def collectpot(players):
    arr = []
    for i in range(len(players)):
        player = players[i]
        arr.append({ 'chipsleft': player['chipsleft'], 'chipsinplay': player['chipsinplay'], 'idx': i })
    arr = sorted(arr, key = lambda x: x['chipsinplay'])
    pots = [{ 'chips': 0, 'players': [] }]
    for i in range(len(arr)):
        player = arr[i]
        if player['chipsleft'] == 0 and player['chipsinplay'] > 0:
            chipsmax = player['chipsinplay']
            chips = 0
            for j in range(len(arr)):
                playerj = arr[j]
                if playerj['chipsleft'] == 0 and playerj['chipsinplay'] == chipsmax:
                    pots[-1]['players'].append(playerj['idx'])
                if playerj['chipsinplay'] >= chipsmax:
                    chips += chipsmax
                    playerj['chipsinplay'] = playerj['chipsinplay'] - chipsmax
                else:
                    chips += playerj['chipsinplay']
                    playerj['chipsinplay'] = 0
            pots[-1]['chips'] = chips
            pots.append({ 'chips': 0, 'players': [] })
    chips = 0
    for i in range(len(arr)):
        chips += arr[i]['chipsinplay']
    pots[-1]['chips'] = chips
    return pots

if __name__ == '__main__':
    pots = collectpot([{ 'chipsleft': 20, 'chipsinplay': 20 }, { 'chipsleft': 20, 'chipsinplay': 40 }, { 'chipsleft': 20, 'chipsinplay': 40 },
                       { 'chipsleft': 20, 'chipsinplay': 40 }, { 'chipsleft': 20, 'chipsinplay': 0 }, { 'chipsleft': 20, 'chipsinplay': 0 }])
    if len(pots) != 1 or pots[0]['chips'] != 140 or len(pots[0]['players']) != 0:
        print('Test1 fail')
    pots = collectpot([{ 'chipsleft': 0, 'chipsinplay': 20 }, { 'chipsleft': 20, 'chipsinplay': 40 }, { 'chipsleft': 20, 'chipsinplay': 40 },
                       { 'chipsleft': 20, 'chipsinplay': 40 }, { 'chipsleft': 20, 'chipsinplay': 0 }, { 'chipsleft': 20, 'chipsinplay': 0 }])
    if len(pots) != 2 or pots[0]['chips'] != 80 or pots[1]['chips'] != 60 or len(pots[0]['players']) != 1 or pots[0]['players'][0] != 0:
        print('Test2 fail')
    pots = collectpot([{ 'chipsleft': 0, 'chipsinplay': 20 }, { 'chipsleft': 0, 'chipsinplay': 40 }, { 'chipsleft': 20, 'chipsinplay': 40 },
                       { 'chipsleft': 20, 'chipsinplay': 40 }, { 'chipsleft': 20, 'chipsinplay': 0 }, { 'chipsleft': 20, 'chipsinplay': 0 }])
    if (len(pots) != 3 or pots[0]['chips'] != 80 or pots[1]['chips'] != 60 or pots[2]['chips'] != 0 or
        len(pots[0]['players']) != 1 or pots[0]['players'][0] != 0 or len(pots[1]['players']) != 1 or pots[1]['players'][0] != 1):
        print('Test3 fail')
