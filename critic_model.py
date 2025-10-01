import numpy as np
import math
import rlmodel


def leaky_relu(Z,a=0.01):
    return np.maximum((a*Z),Z)


def forward_prop(critic, X):
    Z1 = critic[0].dot(X) + critic[1]
    A1 = leaky_relu(Z1)
    Z2 = critic[2].dot(A1) + critic[3]
    A2 = leaky_relu(Z2)
    Z3 = critic[4].dot(A2) + critic[5]
    A3 = np.tanh(Z3)
    return [Z1, A1, Z2, A2, Z3, A3]

