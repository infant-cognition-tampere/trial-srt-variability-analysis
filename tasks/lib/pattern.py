from .categorical import Categorical

class Pattern(object):

    def __init__(self):
        self.order1 = {}
        self.order0 = Categorical()
        self.previous = None

    def learn(self, event):

        self.order0.learn(event)

        if self.previous is not None:
            if self.previous 

        if event in self.condition:
            self.condition[event] = 1
        else:


    def prob(self, event, given=None):
        return self.prob(event)

    def mode(self):
        pass
