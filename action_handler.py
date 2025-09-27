import math
import market_sim

def max_buy(ticker,cash,data,day_id):
    open = list(data['Open'][ticker])[day_id]
    buy = cash/open
    buy = math.floor(buy)
    return buy



def action_handler(actions, portfolio, stock_data, day_id, tickers):
    #actions look like a list of all the stocks as a variable
    #that variable is between -1 and 1

    for action in actions:
        ticker = tickers[actions.index(action)]
        if action > 0:
            total = max_buy(ticker,portfolio['cash'],stock_data,day_id)
            buy_amount = action * total
            buy_amount = math.floor(buy_amount)
            if buy_amount > 0:
                portfolio = market_sim.buy_request(buy_amount,portfolio,ticker,stock_data,day_id)
            else:
                continue
        if action < 0:
            total = portfolio['stocks'][ticker][0]
            if total > 0:
                sell_amount = -action * total
                math.floor(sell_amount)
                if sell_amount > 0:
                    portfolio = market_sim.sell_request(sell_amount,portfolio,ticker,stock_data,day_id)
                else:
                    continue
    return portfolio