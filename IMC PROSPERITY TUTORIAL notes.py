# IMC PROSPERITY TUTORIAL 

# format for the trading algorithm 
    # predefined 'trader' class, with a single method 'run'
    # after being run in the simulation environment, after each iteration the 'run' method will be called and provided with a 'tradingstate' object
    #   'tradingstate' contains a per product overview of outstanding buy and sell orders (quotes) 
    # based on the logic present in the run method, the algorithm can choose to buy or sell the seashells, which will result in a trade 
        # if the buy order sent is larger than the selling amount available, the excess buy will be an outstanding buy quote that the bots will potentially trade on 
        # same logic applies to the sell side, where if you want to sell more than what is wanted to be bought, then there will be an excess of selling seashells available 
    # after the next iteration, the 'tradingstate' object will then reveal whether any of the bots decided to trade on the quote 
        # if none of the bots trade on an outstanding palyer quote, the quote is automatically cancelled at the end of the iteration 
    # algorithm is restricted by per product position limits, which define the limits both long and short the algorithm cannot exceed 
        # if the quantity of all buy order results in a long position exceeding the limit, then all the orders placed are cancelled by the exchange 
            # similar to how in darts you cannot score past 0 when you are playing 
            
            
# overview of the trader class 
    # the trader class outputs a dictionary{} named 'result' which contains all the orders the algorithm decides to send based on the logic in the 'run' method 
    
    # EXAMPLE OF FORMAT OF THE TRADER CLASS
# The Python code below is the minimum code that is required in a submission file:
# 1. The "datamodel" imports at the top. Using the typing library is optional.
# 2. A class called "Trader", this class name should not be changed.
# 3. A run function that takes a tradingstate as input and outputs a "result" dict.

# from typing import Dict, List
# from datamodel import OrderDepth, TradingState, Order

# class Trader:
#     def run(self, state: TradingState) -> Dict[str, List[Order]]:
# 	# Takes all buy and sell orders for all symbols as an input,
# 	# and outputs a list of orders to be sent
#         result = {}
#         return result



# overview of the 'tradingstate' class 
#     # DEFINITION OF THE TRADINGSTATE CLASS 
# Time = int
# Symbol = str
# Product = str
# Position = int
# Observation = int

# class TradingState(object):
#     def __init__(self,
#                  timestamp: Time,
#                  listings: Dict[Symbol, Listing],
#                  order_depths: Dict[Symbol, OrderDepth],
#                  own_trades: Dict[Symbol, List[Trade]],
#                  market_trades: Dict[Symbol, List[Trade]],
#                  position: Dict[Product, Position],
#                  observations: Dict[Product, Observation]):
#         self.timestamp = timestamp
#         self.listings = listings
#         self.order_depths = order_depths    # all the buy and sell orders per product that other market participants
#         self.own_trades = own_trades  # the trades the algorithm itself has done since the last tradingstate came in, a dictionary of trade objects 
#         self.market_trades = market_trades   # trades that other market participants have done since the last tradingstate came in, a list of trade objects
#         self.position = position   # long and short of EACH product, is a dictionary with the product as the keys
#         self.observations = observations
        
#     def toJSON(self):
#         return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)    
    
    
# The 'trade' class 
    # within the tradingstate object, the own_trades and market_trades properties provide a list of trades per products 
    
# Symbol = str
# UserId = str

# class Trade:
#     def __init__(self, symbol: Symbol, price: int, quantity: int, buyer: UserId = "", seller: UserId = "") -> None:
#         self.symbol = symbol
#         self.price: int = price     
#         self.quantity: int = quantity
#         self.buyer = buyer
#         self.seller = seller

#     def __str__(self) -> str:
#         return "(" + self.symbol + ", " + self.buyer + " << " + self.seller + ", " + str(self.price) + ", " + str(self.quantity) + ")"

#     def __repr__(self) -> str:
#         return "(" + self.symbol + ", " + self.buyer + " << " + self.seller + ", " + str(self.price) + ", " + str(self.quantity) + ")"
    
        # the trades here have 5 distinct properties 
            # the symbol/product that the trade corresponds to 
            # the price of exchange 
            # the quantity that was exchanged 
            # the identity of the buyer in the transaction 
            # the identity of the seller in the transaction 
                # the identity of the buyer and seller will only be disclosed if the algorithm itself is the buyer or seller 
                
                
# The 'orderdepth' class 
    # within the 'tradingstate' class is also the 'orderdepth' per symbol, which contains all outstanding buy and sell orders that were sent by trading bots 
    # this 'orderdepth' class is a dictionary with the prices associated with each buy and sell order 
# class OrderDepth:
# def __init__(self):
#     self.buy_orders: Dict[int, int] = {}
#     self.sell_orders: Dict[int, int] = {}
    # the daily orders are aggregated on a dictionary
    # eg, if the dict looked like {9:5, 10:4}, then this would mean there were 5 buy orders on the price of 9 and 4 buy orders on the price of 10 
        # but for sell orders, the integer would be negative to represent the selling of the assets: {9:-6, 10:-3}
# to confirm any trades that should have happened, the number of buy orders should always be less than the number of sell orders



