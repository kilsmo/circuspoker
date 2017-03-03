from deck import Deck
import playeraction
import nextplayertoact
import collectpot
import generatehandcombinations
import handstrength
import payout
import movebutton

_blinds = [
    (150, 300),
    (200, 400),
    (250, 500),
    (300, 600),
    (400, 800),
    (500, 1000),
    (600, 1200),
    (800, 1600),
    (1000, 2000),
    (1200, 2400),
    (1500, 3000),
    (2000, 4000),
    (2500, 5000),
    (3000, 6000)
]

class Game:
    def __init__(self):
        self.handnr = 0
        self.dealer = 5
        self.players = [
            { 'chips': 15000, 'name': 'Bamse' },
            { 'chips': 15000, 'name': 'Skalman' },
            { 'chips': 15000, 'name': 'Lille skutt' },
            { 'chips': 15000, 'name': 'Vargen' },
            { 'chips': 15000, 'name': 'Brummelisa' },
            { 'chips': 15000, 'name': 'Nallemaja' }
        ]
        self.sb = 0
        self.bb = 1
        self.sbsize, self.bbsize = self._getsbbb()        
    
    def start(self):
        self.hand = Hand(self.players, self.sb, self.bb, self.dealer, self.sbsize, self.bbsize)
        return self.gettabledata()
    
    def gettabledata(self):
        tabledata = self.hand.gettabledata()
        tabledata['sb'] = self.sbsize
        tabledata['bb'] = self.bbsize
        for i in range(len(tabledata['players'])):
            tabledata['players'][i]['name'] = self.players[i]['name']
        return tabledata

    def command(self, action, amount = 0):
        playeractiondata = self.hand.getplayeractiondata()
        ret = playeraction.playeraction(action,
                                        amount,
                                        playeractiondata['chipsleft'],
                                        playeractiondata['chipsinplay'],
                                        playeractiondata['lastraise'],
                                        playeractiondata['amounttocall'])
        if not 'fail' in ret:
            self.hand.updateplayeraction(ret)
            nextplayer = self.nextplayertoact()
            if nextplayer == -1:
                self.collectpot()
                if self.hand.morebettingrounds() and self.hand.hastwoactiveplayers():
                    self.hand.newbettinground()
                else:
                    if self.hand.hastwoplayerswithcards():
                        self.hand.dealmissingcards()
                    self.payout()
                    self.movebutton()
                    self.handnr += 1

        return self.gettabledata()

    def payout(self):
        players, tablecards = self.hand.getplayerandtablecards()
        strengths = []
        for player in players:
            if player:
                strengths.append(self.getbesthand(player, tablecards))
            else:
                strengths.append(False)
        pots = self.hand.getpots()
        payouts = payout.payout(strengths, pots)
        self.hand.updatepayouts(payouts)

    def movebutton(self):
        players, bb, sb, dealer = self.hand.getmovebuttondata()
        newbb, newsb, newdealer = movebutton.movebutton(players, bb, sb, dealer)
        self.hand.updatemovebutton(newbb, newsb, newdealer)
        if newdealer != -1:
            self.hand.newhand(newsb, newbb, newdealer, self.sbsize, self.bbsize)

    def getbesthand(self, privatecards, publiccards):
        combinations = generatehandcombinations.generatehandcombinations(privatecards, publiccards)
        besthand = handstrength.handstrength(combinations[0])
        for i in range(1, len(combinations)):
            strength = handstrength.handstrength(combinations[i])
            if strength > besthand:
                besthand = strength
        return besthand

    
    def collectpot(self):
        pots = collectpot.collectpot(self.hand.getplayers())
        self.hand.updateaftercollectpot(pots)

    def nextplayertoact(self):
        nextplayerdata = self.hand.getnextplayerdata()
        startbet = 0
        if nextplayerdata['firstbettinground']:
            startbet = self.bbsize
        nextplayer = nextplayertoact.nextplayertoact(nextplayerdata['players'],
                                                     nextplayerdata['bb'],
                                                     nextplayerdata['dealer'],
                                                     startbet,
                                                     nextplayerdata['amounttocall'],
                                                     nextplayerdata['currentplayer'])
        self.hand.updatecurrentplayer(nextplayer)
        return nextplayer

    def fold(self):
        return self.command('fold')

    def check(self):
        return self.command('check')
    
    def call(self):
        return self.command('call')

    def bet(self, amount):
        return self.command('raise', amount)

    def _getsbbb(self):
        idx = self.handnr // 6
        if idx >= 13:
            idx = 13
        return _blinds[idx]

