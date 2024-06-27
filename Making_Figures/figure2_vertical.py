#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 15:47:00 2023

@author: jacquelinedowling
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
from operator import add

# print(len(dates))

#%% Import Functions

from extract_data_pgp_model import get_data 

#%% Get Data

path = '/Users/jacquelinedowling/MEM/Output_Data/to_PGPPGP_storagefrom_PGPfixed_costefficiency'
data = get_data(path, 5, 'fixed_cost')

# toPGP_cost = data['toPGP_cost']
PGP_eff = data['PGP_eff']
PGP_cost = data['pgp_cost']
system_cost = data['system_cost']

wind_avg_dispatch = data['wind_avg_dispatch']
solar_avg_dispatch = data['solar_avg_dispatch']

curtail = data['main_curtailment']
pgp_storage_cap = data['PGP_storage capacity']
pgp_output_cap = data['from_PGP capacity']
pgp_input_cap = data['to_PGP capacity']


cost_elec_to_main_demand = data['cost_elec_to_main_demand']
cost_elec_to_PGP = data['cost_elec_to_PGP']
cost_elec_from_PGP = data['cost_elec_from_PGP']


# path = '/Users/jacquelinedowling/MEM/Output_Data/from_PGPfrom_PGP'
# data2 = get_data(path, 7, 'fixed_cost')

# fromPGP_cost = data2['fromPGP_cost']
# fromPGP_eff = data2['fromPGP_eff']
# system_cost2 = data2['system_cost']

#path = '/Users/jacquelinedowling/MEM/Output_Data/batterybattery'
#data3 = get_data(path, 4, 'fixed_cost')
#
#batt_cost = data3['batt_fixed_cost']
#batt_eff = data3['batt_eff']
#system_cost2 = data3['system_cost']

#%% Format Data for Plot

# Get back capital cost from annualized capital cost

#TPGP cos vs. eff
# toPGP_base_capitalcost = 1706.46
# toPGP_crf = 0.080586404
# toPGP_fixed_om = 13.056
# hours_per_year = 8760
# #c_fixed_base = (0.080586404 * 1706.46 + 13.056) / 8760
# c_fixed_base = (toPGP_crf * toPGP_base_capitalcost + toPGP_fixed_om) / hours_per_year
# print('c_fixed_base', c_fixed_base)

# #base_capitalcost = annual_capitalcost * hours_per_year / toPGP_crf
# base_overnightcapital = ((c_fixed_base * hours_per_year) - toPGP_fixed_om)  / toPGP_crf
# print('base_overnightcapital', base_overnightcapital)

basecost = 0.017424228 + 1.87E-05 + 0.014700336
X = [i * 100 for i in PGP_eff]
Y = [i * (1/basecost) * (100) for i in PGP_cost]
# Y = [i * (1/1) * (100) for i in PGP_cost]
# Y = [j  for j in PGP_cost]
# Y = [((i * hours_per_year) - toPGP_fixed_om) / toPGP_crf for i in toPGP_cost]
#Y = [i * hours_per_year for i in toPGP_cost]
Z = system_cost
 
ys = sorted(Y)
xyz_s = sorted(zip(X, Y, Z))

X2 = X
Y2 = Y
Z2 = list(map(add, wind_avg_dispatch, solar_avg_dispatch))

X3 = X
Y3 = Y
# Z3 = curtail
Z3 = cost_elec_to_PGP


X4 = X
Y4 = Y
Z4 = pgp_storage_cap

X5 = X
Y5 = Y
Z5 = pgp_input_cap

X6 = X
Y6 = Y
Z6 = pgp_output_cap

#%% Format Data for Plot

# # Get back capital cost from annualized capital cost

# #TO PGP
# toPGP_base_capitalcost = 1706.46
# toPGP_crf = 0.080586404
# toPGP_fixed_om = 13.056
# hours_per_year = 8760
# #c_fixed_base = (0.080586404 * 1706.46 + 13.056) / 8760
# c_fixed_base = (toPGP_crf * toPGP_base_capitalcost + toPGP_fixed_om) / hours_per_year
# print('c_fixed_base', c_fixed_base)

# #base_capitalcost = annual_capitalcost * hours_per_year / toPGP_crf
# base_overnightcapital = ((c_fixed_base * hours_per_year) - toPGP_fixed_om)  / toPGP_crf
# print('base_overnightcapital', base_overnightcapital)


