import numpy as np
import statistics as stats 
import json
from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order, Trade
from collections import defaultdict

class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        result = {}

        for product in state.order_depths.keys():

            # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
            order_depth: OrderDepth = state.order_depths[product]
            
            best_ask = min(order_depth.sell_orders.keys())
            middle_ask = stats.median(order_depth.sell_orders.keys())
            worst_ask = max(order_depth.sell_orders.keys())
            best_bid = max(order_depth.buy_orders.keys())
            middle_bid = stats.median(order_depth.sell_orders.keys())
            worst_bid = min(order_depth.buy_orders.keys())
            # best_ask is the higher price between best bid and best ask
            
            # VOLATILE COMMODITIES => |slope| over 3.67722
            if product == 'DIVING_GEAR':
                Position_Limit = 50
                mid_price = (best_bid + best_ask)/2
            elif product == 'UKELELE':
                Position_Limit = 50
                mid_price = (best_bid + best_ask)/2
            elif product == 'PICNIC_BASKET':
                Position_Limit = 250
                mid_price = (best_bid + best_ask)/2
            elif product == 'DIP':
                Position_Limit = 300
                mid_price = (best_bid + best_ask)/2  
            elif product == 'PINA_COLADAS':
                Position_Limit = 300
                mid_price = (best_bid + best_ask)/2     

            # INVOLATILE COMMODITIES => |slope| under 3.67722
            elif product == 'PEARLS':
                Position_Limit = 20
                if (best_ask + best_bid)/2 >= 10000:
                    mid_price = (worst_bid + best_ask)/2
                else:
                    mid_price = (best_bid + worst_ask)/2     
            elif product == 'BANANAS':
                Position_Limit = 20
                if (best_ask + best_bid)/2 >= 5000:
                    mid_price = (worst_bid + best_ask)/2
                else:
                    mid_price = (best_bid + worst_ask)/2    
            elif product == 'COCONUTS':    # prices change a lot
                Position_Limit = 600
                if (best_ask + best_bid)/2 >= 8000:
                    mid_price = (best_bid + middle_ask)/2
                else:
                    mid_price = (middle_bid + best_ask)/2     
             
            elif product == 'BERRIES':
                Position_Limit = 250
                if (best_ask + best_bid)/2 >= 4000:
                    mid_price = (worst_bid + best_ask)/2
                else:
                    mid_price = (best_bid + worst_ask)/2    
            elif product == 'BAGUETTE':   # prices change a lot 
                Position_Limit = 600
                if (best_ask + best_bid)/2 >= 12000:
                    mid_price = (best_bid + middle_ask)/2
                else:
                    mid_price = (middle_bid + best_ask)/2    
            
            
            
            
            positions = {}
            positions = defaultdict(lambda:0,positions)
            

            # Initialize the list of Orders to be sent as an empty list
            orders: list[Order] = []
            acceptable_bid_price = mid_price
            acceptable_ask_price = mid_price
            
            best_ask_volume = order_depth.sell_orders[best_ask]
            # If statement checks if there are any SELL orders in the PEARLS market
            if len(order_depth.sell_orders) != 0 and positions[product] <= (Position_Limit - best_ask_volume):

                # Sort all the available sell orders by their price,
                # and select only the sell order with the lowest price
                

                # Check if the lowest ask (sell order) is lower than the above defined fair value
                if best_ask <= acceptable_ask_price:

                    # In case the lowest ask is lower than our fair value,
                    # This presents an opportunity for us to buy cheaply
                    # The code below therefore sends a BUY order at the price level of the ask,
                    # with the same quantity
                    # We expect this order to trade with the sell order
                    #print("BUY", str(-best_ask_volume) + "x", best_ask)
                    print(f"BUY {product},{-best_ask_volume},{best_ask}")
                    orders.append(Order(product, best_ask, -best_ask_volume))
                    positions[product] += -best_ask_volume

            # The below code block is similar to the one above,
            # the difference is that it find the highest bid (buy order)
            # If the price of the order is higher than the fair value
            # This is an opportunity to sell at a premium
            best_bid_volume = order_depth.buy_orders[best_bid]
            if len(order_depth.buy_orders) != 0 and positions[product] >= (-Position_Limit + best_bid_volume):
                
                if best_bid >= acceptable_bid_price:
                    #print("SELL", str(best_bid_volume) + "x", best_bid)
                    print(f"SELL {product},{best_bid_volume},{best_bid}")
                    orders.append(Order(product, best_bid, -best_bid_volume))
                    
                    positions[product] -= best_bid_volume

            # Add all the above the orders to the result dict
            result[product] = orders

            # Return the dict of orders
        
        return result