
import numpy as np
import yfinance as yf
import rlmodel
import action_handler
import critic_model

#set the tickers you want the bot to watch
tickers = ["CMCSA"]
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
    portfolio['stocks'][ticker] = [0,0]

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

def format_inputs(day_data,portfolio):
    list = day_data.copy()
    list.append(portfolio['cash'])
    for stock in portfolio['stocks']:
        list.append(portfolio['stocks'][stock][0])
        list.append(portfolio['stocks'][stock][1])
    return list

def pick_action(actions):
    return list(actions).index(actions.max())


def stock_market(data,tickers,portfolio):
    length_data = len(list(data['Close'][tickers[0]]))
    max_high = max(list(data['High'][tickers[0]]))
    start_cash = portfolio['cash']
    portfolio_value = [start_cash, start_cash]
    portfolio_real = [start_cash, start_cash]
    actor = rlmodel.init_params(((6*len(tickers))+1),16,16,((2*len(tickers))+1))
    critic = rlmodel.init_params(((8*len(tickers))+2),16,16,1)
    for i in range(length_data):
        if i == 0:
            continue
        else:
            cmcsa_high = list(data['High']['CMCSA'])[i-1],
            cmcsa_low = list(data['Low']['CMCSA'])[i-1],
            cmcsa_close = list(data['Close']['CMCSA'])[i-1],
            cmcsa_open = list(data['Open']['CMCSA'])[i],
            #ups_high = list(data['High']['UPS'])[i-1],
            #ups_low = list(data['Low']['UPS'])[i-1],
            #ups_close = list(data['Close']['UPS'])[i-1],
            #ups_open = list(data['Open']['UPS'])[i]

            day_data = [cmcsa_high, cmcsa_low, cmcsa_close, cmcsa_open,
                        #ups_high, ups_low, ups_close, ups_open,
                        ]
            print(day_data,portfolio)
            inputs=format_inputs(day_data,portfolio)
            print(inputs)
            inputs = rlmodel.fix(inputs)
            actor_out = rlmodel.forward_prop(actor, inputs)

            critic_in = list(inputs.copy().T)
            critic_in[0] = list(critic_in[0])
            for output in actor_out[5]:
                critic_in[0].append(output[0])
            critic_in[0] = np.array(critic_in[0])
            critic_in = np.array(critic_in).T
            critic_out = critic_model.forward_prop(critic, critic_in)
            actions = actor_out[5]
            action = pick_action(actions)
            portfolio = action_handler.action_handler(action,portfolio,data,i,tickers)
            if i == 1:
                portfolio_value[1] = get_value(portfolio)
                portfolio_real[1] = get_real(portfolio,data,i)
            else:
                portfolio_value.append(get_value(portfolio))
                portfolio_real.append(get_real(portfolio,data,i))
            #IMPORTANT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #change is being set to the variable
            #the varibale change is set to will determine what the critic optimizes for
            change = (portfolio_real[i]/portfolio_real[i-1])-1
            error = change - critic_out[5]
            critic_stick = rlmodel.backprop(critic_out,critic,critic_in,change,1)
            critic = rlmodel.update_params(critic,critic_stick,0.01)
            actor_corrected_action = list(np.zeros((len(actor_out[5]),1)))
            actor_corrected_action[action] = actor_out[5][action]*((list(list(error)[0])[0]*0.01)+1)
            guideline = []
            for a in actor_corrected_action:
                guideline.append(list(a)[0])
            guideline = rlmodel.fix(guideline)
            actor_stick = rlmodel.backprop(actor_out,actor,inputs,guideline)
            actor = rlmodel.update_params(actor,actor_stick,0.01)
            print('portfolios real value is')
            print(portfolio_real[i])
            print('portfolios static value is')
            print(portfolio_value[i])
            print('cash available')
            print(portfolio['cash'])



stock_market(data,tickers,portfolio)