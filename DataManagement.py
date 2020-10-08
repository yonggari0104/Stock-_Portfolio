#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 16:54:50 2020

@author: kibeomlee
"""

# Download Price and Volume Data

import bs4 as bs
import datetime as dt
import os
import pandas_datareader.data as web
import pickle
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import date, datetime


class DataManagement(object):
    
    def __init__(self, startdate='2020/08/01'):
        
        self.today = date.today()
        self.today = self.today.strftime("%m%d")
        self.startdate = startdate
        
    def load_sp500_tickers(self):
        resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class': 'wikitable sortable'})
        self.tickers = []
        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[0].text
            ticker = ticker.split('\n')[0]
            self.tickers.append(ticker)
 
    def update_ticker(self, tickerlist):
         self.tickers = list( set(self.tickers).union(set(tickerlist)))

    def load_data(self):
        self.tickdata = []
        self.ticklist = []
    
        counter = 0
        for tick in self.tickers:
            try:
                temp = web.DataReader(tick, 'yahoo', start=self.startdate)[['Close']]
                
                self.tickdata.append(temp)
                self.ticklist.append(tick)
                counter += 1
                
                if counter % 50 == 0:
                    print(counter)
                    
            except:
                pass
        

        print('Download Done.')
        
    def modify_frame(self):
        self.tickdata = pd.concat(self.tickdata, axis = 1)
        self.tickdata.columns = self.ticklist
        
        
    def observation_thres(self, nthreshold, frame):
        omitted_list = []
        for col in frame.columns:
            if len(frame[col]) < nthreshold:
                omitted_list.append(col)
            
        print('The following names are excluded due to lack of observations')
        print(col)
        
        return frame[list(set(frame.columns).difference(set(omitted_list)))]
        
        

    def main(self, tickerlist = ['TSLA']):
        
        self.load_sp500_tickers()
        
        if len(tickerlist) > 0:
            self.update_ticker(tickerlist)
            
        self.load_data()
        
        self.modify_frame()
    
