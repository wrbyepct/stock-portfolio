import requests as r
from bs4 import BeautifulSoup
import sys
from error import BadSearchInputError
from dataclasses import dataclass

@dataclass
class Stock:
    ticker: str
    exchange: str
    price: float = 0

  
    def __post_init__(self):
        self.ticker = self.ticker.upper()
        self.exchange = self.exchange.upper()
        self.price = get_price(self.ticker, self.exchange)
        
        
def get_soup(ticker, exchange):
    url = "https://www.google.com/finance/"
    params = f"quote/{ticker}:{exchange}"
        
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


def get_price(ticker, exchange):
    soup = get_soup(ticker, exchange)
    
    # Select the div that contains all of the data information instead of the randomly generated divs
    data_div = soup.select_one('div[data-last-price]')
    price = float(data_div.get('data-last-price'))
    currency = data_div.get('data-currency-code')
    
    ## If not USD convert it USD 
    if currency != "USD":
        price = convert(currency, price)

    return price
    

def convert(currency, price):
    ## We can get conversion rate at Google Finance
    url = "https://www.google.com/finance/"
    params = f"quote/{currency}-USD"
    resp = r.get(url+params)
    soup = BeautifulSoup(resp.content, "html.parser")

    data_div = soup.select_one('div[data-last-price]')
    rate = float(data_div.get('data-last-price'))
    USD = price * rate
    return USD



if __name__ == '__main__':
    bns = Stock('BNS', "TSE")
    shop = Stock('SHOP', 'TSE')
    print(bns.price, shop.price)
   
    
