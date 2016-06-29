# -*- coding: utf-8 -*-
'''
Usage:

> c = Categorical()
> c.learn('1')
> c.mode()
'1'
> c.learn('2')
> c.prob('1')
0.5
> c.nmode(2)
['1', '2']
'''

class CategoricalPredictor(object):

    def __init__(self):
        self.dist = Categorical()

    def perceive(self, percept):
        self.dist.learn(percept)

    def predict(self):
        return self.dist.mode()


class Categorical(object):

    def __init__(self):
        # Mapping from category to number of occurrences
        self.dist = {}
        # Total number of occurrences
        self.n = 0

    def learn(self, category):
        if category in self.dist:
            self.dist[category] += 1
        else:
            self.dist[category] = 1
        self.n += 1

    def prob(self, category):
        '''Return float, the probability of the category'''
        if category in self.dist:
            return self.dist[category] / float(self.n)
        else:
            return 0.0

    def mode(self):
        '''
        Return the category with the highest probability.
        Return None if no categories learnt yet.
        '''
        max_cat = None
        max_n = 0
        for cat, n in self.dist.items():
            if n > max_n:
                max_cat = cat
        return max_cat

    def nmode(self, n):
        '''
        Return n categories with the highest probability.
        Return [] if no categories learnt yet.
        For categories with equal probability, order is not defined.

        >>> c = Categorical()
        >>> c.learn('a')
        >>> c.learn('b')
        >>> c.learn('a')
        >>> c.nmode(1)
        ['a']
        >>> c.nmode(2)
        ['a', 'b']
        >>> c.nmode(0)
        []
        >>> c.nmode(3)
        ['a', 'b']
        '''
        cats = self.dist.items()
        sorted_cats = sorted(cats, key=lambda x: x[1], reverse=True)
        head = sorted_cats[0:min(n,len(cats))]
        return list(map(lambda x: x[0], head))

    def num_cats(self):
        '''
        >>> c = Categorical()
        >>> c.num_cats()
        0
        >>> c.learn('a')
        >>> c.num_cats()
        1
        '''
        return len(self.dist)
