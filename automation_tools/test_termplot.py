# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 23:40:17 2023

@author: HS00935501
"""
import plotext as plt
# X axis values:
x = ['2001','2002','2003','2004','2005','2006','2007','2008','2009','2010']
# Y axis values:
y = [4,7,55,43,2,4,11,22,33,44]
# Create scatter plot:
plt.plot(y)
plt.plotsize(100, 20)
plt.xscale("log")    # for logarithmic x scale
plt.yscale("linear")
plt.show()