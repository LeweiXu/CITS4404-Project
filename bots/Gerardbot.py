import Optimisers

class bot:                                                  # a general class that all bots use
    def __init__(self,f,bounds):                            # f is a function of the hyperparameters and data that returns buy signals
        self.n = f.__code__.co_argcount - 1                 # number of hyperparameters, used by optimisation algorithm
        self.f = f       
        self.bounds = bounds                           

    def buySignals(self, hyperParameters, data):
        return self.f(hyperParameters, data)
        
    def TotalReturn(self, hyperParameters, data): #Calculates the total return given hyperparameters and data
        signals = self.f(hyperParameters, data)
        pass


def CompositeFilter(p1, p2, data):                          # a function defined by each person for their bot, takes n hyper parameters and a data set, returns a list of buy signals
    prices = data['close'].values

    sma_low = wma(prices, p1, sma_filter(p1))
    sma_high = wma(prices, p2, sma_filter(p2))

    signal = np.where((sma_low - sma_high) > threshold, 1, 0)
    signal = np.where((sma_high - sma_low) > threshold, -1, signal)

    signals = np.diff(signal, prepend=0)
    return signals



GerardBot = bot(CompositeFilter, bounds) 

OptimalParams = Optimisers.ABC(GerardBot, data)             # Optimiser uses object.n to determine number of hyperparameters to optimise, bounds to determine their bounds and optimises based on the TotalReturn function


Score = GerardBot.TotalReturn(OptimalParams, data)