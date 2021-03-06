# References
# np.isnan(x) used in Line 39 and Line 102: Numpy documentation
# URL: https://numpy.org/doc/stable/reference/generated/numpy.isnan.html
# Accessed on 5 Nov 2020.

import numpy as np

def moving_average(stock_price, n=7, weights=[]):
    '''
    Calculates the n-day (possibly weighted) moving average for a given stock over time.

    Input:
        stock_price (ndarray): single column with the share prices over time for one stock,
            up to the current day.
        n (int, default 7): period of the moving average (in days).
        weights (list, default []): must be of length n if specified. Indicates the weights
            to use for the weighted average. If empty, return a non-weighted average.

    Output:
        ma (ndarray): the n-day (possibly weighted) moving average of the share price over time.
    '''
     # Create a list to store averages calculated later
    averages = []

    # The function np.isnan(x), in the following code, is cited from Numpy documentation (see more details in References)
    # This function is mainly used to check if the input x(array_like) is NaN(that is, np.nan)
    # Parameters: x(array_like); out(array where returns will be put); where(=True or False, if False, no changes will be made to the array,out)
    # Output: ndarray(True where the element in x is NaN) or bool(True if x is NaN, False if x is not NaN)
    # Get share prices which are not NaN 
    stock_price = np.array([x for x in stock_price if not np.isnan(x)])
    
    # Check if weights is empty, if it is empty, then we will just calculate the average of share prices
    if not weights:
        # Calculate n-day moving average of the share prices
        # For days before n, I will calculate the mean of share prices over past days
        # For example, on day2, the MA is the average of the share prices of day0-day2
        for i in range(0, n):
            average = np.mean(stock_price[0:i+1])
            averages.append(round(average,2))
        # Loop over the share price on each day since the n th day
        for i in range(n-1, len(stock_price)):
            # Calculate the mean of share prices over the past n days
            # Including today's closing share price
            average = np.mean(stock_price[i-n+1:i+1])
            averages.append(round(average,2))
    # If weights is not empty, then we will just calculate the average of share prices    
    if weights:
        # Calculate n-day weighted moving average of the share prices
        # For days before n, I will calculate the weighted average of share prices over past days
        # For example, on day1, the WMA is the weighted average of share prices of day0-day2
        # The weight used for day0 is weights[0], day1 is weights[1]...day n-1 is weights[n-1]
        for i in range(0, n):
            # Create a list to store weight_price, which is weights * prices
            weight_prices = []
            # Get the share prices of the stock beginning from day 0
            prices = stock_price[0:n]
            # Loop over days before i (including i)
            for m in range(0, i+1):
                # Change the object type to float
                weight_price = float(weights[m]*prices[m])
                weight_prices.append(weight_price)
            # Get the data of weights
            weights_new = weights[0:i+1] 
            average = sum(weight_prices) / sum(weights_new)
            averages.append(round(average,2))
                
        # Loop over the share price on each day since the n th day
        for i in range(n-1, len(stock_price)):
            # Create a list to store weight_price, which is weights * prices
            weight_prices = [0]*n
            # Get the data of share prices over the past n days, including today's
            prices = stock_price[i-n+1:i+1]
            # Loop over indexes in weights/weight_price/prices
            for m in range(0, n):
                # Calculate weighted values
                weight_prices[m] = float(weights[m]*prices[m])
            # Calculate the weighted average of these share prices
            average = sum(weight_prices) / sum(weights)
            averages.append(round(average,2))
    # Convert the object type to array
    averages = np.array(averages)
    return averages 


