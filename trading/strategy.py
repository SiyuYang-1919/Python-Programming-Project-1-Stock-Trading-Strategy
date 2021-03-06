# References
# matplotlib.pyplot.subplots_adjust() used in Line 81, 171, and 296: Matplotlib documentation
# URL: https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.subplots_adjust.html
# Accessed on 5 Nov 2020.

# Functions to implement our trading strategy.
# Import modules will be used later
import numpy as np
import matplotlib.pyplot as plt
import trading.process as proc
import trading.indicators as indi

def random(stock_prices, period=7, amount=5000, fees=20, ledger='ledger_random.txt'):
    '''
    Randomly decide, every period, which stocks to purchase, do nothing, or sell (with equal probability).
    Spend a maximum of amount on every purchase. 
    Plot(s) of the stock prices of each stock and red markers to indicate when the operations(buy or sell) are conducted will be presented.
    All the transactions will be logged into a ledger file.

    Input:
        stock_prices (ndarray): the stock price data
        period (int, default 7): how often we buy/sell (days)
        amount (float, default 5000): how much we spend on each purchase
            (must cover fees)
        fees (float, default 20): transaction fees
        ledger (str): path to the ledger file

    Output: None
    '''
   # Set up the default_rng from Numpy
    rng = np.random.default_rng()

    # Create a portfolio on day 0
    # Invest amount equally between available stocks
    N = stock_prices.shape[1]
    portfolio = proc.create_portfolio([amount]*N, stock_prices, fees, ledger)
    
    # Find trading dates, starting from day 1 and ending on the day before the last day
    # We will sell all the shares on the last day anyway, so there is no point to conduct other operations on that day
    trading_days = []
    for dates in range(1, stock_prices.shape[0]-1):
        if dates % period == 0:
            trading_days.append(dates)

    # Create two arrays to store days when buy or sell is conducted, this step is mainly to prepare data for plot(s)     
    buy = np.zeros([len(trading_days),stock_prices.shape[1]])
    sell = np.zeros([len(trading_days), stock_prices.shape[1]]) 

    # Loop over each trading day that we found earlier
    for d in trading_days:
        # Loop over each stock
        for stock in range(stock_prices.shape[1]):
            # Here, we need to deal with the situation when share prices become NaN
            # The references and detailed explanation of np.isnan() are witten in indicators.py
            # Check if the share price of stock on day d is NaN or not, if not, then...
            if np.isnan(stock_prices[d, stock]) == False:
                # Randomly choose a strategy
                strategy = rng.choice(['buy','sell','wait'], p=[1/3, 1/3, 1/3])
                if strategy == 'buy':
                    # Put the trading date in the list, buy
                    buy[trading_days.index(d),stock] = d
                    # Log the transaction into ledger file
                    proc.buy(d, stock, amount, stock_prices, fees, portfolio, ledger)
                elif strategy == 'sell':
                    # Check if I have shares in this stock
                    if portfolio[stock] != 0:
                        sell[trading_days.index(d),stock] = d
                        proc.sell(d, stock, stock_prices, fees, portfolio, ledger)
                else:
                    None
            else:
                None

    # Create subplot(s), the number of plots is equal to the number of stocks and the size of the figure will chang accordingly
    fig, ax = plt.subplots(stock_prices.shape[1], 1, figsize=(20,5*N))
    # Adjust the height reserved for space between subplots
    # The function plt.subplots_adjust() used below is mainly to adjust the layout of subplots
    # Paramters: left/right/bottom/top(float): the left/right/bottom/top side of subplots in the figure;
                # wspace(float): the amount of width reserved for space between subplots, expressed as a fraction of the average axis width
                # hspace(float): the amount of height reserved for space between subplots, expressed as a fraction of the average axis height
    plt.subplots_adjust(hspace=0.5)
    # Prepare data for red markers in plot(s)
    for stock in range(stock_prices.shape[1]):
        # Choose data for a stock
        stock_price = stock_prices[:, stock]
        # Create lists to store data
        x_1 = []
        y_1 = []
        # Change the data type of numbers in buy to int as the number will be used as indexes later
        buy_new = [int(num) for num in buy[:, stock] if num]
        # Loop over elements in buy
        for x1 in buy_new:
            # If the element != 0, then put it in the x_1 list and get its corresponding share price
            if x1:
                y1 = stock_price[x1]
                x_1.append(x1)
                y_1.append(y1)
        # The same logic as the code above, except that we loop over the list, sell, this time
        x_2 = []
        y_2 = []
        sell_new = [int(num) for num in sell[:, stock] if num]
        for x2 in sell_new:
            if x2:
                y2 = stock_price[x2]
                x_2.append(x2)
                y_2.append(y2)
    
        # Make plot(s), we have to consider two conditions here
        # The first condition is when we need to plot data of several stocks
        if stock_prices.shape[1] != 1:
            ax[stock].plot(stock_price, label='stock price')
            ax[stock].scatter([x_1], [y_1], marker='^', c='r',label='buy' )
            ax[stock].scatter([x_2], [y_2], marker='v', c='r', label='sell')
            ax[stock].legend(loc='lower right', fontsize=10)
            ax[stock].set_xlabel('Day', fontsize=10)
            ax[stock].set_ylabel('Price', fontsize=10)
            ax[stock].set_title('Stock'+str(stock), fontsize=12)
        # The second condition is when we just have the data of one stock
        else:
            ax.plot(stock_price, label='stock price')
            ax.scatter([x_1], [y_1], marker='^', c='r',label='buy' )
            ax.scatter([x_2], [y_2], marker='v', c='r', label='sell')
            ax.legend(loc='lower right', fontsize=10)
            ax.set_xlabel('Day', fontsize=10)
            ax.set_ylabel('Price', fontsize=10)
            ax.set_title('Stock'+str(stock), fontsize=12)
    
    # Finally, we need to sell all the shares of stocks that we have on the last day
    # Loop over all the stocks
    for stock in range(stock_prices.shape[1]):
        # Check if we have shares in the stock and if the share price of the stock on the last day is NaN or not
        # If we have shares and the share price is not NaN, then we should sell all the shares, otherwise, do nothing
        if portfolio[stock] != 0 and np.isnan(stock_prices[stock_prices.shape[0]-1, stock]) == False:
            proc.sell(stock_prices.shape[0]-1, stock, stock_prices, fees, portfolio, ledger)
            # Plot red marker for the sell operaion on the last day
            # Check if the number of stocks as we did in the 'Make plot(s)' part
            if stock_prices.shape[1] != 1:
                ax[stock].scatter(stock_prices.shape[0]-1, stock_prices[stock_prices.shape[0]-1, stock], marker='v', c='r')
            else:
                ax.scatter(stock_prices.shape[0]-1, stock_prices[stock_prices.shape[0]-1, stock], marker='v', c='r')
        else:
            None

    return None


