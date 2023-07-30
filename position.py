class Position:
    def __init__(self, stock, quantity):
        self.stock = stock
        self.quantity = quantity
        self.market_value = stock.price * quantity
    