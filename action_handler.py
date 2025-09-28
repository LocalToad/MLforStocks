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
    buy = []
    sell = []
    for action in actions:
        ticker = tickers[actions.index(action)]
        if action > 0:
            buy.append(ticker)
        if action < 0:
            sell.append(ticker)
    for ticker in sell:
        total = portfolio['stocks'][ticker][0]
        if total > 0:
            portfolio = market_sim.sell_request(total,portfolio,ticker,stock_data,day_id)
        else:
            continue
    n=len(buy)
    cash_per_stock = portfolio['cash']/n
    for ticker in buy:
        buy_amount = cash_per_stock/list(stock_data['Open'][ticker])[day_id]
        if buy_amount > 0:
            portfolio = market_sim.buy_request(buy_amount,portfolio,ticker,stock_data,day_id)
        else:
            continue



    return portfolio