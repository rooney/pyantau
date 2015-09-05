from collections import OrderedDict, deque

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
    tagged_words.reverse()
    tagged_words = [(word, tag) for word, tag in tagged_words if tag]
    commodities = deque()
    
    class tmp(object):
        name, price, amount = deque(), deque(), deque()
    
    def commit():
        print 'committing', tmp.name, tmp.price, tmp.amount
        if not tmp.amount and len(tmp.price) > 1:
            tmp.amount.append(tmp.price.pop())
        if tmp.amount:
            while tmp.amount[0] not in ('per', 'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh', 'delapan') and not tmp.amount[0].startswith('se') and tmp.price:
                tmp.amount.appendleft(tmp.price.pop())
                
        commodities.appendleft(Commodity(
            ' '.join(tmp.name), 
            ' '.join(tmp.price), 
            ' '.join(tmp.amount),
        ))
    
    cardinal_target = tmp.price
    last_target = None
    for word, tag in tagged_words:
        cardinal_target = {
            'NN' : tmp.price,
            'RP' : tmp.price,
            'DT' : tmp.price if word.startswith('se') else tmp.amount,
            'IN' : tmp.price,
            'CD' : cardinal_target,
        }[tag]
        def get_target():
            return {
                'NN' : tmp.name,
                'RP' : tmp.price,
                'IN' : tmp.amount,
                'DT' : tmp.amount,
                'CD' : cardinal_target,
            }[tag]
        
        target = get_target()
        print word, tag, ' '.join(target)
        if target:
            if (target != last_target and last_target is not None) or (target == tmp.amount and word.startswith('se')):
                commit()
                tmp.name, tmp.price, tmp.amount = deque(), deque(), deque()
                cardinal_target = tmp.price
        
        last_target = get_target()
        last_target.appendleft(word)            
                    
    if tmp.name or tmp.price or tmp.amount:
        commit()
        
    return commodities

