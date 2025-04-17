import Optimisers

class bot:                                          # a general class that all bots use
    def __init__(self,f):                           # f is a function of the hyperparameters and data that returns buy signals
        self.n = f.__code__.co_argcount - 1         # number of hyperparameters, used by optimisation algorithm
        self.f = f                                  

    def buySignals(self, hyperParameters, data):
        return self.f(hyperParameters, data)
        
    def TotalReturn(self, hyperParameters, data):
        pass


def CompositeFilter(p1, p2, data):                                # a function defined by each person for their bot
    prices = data['close'].values

    sma_low = wma(prices, p1, sma_filter(p1))
    sma_high = wma(prices, p2, sma_filter(p2))

    signal = np.where((sma_low - sma_high) > threshold, 1, 0)
    signal = np.where((sma_high - sma_low) > threshold, -1, signal)

    signals = np.diff(signal, prepend=0)
    return signals



GerardBot = bot(CompositeFilter) 

OptimalParams = Optimisers.ABC(GerardBot, data)


Score = GerardBot.TotalReturn(OptimalParams, data)