# HOW TO SEND ORDERS USING THE 'ORDER' CLASS 
    # 'run' method should output a dictionary containing the orders that the algorithm wants to send with the keys being the products and the values being the amount 
    # the orders coming from the run method should be an instance of the order class 
        # must have the symbol of the product for each order
        # must have the price of the order: maximum buying price or the minimum selling price 
        # the quantity of the order: positive is buy and negative is sell
    # any remaining orders are active until the next 'tradingstate' comes in, which means that your order can still be triggered even while waiting for the next 'tradingstate'
    # once the new tradingstate is activated, then the previous orders are all cancelled 
            
#     Symbol = str

# class Order:
#     def __init__(self, symbol: Symbol, price: int, quantity: int) -> None:
#         self.symbol = symbol
#         self.price = price
#         self.quantity = quantity

#     def __str__(self) -> str:
#         return "(" + self.symbol + ", " + str(self.price) + ", " + str(self.quantity) + ")"

#     def __repr__(self) -> str:
#         return "(" + self.symbol + ", " + str(self.price) + ", " + str(self.quantity) + ")"



# Position limits 
    # if the position limit is exceeded, then all orders are cancelled 
    # example with product1 having a position limit of 10 and product2 having a position limit of 20 
        # the first iteration has the run method call the tradingstate that is generated by the code below
        # the datamodel to import is in appendix B
        
# CODE BELOW IS AN EXAMPLE OF A TRADINGSTATE OBJECT
        
# from datamodel import Listing, OrderDepth, Trade, TradingState

# timestamp = 1000

# listings = {
# 	"PRODUCT1": Listing(
# 		symbol="PRODUCT1", 
# 		product="PRODUCT1", 
# 		denomination: "SEASHELLS"
# 	),
# 	"PRODUCT2": Listing(
# 		symbol="PRODUCT2", 
# 		product="PRODUCT2", 
# 		denomination: "SEASHELLS"
# 	),
# }

# order_depths = {
# 	"PRODUCT1": OrderDepth(
# 		buy_orders={10: 7, 9: 5},
# 		sell_orders={11: -4, 12: -8}
# 	),
# 	"PRODUCT2": OrderDepth(
# 		buy_orders={142: 3, 141: 5},
# 		sell_orders={144: -5, 145: -8}
# 	),	
# }

# own_trades = {
# 	"PRODUCT1": [],
# 	"PRODUCT2": []
# }

# market_trades = {
# 	"PRODUCT1": [
# 		Trade(
# 			symbol="PRODUCT1",
# 			price=11,
# 			quantity=4,
# 			buyer="",
# 			seller="",
# 		)
# 	],
# 	"PRODUCT2": []
# }

# position = {
# 	"PRODUCT1": 3,
# 	"PRODUCT2": -5
# }

# observations = {}

# state = TradingState(
# 	timestamp=timestamp,
#   listings=listings,
# 	order_depths=order_depths,
# 	own_trades,
# 	market_trades
# )



# TECHNICAL NOTES 
    # the supported libraries are in appendix C; they are pandas, numpy, statistics, math, typing 
    # each time the 'run' method is called, it should generate a response in less than 900ms, so the code we write will have to be sufficiently lightweight 
    
    
# RESOURCES TO HELP BUILD ALGORITHM
    # for every new product introduced, several days of sample data are provided. For each of these days two .csv files will be made available
        # one file will be all the trades done on that day and the other will be all the market orders at each timestep
    # the algorithm we submit will be tested for 1000 iterations using data from a sample day, a logfile will be provided which will aid in debugging the algorithms 
    
    
    
# APPENDIX A: TRADER CLASS EXAMPLE 
from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order


class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        # Initialize the method output dict as an empty dict
        result = {}

        # Iterate over all the keys (the available products) contained in the order depths
        for product in state.order_depths.keys():

            # Check if the current product is the 'PEARLS' product, only then run the order logic
            if product == 'PEARLS':

                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]

                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []

                # Define a fair value for the PEARLS.
                # Note that this value of 1 is just a dummy value, you should likely change it!
                acceptable_price = 1

                # If statement checks if there are any SELL orders in the PEARLS market
                if len(order_depth.sell_orders) > 0:

                    # Sort all the available sell orders by their price,
                    # and select only the sell order with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    # Check if the lowest ask (sell order) is lower than the above defined fair value
                    if best_ask < acceptable_price:

                        # In case the lowest ask is lower than our fair value,
                        # This presents an opportunity for us to buy cheaply
                        # The code below therefore sends a BUY order at the price level of the ask,
                        # with the same quantity
                        # We expect this order to trade with the sell order
                        print("BUY", str(-best_ask_volume) + "x", best_ask)
                        orders.append(Order(product, best_ask, -best_ask_volume))

                # The below code block is similar to the one above,
                # the difference is that it finds the highest bid (buy order)
                # If the price of the order is higher than the fair value
                # This is an opportunity to sell at a premium
                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    if best_bid > acceptable_price:
                        print("SELL", str(best_bid_volume) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_volume))

                # Add all the above orders to the result dict
                result[product] = orders

                # Return the dict of orders
                # These possibly contain buy or sell orders for PEARLS
                # Depending on the logic above
        return result