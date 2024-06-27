#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 16:36:13 2021

@author: jacquelinedowling
"""

#NG Sweeps

import pickle
import numpy as np
import matplotlib.pyplot as plt
import glob
import matplotlib.ticker as ticker
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FormatStrFormatter

#tech_list[0] is demand
#tech_list[1] is curtainment
#tech_list[2] is solar
#techlist[3] is wind
#techlist[4] is battery
#techlist[5] is to_PGP
#techlist[6] is PGP_storage
#technlist[7] is from_PGP

#dict_keys(['tech_name', 'tech_type', 'node_to', 'series_file', 'fixed_cost'])
#dict_keys(['tech_name', 'tech_type', 'node_to', 'node_from', 'fixed_cost', 'var_cost', 'efficiency', 'charging_time', 'decay_rate'])
#dict_keys(['tech_name', 'tech_type', 'node_to', 'node_from', 'fixed_cost', 'var_cost', 'efficiency'])

#======================================================
def get_cost_contributions(base):
    #mulitply var cost by dispatch
    #multiply fixed cost by capacity
    info = base[0]
    inputs = base[0][1]
    results = base[1]
    name_list = []
    fixed_costs = []
    var_costs = []
#    print(inputs)
    for tech in inputs:
        if tech['tech_name'] == 'demand':
            continue
        if tech['tech_name'] == 'main_curtailment':
            continue
        name_list.append(tech['tech_name'])
        fixed_costs.append(tech['fixed_cost'])
        if 'var_cost' in tech:
            var_costs.append(tech['var_cost'])
        else:
            var_costs.append(0)
#    print(name_list)
#    print(fixed_costs)
    caps = []
    disps = []
    for i in name_list:
        caps.append(results[1][str(i) + ' capacity'])
        if i == 'wind' or i =='PV':
            disps.append(np.mean(results[2][str(i) + ' potential'])) 
        else:
            disps.append(np.mean(results[2][str(i) + ' dispatch']))
    cost_list = []
    for i in range(len(name_list)):
        cost_list.append(fixed_costs[i]*caps[i] + var_costs[i]*disps[i])
    costconts = {}
    for k, v in zip(name_list, cost_list):
        costconts[k] = v
        
    return costconts
#======================================================
    

#======================================================
    
def getsweepdata(path, var):
    unsortedlist = glob.glob(path + '/*.pickle')
    #Get fixed values for x axis for toPGP
    par_list = []
    for i in range(len(unsortedlist)):
        pickle_in = open(unsortedlist[i],"rb")
#        print(unsortedlist[i])
        base = pickle.load(pickle_in)
        info = base[0]
        inputs = base[0][1]
        results = base[1]
        #var, pickle
        par_list.append((info[0][var], base))
#        print(info[0][var])
#    print(par_list)
#    par_list_sorted = sorted(par_list)
    par_list.sort(key=lambda x:x[0])
    par_list_sorted = par_list
#    par_list_sorted = sorted(par_list)
#    print(par_list_sorted)
    
    varlist = [i[0] for i in par_list_sorted]
    baselist = [i[1] for i in par_list_sorted]
#    print(varlist)
    sun_cost=[]
    wind_cost=[]
    batt_cost=[]
    pgp_cost=[]
    elec_cap = []
    ng_cost = []
    system_cost =[]
    topgp_cost = []
    storagepgp_cost =[]
    frompgp_cost = []
    for base in baselist:
        info = base[0]
        inputs = base[0][1]
        results = base[1]
#        elec_cap.append(results[1]['to_PGP capacity'])
#        print(results[1])
        dic = get_cost_contributions(base)
        sun_cost.append(dic['PV'])
        wind_cost.append(dic['wind'])
        batt_cost.append(dic['battery'])
        pgp_cost.append(dic['to_PGP']+dic['PGP_storage']+dic['from_PGP'])
        ng_cost.append(dic['natgas'])
        system_cost.append(results[0]['system_cost'])
        topgp_cost.append(dic['to_PGP'])
        storagepgp_cost.append(dic['PGP_storage'])
        frompgp_cost.append(dic['from_PGP'])
    data = (varlist, wind_cost, sun_cost, batt_cost, pgp_cost, ng_cost,system_cost, topgp_cost, storagepgp_cost, frompgp_cost)
    return data


#======================================================
#======================================================



#======================================================
def plot(path, title, gridx, gridy, plotgridx, plotgridy, legend, xax, yax, sidetitle, st):
    data = getsweepdata(path, 'co2_constraint')
    varlist = data[0]
    wind_cost = data[1]
    sun_cost = data[2]
    batt_cost = data[3]
    pgp_cost = data[4]
    ng_cost = data[5]
    system_cost = data[6]
    topgp_cost = data[7]
    storagepgp_cost = data[8]
    frompgp_cost = data[9]

    print(title)
    x = np.array(varlist)*(1/4038.36)*100  #turn Co2 constraint into a percent
#    print(x)
#    print(pgp_cost)
#    print(x)
#    print(pgp_cost[10])
#    print(x[10])
    axline = 50
    for i in range(0, len(pgp_cost)):
#        print('pgp_cost[i], x[i]',pgp_cost[i], x[i])
#        print('x[i]',x[i])
#        if pgp_cost[i] == 0:
#        if pgp_cost[i] < 0.001:
#        print('pgp_cost[i]/system_cost[i]*100', pgp_cost[i]/system_cost[i]*100)
        if pgp_cost[i]/system_cost[i]*100 < 2:
#            print(pgp_cost[i-1])
#            print(x[i-1])
#            axline = x[i-1]
            axline = x[i]
            print('axline',axline)
            break

    y = np.vstack([ng_cost, wind_cost, sun_cost, batt_cost, topgp_cost, storagepgp_cost, frompgp_cost])
    pal = ['saddlebrown','blue', 'orange', 'purple', 'pink', 'tab:pink', 'm']
    labels = ["Natural Gas","Wind", "Solar", "Battery", "Power-to-H$_{2}$","H$_{2}$ Storage", "H$_{2}$-to-Power"]
    
    
#    y = np.vstack([wind_cost, sun_cost, batt_cost, topgp_cost, storagepgp_cost, frompgp_cost, ng_cost])
#    pal = ['blue', 'orange', 'purple', 'pink', 'tab:pink', 'm', 'saddlebrown']
#    labels = ["Wind", "Solar", "Battery", "Power-to-H$_{2}$","H$_{2}$ Storage", "H$_{2}$-to-Power","Natural Gas"]
#    
#    y = np.vstack([wind_cost, sun_cost, batt_cost, pgp_cost,ng_cost])
#    pal = ['blue', 'orange', 'purple', 'pink', 'saddlebrown']
#    labels = ["Wind", "Solar", "Battery", "PGP","Natural Gas"]
    
    #plotting Linear
    #ax3 = plt.subplot2grid((2, 3), (0, 0), colspan=2, rowspan=1)
    ax1 = plt.subplot2grid((gridx, gridy), (plotgridx, plotgridy), colspan=1, rowspan=1)
    ax1.stackplot(x, y, colors=pal, labels=labels)
    ax1.axvline(x=axline, color='tab:pink', linestyle='-', linewidth=1.5, label='H$_{2}$ enters ')
    # ax1.text(96, .10, 'a')
    
    #UNCOMMENT THIS FOR VALUES!!!!
    # ax1.text(3, .1, str(round(axline, 0))+ '%', color='tab:pink')

        # ax1.text(axline+10, .1, str(round(axline, 0))+ '%',fontweight='bold')
    #ax3.legend(loc='upper center', bbox_to_anchor=(1.25, 1.03))
    #chartBox = ax3.get_position()
    #ax3.set_position([chartBox.x0, chartBox.y0, chartBox.width, chartBox.height])
    #ax1.plot(x, elec_cap, color='red', linestyle='-', label = 'Electryolyzer\ncapacity')
    ax1.set_xscale('log')
    ax1.xaxis.set_major_formatter(ScalarFormatter())
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(0.04))
    ax1.xaxis.set_major_formatter(ticker.PercentFormatter())
    ax1.set_xlim(100,.9)
    ax1.set_ylim(0, 0.12)
    #ax3.xaxis.set_major_locator(ticker.MultipleLocator(.1))
    #ax3.xaxis.set_minor_locator(ticker.MultipleLocator(0.5))
    #ax3.xaxis.set_major_formatter(FormatStrFormatter('%gx'))
    #ax1.xaxis.set_major_formatter(ticker.PercentFormatter())
#    ax1.set_title(path.split('/')[-1])
    ax1.set_title(title)
    if sidetitle == True:
        ax1.set_ylabel(str(st))
        ax1.yaxis.set_label_position("right")
    if yax == True:
        ax1.set_ylabel('System cost ($/kWh)') #,color='white'
        ax2 = ax1.twinx()
        ax2.set_ylabel(st) #,color='white'
        ax2.yaxis.set_label_position("right")
        # ax2.yaxis.tick_right()
        ax2.set_yticks([])
        # ax2.spines['right'].set_visible(False)
        # ax2.axes.get_yaxis().set_visible(False)
    if xax == True:
        ax1.set_xlabel('Natural gas restriction\n(% of dispatch)')
    
    if legend == True:
        ax1.legend(loc='upper center', bbox_to_anchor=(1.35, 1.03))
        chartBox = ax1.get_position()
        ax1.set_position([chartBox.x0, chartBox.y0, chartBox.width*1, chartBox.height])

#======================================================
path1 = '/Users/jacquelinedowling/MEM/Output_Data/NG_tank_mcfc'
path2 = '/Users/jacquelinedowling/MEM/Output_Data/NG_tank_pemfc'
path3 = '/Users/jacquelinedowling/MEM/Output_Data/NG_tank_h2tur'    

path4 = '/Users/jacquelinedowling/MEM/Output_Data/NG_salt_mcfc'
path5 = '/Users/jacquelinedowling/MEM/Output_Data/NG_salt_pemfc'
path6 = '/Users/jacquelinedowling/MEM/Output_Data/NG_salt_h2tur'

path7 = '/Users/jacquelinedowling/MEM/Output_Data/NG_dpr_mcfc'
path8 = '/Users/jacquelinedowling/MEM/Output_Data/NG_dpr_pemfc'
path9 = '/Users/jacquelinedowling/MEM/Output_Data/NG_dpr_h2tur'

cc1 = "Aboveground tank\n($15/kWh)"
cc2 = "Salt cavern\n($2/kWh)"
cc3 = "Depleted reservoir\n($0.04/kWh)"

st1 = "MC fuel cell ($4,600/kW)"
st2 = "PEM fuel cell ($1,414/kW)"
st3 = "H$_{2}$ turbine ($1,000/kWh)"


c1 = "Aboveground tank"
c2 = "Salt cavern"
c3 = "Depleted reservoir"

# st1 = "MC fuel cell"
# st2 = "PEM fuel cell"
# st3 = "H$_{2}$ turbine"

nt = ''
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
    

# t1 = "Aboveground tank\n + MC fuel cell"
# t2 = "Aboveground tank\n + PEM fuel cell"
# t3 = "Aboveground tank\n + H$_{2}$ turbine"

# t4 = "Salt cavern\n + MC fuel cell"
# t5 = "Salt cavern\n + PEM fuel cell"
# t6 = "Salt cavern\n + H$_{2}$ turbine"

# t7 = "Depleted reservoir\n + MC fuel cell"
# t8 = "Depleted reservoir\n + PEM fuel cell"
# t9 = "Depleted reservoir\n + H$_{2}$ turbine"


##==============================================
plt.rcParams.update({'axes.titlesize': 'large'})
plt.rcParams.update({'axes.labelsize': 'large'})

import matplotlib.pylab as pylab
params = {'legend.fontsize': 'medium',
          'figure.figsize': (9, 8),
         'axes.labelsize': 'large',
         'axes.titlesize':'large',
         'xtick.labelsize':'large',
         'ytick.labelsize':'large'}
pylab.rcParams.update(params)
#================================================


fig = plt.figure()

#fig, ax = plt.subplots(nrows=3, ncols=3, sharex=True, sharey=True, figsize=(6, 6))
#
#fig.text(0.5, 0.04, 'common X', ha='center')
#fig.text(0.04, 0.5, 'common Y', va='center', rotation='vertical')

# def plot(path, title, gridx, gridy, plotgridx, plotgridy, legend, xax, yax, bold=False):
    

plot(path1, cc1, 3,3, 0 , 0, False, False, True, False,'MC fuel cell')
plot(path2, c1, 3,3, 1 , 0, False, False, True,False,"PEM fuel cell")
plot(path3, c1, 3,3, 2 , 0, False, True, True,False, 'H$_2$ turbine')

plot(path4, cc2, 3,3, 0 , 1, False, False, False, True,'MC fuel cell')
plot(path5, c2, 3,3, 1 , 1, False, False, False, True, "PEM fuel cell")
plot(path6, c2, 3,3, 2 , 1, False, True, False,True,  'H$_2$ turbine')

plot(path7, cc3, 3,3, 0 , 2, False, False, False, True,'MC fuel cell\n($4,600/kW)')
plot(path8, c3, 3,3, 1 , 2, False, False, False, True,"PEM fuel cell\n($1,414/kW)")
plot(path9, c3, 3,3, 2 , 2, False, True, False,True, 'H$_2$ turbine\n($1,000/kW)')

plt.tight_layout()
plt.savefig('ngsweep_9panel.pdf', bbox_inches='tight')
plt.savefig('ngsweep_9panel.png', bbox_inches='tight')
plt.show()


# ##==============================================
# plt.rcParams.update({'axes.titlesize': 'large'})
# plt.rcParams.update({'axes.labelsize': 'large'})

# import matplotlib.pylab as pylab
# params = {'legend.fontsize': 'medium',
#           'figure.figsize': (8, 10),
#          'axes.labelsize': 'large',
#          'axes.titlesize':'x-large',
#          'xtick.labelsize':'large',
#          'ytick.labelsize':'large'}
# pylab.rcParams.update(params)
# #================================================

# fig = plt.figure()
# plot(path1, nt, 3,1, 0 , 0, True,False, False)
# plot(path5, nt, 3,1, 1 , 0, False,False, True)
# plot(path9, nt, 3,1, 2 , 0, False,True, False)

# #fig.text(0.5, 0.04, 'common X', ha='center')
# #fig.text(0.5, 0.04, 'common X', ha='center')



# plt.tight_layout()
# plt.savefig('ngsweep_3panel.pdf', bbox_inches='tight')
# plt.show()