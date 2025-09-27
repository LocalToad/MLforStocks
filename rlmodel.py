import random

import numpy as np



class Agent:
    def __init__(self, inputs, outputs, hidden_layers=[0]):
        self.inputs = inputs
        self.outputs = outputs
        self.hidden_layers = hidden_layers
        brain = {}
        self.brain = brain
        brain['inputs'] = {}
        if outputs > 0:
            self.generate_nodes(0,inputs+1,nodes)
            for i in range(hidden_layers):
                brain[f'layer{i}'] = {}
                if i < hidden_layers:
                    self.generate_nodes(i,nodes,nodes)
                else:
                    self.generate_nodes(i,nodes,outputs)
        else:
            self.generate_nodes(0,inputs+1,outputs)
        self.generate_outputs(outputs)


    def generate_nodes(cls, layer, num_nodes, num_outputs):
        for node in range(num_nodes):
            cls.brain[layer][f'node{layer}{node}'] = {}
            cls.brain[layer][f'node{layer}{node}']['output_biases'] = []
            for output in range(num_outputs):
                random_bias = random.uniform(-1, 1)
                cls.brain[layer][f'node{layer}{node}']['output_biases'].append(random_bias)

    def generate_outputs(cls, outputs):
        for node in range(outputs):
            cls.brain[f'output{node}'][''] = []

