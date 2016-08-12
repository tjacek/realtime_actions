import numpy as np
from lasagne import layers
from lasagne.updates import nesterov_momentum
from nolearn.lasagne import NeuralNet

nn_cls = NeuralNet(
    layers=[
        ('input', layers.InputLayer),
        
        ('encode_layer', layers.DenseLayer),
        ('hidden', layers.DenseLayer),  # output_dense
        
        ]))