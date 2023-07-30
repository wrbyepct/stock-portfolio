import requests as r
from bs4 import BeautifulSoup
import sys
from error import BadSearchInputError
from dataclasses import dataclass

@dataclass
class Stock:
    ticker: str
    exchange: str
    quantity: int 

    def __post_init__(self):
        self.ticker = self.ticker.upper()
        self.exchange = self.exchange.upper()
        self.price = get_price(self.ticker, self.exchange)
        self.market_value = self.price * self.quantity  


@dataclass
class Portfolio:
    positions: list[Stock]
    def __post_init__(self):
        self.total = self._get_total(self.positions)
        self.positions = self._get_positions(self.positions)
        
        
    def _get_total(self, positions):
        total = sum([p.market_value for p in positions])
        return round(total, 2)
    
    
    def _get_positions(self, positions):
        tickers = [p.ticker for p in positions]
        exchanges = [p.exchange for p in positions]
        quantity = [p.quantity for p in positions]
        prices = ["{:.2f}".format(p.price) for p in positions]
        market_values = ["{:.2f}".format(p.market_value) for p in positions]
        
        allocs = [round(p.market_value / self.total * 100, 2) for p in positions]
        allocations = ["{:.2f}".format(alloc) for alloc in allocs]
        
        position_dict = {
            "Ticker": tickers, 
            "Exchange": exchanges,
            "Price": prices,
            "Quantity": quantity,
            "Market Value": market_values,
            "% Allocation": allocations
        }
            
        return position_dict
        
        
def get_soup(ticker, exchange):
    url = "https://www.google.com/finance/"
    params = f"quote/{ticker}:{exchange}"
        
    ## Request the website
    resp = r.get(url + params)
    
    ## Search for price text and convert it to usful float
    soup = BeautifulSoup(resp.content, "html.parser")
    
    ## Catch bad input: non-existing ticker or exchange
    try:
        could_not_find = soup.find('div', string="We couldn't find any match for your search.")
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
    bns = Stock('BNS', 'zzE', 100)
    googl = Stock('GOOGL', 'NASDAQ', 30)
    shop = Stock('SHOP', 'TSE', 10)
    msft = Stock('MSFT', 'NASDAQ', 2)

    positions = [
        bns,
        googl,
        shop,
        msft
    ]

    portfolio = Portfolio(positions)

    print(portfolio.positions)
    
