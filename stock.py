import requests as r
from bs4 import BeautifulSoup
import re
import json 
import os
import sys
from dotenv import load_dotenv, find_dotenv
from error import BadSearchInputError

_ = load_dotenv(find_dotenv())
API_KEY = os.environ.get("EXCHANGERATES_API_KEY")


class Stock:
    
    def __init__(self, ticker, exchange):
        self.ticker = ticker.upper()
        self.exchange = exchange.upper()
        self.price = self._get_price()
        
        
    def _get_soup(self):
        url = "https://www.google.com/finance/"
        params = f"quote/{self.ticker}:{self.exchange}"
            
        ## Request the website
        resp = r.get(url + params)
        
        ## Search for price text and convert it to usful float
        soup = BeautifulSoup(resp.content, "html.parser")
        
        ## Catch bad input: non-existing ticker or exchange
        try:
            could_not_find = soup.find('div', attrs={'class': 'b4EnYd'})
            if could_not_find is not None:
                raise BadSearchInputError
            else:
                return soup
                
        except BadSearchInputError as e:
            print(e.message)
            sys.exit()

    
    def _get_price(self):
        soup = self._get_soup()
        
        # Select the div that contains all of the data information instead of the randomly generated divs
        data_div = soup.select_one('div[data-last-price]')
        price = float(data_div.get('data-last-price'))
        currency = data_div.get('data-currency-code')
       
        ## If not USD convert it USD 
        if currency != "USD":
            price = self._convert(currency, price)

        return price
      
    
    def _convert(self, currency, price):
        ## We can get conversion rate at Google Finance
        url = "https://www.google.com/finance/"
        params = f"quote/{currency}-USD"
        resp = r.get(url+params)
        soup = BeautifulSoup(resp.content, "html.parser")

        data_div = soup.select_one('div[data-last-price]')
        rate = float(data_div.get('data-last-price'))
        USD = price * rate
        return USD


        # ## call exchange rate api 
        # base_endpoint = "http://api.exchangeratesapi.io/v1/latest"
        # params = {
        #     "access_key": API_KEY,
        # }
        # resp = r.get(base_endpoint, params=params)
        
        # ## Convert raw response to json
        # resp = json.loads(resp.content.decode())
        
        # ## Convert the rate
        # rates = resp['rates']
        # ## Because this endpoint only has EUR as the base 
        # ## So we need to convert it back to EUR and then convert it to target currency
        # USD = amount / rates[f'{currency}'] * rates['USD']
  
        return USD


if __name__ == '__main__':
    bns = Stock('BNS', "TSE")
    shop = Stock('SHOP', 'TSE')
    print(bns.price, shop.price)
   
    
