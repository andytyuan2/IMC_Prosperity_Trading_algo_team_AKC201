import numpy as np
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
            best_bid = max(order_depth.buy_orders.keys())
            worst_ask = max(order_depth.sell_orders.keys())
            worst_bid = min(order_depth.buy_orders.keys())
            mid_price = (worst_bid + worst_ask)/2
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
            
            positions = {}
            positions = defaultdict(lambda:0,positions)
            

            # Initialize the list of Orders to be sent as an empty list
            orders: list[Order] = []
            acceptable_bid_price = mid_price
            acceptable_ask_price = mid_price
            # if product == 'PEARLS':
            #     acceptable_price = 10000
            # elif product == 'BANANAS':
            #     acceptable_price = 4890
            # elif product == 'COCONUTS':
            #     acceptable_price = 8000
            # elif product == 'PINA COLADA':
            #     acceptable_price = 15000
            # elif product = 'MAYBERRIES':
            #     acceptable_price = 3900
            # elif product = 'DIVING GEAR'
            #     acceptable_price = 99500
            # elif product = 'DOLPHIN SIGHTINGS'
            #     acceptable_price = 3100
            

            # If statement checks if there are any SELL orders in the PEARLS market
            if len(order_depth.sell_orders) != 0 and positions[product] <= Position_Limit:

                # Sort all the available sell orders by their price,
                # and select only the sell order with the lowest price
                best_ask_volume = order_depth.sell_orders[best_ask]

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
            if len(order_depth.buy_orders) != 0 and positions[product] >= -Position_Limit:
                best_bid_volume = order_depth.buy_orders[best_bid]
                if best_bid >= acceptable_bid_price:
                    #print("SELL", str(best_bid_volume) + "x", best_bid)
                    print(f"SELL {product},{best_bid_volume},{best_bid}")
                    orders.append(Order(product, best_bid, -best_bid_volume))
                    
                    positions[product] -= best_bid_volume

            # Add all the above the orders to the result dict
            result[product] = orders

            # Return the dict of orders
        
        return result