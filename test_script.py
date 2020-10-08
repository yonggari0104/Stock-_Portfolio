#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 18:48:41 2020

@author: kibeomlee
"""

# Prototype

# Acquire Price Data
from DataManagement import DataManagement
data = DataManagement()
data.main()


# Portfolio Module
from Portfolio import Portfolio
myportfolio = {'TSLA': 2, 'MSFT': 3, 'SBUX': 8, 'DELL':8, 'AAPL': 3}
portfolio = Portfolio(myportfolio)
portfolio.main(data.tickdata)
