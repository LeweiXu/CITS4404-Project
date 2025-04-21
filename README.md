# CITS4404-Project

## A Trading Bot Optimization Algorithm

1. **Dataset**: [BTC/USD Dataset](https://www.kaggle.com/datasets/prasoonkottarathil/btcinusd)

2. **Background**:  
    After a nice conversation with gupta, I realized that many of you may not have a coding background and/or y'all are busy with other assignments. Therefore, I have tried to abstract this project as much as possible so that all you have to do now is implement a bot in the `bots/` folder. I have created an example bot, take a look at how its done and should be able to follow the same format. Of course, if someone could look over all my code and check against the project description that would be great.

    Everything below this is basically a draft for the report introduction.

3. **Documentation**:  
    - The ultimate goal of this project is to optimize hyperparameters using an algorithm. The number of hyperparameters may vary depending on the type of filters used (the type of filter itself may also be a hyperparameter).  
    - Datasets are located in the `data/` folder. You can choose which dataset to use. The datasets are separated into daily and hourly data, categorized as before 2020 and after 2020. Please use the datasets for before 2020 as specified in the project.
    - A function in `utils.data_loader` reads the CSV files. It accepts arguments to customize how the files are read. Refer to the documentation for details.
    - Basic filters are defined in `filters.wma`. Refer to the documentation for more information.
    - Run `bots_tester.py` when your bot is ready to compare with other bots. The function in `bots_tester.py` uses 2020 and 2021 data to evaluate the bots, DO NOT use these 2 datasets when training your bot (as per the project guidelines).

4. **The `bot` class**:
    - A bot can be defined as an object that takes *n* hyperparameters and outputs a *fitness* value. 
    - In order to achieve this, we can create a bot class that contains a general `fitness()` function that takes an array of signals and a corresponding array of BTC/USDT conversion rates.
        - Note that there is a small quirk in this function as it allows for consecutive buy/sell signals e.g [1, 1, 1, 0, 0, -1, -1]. In this situation, the simulation will try to buy but will have no cash after the 1st buy signal, so the second and third buy signals will be ignored (treated as a 0/hold signal), same goes for the second sell signal in which it will have no btc to sell.
    - We can then extend this bot class (inheritance) into individual bots in which we define a `generate_signals()` function that uses a *trading strategy* and its hyperparameters to generate an array of trading signals. 
        - The hyperparameters are stored internally in the bot object.
        - We also need to define the *bounds* of the hyperparameters. To do this, each bound can be defined as a `2-tuple` to indicate a continuous variable or as a `list` to indicate a discrete variable.
    - To optimise a bot, we can create an instance of the bot class and pass it to a optimisation function that will modify the internal hyperparameters of the bot object and use the inbuilt `fitness` function to achieve this.

5. **Goal** i.e. tasks:
    - **Each group member**: extend the `bot` class in bots/bot_base.py, define a trading strategy in `generate_signals()` method and define the bounds of the hyperparameters in the class.
    - Anyone that wishes to (may be necessary for completing your bot)
        - Create a generalised optimisation function that can optimise a bot of *n* hyperparameters
        - Implement some custom filters and MACD filters.
        - Use matplotlib to generate some plots with buy/sell signals marked for each bot
        - Start writing the report or draft of report

6. **Other Notes**:  
    - Use `test.py` if you wish to test your bot outside of the leaderboard functionality.
    - The **design** of the bot itself may become a parameter (e.g. choice between ema and lma for the higher frequency moving average).
    - There are 5 values for each datapoint (OHLCV). The `leaderboards.py` will use the closing value for the fitness evaluation (and your optimiser should use this value as the fitness evaluation as well, see point #10 for more justification), however your optimizer may use OHL & V values to optimise (maybe theres a correlation between OHL & V and C)
    - There are many more **trading strategies** than the one mentioned in the project report:
        1. **Moving Average Crossover** – Buy when a short-term moving average crosses above a long-term one, and sell when it crosses below.
        2. **MACD Strategy** – Trade based on the crossover between the MACD line (difference of two EMAs) and its signal line.
        3. **Zero-Crossing Strategy** – Buy when the difference between short and long moving averages crosses above zero, and sell when it crosses below.
        4. **Slope-Based Strategy** – Enter trades when the slope of a moving average turns positive (buy) or negative (sell).
        5. **Filter Combo Strategy** – Combine multiple types of moving averages with weights and trade based on their aggregated signal.
        6. **Bollinger Band Bounce** – Buy when the price hits the lower Bollinger Band and rebounds, sell when it hits the upper band.
        7. **Volatility Breakout Strategy** – Buy when price breaks above a recent high during high volatility, sell when it breaks below a recent low.
        8. **Mean Reversion Strategy** – Trade on the assumption that the price will revert back to the mean when it deviates significantly.
        9. **Chop Filter Strategy** – Avoid trades in low-volatility, sideways markets by using a volatility or momentum threshold.
        10. **Confidence Threshold Strategy** – Only execute trades when the signal strength (like MA difference) exceeds a minimum threshold.
        11. **Multi-Timescale Strategy** – Combine signals from different timescales (e.g., hourly and daily) and trade only when both agree.

7. **Algorithms to Implement** (choose from these if you wish):
    - CCS
    - CCS with "Acceleration Step"
    - Powell's Method
    - Hook-Jeeves
    - GPS
    - Nelder-Mead Simplex
    - Steepest Ascent Hill Climbing
    - Steepest Ascent Hill Climbing with Replacement
    - Hill Climbing with Restarts
    - Simulated Annealing
    - Tabu Search
    - ILS
    - ABC
    - PSO
    - BFO
    - GWO
    - ACO
    - WOA

8. **Possible Hyperparameters**:  
    - `N_short`: Short MA window  
    - `N_long`: Long MA window  
    - `filter_type_short`: Type of filter for short MA (e.g., 0 = SMA, 1 = EMA, 2 = LMA)  
    - `filter_type_long`: Type of filter for long MA  
    - `alpha_short`: EMA decay for short MA (if used)  
    - `alpha_long`: EMA decay for long MA (if used)  
    - `threshold`: Optional crossover margin  
    - `smooth_window`: Optional signal smoothing  
    - `rebuy_delay`: Delay between trades  
    - `hold_threshold`: Minimum price drop to trigger a sell

9. **Nerd stuff if you want to check my code and assumptions**
    - Determining which value to use for buy/sell:
        - Each row in the dataset has 5 values: open, high, low, close & volume. We cannot use high or low as the exchange rate as we simply do not know at what time this occured during the day (or during the minute/hour depending on the dataset).
        - Open and close are basically the same thing, e.g. the closing exchange rate on the 16/04 is usually almost the same as the opening exchange rate on the 17/04.
        - However, it wouldn't make sense to use the opening value, as that is the exchange rate at 00:00:00 at the start of the day, when would we make the trade?
        - With the closing value, we assume that we make the trade 1 second before midnight (or as close to midnight as possible)
        - And of course volume is just the sum of the trades that happened in that time frame, it is not an exchange rate.
    - When running the optimizer: although it may seem like we are giving the bot the entire dataset, when running the optimiser to generate buy/sell signals, the algorithm has no info on future exchange rates (its a for/while loop), it is trying to predict if the exchange rate will go up or go down and buy/sell accordingly.
    - When we have an array of buy/sell/hold signals of the same length as the datapoints, we assume that the bot can only make the same number of actions as the length of the datasets.
        - E.g. the 2020 dataset with 366 days/datapoints. At each day right before midnight, the bot chooses if it will buy, sell or hold. It would not make sense to have buy/sell signals of greater length than 366, as 1. how would the signals align and 2. we would not make 2 actions in one day (how can we buy and sell on the same day, we only know the closing/opening exchange rate at midnight, and if we buy/sell at the same time its the same as holding)
        - This applies to all the datasets of different time frames, e.g. the hourly dataset contains 24 x 365 = 8760 datapoints, hence at the end of each hour we decide if we want to buy/sell/hold.