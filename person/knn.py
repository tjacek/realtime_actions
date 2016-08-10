import sys,os
sys.path.append(os.path.abspath('../realtime_actions'))
import numpy as np
import utils.imgs 

class LazyCls(object):
    def __init__(self, pos_insts):
        self.pos_insts=pos_insts

    def best_match(self,candidates):
        dist=[ self.distance(cand_i)
    	       for cand_i in candidates]
        return np.argmax(dist)

    def distance(self,img_i):
        return min([ d(img_i,img_j)
    	           for img_j in self.pos_insts])

def d(x,y):
    return np.linalg.norm(x-y)
		