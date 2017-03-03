def handstrength(hand):
    sortedhand = sorted(hand, key = lambda x: x[1], reverse = True)
    values = [x[1] for x in sortedhand]
    suites = [x[0] for x in sortedhand]
    return _handstrength(values, suites)

def _handstrength(values, suites):
    if _isFourOfAKind(values):
        return _getFourOfAKindValue(values)
    if _isFullHouse(values):
        return _getFullHouseValue(values)
    if _isThreeOfAKind(values):
        return _getThreeOfAKindValue(values)
    if _isTwoPair(values):
        return _getTwoPairValue(values)
    if _isPair(values):
        return _getPairValue(values)
    if _isStraightFlush(values, suites):
        return _getStraightFlushValue(values)
    if _isFlush(suites):
        return _getFlushValue(values)
    if _isStraight(values):
        return _getStraightValue(values)
    return _getHighCardValue(values)
    
def _isFourOfAKind(values):
    return values[0] == values[3] or values[1] == values[4]

def _isFullHouse(values):
    return (values[0] == values[2] and values[3] == values[4]) or (values[0] == values[1] and values[2] == values[4])

def _isThreeOfAKind(values):
    return values[0] == values[2] or values[1] == values[3] or values[2] == values[4]

def _isTwoPair(values):
    return ((values[0] == values[1] and values[2] == values[3]) or
            (values[1] == values[2] and values[3] == values[4]) or
            (values[0] == values[1] and values[3] == values[4]))

def _isPair(values):
    for i in range(4):
        if values[i] == values[i + 1]:
            return True
    return False

def _isStraightFlush(values, suites):
    return _isFlush(suites) and _isStraight(values)

def _isFlush(suites):
    return suites.count(suites[0]) == 5

def _isStraight(values):
    if values[0] == 14 and values[1] == 5:
        return True
    return values[0] == values[4] + 4

def _getStraightFlushValue(values):
    return _straightValue(values, 8)

def _getStraightValue(values):
    return _straightValue(values, 4)

def _straightValue(values, strength):
    if values[0] == 14 and values[1] == 5:
        return [strength, 5]
    return [strength, values[0]]

def _getHighCardValue(values):
    return _highCardValue(values, 0)

def _getFlushValue(values):
    return _highCardValue(values, 5)

def _highCardValue(values, strength):
    return [strength] + values

def _twoValues(values, strength):
    if values[0] == values[2]:
        return [strength, values[0], values[4]]
    return [strength, values[4], values[0]]

def _getFullHouseValue(values):
    return _twoValues(values, 6)

def _getFourOfAKindValue(values):
    return _twoValues(values, 7)

def _getThreeOfAKindValue(values):
    if values[0] == values[2]:
        return [3, values[0], values[3], values[4]]
    if values[1] == values[3]:
        return[3, values[1], values[0], values[4]]
    return [3, values[2], values[0], values[1]]

def _getTwoPairValue(values):
    if values[0] == values[1]:
        if values[2] == values[3]:
            return [2, values[0], values[2], values[4]]
        else:
            return [2, values[0], values[3], values[2]]
    return [2, values[1], values[3], values[0]]

def _getPairValue(values):
    if values[0] == values[1]:
        return [1, values[0], values[2], values[3], values[4]]
    if values[1] == values[2]:
        return [1, values[1], values[0], values[3], values[4]]
    if values[2] == values[3]:
        return [1, values[2], values[0], values[1], values[4]]
    return [1, values[3], values[0], values[1], values[2]]

if __name__ == '__main__':
    if handstrength([('h', 5), ('s', 5), ('s', 7), ('d', 7), ('c', 7)]) != [6, 7, 5]:
        print('test1 failed')
    if handstrength([('h', 7), ('s', 5), ('s', 7), ('d', 7), ('c', 7)]) != [7, 7, 5]:
        print('test2 failed')
    if handstrength([('h', 8), ('s', 5), ('s', 7), ('d', 5), ('c', 7)]) != [2, 7, 5, 8]:
        print('test3 failed')
    if handstrength([('h', 8), ('s', 7), ('s', 7), ('d', 5), ('c', 7)]) != [3, 7, 8, 5]:
        print('test4 failed')
    if handstrength([('h', 8), ('s', 7), ('s', 7), ('d', 5), ('c', 9)]) != [1, 7, 9, 8, 5]:
        print('test5 failed')
    if handstrength([('h', 8), ('s', 7), ('s', 6), ('d', 10), ('c', 9)]) != [4, 10]:
        print('test6 failed')
    if handstrength([('s', 8), ('s', 7), ('s', 6), ('s', 10), ('s', 9)]) != [8, 10]:
        print('test7 failed')
    if handstrength([('h', 8), ('s', 7), ('s', 11), ('d', 5), ('c', 9)]) != [0, 11, 9, 8, 7, 5]:
        print('test8 failed')
    if handstrength([('s', 8), ('s', 7), ('s', 11), ('s', 5), ('s', 9)]) != [5, 11, 9, 8, 7, 5]:
        print('test8 failed')