class Hand:
    def __init__(self, players, sb, bb, dealer, sbsize, bbsize):
        self.players = []
        for player in players:
            self.players.append({ 'chipsleft': player['chips'], 'chipsinplay': 0 })
        self.newhand(sb, bb, dealer, sbsize, bbsize)

    def _nextplayer(self):
        nextplayer = self.bb + 1
        if nextplayer >= len(self.players):
            nextplayer = 0
        while True:
            if self.players[nextplayer]['chipsleft'] > 0:
                return nextplayer
            nextplayer += 1
            if nextplayer >= len(self.players):
                nextplayer = 0

    def newhand(self, sb, bb, dealer, sbsize, bbsize):
        self.tablecards = []
        self.pots = [{ 'chips': 0, 'players': [] }]
        self.dealer = dealer
        self.sb = sb
        self.bb = bb
        self.currentplayer = self._nextplayer()
        self.bbsize = bbsize
        self.amounttocall = bbsize
        self.lastraise = bbsize
        self.deck = Deck()
        for i in range(len(self.players)):
            chips = self.players[i]['chipsleft']
            chipsinplay = 0
            cards = []
            if chips > 0:
                cards.append(self.deck.dealcard())
                cards.append(self.deck.dealcard())
            if i == sb:
                if chips < sbsize:
                    chipsinplay = chips
                else:
                    chipsinplay = sbsize
            elif i == bb:
                if chips < bbsize:
                    chipsinplay = chips
                else:
                    chipsinplay = bbsize
            self.players[i] = { 'chipsleft': chips - chipsinplay, 'chipsinplay': chipsinplay, 'cards': cards }
    
    def morebettingrounds(self):
        return len(self.tablecards) < 5
    
    def hastwoactiveplayers(self):
        count = 0
        for player in self.players:
            if player['chipsleft'] > 0 and player['cards']:
                count += 1
        return count >= 2
    
    def hastwoplayerswithcards(self):
        count = 0
        for player in self.players:
            if player['cards']:
                count += 1
        return count >= 2
    
    def dealmissingcards(self):
        cardstodeal = 5 - len(self.tablecards)
        for i in range(cardstodeal):
            self.tablecards.append(self.deck.dealcard())

    def firstactiveplayer(self):
        idx = self.dealer
        idx += 1
        if idx >= len(self.players):
            idx = 0
        while idx != self.dealer:
            if self.players[idx]['chipsleft'] > 0 and self.players[idx]['cards']:
                return idx
            idx += 1
            if idx >= len(self.players):
                idx = 0
        return -1
            
    def newbettinground(self):
        cards = self.tablecards
        if len(cards) == 0:
            cards.append(self.deck.dealcard())
            cards.append(self.deck.dealcard())
            cards.append(self.deck.dealcard())
        else:
            cards.append(self.deck.dealcard())
        self.tablecards = cards
        if not self.hastwoactiveplayers():
            self.currentplayer = -1
        else:
            self.currentplayer = self.firstactiveplayer()
        self.amounttocall = 0
        self.lastraise = 0

    def getplayerandtablecards(self):
        players = []
        for player in self.players:
            if (player['cards']):
                players.append(player['cards'])
            else:
                players.append(False)
        return players, self.tablecards
    
    def getpots(self):
        return self.pots

    def getplayers(self):
        return self.players

    def getplayeractiondata(self):
        player = self.players[self.currentplayer]
        return {
            'chipsleft': player['chipsleft'],
            'chipsinplay': player['chipsinplay'],
            'lastraise': self.lastraise,
            'amounttocall': self.amounttocall
        }

    def gettabledata(self):
        players = []
        for i in range(len(self.players)):
            players.append({
                'chipsleft': self.players[i]['chipsleft'],
                'chipsinplay': self.players[i]['chipsinplay'],
                'cards': self.players[i]['cards']
            })
        return {
            'players': players,
            'currentplayer': self.currentplayer,
            'dealer': self.dealer,
            'tablecards': self.tablecards,
            'pots': self.pots
        }
    
    def getnextplayerdata(self):
        firstbettinground = len(self.tablecards) == 0
        players = []
        for player in self.players:
            if player['cards']:
                players.append([player['chipsleft'], player['chipsinplay']])
            else:
                players.append(False)
        return {
            'players': players,
            'dealer': self.dealer,
            'bb': self.bb,
            'amounttocall': self.amounttocall,
            'currentplayer': self.currentplayer,
            'firstbettinground': firstbettinground
        }
    
    def getmovebuttondata(self):
        players = []
        for player in self.players:
            if player['chipsleft'] > 0:
                players.append(True)
            else:
                players.append(False)
        return players, self.bb, self.sb, self.dealer

    def updateplayeraction(self, data):
        player = self.players[self.currentplayer]
        if 'fold' in data:
            player['cards'] = []
        if 'chipsleft' in data:
            player['chipsleft'] = data['chipsleft']
        if 'chipsinplay' in data:
            player['chipsinplay'] = data['chipsinplay']
        if 'amounttocall' in data:
            self.amounttocall = data['amounttocall']
        if 'lastraise' in data:
            self.lastraise = data['lastraise']
    
    def updatecurrentplayer(self, currentplayer):
        self.currentplayer = currentplayer
    
    def updateaftercollectpot(self, pots):
        for player in self.players:
            player['chipsinplay'] = 0
        self.pots[-1]['chips'] += pots[0]['chips']
        self.pots[-1]['players'] = pots[0]['players']
        for i in range(1, len(pots)):
            self.pots.append(pots[i])
    
    def updatemovebutton(self, bb, sb, dealer):
        self.bb = bb
        self.sb = sb
        self.dealer = dealer

    def updatepayouts(self, payouts):
        for i in range(len(payouts)):
            self.players[i]['chipsleft'] += payouts[i]
