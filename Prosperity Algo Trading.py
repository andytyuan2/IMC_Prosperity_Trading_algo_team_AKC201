import numpy as np
import statistics as stats 
import json
from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
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
            middle_bid = stats.median(order_depth.buy_orders.keys())
            worst_bid = min(order_depth.buy_orders.keys())
            
            mid_price = (worst_bid + worst_ask + best_ask + best_bid + middle_ask + middle_bid)/6
            # best_ask is the higher price between best bid and best ask
            
            
            if product == 'PEARLS' or 'BANANAS':
                Position_Limit = 20
            elif product == 'COCONUTS':
                Position_Limit = 600
            elif product == 'PINA_COLADAS':
                Position_Limit = 300
            elif product == 'DIVING_GEAR':
                Position_Limit = 50
            elif product == 'BERRIES':
                Position_Limit = 250
            elif product == 'BAGUETTE':
                Position_Limit = 600
            elif product == 'DIP':
                Position_Limit = 300
            elif product == 'UKELELE':
                Position_Limit = 50
            elif product == 'PICNIC_BASKET':
                Position_Limit = 250
            
            positions = {}
            positions = defaultdict(lambda:0,positions)
            # Initialize the list of Orders to be sent as an empty list
            orders: list[Order] = []

            
            greater_than_mid = []
            for ask in order_depth.sell_orders.keys():
                if ask >= mid_price:
                    greater_than_mid.append(ask)
            # gives prices that can satisfy the mid_price requirement
                    
            lesser_than_mid = []
            for bid in order_depth.buy_orders.keys():
                if bid <= mid_price:
                    lesser_than_mid.append(bid)

            # If statement checks if there are any SELL orders 
            if len(order_depth.sell_orders) != 0:

                for ask in lesser_than_mid:
                    if positions[product] <= Position_Limit:
                        vol = -order_depth.sell_orders[ask]
                        vol = min(Position_Limit-positions[product],vol)
                        print(f"BUY {product},{vol},{ask}")
                        orders.append(Order(product, ask, vol))
                    else:
                        break
                
                
            # The below code block is similar to the one above,
            # the difference is that it find the highest bid (buy order)
            # If the price of the order is higher than the fair value
            # This is an opportunity to sell at a premium
            if len(order_depth.buy_orders) != 0:

                for bid in greater_than_mid:
                    if positions[product] > -Position_Limit:
                        vol = order_depth.buy_orders[bid]
                        vol = min(-Position_Limit-positions[product],vol) 
                        print(f"SELL {product},{vol},{bid}")
                        orders.append(Order(product, bid, vol)) #vol is negative
                    else:
                        break
                    
                

            # Add all the above the orders to the result dict
            result[product] = orders

            # Return the dict of orders
        
        return result