# X = [i * 100 for i in toPGP_eff]
# Y = [((i * hours_per_year) - toPGP_fixed_om) / toPGP_crf for i in toPGP_cost]
# #Y = [i * hours_per_year for i in toPGP_cost]
# Z = system_cost

#%% FROM PGP


# fromPGP_base_capitalcost = 1414.74
# fromPGP_crf = 0.080586404
# fromPGP_fixed_om = 13.056
# hours_per_year = 8760
# #c_fixed_base = (0.080586404 * 1706.46 + 13.056) / 8760
# c_fixed_base = (fromPGP_crf * fromPGP_base_capitalcost + fromPGP_fixed_om) / hours_per_year
# print('c_fixed_base', c_fixed_base)

# #base_capitalcost = annual_capitalcost * hours_per_year / toPGP_crf
# base_overnightcapital = ((c_fixed_base * hours_per_year) - fromPGP_fixed_om)  / fromPGP_crf
# print('base_overnightcapital', base_overnightcapital)



# X2 = [i * 100 for i in fromPGP_eff]
# Y2 = [((i * hours_per_year) - fromPGP_fixed_om) / fromPGP_crf for i in fromPGP_cost]
# #Y2 = [i * hours_per_year for i in fromPGP_cost]
# #Y2 = [i * hours_per_year / fromPGP_crf for i in fromPGP_cost]
# Z2 = system_cost2

#%% Display Z

#z = np.transpose(np.array(Z).reshape(10,10))
#z2 = np.transpose(np.array(Z2).reshape(10,10))
#disp = pd.DataFrame(z2).round(3)

#%% Contour Plot

#%% Plot Settings

# import matplotlib.pylab as pylab
# params = {'legend.fontsize': 'medium',
#           'figure.figsize': (10, 8),
#          'axes.labelsize': 'large',
#          'axes.titlesize':'x-large',
#          'xtick.labelsize':'large',
#          'ytick.labelsize':'large'}
# pylab.rcParams.update(params)


import matplotlib.pylab as pylab
params = {'legend.fontsize': 'medium',
          'figure.figsize': (9, 10),
         'axes.labelsize': 'large',
         'axes.titlesize':'large',
         'xtick.labelsize':'large',
         'ytick.labelsize':'large'}
pylab.rcParams.update(params)
cmap = cm.get_cmap('viridis_r')

#%% Make Plot

#%% Full Plot

fig = plt.figure()
ax1 = plt.subplot2grid((3,2), (0,0))
#ax1.set_aspect('equal')

ax1.set_xlabel('H$_{2}$ round-trip efficiency')


# 1st Y axis
#plt.yscale('log')
ax1.set_ylim(0, 100)
ax1.set_xlim(0, 100)
ax1.set_ylabel('H$_{2}$ total capital cost (% of base case)')
ax1.set_title('System cost ($/kWh)')
ax1.xaxis.set_major_locator(ticker.MultipleLocator(25))
ax1.yaxis.set_major_locator(ticker.MultipleLocator(25))
ax1.xaxis.set_major_formatter(ticker.PercentFormatter())
ax1.yaxis.set_major_formatter(ticker.PercentFormatter())

#plt.axis('square')

#levels = [0.0600, 0.0625, 0.0650, 0.0675, 0.0700, 0.0725, 0.0750, 0.0775, 0.0800, 0.0825]
#levels = [0.00, 0.02, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12, 0.13, 0.14]
#levels = [0.06, 0.0625, 0.065, 0.0675, 0.07,0.0725, 0.075,0.0775, 0.08,0.0825, 0.085, 0.0875, 0.09,0.0925,0.095]
# levels = [0.05, 0.055,0.06, 0.065, 0.07, 0.075, 0.08, 0.085,  0.09,0.095, .10, .105,.11,.115,.12,.13]
levels = [0.04,0.045, 0.05,0.055, 0.06,0.065, 0.07, 0.075,0.08, 0.085,0.09,0.095, .10, .105,.11,.115,.12]

cpf = ax1.tricontourf(X, Y, Z, levels, cmap=cmap)


# levels_short = [0.060, 0.065, 0.070, 0.075, 0.080, 0.085,0.09]
levels_short = [0.04, 0.05, 0.06, 0.07,  0.08 ,0.09, 0.10, .11, .12]
levels_shorter = [0.04, 0.05, 0.06, 0.07,  0.08 ,0.09]
cp = ax1.tricontour(X, Y, Z, levels=levels_short, colors='k')
# levels_shorter = [0.060, 0.065, 0.070, 0.075, 0.080, 0.085]
#cp2 = ax1.tricontour(X, Y, Z, levels=levels_shorter, colors='k')
#cp = ax1.tricontour(X, Y, Z, colors='k')

