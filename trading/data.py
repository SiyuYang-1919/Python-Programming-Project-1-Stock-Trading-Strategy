# References
# numpy.ndarray.tolist() used in Line 181, 184, 212, 246, and 273: Numpy documentation
# URL: https://numpy.org/doc/stable/reference/generated/numpy.ndarray.tolist.html
# Accessed on 1 Nov 2020.

# numpy.delete() used in Line 191: Numpy documentation
# URL: https://numpy.org/doc/stable/reference/generated/numpy.delete.html
# Accessed on 1 Nov 2020.

# list.index() used in in Line 218, 248, and 275: Python documentation
# URL: https://docs.python.org/3/tutorial/datastructures.html
# Accessed on 1 Nov 2020.

# Revised and debugged version of the code
import numpy as np

def generate_stock_price(days, initial_price, volatility):
    '''
    The function is to generate daily closing share prices for a company,
    for each day within a given number of days.
    
    Input:
    days - an integer that represents the number of days;
    initial_price - an number that represents the initial price of the company's stock;
    volatility - a number that represents the volatility of standard deviation of the increments.
    
    Output:
    an array with the shape (days) contains the daily closing price for each day.
    '''
    # Set stock_prices to be a zero array with length days
    stock_prices = np.zeros(days)
    
    # Set stock_prices in row 0 to be initial_price
    stock_prices[0] = initial_price
    
    # Set total_drift to be a zero array with length days
    totalDrift = np.zeros(days)
    
    # Set up the default_rng from Numpy
    rng = np.random.default_rng()
    
    # Loop over a range(1, days)
    for day in range(1, days):
        # Get the random normal increment
        inc = rng.normal(0, volatility)
        # Add stock_prices[day-1] to inc to get NewPriceToday
        NewPriceToday = stock_prices[day-1]+inc

        # Check whether an event happens today 
        news_today = rng.choice([0,1], p = [0.99, 0.01])
        
        if news_today == 1:
            # Randomly choose the multiplier of volatility
            m = rng.normal(0,2)
            # Calculate the drift
            drift = m * volatility
            # Randomly choose the duration         
            duration = rng.integers(3,15)
            
            # Check if day+duration is greater than days
            if day+duration <= days:
                for i in range(day, day+duration):
                    # Add the values of drifts to corresponding elements in totalDrift
                    totalDrift[i] += drift
            else:
                for i in range(day, days):
                    totalDrift[i] += drift
        
        # Add drifts to NewPriceToday
        NewPriceToday += totalDrift[day]
        
        # Check NewPriceToday is lower or equal to 0 
        if NewPriceToday <=0:
            # Assign NaN to stock_prices[day]
            stock_prices[day] = np.nan
        else:
            # Assign the value of NewPriceToday to stock_prices[day]
            stock_prices[day] = NewPriceToday
    
    return stock_prices


