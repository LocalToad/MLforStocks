Machine Learning for Stocks 1.0

This is a program that will spawn an Actor/Critic model for machine learning and let it explore a stock market environment that is setup.
This program handles forward and backward propogation, activation functions, layer building, downloading stock market data, vector math, and many more.
You can set the amount of nodes you want in your hidden layer by changing the n variable in the main loop(complexity of the hyperspace).
You can change the learning alpha by changing alpha in the main loop(step size).
You can change how much the temporal difference favours the future there is a '* float' in the function for the TD variable, change that float to the decimal form percent.(percent of how much the program cares about future rewards)
