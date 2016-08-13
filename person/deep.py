from lasagne import layers
from lasagne.updates import nesterov_momentum
from lasagne.nonlinearities import softmax
from nolearn.lasagne import NeuralNet

INPUT_SIZE = 1084
N_CATS = 2

net1 = NeuralNet(
    layers=[  
        ('input', layers.InputLayer),
        ('hidden', layers.DenseLayer),
        ('output', layers.DenseLayer),
        ],
    # layer parameters:
    input_shape=(None, INPUT_SIZE),  
    hidden_num_units=100, 
    output_nonlinearity=softmax,  
    output_num_units=N_CATS, 

    update=nesterov_momentum,
    update_learning_rate=0.01, 
    update_momentum=0.9, 

    regression=False,  
    max_epochs=400, 
    verbose=1, 
    )

#X_train, Y_train = load() 
#net1.fit(X_train, Y_train)
