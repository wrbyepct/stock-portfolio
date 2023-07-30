class BadSearchInputError(Exception):
    def __init__(self, message="Ticker or Exchange does not exist, please check your input again."):
        self.message = message

class BadTickerInputError(Exception):
    def __init__(self, message="Bad Ticker name input. Please check again if your ticker name is corrct."):
        self.message = message

class BadExchangeInputError(Exception):
    def __init__(self, message="Bad Exchange name input. Please check again if your Exchange name is corrct."):
        self.message = message

class BadQuantityInputError(Exception):
    def __init__(self, message="Please enter only positive integer number."):
        self.message = message

class BadActionAnswerInputError(Exception):
    def __init__(self, message="Please enter only y(yes) or n(no)."):
        self.message = message