def get_data(method='read', initial_price=None, volatility=None):
    '''
    Generates or reads simulation data for one or more stocks over 5 years,
    given their initial share price and volatility.
    
    Input:
        method (str): either 'generate' or 'read' (default 'read').
            If method is 'generate', use generate_stock_price() to generate
                the data from scratch.
            If method is 'read', use Numpy's loadtxt() to read the data
                from the file stock_data_5y.txt.
            
        initial_price (list): list of initial prices for each stock (default None)
            If method is 'generate', use these initial prices to generate the data.
            If method is 'read', choose the column in stock_data_5y.txt with the closest
                starting price to each value in the list, and display an appropriate message.
        
        volatility (list): list of volatilities for each stock (default None).
            If method is 'generate', use these volatilities to generate the data.
            If method is 'read', choose the column in stock_data_5y.txt with the closest
                volatility to each value in the list, and display an appropriate message.

        If no arguments are specified, read price data from the whole file.
        
    Output:
        sim_data (ndarray): NumPy array with N columns, containing the price data
            for the required N stocks each day over 5 years.
    
    Examples:
        Returns an array with 2 columns:
            >>> get_data(method='generate', initial_price=[150, 250], volatility=[1.8, 3.2])
            
        Displays a message and returns None:
            >>> get_data(method='generate', initial_price=[150, 200])
            Please specify the volatility for each stock.
            
        Displays a message and returns None:
            >>> get_data(method='generate', volatility=[3])
            Please specify the initial price for each stock.
        
        Returns an array with 2 columns and displays a message:
            >>> get_data(method='read', initial_price=[210, 58])
            Found data with initial prices [200, 50] and volatilities [1.5, 0.7].
        
        Returns an array with 1 column and displays a message:
            >>> get_data(volatility=[5.1])
            Found data with initial prices [850] and volatilities [5].
        
        If method is 'read' and both initial_price and volatility are specified,
        volatility will be ignored (a message is displayed to indicate this):
            >>> get_data(initial_price=[210, 58], volatility=[5, 7])
            Found data with initial prices [200, 50] and volatilities [1.5, 0.7].
            Input argument volatility ignored.
    
        No arguments specified, all default values, returns price data for all stocks in the file:
            >>> get_data()
    '''
    # Check if the argument method is assigned to 'generate'
    if method == 'generate':
        
        # Check if the argument volatility is assigned to any values
        if not volatility:
            print('Please specify the volatility for each stock.')
            return None     
            
        # Check if the argument initial_price is assigned to any values
        elif not initial_price:
            print('Please specify the initial price for each stock.')
            return None
        
        # Check if two lists have the same number of values
        elif len(initial_price) != len(volatility):
            print('The number of values in volatility and initial price should be the same.')
            return None
        
        # Pass the tests for inputs
        else:
            # Create an array to store data generated
            # There are 365*5 rows in sim_data, that is, 5 years' data
            N = len(initial_price)
            sim_data = np.zeros([365*5, N])
            
            # Loop over companies and store data generated by generate_stock_price()
            for i in range(N):
                sim_data[:, i] = generate_stock_price(365*5, initial_price[i], volatility[i])
                                                      
            return sim_data
    
    # If method is assigned to 'read'...
    if method == 'read':
        
        # Read the data file
        read_data = np.loadtxt('stock_data_5y.txt')
        # Get the data of initial prices of each company
        starting_price = read_data[1,:]
        # The function numpy.ndarray.tolist() is mainly used to convert an array to a list.
        # Parameters: None
        # Output: y(object/list of object...): a list(or list of lists) and all the values and the sequence of values in the array remain the same
        starting_price = starting_price.tolist()
        # Get the data of volatilities of each company
        volatilities = read_data[0,:]
        volatilities = volatilities.tolist()
        
        # Deleting the first row of data (volatilities) in read_data
        # The function numpy.delete() is mainly used to get an array with sub-arrays removed from the original array
        # Parameters: arr(array_like): the original array; obj(slice, int, or array of ints): the indices of rows or columns that we want to remove;
                    # axis(int): the axis along which to delete (row or column)
        # Output: out(ndarray): the new array with some rows or columns removed
        data = np.delete(read_data, 0, 0)
        
        # Create two lists to store data found closest to each value
        # in starting_price and volatilities
        initial_price_found = []
        volatility_found = []
           
        # Check if initial_price and volatility are assigned values
        if initial_price and volatility:
            
            # Create an array to store share price data
            N = len(initial_price)
            sim_data = np.zeros([365*5, N])
            # Loop over elements in initial_price
            for i in range(len(initial_price)):
                
                # The list, differences, contain differences between each element
                # in starting_price and the value, initial_price[i]
                differences = [elements - initial_price[i] for elements in starting_price]
                # Get an list contains the absolute values of elements in differences
                diff = np.absolute(differences)
                diff = diff.tolist()
                # Get the index of the smallest number in diff
                # The function list.index() is to return the index in the list of the first element equal to x
                # Paramters: x (an object): the given value; 
                   # start and end: the slice notation and are used to limit the search to a particular sequence of the list.
                # Output: an index (int)
                index = diff.index(min(diff))
                
                # Get the number with the samllest difference in starting_price
                p_found = starting_price[index]
                # Get the corresponding volatility in the same company
                v_found = volatilities[index]
                # Append data in the lists created at the beginning 
                initial_price_found.append(p_found)
                volatility_found.append(v_found)
                # Get corresponding share price data from data file
                sim_data[:, i] = data[:, index]
            
            print('Found data with initial prices '+str(initial_price_found)+' and volatilities '+str(volatility_found)+'.')
            print('Input argument volatility ignored.')
            return sim_data
        
        # Only initial_price is assigned to some values...
        # Codes are basically the same as the codes used under the first condition
        # So I omit comments in this part
        elif initial_price:
            
            N = len(initial_price)
            sim_data = np.zeros([365*5, N])
            
            for i in range(len(initial_price)):
                
                differences = [elements - initial_price[i] for elements in starting_price]
                diff = np.absolute(differences)
                diff = diff.tolist()
                
                index = diff.index(min(diff))
                p_found = starting_price[index]
                v_found = volatilities[index]
                
                initial_price_found.append(p_found)
                volatility_found.append(v_found)
                sim_data[:, i] = data[:, index]
            
            print('Found data with initial prices '+str(initial_price_found)+
                  ' and volatilities '+str(volatility_found)+'.')   
            return sim_data
        
        # Only volatility is assigned to some values
        # Codes are similar to the codes used under the first condition
        # So I just write comments for codes that are different
        elif volatility:
            # Get the length of volatility
            N = len(volatility)
            sim_data = np.zeros([365*5, N])
            
            for i in range(len(volatility)):
                # The list, differences, contain differences between each element
                # in volatilities and the value, volatility[i]
                differences = [elements - volatility[i] for elements in volatilities]
                diff = np.absolute(differences)
                diff = diff.tolist()
                
                index = diff.index(min(diff))
                p_found = starting_price[index]
                v_found = volatilities[index]
                
                initial_price_found.append(p_found)
                volatility_found.append(v_found)
                sim_data[:, i] = data[:, index]
            
            print('Found data with initial prices '+str(initial_price_found)+
                  ' and volatilities '+str(volatility_found)+'.')
            return sim_data
            
        else:
            return data