def oscillator(stock_price, n=7, osc_type='stochastic'):
    '''
    Calculates the level of the stochastic or RSI oscillator with a period of n days.

    Input:
        stock_price (ndarray): single column with the share prices over time for one stock,
            up to the current day.
        n (int, default 7): period of the moving average (in days).
        osc_type (str, default 'stochastic'): either 'stochastic' or 'RSI' to choose an oscillator.
    Output:
        osc (ndarray): the oscillator level with period $n$ for the stock over time.
    '''
    # Create an list to store oscillators
    # Suppose the first indicator is 0.0, as the oscillator on the first day literally can't be calculated in the normal way
    # So I just give it a number 0.0
    osc = [float(0)]
    # Get share prices which are not NaN, the function np.isnan() is already explained above :)
    stock_price = np.array([x for x in stock_price if not np.isnan(x)])

    # If the user chooses the stochastic oscillator, then...
    if osc_type == 'stochastic':
        # Loop over the share price on each day from day0 to day n-1
        # For days before n, the stochastic of each day is calculated in a similar way to how stochastic is normally calculated
        # The only difference is that the stock prices used are those of all past days
        # For example, to calculate the indicator of day 2, I will use prices on day0-day2
        for i in range(1, n-1):
            # Get the data of share prices over the past days, including today's
            prices = stock_price[0:i+1]
            # Find the highest and lowest prices over the past n days
            highest = np.max(prices)
            lowest = np.min(prices)
            # Calculate the difference between today's price and the lowest price
            # Here, we need to change the datatype a little bit as the object type of stock_price[i] is numpy.ndarray
            # Which can not be rounded by round()
            diff = float(stock_price[i]) - lowest
            # Calculate the difference between highest price and lowest price
            diff_max = highest - lowest
            # Calculate the ratio and put the ratio into the list, osc
            ratio = diff / diff_max
            osc.append(round(ratio,2))

        # Loop over the share price on each day since the n th day
        # The code is basically the same as the code used above, so I omit some comments
        for i in range(n-1, len(stock_price)):
            # Get the data of share prices over the past n days, including today's
            prices = stock_price[i-n+1:i+1]
            highest = np.max(prices)
            lowest = np.min(prices)
            diff = float(stock_price[i]) - lowest
            diff_max = highest - lowest
            ratio = diff / diff_max
            osc.append(round(ratio,2))
    
    elif osc_type == 'RSI':
        # Loop over the share price on each day from day 0 to day n-1
        # For days before n, the RSI of each day is calculated in a similar way to how RSI is normally calculated
        # The only difference is that the stock prices used are those of all past days
        # For example, to calculate the indicator of day 2, I will use prices on day0-day2
        for i in range(1, n-1):
            prices = stock_price[0:i+1]
        # Create two list to store positive price differences and negative
            pos_diffs = []
            neg_diffs = []
            # Loop over share prices starting from the second element in prices
            for m in range(1, i+1):
                # Calculate the diffrences between consecutive numbers
                diff = stock_price[m] - stock_price[m-1]
                # Check if the difference is positive
                if diff > 0:
                    pos_diffs.append(diff)
                elif diff < 0:
                    neg_diffs.append(diff)
                else:
                    None
            # Calculate RS and RSI
            # If neg_diffs is not empty, then...
            # Here it does not matter whether pos_diffs will be empty or not
            # Because RS will be 0.0 in that case and we can still calculate RSI
            if neg_diffs:
                RS = float(sum(pos_diffs) / sum(np.abs(neg_diffs)))
                RSI = 1 - (1 / (1 + RS))
            # If it is empty, then we can not compute RS
            # But RSI can be calculated directly without calculating RS in this case
            # And RSI will be 1.0 no matter what the number of sum(pos_diffs) is
            else:
                RSI = float(1)
            # Put RSI into the list, osc
            osc.append(round(RSI,2))
            
        # Loop over the share price on each day since the n th day
        for i in range(n-1, len(stock_price)):
            # Get the data of share prices over the past n days, including today's
            # The code is basically the same as the code used above, so I omit the comments
            prices = stock_price[i-n+1:i+1]
            pos_diffs = []
            neg_diffs = []
            for m in range(i-n+2, i+1):
                diff = stock_price[m] - stock_price[m-1]
                if diff > 0:
                    pos_diffs.append(diff)
                elif diff < 0:
                    neg_diffs.append(diff)
                else:
                    None
            if neg_diffs :
                RS = float(sum(pos_diffs) / sum(np.abs(neg_diffs)))
                RSI = 1 - (1 / (1 + RS))
            else:
                RSI = float(1)
            osc.append(round(RSI,2))
            
    else:
        print(' Something wrong with the osc_type, please choose again :( ')
    # Convert the list to an array
    osc = np.array(osc)
    return osc