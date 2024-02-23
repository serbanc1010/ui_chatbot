import json

class Stocks:

    """Utility class for interpreting the JSON stock data"""

    def __init__(self, stock_data_file):
        with open(stock_data_file, "r") as f:
            self.stock_data = json.load(f)

    def get_stock_exchange_list(self):
        """ Description: 
                Get the list of stock exchanges from JSON file
            Arguments:
                * n/a
            Return Value: 
                * stock_exchange_list - list of stock exchanges
        """
        stock_exchange_list = []
        for item in self.stock_data:
            stock_exchange_list.append(item["stockExchange"])
    
        return stock_exchange_list
    
    def get_stock_list(self, stock_exchange):
        """ Description: 
                Get the list of stocks for a given stock exchange
            Arguments:
                * stock_exchange - given stock exchange (e.g. Nasdaq) 
            Return Value: 
                * stock_list - list of stocks for given stock exchange
        """
        stock_list = []
        for item in self.stock_data:
            if item["stockExchange"] == stock_exchange:
                for top_stock in item["topStocks"]:
                    stock_list.append(top_stock["stockName"])
    
        return stock_list
    
    
    def get_stock_price(self, stock_exchange, stock):
        """ Description: 
                Get stock price for a given stock
            Arguments:
                * stock_exchange - given stock exchange (e.g. Nasdaq)
                * stock - given stock (e.g. AMD) 
            Return Value: 
                * stock price for given stock
        """
        for item in self.stock_data:
            if item["stockExchange"] == stock_exchange:
                top_stocks = item["topStocks"]
                for top_stock in top_stocks:
                    if top_stock["stockName"] == stock:
                        return top_stock["price"]