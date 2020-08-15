
# coding: utf-8


import numpy as np
import math
from helper_methods_cy import *
from simulation_up_cy import *
from find_alpha import *
import sys
import os


def main(args):
    
    gene_names_ = []
    exp_den_ = []
    bracs_ = []
    sweeps = 0
    rel_tol = 1
    
    in_file_name = args[0]
    rates_path = args[1]
    
    filein = open(in_file_name,'r')
    fileout = open(in_file_name[:-4]+'_alpha.dat','a')
    fileout_check = open(in_file_name[:-4]+'_alpha.dat','r')
    
    lines_check = fileout_check.readlines()
    
    if len(args) > 2:
        
        if args[2] == 'Sweeps' or args[2] == 'sweeps':
            
            sweeps = int(args[3])
            
        elif args[2] == 'Tolrance' or args[2] == 'tolrance':
            
            rel_tol = float(args[3])
        
        
    lines= filein.readlines()
    filein.close()
    
    
    line_no = 0
    for line in lines:
        
        line_no += 1
        
        if line_no > len(lines_check):
            data = line.split(',')
            gene_names_.append(data[0])
        
            exp_den_.append(float(data[3]))
        
            bracs_.append([1e-4,1])
        
            if '#' not in data[4]:
                exp_alpha = float(data[4])
            
            else: 
            
                exp_alpha = -1
            
        
            if exp_alpha != -1 and exp_alpha > 0.2:
            
                bracs_[-1][0] = exp_alpha-0.2
        
            if exp_alpha != -1 and exp_alpha < 0.8:
            
                bracs_[-1][1] = exp_alpha+0.2
           
            
    n = 0
    for (gene,bracs,exp_den) in zip(gene_names_,bracs_,exp_den_):
        
        sys.stdout.write("Genes Computed: "+str(n)+'\n')
        sys.stdout.flush()  
        
        rates_file = rates_path+'/'+gene+'_rates.dat'
        
        sim = Simulation(10,sweeps = sweeps, rel_tol= rel_tol)
        sim.ExtractRates(rates_file,0.1,18.03)
        
        
        try:
            a = calcAlpha((exp_den,sim),bracs)
        
        except(ValueError):
            
            print("\n Wrong Brackets for gene number:  "+str(n)+'\n')
            a = ['N/A']
        
        fileout.write(gene+','+str(a[0])+str('\n'))
        
        n += 1
        
        
    fileout.close()
        
    


if __name__ == '__main__':
    main(sys.argv[1:])

