# References
# numpy.argsort used in Line 54 and 101: Numpy documentation
# URL: https://numpy.org/doc/stable/reference/generated/numpy.argsort.html
# Accessed on 10 Nov 2020.

# defaultdict() used in Line 61 and 105: Python documentation
# URL: https://docs.python.org/3/library/collections.html#collections.defaultdict
# Accessed on 10 Nov 2020.

# list.set() used in Line 158: Python documentation
# URL: https://docs.python.org/3/tutorial/datastructures.html
# Accessed on 8 Nov 2020.

# list.count() used in Line 171: Python documentation
# URL: https://docs.python.org/3/tutorial/datastructures.html
# Accessed on 8 Nov 2020.

# dict.update() used in Line 171: Python documentation
# URL: https://docs.python.org/3/tutorial/datastructures.html
# Accessed on 8 Nov 2020.

# Evaluate performance.
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

def read_ledger(ledger_file):
    '''
    The function is to get useful data from ledger_file and calculate the the total number of transactions and overall profits.
    Also, a plot will be made to indicate the money that we have over time.

    Input:
        ledger_files(str): path to the ledger file
        Note: the ledger file should include data of several days' transactions. 
              If it only includes one day's data, there is no point to make a plot.
    
    Output: 
        total_transactions(int): total number of transactions performed
        final_profits(float): the final profit
    '''
    # Load data from the ledger_file
    # Here, I only read column1 and column5 (transaction days and amounts)
    data = np.loadtxt(fname = ledger_file, delimiter = ',', usecols = (1, 5))
    # Count the number of transactions
    total_transactions = data.shape[0]
    # Calculate the final profit
    final_profits = sum(data[:,1])
    
    # Sort transaction amounts by transaction days
    # numpy.argsort is mainly used to sort an array
    # Paramters: a(array_like): an array; axis(int): the axis to sort; kind(str): the kind of sorting algorithm, such as quicksort;
               # order: specified which fileds in an array to compare first, second...
    # Output: an array of indices of the original array already sorted
    sort = np.argsort(data[:,0])
    # Input the sorted indices to data to get a new array, data_sorted, which is sorted bythe first column
    data_sorted = data[sort]
    
    # Create a default dictionary
    # defaultdict() is mainly used to create a new dictionary. It provides a fast way to group a sequence of key-value pairs into a dictionary of lists.
    # Just as the code in the following two lines:
    d = defaultdict(list)
    for key, val in data_sorted:
        d[key].append(val)
    
    # Get the keys in the dictionary, that is, transaction days
    keys = list(d)
    # Set the initial money we have as 0
    amounts = [0]
    # Loop over keys in the dictionary and calculate the total money involved in the transactions on each day
    # And calculate the total amount money we have after each day's transactions
    for key in keys:
        total_amount = round(sum(d[key]) + amounts[-1], 2)
        amounts.append(total_amount)
    # The amount starts from 0, so we need to add a key(day) before day0 to make x and y have the same length
    keys.insert(0, 0)
    fig, ax = plt.subplots()
    ax.plot(keys, amounts)
    ax.set_xlabel('Day', fontsize=10)
    ax.set_ylabel('Amount of money', fontsize=10)
    ax.set_title('Total Amount of Money Over Time', fontsize=12)

    return total_transactions, round(final_profits, 2)


def overall_profits_eachStock(ledger_file):
    '''
    Reads useful information from ledger_file and calculates the final profits of each stock under the same trading strategy.

    Input:
        ledger_file(str): path to the ledger file
    
    Output: 
        final profits(list): a list of values of final profits for each stock
    '''
    # Calculate the final profit of each stock when the data of stock prices include several stocks
    # Similar steps to the function above
    # Load data from the ledger_file
    # Here, I only read column2 and column5 (transaction stocks and amounts)
    data = np.loadtxt(fname = ledger_file, delimiter = ',', usecols = (2, 5))
    # Sort data by stocks
    sort = np.argsort(data[:,0])
    data_sorted = data[sort]
    # keys: each stock
    # values: money involved in each transaction of each stock
    d = defaultdict(list)
    for key, val in data_sorted:
        d[key].append(val)
    
    final_profits = []
    for key in d.keys():
        # Calculate the final profit by summing up values of each key
        total_amount = sum(d[key])
        final_profits.append(round(total_amount, 2))

    return final_profits
        

def evaluate(stock_prices, ledger_files):
    '''
    This function is to evaluate the performance of each strategy. 
    By calculating how many times(and corresponding rates) the final profit of each stock under each strategy is greater than that of other strategies.

    Input:
        stock_prices(ndarray): the data of stock prices used
        ledger_files(list): a list of paths to the ledger files, each file contains transactions conducted by each strategy

    Output:
        dict(dictionary): a dictionary contains information about how many times each strategy wins other strategies
                          the format of output would be something like {0: 4, 1: 7, 2: 4, 3: 5...}, 0 represents the first ledger file in ledger_files (the list)
                          1 is the second ledger file...
        dict_ratio(dictionary): a dictionary contains information about the winning rates of each strategy
                                the format of output would be something like {0: 0.2, 1: 0.35, 2: 0.35, 3: 0.2...}
    '''
    # Create a list to store lists of final profits
    final_profits_data = []
    # Get data of final profits of each stock in each ledger file (under the each strategy)
    # Loop over each ledger (represents different strategy)
    for ledger in ledger_files:
        profits_data = overall_profits_eachStock(ledger)
        final_profits_data.append(profits_data)
    
    # Change the object type to numpy.ndarray
    final_profits_new = np.array(final_profits_data)
    # Create a list to store the 'winner' for each stock
    win = []
    # Loop over each stock
    for i in range(0, stock_prices.shape[1]):
        # Get the data of final profits of one stock under each strategy
        # Change the object type to list
        compare_profits = final_profits_new[:, i].tolist()
        # Get the index of the maximum final profit
        index = compare_profits.index(max(compare_profits))
        win.append(index)
    # Get unique values in the list win
    # The function list.set() is mainly to create a new list with unique values in the original list
    # Parameters: iterable: the original list
    # Output: an iterable with unordered unique values in the original iterable
    set_new = set(win)
    # Create an empty dictionary
    dict = {}
    # Loop over elements in the new list
    for num in set_new:
        # The function dict.update() is mainly used to update the dictionary with values (keys will be added 
        # to the updated dictionary automatically if they are not in the dictionary)
        # Parameters: another dictionary object or an iterable of key/value pairs (as tuples or other iterables of length two)
        # Output: an updated dictonary

        # The function list.count() is mainly to count how many times a certain elemant appears in a list
        # Parameters: x(an object): the given value;
        # Output: a number(int): the number of times x appears in the list
        dict.update({num: win.count(num)})
    
    # Create an empty dictionary to store winning rates
    dict_ratio = {}
    for num in set_new:
        # Calculate the ratio by dividing the total number of stocks and round the ratio to 2 decimals
        dict_ratio.update({num: round(win.count(num)/stock_prices.shape[1], 2)})
    
    return dict, dict_ratio