def crossing_averages(stock_prices, period_n=200, period_m=50, amount=5000, fees=20, ledger='ledger_crossing_averages.txt'):
    '''
    The function is to perform crossing average trading strategy.
    The basic idea is when FMA crosses the SMA from below, I will buy more shares of that specific stock;
    When FMA crosses the SMA from above, I will sell all shares of that stock if I have shares.
    
    Inputs:
         stock_prices(ndarray):the stock price data
         period_n(int, default 200): the period used in calculating SMA
         period_m(int, default 50): the period used in calculating FMA (period_n should always be larger than period_m)
         amount(float, default 5000): the amount that invested to buy shares every time (cover fees)
         fees(float, default 20): transaction fees
         ledger(str, default 'ledger_crossing_averages.txt'): the file recorded transactions
    
    Output: None
    '''
    # Create a portfolio on day 0
    # Invest amount equally between available stocks
    N = stock_prices.shape[1]
    portfolio = proc.create_portfolio([amount]*N, stock_prices, fees, ledger)

    # Create subplot(s), the number of plots is equal to the number of stocks and the size of the figure will chang accordingly
    fig, ax = plt.subplots(stock_prices.shape[1], 1, figsize=(20,5*N))
    # Adjust the height reserved for space between subplots
    plt.subplots_adjust(hspace=0.5)

    # Calculate 2 different moving averages
    # Loop over every stock
    for stock in range(stock_prices.shape[1]):
        stock_price = stock_prices[:,stock]
        # Compute SMA
        SMA = indi.moving_average(stock_price, n=period_n)
        # Compute FMA
        FMA = indi.moving_average(stock_price, n=period_m)
        # Calculate the differences between SMA and FMA
        # Here, I do not calculate the difference on the last day
        # Because no matter what happens, I will sell all the shares I have on the last day anyway
        diff = [FMA[i] - SMA[i] for i in range(len(FMA)-1)]
        diff = np.around(diff, 2)

        # Create two lists to store days when buy or sell is conducted, this step is mainly to prepare data for plot(s)
        buy = []
        sell = []
        # Calculate the products of each two consecutive elements in diff
        # Starting from day 50, because the moving averages on day 0 - day 49 will be the same
        for index in range(51, len(diff)):
            # Calculate the products of today's difference
            product = diff[index-1] * diff[index]
            # If product < 0, it actually means that there is a crossing point today
            if product < 0:
                # If so, it means that FMA crosses from below
                if diff[index-1] < 0:
                    buy.append(index)
                    proc.buy(index, stock, amount, stock_prices, fees, portfolio, ledger)
                # This means FMA crosses from above
                elif diff[index-1] > 0:
                    # Check if I have shares for this stock
                    if portfolio[stock] != 0:
                        sell.append(index)
                        proc.sell(index, stock, stock_prices, fees, portfolio, ledger)
            elif product == 0:
                if diff[index-1] == 0:
                    if diff[index] > 0:
                        buy.append(index)
                        proc.buy(index, stock, amount, stock_prices, fees, portfolio, ledger)
                    elif diff[index] < 0:
                        if portfolio[stock] != 0:
                            sell.append(index)
                            proc.sell(index, stock, stock_prices, fees, portfolio, ledger)  
        
        # Prepare data for red markers in plot(s)
        y_1 = []
        for x1 in buy:
            y1 = stock_price[x1]
            y_1.append(y1)
        
        y_2 = []
        for x2 in sell:
            y2 = stock_price[x2]
            y_2.append(y2)
        
        # Make plot(s)
        # If we have data of several stocks
        if stock_prices.shape[1] != 1:
            ax[stock].plot(stock_price, label='stock price')
            ax[stock].plot(SMA, label='SMA')
            ax[stock].plot(FMA, label='FMA')
            ax[stock].scatter([buy], [y_1], marker='^', c='r', label='buy')
            ax[stock].scatter([sell], [y_2], marker='v', c='r', label='sell')
            ax[stock].legend(loc='lower right', fontsize=10)
            ax[stock].set_xlabel('Day', fontsize=10)
            ax[stock].set_ylabel('Price', fontsize=10)
            ax[stock].set_title('Stock'+str(stock), fontsize=12)
        # If we only have data of one stock
        else:
            ax.plot(stock_price, label='stock price')
            ax.plot(SMA, label='SMA')
            ax.plot(FMA, label='FMA') 
            ax.scatter([buy], [y_1], marker='^', c='r', label='buy')
            ax.scatter([sell], [y_2], marker='v', c='r', label='sell')
            ax.legend(loc='lower right', fontsize=8)
            ax.set_xlabel('Day', fontsize=10)
            ax.set_ylabel('Price', fontsize=10)
            ax.set_title('Stock'+str(stock), fontsize=12)

    # Finally, we need to sell all the shares of stocks that we have on the last day
    # Loop over all the stocks
    for stock in range(stock_prices.shape[1]):
        # Check if we have shares in the stock and if the share price of the stock on the last day is NaN or not
        # If we have shares and the share price is not NaN, then we should sell all the shares, otherwise, do nothing
        if portfolio[stock] != 0 and np.isnan(stock_prices[stock_prices.shape[0]-1, stock]) == False:
            proc.sell(stock_prices.shape[0]-1, stock, stock_prices, fees, portfolio, ledger)
            # Plot red marker for the sell operaion on the last day
            if stock_prices.shape[1] != 1:
                ax[stock].scatter(stock_prices.shape[0]-1, stock_prices[stock_prices.shape[0]-1, stock], marker='v', c='r')
            else:
                ax.scatter(stock_prices.shape[0]-1, stock_prices[stock_prices.shape[0]-1, stock], marker='v', c='r')
    
    return None  


