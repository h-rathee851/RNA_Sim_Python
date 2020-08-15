
# coding: utf-8

# In[15]:

import numpy as np
from scipy.optimize import brentq
import math
from helper_methods_cy import *
from simulation_up_cy import *


def rho_alpha(alpha,sim):
    
      
    sim.ChangeAlpha(alpha)
    
    sim.Reach_steady()
    sim.Run_Sim()
    
    return sim.getTot_den()


def func_for_brent(alpha,exp_den,*args):
    
    return rho_alpha(alpha,*args) - exp_den

def plot_rho(low_bound,upper_bound,file, rho_exp):
    
    alpha_ = []
    totden_ = []
    n = 0
    steps = 5 
    
    for i in np.linspace(low_bound,upper_bound,steps):
        
        
#         totden_ += [rho_alpha(i,10,18.03,'kvalue_dummy.dat')]
        totden_ += [func_for_brent(i,rho_exp,10,18.03,file)]
        alpha_ += [i]
        n += 1
        print(str(n*100/steps)+'% done')
        
        
        
    plt.plot(alpha_,totden_)
    plt.show()
    
def calcAlpha(args,brac):
    
    alpha, *aux = brentq(func_for_brent,*brac,args = args, full_output= True)
    
    return alpha,aux

def calcAvgAndErr_rho(alpha,sim):
        
    rho_ = []
    
    for i in range(5):
        
        rho_.append(rho_alpha(alpha,sim))

    
    rho_ = np.array(rho_)
    
    mean = np.mean(rho_)
    
    error = np.std(rho_)/math.sqrt(5)
    
    rel_error = error*100/mean
    
    return mean,error,rel_error

def calcAvgAndErr_alpha(args,brac):
    
    alpha_ = []
    
    for i in range(5):
        
        a = calcAlpha(args,brac)
        alpha_.append(a[0])
        
    
    alpha_ = np.array(alpha_)
    
    mean = np.mean(alpha_)
    
    error = np.std(alpha_)/math.sqrt(5)
    
    rel_error = error*100/mean
    
    return mean,error,rel_error