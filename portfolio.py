class Portfolio:
    def __init__(self, positions):
        self.total = self._get_total(positions)
        self.positions = self._get_positions(positions)
        
        
    def _get_total(self, positions):
        total = sum([p.market_value for p in positions])
        return round(total, 2)
    
    
    def _get_positions(self, positions):
        tickers = [p.stock.ticker for p in positions]
        exchanges = [p.stock.exchange for p in positions]
        quantity = [p.quantity for p in positions]
        prices = ["{:.2f}".format(p.stock.price) for p in positions]
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