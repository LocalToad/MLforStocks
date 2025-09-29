#i know that this is empty dont mention it
#Model environment
#Feed Environment to Actor
    #Actor Receives: 7n+1 inputs (n=stocks watched)
      #For each stock being tracked(
        #Stock Open Today
        #Stock Close Yesterday
        #Stock High Yesterday
        #Stock Low Yesterday
        #Stock Owned
        #Stock Owned Static Value
            #(value of stock when purchased * number of stock purchased)<- sum of all times stock has been bought divided by stock value
            #this is generally displayed in the brokerage app
        #)
      #Cash Available
#Actor takes a guess on actions
    #Actor will have these outputs 2n outputs(n = stocks watched)
        #For each stock being tracked(
            #Stock sell
            #Stock Buy
        #)
    #All outputs will be in range of 0-1 and will represent the probablity that the actor thinks an action will result in a good outcome
#Feeds Environment and actions to Critic (9n+1 inputs n=stocks watched)
    #Critic will see all the same data that the actor can but it can also see all of the outputs of the actor
#Critic Takes a guess on loss
    #Critic will output a single number, if it is 0 then it expects the price of the portfolio to go down
        #if the number is greater than 0 than the critic expects the portfolio price to increase by that much
#Actor affects environment
    #
#Calculate Difference between loss guess and real loss
#Critic learns from mistake
#Critic tells Actor how bad it sucks
#Actor Learns from mistake
import tf_keras
from tf_keras.models import Sequential, load_model
from tf_keras.layers import Dense

class Actor():

    def __init__(self, stocks,layer1):
        super().__init__()
        input_length = (7*stocks)+1
        output_length = 2*stocks
        self.model = Sequential()
        self.input = tf_keras.layers.Input(shape=(input_length,))
        self.layer0 = tf_keras.layers.Dense(units=layer1, activation='leaky_relu')(self.input)
        self.layer1 = tf_keras.layers.Dense(units=layer1, activation='leaky_relu')(self.layer0)
        self.output = tf_keras.layers.Dense(units=output_length, activation='softmax')

    def call(self, inputs):
        x = tf_keras.models.Model(inputs=self.input, outputs=self.output)
        return x.output(inputs)

    def summary(self):
        self.model.summary()


class Critic():
    def __init__(self, stocks,layer1):
        super().__init__()
        input_length = (9*stocks)+1
        self.model = Sequential()
        self.model.add(tf_keras.layers.Input(shape=(input_length,)))
        self.model.add(tf_keras.layers.Dense(units=layer1, activation='leaky_relu', input_dim=input_length))
        self.model.add(tf_keras.layers.Dense(units=layer1, activation='leaky_relu'))
        self.model.add(tf_keras.layers.Dense(units=1, activation='leaky_relu'))

    def call(self, inputs):
        return self.model.output(inputs)

    def summary(self):
        self.model.summary()

#a = Actor(1,16)
#c = Critic(1,16)
#a.summary()
#c.summary()