import math
import market_sim

def max_buy(ticker,cash,data,day_id):
    open = list(data['Open'][ticker])[day_id]
    buy = cash/open
    buy = math.floor(buy)
    return buy



def action_handler(actions, portfolio, stock_data, day_id, tickers):
    buy_prob = max(actions)
    sell_prob = min(actions)
    if buy_prob > -sell_prob:
        buy_amt=portfolio['cash']/list(stock_data['Open'][tickers[actions.index(buy_prob)]])[day_id]
        portfolio=market_sim.buy_request(buy_amt,portfolio,tickers[actions.index(buy_prob)],stock_data,day_id)
    elif -sell_prob > buy_prob:
        portfolio=market_sim.sell_request(portfolio['stocks'][tickers[actions.index(sell_prob)]][0],portfolio,tickers[actions.index(sell_prob)],stock_data,day_id)
    return portfolio