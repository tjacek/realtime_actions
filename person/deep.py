import sys,os
sys.path.append(os.path.abspath('../realtime_actions'))
import numpy as np
from lasagne import layers
from lasagne.updates import nesterov_momentum
from lasagne.nonlinearities import softmax
from nolearn.lasagne import NeuralNet
import utils.imgs
import hog
import copy

class DeepCls(object):
    def __init__(self,n_cats=2,input_size=1040):
        self.net1 = NeuralNet(
            layers=[  
                    ('input', layers.InputLayer),
                    ('hidden', layers.DenseLayer),
                    ('output', layers.DenseLayer),
                   ],
            input_shape=(None, input_size),  
            hidden_num_units=300, 
            output_nonlinearity=softmax,  
            output_num_units=n_cats, 

            update=nesterov_momentum,
            update_learning_rate=0.01, 
            update_momentum=0.9, 

            regression=False,  
            max_epochs=2500, 
            verbose=1, 
        )

def train_cls(in_path='person/data',out_path='person/nn'):
    x,y=read_dataset(in_path)
    deep_cls=DeepCls()
    deep_cls.net1.fit(x,y)
    deep_cls.net1.save_params_to(out_path)

def read_dataset(in_path):
    pos=utils.imgs.read_images(in_path+'/pos')
    neg=utils.imgs.read_images(in_path+'/neg')
    x_pos,y_pos=hog_dataset(pos,0)
    x_neg,y_neg=hog_dataset(neg,1)
    print(len(y_pos))
    x=x_pos+x_neg
    y=y_pos+y_neg
    print(len(y))
    return np.array(x),np.array(y,dtype=np.int32)

def hog_dataset(raw_data,cat):
    x=[hog.compute(x_i)
        for x_i in raw_data]
    y=[cat for i in range(len(x))]
    return x,y

if __name__ == "__main__":
    train_cls()
#img_i=np.expand_dims(img_i,1)
#print(net1.predict_proba(img_i))