import itertools

def generatehandcombinations(privateCards, publicCards):
    return list(itertools.combinations(privateCards + publicCards, 5))

if __name__ == '__main__':
    print(generatehandcombinations([1, 2], [3, 4, 5, 6, 7]))
