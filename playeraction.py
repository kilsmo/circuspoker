def playeraction(action, amount, chipsleft, chipsinplay, lastraise, amounttocall):
    chipstotal = chipsinplay + chipsleft

    if action == 'fold':
        if chipsinplay < amounttocall:
            return { 'fold': True }
        return { 'fail': True }
    elif action == 'check':
        if chipsinplay != amounttocall:
            return { 'fail': True }
        return {}
    elif action == 'call':
        if chipsinplay >= amounttocall:
            return { 'fail': True }
        if amounttocall > chipstotal:
            return { 'chipsleft': 0, 'chipsinplay': chipstotal }
        return { 'chipsleft': chipstotal - amounttocall, 'chipsinplay': amounttocall }
    elif action == 'raise':
        if amount <= amounttocall:
            return { 'fail': True }
        if amount >= chipstotal:
            retval = {
                'chipsleft': 0,
                'chipsinplay': chipstotal,
                'amounttocall': chipstotal
            }
            if chipstotal >= amounttocall + lastraise:
                retval['lastraise'] = chipstotal - amounttocall
            return retval
        if amount < amounttocall + lastraise:
            return { 'fail': True }
        return {
            'chipsleft': chipstotal - amount,
            'chipsinplay': amount,
            'amounttocall': amount,
            'lastraise': amount - amounttocall
        }
    return { 'fail': True }

if __name__ == '__main__':
    action = playeraction('fold', -1, 10, 20, 10, 30)
    if not action['fold']:
        print('Test1 failed')
    action = playeraction('fold', -1, 10, 20, 10, 20)
    if not action['fail']:
        print('Test2 failed')
    action = playeraction('call', -1, 10, 20, 10, 20)
    if not action['fail']:
        print('Test3 failed')
    action = playeraction('call', -1, 10, 20, 10, 30)
    if action['chipsleft'] != 0 and action['chipsinplay'] != 30:
        print('Test4 failed')
    action = playeraction('call', -1, 5, 20, 10, 30)
    if action['chipsleft'] != 0 and action['chipsinplay'] != 25:
        print('Test5 failed')
    action = playeraction('call', -1, 20, 20, 10, 30)
    if action['chipsleft'] != 10 and action['chipsinplay'] != 30:
        print('Test6 failed')
    action = playeraction('check', -1, 20, 20, 10, 30)
    if not action['fail']:
        print('Test7 failed')
    action = playeraction('check', -1, 20, 20, 10, 30)
    if not action:
        print('Test8 failed')
    action = playeraction('raise', 30, 20, 20, 10, 30)
    if not action['fail']:
        print('Test9 failed')
    action = playeraction('raise', 30, 20, 20, 10, 25)
    if not action['fail']:
        print('Test10 failed')
    action = playeraction('raise', 40, 20, 20, 10, 25)
    if action['chipsleft'] != 0 or action['chipsinplay'] != 40 or action['amounttocall'] != 40 or action['lastraise'] != 15:
        print('Test11 failed')
    action = playeraction('raise', 40, 20, 20, 20, 25)
    if action['chipsleft'] != 0 or action['chipsinplay'] != 40 or action['amounttocall'] != 40 or 'lastraise' in action:
        print('Test12 failed')
    action = playeraction('raise', 30, 20, 20, 10, 20)
    if action['chipsleft'] != 10 or action['chipsinplay'] != 30 or action['amounttocall'] != 30 or action['lastraise'] != 10:
        print('Test13 failed')
    action = playeraction('raise', 30, 20, 20, 15, 20)
    if not action['fail']:
        print('Test14 failed')