q = plt.clabel(cp, inline=1, fontsize=12, levels=levels_shorter)

# Colorbar
s=.9
cbar = plt.colorbar(cpf, shrink = s)
cbar.ax.set_ylabel('$/kWh')
# cbar.add_lines(cp)
# cbar.set_ticks(levels)


## Specific points
# ax1.scatter(36, 100, marker="o", color='white', s=50)
# ax1.annotate('PEM\nElectrolysis', (36, 100), xytext=(-30, 20), 
            # textcoords='offset pixels', color='w', size='medium', fontweight='bold')


# ax1.set_box_aspect(1)

#%% Zoomed in Plot

ax2 = plt.subplot2grid((3,2), (1,0))

# #ax2.set_aspect('equal')
# #ax2.set_title("H$_{2}$-to-Power")

# # X Axis
# #plt.xscale('log')
# #ax2.set_xlim(10, 1000)
# #ax2.set_xlabel('H$_{2}$-to-Power efficiency (%)', labelpad=15)
ax2.set_xlabel('H$_{2}$ round-trip efficiency')
ax2.set_ylabel('H$_{2}$ total capital cost (% of base case)')
ax2.set_title('Wind + solar dispatch (kW)')

# # 1st Y axis
# #plt.yscale('log')
# ax2.set_ylim(0, 6000)
ax2.set_xlim(0, 100)
ax2.set_ylim(0, 100)

levels = [1.001,1.05,1.1,1.15, 1.2,1.25, 1.3, 1.35,1.4, 1.45,1.5, 1.55,1.6,1.65, 1.7,1.75,1.8,1.85,1.9,1.95,2]

levels_short = [1, 1.1, 1.2, 1.3, 1.4,  1.5]

levels_shorter = [1.0, 1.1, 1.2, 1.3, 1.4,  1.5, 1.6, 1.7, 1.8,1.9,2]
# levels_shorter = [1.0,  1.2,  1.4,   1.6, 1.8,2]
# levels_shorter = [0.9,1.0,  1.1, 1.2, 1.3, 1.4,  1.5, 1.6, 1.7,1.8]
# levels = [0.05, 0.055,0.06, 0.065, 0.07, 0.075, 0.08, 0.085,  0.09,0.095, .10, .105,.11,.115,.12]
# #levels = [0.074, 0.075, 0.076, 0.077, 0.078, 0.079, 0.080, 0.081]
cmap = plt.colormaps['viridis_r'].with_extremes(under="white", over="gray")
cpf = ax2.tricontourf(X2, Y2, Z2, levels=levels, cmap=cmap, extend='min')
# cpf = ax2.tricontourf(X2, Y2, Z2,  cmap=cmap)

# levels_short = [0.06, 0.07, 0.08, 0.09, .10,.11,.12]
cp = ax2.tricontour(X2, Y2, Z2, levels=levels_short, colors='k')
# #cp = ax2.tricontour(X2, Y2, Z2,  colors='k')
fmt = ticker.FormatStrFormatter('$%.4f')
q = plt.clabel(cp, inline=1, fontsize=12)


# # Colorbar
cbar = plt.colorbar(cpf, shrink = s)
cbar.ax.set_ylabel('1 = mean U.S. demand')
cbar.set_ticks(levels_shorter)
# cbar.add_lines(cp)

# levels = [.999, 1.001]
# ax2.tricontourf(X2, Y2, Z2, levels=levels, colors='w')

# ax2.set_box_aspect(1)

#%% Zoomed in Plot

ax3 = plt.subplot2grid((3,2), (2,0))
# #ax2.set_aspect('equal')
# #ax2.set_title("H$_{2}$-to-Power")

# # X Axis
# #plt.xscale('log')
# #ax2.set_xlim(10, 1000)
# #ax2.set_xlabel('H$_{2}$-to-Power efficiency (%)', labelpad=15)
ax3.set_xlabel('H$_{2}$ round-trip efficiency')
ax3.set_ylabel('H$_{2}$ total capital cost (% of base case)')
ax3.set_title('Mean instantaneous cost of\n electrolyzer buying electricity')

