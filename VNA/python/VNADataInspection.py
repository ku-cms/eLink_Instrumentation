#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 01:52:57 2019

@author: skhalil
"""
import skrf as rf
import pylab

vna = rf.Network('TP_07_05Jun2019_T1.s4p')

z0 = vna.z0

print(vna)

# charachteristic impedence
#print(z0)

# S-parameters
print(vna.s)

# smith chart for element 01 of S-Matrix => S12
vna.plot_s_smith(m=0,n=1,color='b', marker='x')


pylab.show()
