

import yfinance as yf
import rlmodel
import action_handler

#set the tickers you want the bot to watch
tickers = ("CMCSA", "UPS")
start_date = "2000-01-01"
end_date = "2010-12-31"

start_cash = 50
#download the data
data = yf.download(tickers, start_date, end_date)
data.fillna(0)
data.head()

portfolio = {'stocks': {}, 'cash': start_cash}
dict(portfolio)
for ticker in tickers:
    portfolio['stocks'][ticker] = (0,0)

def get_value(portfolio):
    cash = portfolio['cash']
    stocks_value = 0
    for ticker in portfolio['stocks']:
        stocks_value += portfolio['stocks'][ticker][1]
    total = cash + stocks_value
    return total

def get_real(portfolio,data,day_id):
    cash = portfolio['cash']
    stocks_value = 0
    for ticker in portfolio['stocks']:
        stocks_value += portfolio['stocks'][ticker][0]* list(data['Close'][ticker])[day_id]
    real = cash + stocks_value
    return real

def stock_market(data,tickers,portfolio):
    length_data = len(list(data['Close'][tickers[0]]))
    start_cash = portfolio['cash']
    portfolio_value = [start_cash, start_cash]
    for i in range(length_data):
        if i == 0:
            continue
        else:
            cmcsa_high = list(data['High']['CMCSA'])[i-1],
            cmcsa_low = list(data['Low']['CMCSA'])[i-1],
            cmcsa_close = list(data['Close']['CMCSA'])[i-1],
            cmcsa_open = list(data['Open']['CMCSA'])[i],
            ups_high = list(data['High']['UPS'])[i-1],
            ups_low = list(data['Low']['UPS'])[i-1],
            ups_close = list(data['Close']['UPS'])[i-1],
            ups_open = list(data['Open']['UPS'])[i]

            day_data = (cmcsa_high, cmcsa_low, cmcsa_close, cmcsa_open,
                        ups_high, ups_low, ups_close, ups_open,
                        )

            actions = rlmodel.rlmodel(data, day_data, portfolio, i)
            portfolio = action_handler.action_handler(actions,portfolio,data,i,tickers)
            if i == 1:
                portfolio_value[1] = get_value(portfolio)
            else:
                portfolio_value.append(get_value(portfolio))
            portfolio_real = get_real(portfolio,data,i)
            print('portfolios real value is')
            print(portfolio_real)
            print('portfolios static value is')
            print(portfolio_value[i])
            print('cash available')
            print(portfolio['cash'])


stock_market(data,tickers,portfolio)