def momentum(stock_prices, T_over=0.75, T_under=0.25, period=7, days_wait=10, osc_type='stochastic', amount=5000, fees=20, ledger='ledger_momentum.txt'):
    '''
    This function is to perform momentum trading strategy using oscillators.
    The basic idea is that using oscillators to guess if the price of a share is currently overvalued or undervalued:
    When the oscillator is above a threshold(a number in 0.7~0.8), I will sell all my shares if I have any;
    When the oscillator is under a threshold(a number in 0.2~0.3), I will buy more shares.
    
    Inputs:
           stock_prices(ndarray):the stock price data
           T_over(int, default 0.75): a threshold (the higher one)
           T_under(int, default 0.25): a threshold (the lower one), T_over + T_under  = 1
           period(int, default 7): the period used in calculating oscillators
           days_wait(int, default 10): the number of days I will wait before operating
           osc_type(str, default 'stochastic'): the type of oscillator that will be used
           amount(float, default 5000): the amount that invested to buy shares every time (cover fees)
           fees(float, default 20): transaction fees
           ledger(str, default 'ledger_momentum.txt'): the file recorded transactions
    
    Output: None
    '''
    # Create a portfolio on day 0
    # Invest amount equally between available stocks
    N = stock_prices.shape[1]
    portfolio = proc.create_portfolio([amount]*N, stock_prices, fees, ledger)
    
    # Create subplot(s), the number of plots is equal to the number of stocks and the size of the figure will chang accordingly
    fig, ax = plt.subplots(stock_prices.shape[1], 1, figsize=(30,10*N))
    # Adjust the height reserved for space between subplots
    plt.subplots_adjust(hspace=0.5)

    # Calculate 2 different moving averages
    # Compute oscs
    for stock in range(stock_prices.shape[1]):
        stock_price = stock_prices[:,stock]
        # Calculate the indicators of the stock
        oscs = indi.oscillator(stock_price, period, osc_type)
        
        # Create two lists to store days when buy or sell is conducted, this step is mainly to prepare data for plot(s)
        buy = []
        sell = []

        # Wait until the oscillator has remained beyond a threshold for the past days_wait days (including today)
        # Loop over oscs, not including the first day_wait days
        for i in range(days_wait, len(oscs)):
            # This indicates that the price is overvalued
            # If all the share prices of these days > T_over, then we should sell them
            if sum(oscs[i-days_wait+1:i+1] > T_over) == days_wait:
                # Check if I have shares for this stock
                if portfolio[stock] != 0:
                    sell.append(i)
                    proc.sell(i, stock, stock_prices, fees, portfolio, ledger)
            # This indicates that the price is undervalued
            # If all the share prices of these days < T_over, then we should buy them
            elif sum(oscs[i-days_wait+1:i+1] < T_under) == days_wait:
                buy.append(i)
                proc.buy(i, stock, amount, stock_prices, fees, portfolio, ledger)
            else:
                None
        # Prepare data for red markers in plot(s)     
        y_1 = []
        for x1 in buy:
            y1 = stock_price[x1]
            y_1.append(y1)
    
        y_2 = []
        for x2 in sell:
            y2 = stock_price[x2]
            y_2.append(y2)
        
        # Make plot(s)
        # If we have data of several stocks
        if stock_prices.shape[1] != 1:
            ax[stock].plot(stock_price, label='stock price')
            ax[stock].scatter([buy], [y_1], marker='^', c='r', label='buy')
            ax[stock].scatter([sell], [y_2], marker='v', c='r', label='sell')
            ax2 = ax[stock].twinx()
            ax2.plot(oscs, 'c-.', label='oscs')
            ax[stock].legend(loc='lower left', fontsize=10)
            ax2.legend(loc='lower right', fontsize=10)
            ax[stock].set_xlabel('Day', fontsize=10)
            ax[stock].set_ylabel('Price', fontsize=10)
            ax2.set_ylabel('Oscs', fontsize=10)
            ax[stock].set_title('Stock'+str(stock), fontsize=12)
        # If we only have data of one stock
        else:
            ax.plot(stock_price, label='stock price')
            ax.scatter([buy], [y_1], marker='^', c='r',label='buy' )
            ax.scatter([sell], [y_2], marker='v', c='r', label='sell')
            ax2 = ax.twinx()
            ax2.plot(oscs, 'c-.', label='oscs')
            ax.legend(loc='lower left', fontsize=10)
            ax2.legend(loc='lower right', fontsize=10)
            ax.set_xlabel('Day', fontsize=10)
            ax.set_ylabel('Price', fontsize=10)
            ax2.set_ylabel('Oscs', fontsize=10)
            ax.set_title('Stock'+str(stock), fontsize=12)
        
    # Finally, we need to sell all the shares of stocks that we have on the last day
    # Loop over all the stocks
    for stock in range(stock_prices.shape[1]):
        # Check if we have shares in the stock and if the share price of the stock on the last day is NaN or not
        # If we have shares and the share price is not NaN, then we should sell all the shares, otherwise, do nothing
        if portfolio[stock] != 0 and np.isnan(stock_prices[stock_prices.shape[0]-1, stock]) == False:
            proc.sell(stock_prices.shape[0]-1, stock, stock_prices, fees, portfolio, ledger)
            # Plot red marker for the sell operaion on the last day
            if stock_prices.shape[1] != 1:
                ax[stock].scatter(stock_prices.shape[0]-1, stock_prices[stock_prices.shape[0]-1, stock], marker='v', c='r')
            else:
                ax.scatter(stock_prices.shape[0]-1, stock_prices[stock_prices.shape[0]-1, stock], marker='v', c='r')
    
    return None
