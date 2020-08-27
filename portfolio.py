import pandas as pd
from datetime import date
import pandas_datareader.data as web
import numpy as np
import matplotlib.pyplot as plt


#%%
# Date information

today = date.today()

d1 = today.strftime("%m%d") # dd/mm/YY

start = '2020-06-26'


#WATCHLIST
mylist = ['GS\n', 'MSFT\n', 'RY\n','SBUX\n', 'DELL\n']
myhold = [3, 3, 6, 8, 8]
mycur = ['CAD', 'CAD', 'CAD', 'USD', 'CAD']
myportfolio = {'Ticker': mylist, 'Hold': myhold, 'Currency': mycur}


def load_df(myportfolio, start_date):
    tickdata = []
    ticklist = []
    
    counter = 0
    for tick in myportfolio['Ticker']:
        tick = tick[:-1]
        try:
            temp = web.DataReader(tick, 'yahoo', start=start_date)[['Close']]
            tickdata.append(temp)
            ticklist.append(tick)
            counter += 1
            
            if counter % 20 == 0:
                print(counter)
                
        except:
            pass
        
    # Ticker Data
    tickdata = pd.concat(tickdata, axis = 1)
    tickdata.columns = ticklist
    
    # Currency
    curlist = list(set(myportfolio['Currency']).difference({"USD"}))
    for i in range(len(curlist)):
        curlist[i] = curlist[i] + "=X"
    currency =  web.DataReader(curlist, 'yahoo')['Close']
    currency.columns = curlist
    
    # concat
    temp_data = pd.concat([tickdata, currency], axis = 1).dropna()
    stock_data = temp_data[ticklist]
    currency_data = temp_data[curlist]
    
    # Transform in USD
    #curlist = myportfolio['Currency']
    for i in range(0, len(ticklist)):
        c =  myportfolio['Currency'][i]
        if c != 'USD':
            stock_data[ticklist[i]] = stock_data[ticklist[i]] * currency_data[myportfolio['Currency'][i]+'=X']
        else:
            pass
    
    # Calculate the return and portfolio return
    for i in range(0, len(ticklist)):
        stock_data[ticklist[i]] = stock_data[ticklist[i]] * myhold[i]
    
    stock_data['PORTFOLIO'] = stock_data.sum(1)
    ret_data = np.log(stock_data).diff().dropna()
    ret_data['PORTFOLIO'] = ret_data.sum(1)

    return {'Stock': stock_data, 'Currency': currency_data, 'Cumulative': np.cumsum(ret_data, axis = 0), 
            'Return': ret_data}


#GRAPH THE TICKS
data = load_df(myportfolio, start)

plt.figure(1)
plt.plot(data['Stock'])
plt.legend(data['Stock'].columns)


plt.figure(2)
plt.plot(data['Cumulative'])
plt.legend(data['Cumulative'].columns)