# # 1st Y axis
# #plt.yscale('log')
ax3.set_ylim(0, 100)
ax3.set_xlim(0, 100)
levels = [0,0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,0.01]
levels_short = [0.001,0.003,0.005,0.007,0.009]
levels_shorter = [0.001,0.003,0.005,0.007,0.009]
# levels_short = [0,0.002,0.004,0.006,0.008,0.01]
# levels_shorter = [0.002,0.004,0.006,0.008,0.01]


cmap = plt.colormaps['viridis_r'].with_extremes(under="white", over="gray")
cpf = ax3.tricontourf(X3, Y3, Z3, cmap=cmap, levels=levels, extend='min')
cp = ax3.tricontour(X3, Y3, Z3, levels=levels_shorter, colors='k')
# cp = ax3.tricontour(X3, Y3, Z3,  colors='k')
q = plt.clabel(cp, inline=1, fontsize=12, levels=levels_shorter)

# # Colorbar
cbar = plt.colorbar(cpf, shrink = s, extend='min')
cbar.ax.set_ylabel('$/kWh')
# cbar.set_ticks(levels_shorter)
# levels = [-.0001, 0.0001]
# plt.tricontourf(X3, Y3, Z3, levels=levels, colors='w')


#%% Zoomed in Plot

ax4 = plt.subplot2grid((3,2), (1,1))
cmap = cm.get_cmap('cool')
# #ax2.set_aspect('equal')
# #ax2.set_title("H$_{2}$-to-Power")

# # X Axis
# #plt.xscale('log')
# #ax2.set_xlim(10, 1000)
# #ax2.set_xlabel('H$_{2}$-to-Power efficiency (%)', labelpad=15)
ax4.set_xlabel('H$_{2}$ round-trip efficiency')
ax4.set_ylabel('H$_{2}$ total capital cost (% of base case)')
ax4.set_title('H$_{2}$ storage capacity (kWh)')

ax4.set_xlim(0, 100)
ax4.set_ylim(0, 100)

levels = [0,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400]
levels_short = [0,200,400,600,800,1000,1200,1400]
levels_shorter = [0,200,400,600,800,1000,1200,1400]
levels_shortest = [400,600,800,1000]

cmap = plt.colormaps["cool"].with_extremes(under="white", over="gray")
cs = ax4.tricontourf(X4, Y4, Z4, levels, cmap=cmap, extend="min")
CS2 = ax4.tricontour(cs, levels=levels_shorter, colors='k')
q = plt.clabel(CS2, inline=1, fontsize=12, levels=levels_shortest)
cbar = plt.colorbar(cs, shrink = s)
cbar.ax.set_ylabel('hours of mean U.S. demand')



#%% Zoomed in Plot

ax5 = plt.subplot2grid((3,2), (0,1))
cmap = cm.get_cmap('cool')
ax5.set_xlabel('H$_{2}$ round-trip efficiency')
ax5.set_ylabel('H$_{2}$ total capital cost (% of base case)')
ax5.set_title('H$_{2}$ electrolyzer capacity (kW)')
ax5.set_xlim(0, 100)
ax5.set_ylim(0, 100)
levels = [0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1,1.1,1.2,1.3,1.4]
levels_short = [0.0, 0.2,0.4,0.6,0.8,1,1.2,1.4]
levels_shorter = [0,0.2,0.4,0.6,0.8,1]
levels_shortest = [0,0.4,0.6,0.8,1]
# cpf = ax5.tricontourf(X5, Y5, Z5, levels=levels_short, cmap=cmap)
# cpf = ax5.tricontourf(X5, Y5, Z5,  cmap=cmap)
# levels_short = [0.06, 0.07, 0.08, 0.09, .10,.11,.12]
# cp = ax5.tricontour(X5, Y5, Z5, levels=levels_short, colors='k')
# cp = ax5.tricontour(X5, Y5, Z5,  colors='k')
# fmt = ticker.FormatStrFormatter('$%.4f')
# q = plt.clabel(cp, inline=1, fontsize=12)
# # Colorbar
# cbar = plt.colorbar(cpf, shrink = s)
# cbar.ax.set_ylabel('1 = mean U.S. demand')
cmap = plt.colormaps["cool"].with_extremes(under="white", over="gray")
cs = ax5.tricontourf(X5, Y5, Z5, levels, cmap=cmap, extend="min")
CS2 = ax5.tricontour(cs, levels=levels_shorter, colors='k')
q = plt.clabel(CS2, inline=1, fontsize=12, levels=levels_shortest)
cbar = plt.colorbar(cs, shrink = s)
cbar.ax.set_ylabel('1 = mean U.S. demand')
# cbar.add_lines(CS2)
# levels = [-0.001, .13]
# ax5.tricontourf(X5, Y5, Z5, levels=levels, colors='w')


