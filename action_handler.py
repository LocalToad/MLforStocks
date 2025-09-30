import math
import market_sim

def max_buy(ticker,cash,data,day_id):
    open = list(data['Open'][ticker])[day_id]
    buy = cash/open
    buy = math.floor(buy)
    return buy



def action_handler(action, portfolio, stock_data, day_id, tickers):
    if action > 0:
        if action % 2 == 0:
            portfolio=market_sim.sell_request(1,portfolio,tickers[int(((1-action)/2)-1)],stock_data,day_id)
        else:
            portfolio=market_sim.buy_request(1,portfolio,tickers[int((action/2)-1)],stock_data,day_id)
    return portfolio