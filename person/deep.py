import sys,os
sys.path.append(os.path.abspath('../realtime_actions'))
import numpy as np
from lasagne import layers
from lasagne.updates import nesterov_momentum
from lasagne.nonlinearities import softmax
from nolearn.lasagne import NeuralNet
import utils.imgs
import hog

INPUT_SIZE = 1040
N_CATS = 2

net1 = NeuralNet(
    layers=[  
        ('input', layers.InputLayer),
        ('hidden', layers.DenseLayer),
        ('output', layers.DenseLayer),
        ],
    # layer parameters:
    input_shape=(None, INPUT_SIZE),  
    hidden_num_units=300, 
    output_nonlinearity=softmax,  
    output_num_units=N_CATS, 

    update=nesterov_momentum,
    update_learning_rate=0.01, 
    update_momentum=0.9, 

    regression=False,  
    max_epochs=4000, 
    verbose=1, 
    )

def read_dataset(in_path):
    pos=utils.imgs.read_images(in_path+'/pos')
    neg=utils.imgs.read_images(in_path+'/pos')
    x_pos,y_pos=hog_dataset(pos,0)
    x_neg,y_neg=hog_dataset(neg,1)
    return np.array(x_pos+x_neg),np.array(y_pos+y_neg,dtype=np.int32)

def hog_dataset(raw_data,cat):
    x=[hog.compute(x_i)
        for x_i in raw_data]
    y=[cat for i in range(len(x))]
    return x,y

x,y=read_dataset('person/data')
print(x[0].shape)
net1.fit(x,y)