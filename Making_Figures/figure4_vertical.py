# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 17:49:43 2021

@author: Anna
"""

#%% Import

from __future__ import division
import os
import sys
import copy
import numpy as np
import math as m
import pandas as pd

import pickle
from numpy import genfromtxt
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
import matplotlib.colors as colors

import datetime
from matplotlib.dates import DayLocator, MonthLocator, HourLocator, AutoDateLocator, DateFormatter, drange
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU, WeekdayLocator
from numpy import arange
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FormatStrFormatter

import matplotlib.cm as cm
import matplotlib.mlab as mlab

import glob

# print(len(dates))

#%% Import Functions

from extract_data_pgp_model import get_data 

#%% Get Data

path = '/Users/jacquelinedowling/MEM/Output_Data/to_PGPto_PGP'
data = get_data(path, 5, 'fixed_cost')

toPGP_cost = data['toPGP_cost']
toPGP_eff = data['toPGP_eff']
system_cost = data['system_cost']


path = '/Users/jacquelinedowling/MEM/Output_Data/from_PGPfrom_PGP'
data2 = get_data(path, 7, 'fixed_cost')

fromPGP_cost = data2['fromPGP_cost']
fromPGP_eff = data2['fromPGP_eff']
system_cost2 = data2['system_cost']


path = '/Users/jacquelinedowling/MEM/Output_Data/2d_storagePGPcost_vs_PGPeff'
data3 = get_data(path, 6, 'fixed_cost')

PGPstorage_cost = data3['storagePGP_cost']
PGP_eff = data3['PGP_eff']
system_cost3 = data3['system_cost']



#%% Format Data for Plot
# Get back capital cost from annualized capital cost

#TO PGP
toPGP_base_capitalcost = 1706.46
toPGP_crf = 0.080586404
toPGP_fixed_om = 13.056
hours_per_year = 8760
#c_fixed_base = (0.080586404 * 1706.46 + 13.056) / 8760
c_fixed_base = (toPGP_crf * toPGP_base_capitalcost + toPGP_fixed_om) / hours_per_year
print('c_fixed_base', c_fixed_base)

#base_capitalcost = annual_capitalcost * hours_per_year / toPGP_crf
base_overnightcapital = ((c_fixed_base * hours_per_year) - toPGP_fixed_om)  / toPGP_crf
print('base_overnightcapital', base_overnightcapital)


X = [i * 100 for i in toPGP_eff]
Y = [((i * hours_per_year) - toPGP_fixed_om) / toPGP_crf for i in toPGP_cost]
#Y = [i * hours_per_year for i in toPGP_cost]
Z = system_cost


#%%Get back capital cost from annualized capital cost
#FROM PGP
fromPGP_base_capitalcost = 1414.74
fromPGP_crf = 0.080586404
fromPGP_fixed_om = 13.056
hours_per_year = 8760
#c_fixed_base = (0.080586404 * 1706.46 + 13.056) / 8760
c_fixed_base = (fromPGP_crf * fromPGP_base_capitalcost + fromPGP_fixed_om) / hours_per_year
print('c_fixed_base', c_fixed_base)

#base_capitalcost = annual_capitalcost * hours_per_year / toPGP_crf
base_overnightcapital = ((c_fixed_base * hours_per_year) - fromPGP_fixed_om)  / fromPGP_crf
print('base_overnightcapital', base_overnightcapital)



X2 = [i * 100 for i in fromPGP_eff]
Y2 = [((i * hours_per_year) - fromPGP_fixed_om) / fromPGP_crf for i in fromPGP_cost]
#Y2 = [i * hours_per_year for i in fromPGP_cost]
#Y2 = [i * hours_per_year / fromPGP_crf for i in fromPGP_cost]
Z2 = system_cost2

#%%Get back capital cost from annualized capital cost

#STORAGE UPDATE THIS
PGPstorage_base_capitalcost = 2
PGPstorage_crf = 0.080586404 #UPDATE THIS
PGPstorage_fixed_om = 0 #STORAGE UPDATE THIS
hours_per_year = 8760 
#c_fixed_base = (0.080586404 * 1706.46 + 13.056) / 8760
c_fixed_base = (PGPstorage_crf * PGPstorage_base_capitalcost + PGPstorage_fixed_om) / hours_per_year
print('c_fixed_base', c_fixed_base)

#base_capitalcost = annual_capitalcost * hours_per_year / toPGP_crf
base_overnightcapital = ((c_fixed_base * hours_per_year) - PGPstorage_fixed_om)  / PGPstorage_crf
print('base_overnightcapital', base_overnightcapital)


X3 = [i * 100 for i in PGP_eff]
Y3 = [((i * hours_per_year) - PGPstorage_fixed_om) / PGPstorage_crf for i in PGPstorage_cost]
#Y2 = [i * hours_per_year for i in fromPGP_cost]
#Y2 = [i * hours_per_year / fromPGP_crf for i in fromPGP_cost]

Z3 = system_cost3

#%% Display Z

#z = np.transpose(np.array(Z).reshape(10,10))
#z2 = np.transpose(np.array(Z2).reshape(10,10))
#disp = pd.DataFrame(z2).round(3)

#%% Contour Plot

#%% Plot Settings

import matplotlib.pylab as pylab
params = {'legend.fontsize': 'medium',
          'figure.figsize': (4, 12),
         'axes.labelsize': 'large',
         'axes.titlesize':'large',
         'xtick.labelsize':'large',
         'ytick.labelsize':'large'}
pylab.rcParams.update(params)

cmap = cm.get_cmap('viridis_r')

#%% Make Plot

#%% ELECTROLZYER

fig = plt.figure()
ax1 = plt.subplot2grid((3,1), (0,0))
#ax1.set_aspect('equal')

# Plot Title
ax1.set_title("Power-to-H$_{2}$")
# X Axis
#plt.xscale('log')
#ax1.set_xlim(0, 100)
ax1.set_xlabel('Power-to-H$_{2}$\nefficiency (%)')


# 1st Y axis
#plt.yscale('log')
ax1.set_ylim(0, 6000)
ax1.set_xlim(0, 100)
ax1.set_ylabel('Capital cost (\$/kW)')
ax1.xaxis.set_major_formatter(ticker.PercentFormatter())
#plt.axis('square')

color_map = plt.cm.get_cmap('Spectral')
#levels = [0.0600, 0.0625, 0.0650, 0.0675, 0.0700, 0.0725, 0.0750, 0.0775, 0.0800, 0.0825]
#levels = [0.00, 0.02, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12, 0.13, 0.14]
#levels = [0.06, 0.0625, 0.065, 0.0675, 0.07,0.0725, 0.075,0.0775, 0.08,0.0825, 0.085, 0.0875, 0.09,0.0925,0.095]
levels = [0.05, 0.055,0.06, 0.065, 0.07, 0.075, 0.08, 0.085,  0.09,0.095, .10, .105,.11,.115,.12]
cpf = ax1.tricontourf(X, Y, Z, levels, cmap=cmap)

levels_short = [0.060, 0.065, 0.070, 0.075, 0.080, 0.085,0.09]
cp = ax1.tricontour(X, Y, Z, levels=levels_short, colors='k')

#cp2 = ax1.tricontour(X, Y, Z, levels=levels_shorter, colors='k')
#cp = ax1.tricontour(X, Y, Z, colors='k')


levels_shorter = [0.060, 0.065, 0.070, 0.075, 0.080, 0.085]
q = plt.clabel(cp, levels_shorter, inline=1, fontsize=12)

# # Colorbar
# Colorbar
# cbar = plt.colorbar(cpf)
# cbar.ax.set_ylabel('System cost ($/kWh)')
# cbar.set_ticks(levels_short)

# Specific points
ax1.scatter(50, 1706.46 , marker="o", color='pink', s=50)
ax1.annotate('PEM\nElectrolysis', (50, 1706.46), xytext=(0, 20), 
             textcoords='offset pixels', color='pink', size='medium', fontweight='bold', va='center', ha='center')

#ax1.scatter(74, 0.020906 *hours_per_year , marker="o", color='white', s=50)
#ax1.annotate('Steam methane\nreforming', (74, 0.020906*hours_per_year), xytext=(-30, 10), 
#             textcoords='offset pixels', color='white', size='medium', fontweight='bold')


#ax1.set_box_aspect(1)

#%% FUEL CELL

ax2 = plt.subplot2grid((3,1), (2,0))
#ax2.set_aspect('equal')
ax2.set_title("H$_{2}$-to-Power")

# X Axis
#plt.xscale('log')
#ax2.set_xlim(10, 1000)
#ax2.set_xlabel('H$_{2}$-to-Power efficiency (%)', labelpad=15)
ax2.set_xlabel('H$_{2}$-to-Power\nefficiency (%)')
ax2.set_ylabel('Capital cost (\$/kW)')


# 1st Y axis
#plt.yscale('log')
ax2.set_ylim(0, 6000)
ax2.set_xlim(0, 100)
ax2.xaxis.set_major_formatter(ticker.PercentFormatter())

levels = [0.05, 0.055,0.06, 0.065, 0.07, 0.075, 0.08, 0.085,  0.09,0.095, .10, .105,.11,.115,.12]
#levels = [0.074, 0.075, 0.076, 0.077, 0.078, 0.079, 0.080, 0.081]
cpf = ax2.tricontourf(X2, Y2, Z2, levels, cmap=cmap)
#cpf = ax2.tricontourf(X2, Y2, Z2,  cmap=cmap)

levels_short = [0.06, 0.07, 0.08, 0.09, .10,.11,.12]
cp = ax2.tricontour(X2, Y2, Z2, levels=levels_short, colors='k')
#cp = ax2.tricontour(X2, Y2, Z2,  colors='k')
#fmt = ticker.FormatStrFormatter('$%.4f')
q = plt.clabel(cp, inline=1, fontsize=12)

# Colorbar
# Colorbar
# cbar = plt.colorbar(cpf)
# cbar.ax.set_ylabel('System cost ($/kWh)')
# cbar.set_ticks(levels_short)

#ax2.set_box_aspect(1)

# Specific Points
ax2.scatter(70, 4600, marker="o", color='white', s=50)
ax2.annotate('Molten\ncarbonate\nfuel cell', (70, 4600), xytext=(0, 20), 
             textcoords='offset pixels', color='w', size='medium', fontweight='bold', va='center', ha='center')

ax2.scatter(71, 1414.74, marker="o", color='pink', s=50)
ax2.annotate('PEM\nfuel cell', (71, 1414.74), xytext=(15, 20),
             textcoords='offset pixels', color='pink', size='medium', fontweight='bold', va='center', ha='center')

ax2.scatter(50, 1000, marker="o", color='white', s=50)
ax2.annotate('Hydrogen\nturbine', (50, 1000), xytext=(-15, 20),
             textcoords='offset pixels', color='w', size='medium', fontweight='bold', va='center', ha='center')
#%% STORAGE

ax3 = plt.subplot2grid((3,1), (1,0))
#ax2.set_aspect('equal')
ax3.set_title("H$_{2}$ Storage")

# X Axis
#plt.xscale('log')
#ax2.set_xlim(10, 1000)
#ax2.set_xlabel('H$_{2}$-to-Power efficiency (%)', labelpad=15)
ax3.set_xlabel('Power-H$_{2}$-Power\nround-trip efficiency (%)')
ax3.set_ylabel('Capital cost (\$/kWh)')


# 1st Y axis
#plt.yscale('log')
# ax2.set_ylim(0, 6000)
ax3.set_xlim(0, 100)
ax3.xaxis.set_major_formatter(ticker.PercentFormatter())

ax3.set_yscale('log')
ax3.yaxis.set_major_formatter(ScalarFormatter())

levels = [0.05, 0.055,0.06, 0.065, 0.07, 0.075, 0.08, 0.085,  0.09,0.095, .10, .105,.11,.115,.12]
# levels = [0.074, 0.075, 0.076, 0.077, 0.078, 0.079, 0.080, 0.081]
cpf = ax3.tricontourf(X3, Y3, Z3, levels, cmap=cmap)
# cpf = ax3.tricontourf(X3, Y3, Z3,  cmap=cmap)

levels_short = [0.06, 0.07, 0.08, 0.09, .10,.11,.12]
cp = ax3.tricontour(X3, Y3, Z3, levels=levels_short, colors='k')
# cp = ax3.tricontour(X3, Y3, Z3,  colors='k')
# fmt = ticker.FormatStrFormatter('$%.4f')
q = plt.clabel(cp, inline=1, fontsize=12)

# Colorbar
# cbar = plt.colorbar(cpf)
# cbar.ax.set_ylabel('System cost ($/kWh)')
# cbar.set_ticks(levels_short)

#ax2.set_box_aspect(1)

# Specific Points #UPDATE
base_x = 36  #base efficiency
ax3.scatter(base_x,0.038, marker="o", color='w', s=50)
ax3.annotate('Depleted\nreservoir', (base_x, 0.038), xytext=(0, 20), 
            textcoords='offset pixels', color='w', size='medium', fontweight='bold', va='center', ha='center')

ax3.scatter(base_x,2, marker="o", color='pink', s=50)
ax3.annotate('Salt\ncavern', (base_x, 2), xytext=(0, 20), 
            textcoords='offset pixels', color='pink', size='medium', fontweight='bold', va='center', ha='center')

ax3.scatter(base_x, 15, marker="o", color='w', s=50)
ax3.annotate('Above-\nground\ntank', (base_x, 15), xytext=(0, 20), 
            textcoords='offset pixels', color='w', size='medium', fontweight='bold', va='center', ha='center')


#%% cost info

    # if knob1 == 'tank': #tanks
    #     tech_list[storage_PGP_idx]['fixed_cost'] = 0.000140074 #($15/kWh) #1.61524E-04
    #     tech_list[storage_PGP_idx]['decay_rate'] = 1.14155E-08 #(0.01%/year)
        
    # if knob1 == 'salt': #salt cavern #BASE CASE
    #     tech_list[storage_PGP_idx]['fixed_cost'] = 1.86672E-05 #($2/kWh)
    #     tech_list[storage_PGP_idx]['decay_rate'] = 1.14E-08 #(0.01%/year)
    
    # if knob1 == 'dpr': #depleted reservior
    #     tech_list[storage_PGP_idx]['fixed_cost'] = 3.61392E-07 # ($0.038/kWh)
    #     tech_list[storage_PGP_idx]['decay_rate'] = 3.99543E-08 #(0.035%/year)
        
    # if knob2 == 'mcfc': #molten carbonate fuel cell
    #     tech_list[from_PGP_idx]['fixed_cost'] = 0.044442228 #($4,600/kW)
    #     tech_list[from_PGP_idx]['efficiency'] = 0.7
        
    # if knob2 == 'pemfc': #PEM fuel cell #BASE CASE
    #     tech_list[from_PGP_idx]['fixed_cost'] = 0.014700336 #($1414.74/kW)
    #     tech_list[from_PGP_idx]['efficiency'] = 0.71
    
    # if knob2 == 'h2tur': #hydrogen turbine
    #     tech_list[from_PGP_idx]['fixed_cost'] = 1.07683E-02 #($1000/kW)
    #     tech_list[from_PGP_idx]['efficiency'] = 0.5
    
plt.tight_layout()
plt.savefig('contour_effcost_3panel.pdf', bbox_inches='tight')
plt.show()

