import random


def randfloat(a,b,c):
    scale = a-b
    add = scale*c
    value = add+b
    return value

def buy_request(buy_amt,portfolio, ticker, data, day_id):
    cash = portfolio['cash']
    #the buy_amt is the amount the agent is requesting to buy
    #we are going to randomize a prize based on the data, and then fufil the order if its possible
    high = list(data['High'][ticker])[day_id]
    low = list(data['Low'][ticker])[day_id]
    buy_price = randfloat(high,low,random.random())
    buy_order = buy_amt * buy_price
    if buy_order <= cash:
        portfolio['cash'] -= buy_order
        portfolio['stocks'][ticker][0] += buy_amt
        portfolio['stocks'][ticker][1] += buy_order
        return portfolio
    else:
        return portfolio


def sell_request(sell_amt,portfolio, ticker, data, day_id):
    cash = portfolio['cash']
    high = list(data['High'][ticker])[day_id]
    low = list(data['Low'][ticker])[day_id]
    sell_price = randint(low, high)
    sell_order = sell_amt * sell_price
    if sell_order <= portfolio['stocks'][ticker][0]:
        cash += sell_order
        portfolio['stocks'][ticker][1] -= (portfolio['stocks'][ticker][1] / portfolio['stocks'][ticker][0]) * sell_amt
        portfolio['stocks'][ticker][0] -= sell_amt

        return portfolio
    else:
        return portfolio