
def rlmodel(all_data, day_data, portfolio, day_id):
    #idk how to write this yet but we are gonna pretend this exists

    cmcsa=0
    ups=0
    actions = (cmcsa, ups)
    #the stock name will be -1 to 1
    #if negative that means sell
    #if positive that means buy
    #0-1 is a percent scale, the action handler will take 100 percent as the max allowed value
    #for selling that would be 100% = all stocks owned
    #for buying that would be 100% = cash / price_of_stock
    return actions