from tabulate import tabulate
import re

from stock import Stock
from position import Position
from portfolio import Portfolio
import error as e


def get_ticker_input(pattern):
    while True:
        # Catch bad ticker inputs
        try:
            ticker = input("Enter your Ticker: ")
            match = pattern.fullmatch(ticker)
            if match is not None:
                return ticker
            raise e.BadTickerInputError
        except e.BadTickerInputError as eb:
            print(eb.message)
    

def get_exchange_input(pattern):
    while True:
        # Catch bad Exchange inputs
        try:
            exchange = input("Enter your Exchange: ")
            match = pattern.fullmatch(exchange)
            if match is not None:
                return exchange
            raise e.BadExchangeInputError
        except e.BadExchangeInputError as eb:
            print(eb.message)


def get_quantity_input():
    while True:
        # Catch bad Quantity inputs
        try:
            quantity = float(input("Enter the quantity: "))
            # check invalid decimal number, can only be integer
            if quantity % 1 == 0 or quantity <= 0:
                quantity = int(quantity)
                return quantity
            raise e.BadQuantityInputError
        
        except e.BadQuantityInputError as eq:
            print(eq.message)

        except ValueError:
            print("Please enter only positive integer number.")


def get_position():
    pattern = re.compile("[a-zA-Z]+")
    ticker = get_ticker_input(pattern)
    exchange = get_exchange_input(pattern)
    quantity = get_quantity_input()

    print()
    print("Adding to your portfolio...")

    # Append valid stock to stock list
    stock = Stock(ticker, exchange)
    position = Position(stock, quantity)
    return position


def ask_for_adding_stocks():
   
    stocks = []
    while True:
        
        position = get_position()
        stocks.append(position)

        print()
        acceptable_answer = ["y", 'yes', 'yeah', 'n', 'no', 'nah']
        action = input("Keep adding stock to your portfolio? (y/n)").lower()
        print()
        try:
            if action not in acceptable_answer:
                raise e.BadActionAnswerInputError
            if action in acceptable_answer[-3:]:
                print("Preparing your portifolio, please wait for a few seconds...")
                break
        except e.BadActionAnswerInputError as ea:
            print(ea.message)

    return stocks

def display_portifolio(portfolio):
    data = portfolio.positions
    table = tabulate(
        data, headers="keys", 
        tablefmt="fancy_grid", 
        stralign="right", 
        colalign=("left", "left"), 
        disable_numparse=True
    )
    print(table)

    format_total_string = f"Total portfolio value: ${portfolio.total:,.2f}."
    print(format_total_string)


if __name__ == "__main__":
    positions = ask_for_adding_stocks()
    portfolio = Portfolio(positions)

    display_portifolio(portfolio)
    
        

    #     exchange = input("Enter the Exchange: ")
    #     quantity = input("Enter the Exchange: ")

        


    # bns = Stock('BNS', 'TSE')
    # googl = Stock('GOOGL', 'NASDAQ')
    # shop = Stock('SHOP', 'TSE')
    # msft = Stock('MSFT', 'NASDAQ')

    # positions = [
    #     Position(bns, 100),
    #     Position(googl, 30),
    #     Position(shop, 10),
    #     Position(msft, 2)
    # ]
    

