import re
from collections import OrderedDict

class Commodity(object):
    __slots__ = ('name', 'price', 'amount')
    def __init__(self, name, price, amount):
        self.name = name
        self.price = price
        self.amount = amount
    
    def serialize(self):
        return OrderedDict([
            ('name', self.name),
            ('amount', self.amount),
            ('price', self.price),
        ])

is_empty = lambda x: False if x else True

def classify(tagged_words):
    tagged_words = [(word, tag) for word, tag in tagged_words if tag]
    commodities = []
    
    class tmp:
        name, price, amount = [], [], []
        CD_target = 'amount'

        @staticmethod
        def commit(trigger):
            print 'committing', tmp.name, tmp.amount, tmp.price
            allprice_noamount = len(tmp.price) > 1 and not tmp.amount
            if allprice_noamount:
                tmp.amount.append(tmp.price.pop())
            elif len(tmp.price) == 1 and not tmp.amount and re.match(r'^[\d.]{3,}$', tmp.price[0]):
                number = tmp.price[0]
                amount = int(number[-2:])
                if amount > 0:
                    tmp.amount = [str(amount)]
                    tmp.price = [str(int(number) - amount)]
            
            if tmp.amount:
                while (
                    tmp.price
                    and not re.match(r'^[\d.]+$', tmp.amount[0])
                    and not tmp.amount[0].startswith('se') # sembilan sepuluh sebelas seratus seribu sejuta sebuah sekarung dst
                    and tmp.amount[0] not in ('per', 'untuk', 'setiap', 'satunya',
                        'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh', 'delapan') 
                ):
                    tmp.amount = [tmp.price.pop()] + tmp.amount

            if not tmp.price and len(tmp.amount) == 2 and re.match(r'^[\d.]{3,}$', tmp.amount[0]):
                number = tmp.amount[0]
                amount = int(number[-2:])
                if amount > 0:
                    tmp.amount = [str(amount), tmp.amount[1]]
                    tmp.price = [str(int(number) - amount)]

            if allprice_noamount:
                if len(tmp.amount) > len(tmp.price) or len(tmp.amount[0]) > len(tmp.price[0]):
                    tmp.amount, tmp.price = tmp.price, tmp.amount
            
            if not tmp.price and len(tmp.amount) == 2 and trigger == 'DT':
                return # abort
            
            commodities.append(Commodity(
                ' '.join(tmp.name), 
                ' '.join(tmp.price), 
                ' '.join(tmp.amount),
            ))
            tmp.name, tmp.price, tmp.amount = [], [], []
            tmp.CD_target = tmp.amount
        
    last_target = None
    for word, tag in tagged_words:
        tmp.CD_target = {
            'NN' : 'price',
            'RP' : 'amount',
            'DT' : 'price',
            'IN' : 'amount',
            'CD' : tmp.CD_target,
        }[tag]
        
        def get_target():
            return {
                'NN' : tmp.name,
                'RP' : tmp.price,
                'IN' : tmp.amount,
                'DT' : tmp.amount,
                'CD' : tmp.amount if tmp.CD_target == 'amount' else tmp.price,
            }[tag]
            
        if tag == 'IN' and tmp.amount and not tmp.price:
            tmp.price = tmp.amount
            tmp.amount = []
        
        if tag == 'DT' and (word.startswith('se') or word == 'satunya') and not tmp.price:
            tmp.price = tmp.amount
            tmp.amount = []
        
        target = get_target()
        if target and target != last_target and last_target is not None:
            tmp.commit(tag)

        last_target = get_target()
        last_target.append(word)
        print word, tag, ' '.join(last_target)

        if tag == 'DT' and tmp.name and tmp.price:
            tmp.commit(tag)
                            
    if tmp.name or tmp.price or tmp.amount:
        tmp.commit('FINAL')
        
    return commodities