#%% Zoomed in Plot

ax6 = plt.subplot2grid((3,2), (2,1))
cmap = cm.get_cmap('cool')
ax6.set_xlabel('H$_{2}$ round-trip efficiency')
ax6.set_xlabel('Power-H$_{2}$-Power round-trip efficiency')
ax6.set_ylabel('H$_{2}$ total capital cost (% of base case)')
ax6.set_title('H$_{2}$ fuel cell capacity (kW)')
ax6.set_xlim(0, 100)
ax6.set_ylim(0, 100)
levels = [0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1,1.1,1.2,1.3,1.4]
levels_short = [0.0, 0.2,0.4,0.6,0.8,1,1.2,1.4]
levels_shorter = [0,0.4,0.6,0.8,1]
levels_shortest = [0.6,0.8,1]
# cpf = ax6.tricontourf(X6, Y6, Z6, levels=levels_short, cmap=cmap)
# # cpf = ax6.tricontourf(X6, Y6, Z6,  cmap=cmap)
# cp = ax6.tricontour(X6, Y6, Z6, levels=levels_shorter, colors='k')
# # cp = ax6.tricontour(X6, Y6, Z6,  colors='k')
# # fmt = ticker.FormatStrFormatter('$%.4f')
# q = plt.clabel(cp, inline=1, fontsize=12)
# # # Colorbar
# cbar = plt.colorbar(cpf, shrink = s)
# # cbar.ax.set_ylabel('H$_{2}$ out capacity \n(1 kW = mean U.S. demand)')
# cbar.ax.set_ylabel('1 = mean U.S. demand')
# cbar.set_ticks(levels_short)
cmap = plt.colormaps["cool"].with_extremes(under="white", over="gray")
cs = ax6.tricontourf(X6, Y6, Z6, levels, cmap=cmap, extend="min")
# cs = ax6.tricontourf(X6, Y6, Z6, levels_short, cmap=cmap, extend="both")
CS2 = ax6.tricontour(cs, levels=levels_short, colors='k')
q = plt.clabel(CS2, inline=1, fontsize=12, levels=levels_shortest)
cbar = plt.colorbar(cs, shrink = s)
cbar.ax.set_ylabel('1 = mean U.S. demand')
# cbar.add_lines(CS2)


#%% Full figure things

axlist = [ax1, ax2, ax3, ax4, ax5, ax6]
    
xlabel = 'Power-H$_{2}$-Power\nround-trip efficiency'
ylabel = 'Power-H$_{2}$-Power\ncapital cost\n(% of base case)'
# titlelist = ['System cost ($/kWh)',
#              'Wind + solar dispatch (kW)',
#              'Mean instanteous cost of\n electrolyzer buying electricity',
#              'H$_{2}$ storage capacity (kWh)',
#              'H$_{2}$ electrolyzer capacity (kW)',
#              'H$_{2}$ fuel cell capacity (kW)']

titlelist = ['System cost ($/kWh)',
             'Wind + solar dispatch (kW)',
             'Mean instantaneous cost of\n electrolyzer buying electricity',
             'H$_{2}$ storage capacity (kWh)',
             'Power-to-H$_{2}$ capacity (kW)',
             'H$_{2}$-to-Power capacity (kW)']

for z,i in enumerate(axlist):
    i.set_xlabel(xlabel)
    i.set_ylabel(ylabel)
    i.set_title(titlelist[z])
    i.axvline(x=36, color='white', linestyle='-', linewidth=1.5)
    i.xaxis.set_major_locator(ticker.MultipleLocator(25))
    i.yaxis.set_major_locator(ticker.MultipleLocator(25))
    i.xaxis.set_major_formatter(ticker.PercentFormatter())
    i.yaxis.set_major_formatter(ticker.PercentFormatter())


axlist_noy = [ax4, ax5, ax6]
for z,i in enumerate(axlist_noy):
    i.set_ylabel('')
    
axlist_nox = [ax1, ax2, ax4, ax5]
for z,i in enumerate(axlist_nox):
    i.set_xlabel('')

# xticks = [*ax1.get_xticks(),36]
# xticklabels = [*ax1.get_xticklabels(), 36]
# ax1.set_xticks(xticks, labels=xticklabels)


plt.tight_layout()
plt.savefig('contour_costPGP_effPGP_6panel.pdf', bbox_inches='tight')
plt.show()

