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
    #Actor will have these outputs 2n+1 outputs(n = stocks watched)
        #For each stock being tracked(
            #Stock sell
            #Stock Buy
        #)
    #All outputs will be in range of 0-1 and will represent the probablity that the actor thinks an action will result in a good outcome
#Feeds Environment and actions to Critic (9n+2 inputs n=stocks watched)
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
import numpy as np
import pandas as pd



def pick_action(actions):
    return list(actions).index(actions.max())
def fix(data):
    for i in range(len(data)):
        if type(data[i]) == tuple:
            data[i] = data[i][0]
    data = np.array(data)
    data = data.reshape(-1,1)
    return data


def init_params(inputs,layer1_nodes,layer2_nodes,outputs):
    W1 = np.random.randn(layer1_nodes,inputs)
    B1 = np.random.randn(layer1_nodes,1)
    W2 = np.random.randn(layer2_nodes,layer1_nodes)
    B2 = np.random.randn(layer2_nodes,1)
    W3 = np.random.randn(outputs,layer2_nodes)
    B3 = np.random.randn(outputs,1)
    brain = [W1,B1,W2,B2,W3,B3]
    return brain

def leaky_relu(Z,a=0.01):
    return np.maximum((a*Z),Z)

def exp(Z):
    a = np.exp(Z)
    for b in a:
        if list(b)[0] == float('inf'):
            list(b)[0] = 1
        elif list(b)[0] == float('-inf'):
            list(b)[0] = 0
    return a

def softmax(Z):
    a = exp(Z)
    b = exp(Z)
    c = np.sum(b)
    d = a/c
    return d
#array=[-218.71424335,709.66636126,844.82633888]
#array = fix(array)
#softmax(array)

def deriv_leaky_relu(Z, a=0.01):
    dZ = np.ones((1, Z.size))  # Initialize derivative with 1s for positive values
    dZ[Z.T < 0] = a  # Set derivative to alpha for negative values
    return dZ.T

def forward_prop(actor,X):
    Z1 = actor[0].dot(X) + actor[1]
    A1 = leaky_relu(Z1)
    Z2 = actor[2].dot(A1) + actor[3]
    A2 = leaky_relu(Z2)
    Z3 = actor[4].dot(A2) + actor[5]
    action = pick_action(Z3)
    a3 = list(np.zeros((len(Z3),1)))
    a3[action][0] = 1
    A3 =[]
    for a in a3:
        A3.append(list(a)[0])
    A3 = fix(A3)
    out = [Z1, A1, Z2, A2, Z3, A3]
    return out

def backprop(out, brain, X, Y,m=None):
    if m is None:
        m = Y.size
    dZ3 = out[5] - Y
    dW3 = 1 / m * dZ3.dot(out[3].T)
    dB3 = 1 / m * np.sum(dZ3)
    dZ2 = brain[5].T.dot(dZ3) * deriv_leaky_relu(out[2])
    dW2 = 1 / m * dZ2.dot(out[1].T)
    dB2 = 1 / m * np.sum(dZ2)
    dZ1 = brain[3].T.dot(dZ2) * deriv_leaky_relu(out[0])
    dW1 = 1 / m * dZ1.dot(X.T)
    dB1 = 1 / m * np.sum(dZ1)
    return [dW1, dB1, dW2, dB2, dW3, dB3]

def update_params(brain, stick, a):
    for n in range(0,len(brain)):
        brain[n] = brain[n] - a * stick[n]
    return brain


