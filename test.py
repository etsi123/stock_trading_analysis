#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 20:09:50 2023

@author: evan
"""

#import libraries
import pandas as pd
import numpy as np
import yfinance as yf
import datetime
from datetime import date, timedelta
from trading_strats import StockEvaluations
from tqdm import tqdm
import os
from ydata_profiling import ProfileReport
import seaborn as sns

stock = StockEvaluations(ticker='TSLA',num_days=20,num_chunks=2,percent_cutoff=-2)
stock.getStockData()
results = stock.simulateAvgDownStrat()