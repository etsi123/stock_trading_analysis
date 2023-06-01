#Construct a class to simulate an average down strategy. 
import pandas as pd
import numpy as np
import yfinance as yf
import datetime
from datetime import date, timedelta

class stock_data:
    def __init__(self,ticker,num_days,num_chunks,percent_cutoff): 
        self.ticker = ticker
        self.num_days = num_days
        self.num_chunks = num_chunks
        self.percent_cutoff = percent_cutoff
    def get_stock_data(self): 
        """
        Retrieve the stock data for ticker over the specified date range. 
        """
        today = date.today()
        d1 = today.strftime("%Y-%m-%d")
        end_date = d1
        d2 = date.today() - timedelta(days=self.num_days)
        d2 = d2.strftime("%Y-%m-%d")
        start_date = d2

        data = yf.download(self.ticker,start=start_date,end=end_date, progress=False).reset_index()
        data['percent_change'] = (data['Close']-data['Open'])/data['Close']*100    
        self.data = data
        return self.data
    def simulate_avg_down_strategy(self): 
        """
        Code to simulate my average down strategy. 
        """
        total_investable_amount_og = 10000 #Compute a basis amount, everything normalized by this number. 
        total_investable_amount = total_investable_amount_og
        num_chunks = self.num_chunks
        dollar_chunks = total_investable_amount / num_chunks
        total_investable_amount = total_investable_amount - dollar_chunks 

        percent_change_list = self.data.percent_change.tolist()
        close_list = self.data.Close.tolist()
        open_list = self.data.Open.tolist()

        initial_price = close_list.pop(0)
        initial_num_stocks = dollar_chunks / initial_price
        avg_price = initial_price
        num_stocks = initial_num_stocks
        percent_change_list.pop(0)
        open_list.pop(0)
        
        for i in range(0,len(percent_change_list)): 
            #Market Opens
            if avg_price >= open_list[i] and num_stocks > initial_num_stocks: 
                total_investable_amount = total_investable_amount + (num_stocks - initial_num_stocks)*(avg_price)
                num_stocks = initial_num_stocks
            #Market Closes    
            percent_change = percent_change_list[i]
            #Sell at break even. 
            if percent_change < self.percent_cutoff and close_list[i] < avg_price and total_investable_amount >= total_investable_amount_og/num_chunks: 
                purchase_price = close_list[i]
                num_purchased_today = dollar_chunks / purchase_price
                total_investable_amount = total_investable_amount - dollar_chunks
                avg_price = (num_stocks*avg_price + num_purchased_today*purchase_price) / (num_stocks + num_purchased_today)
                num_stocks = num_stocks + num_purchased_today


        profit_dollar = num_stocks*(close_list[-1]-avg_price)
        profit_percentage = np.round(profit_dollar / total_investable_amount_og *100,2)

        strategy_percent_increase = (total_investable_amount + num_stocks* close_list[-1] - total_investable_amount_og)*100/total_investable_amount_og
        strategy_percent_increase = np.round(strategy_percent_increase,2)
        buy_and_hold_increase = np.round(((close_list[-1] - initial_price)/initial_price)*100,2)

        #Summarize results. 
        print('For ticker ' + str(self.ticker) + ' and duration = ' + str(self.num_days) + ' days:')
        print('My strat. yields a ' + str(strategy_percent_increase) + ' % increase. ')
        print('Buy and hold yields a ' + str(buy_and_hold_increase) + str(' % increase')) 

        return [self.ticker,self.num_days,self.num_chunks,self.percent_cutoff,strategy_percent_increase,buy_and_hold_increase]
