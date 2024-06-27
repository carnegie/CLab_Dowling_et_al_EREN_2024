#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 11:05:06 2023

@author: jacquelinedowling
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 18:23:22 2021

@author: jacquelinedowling
"""

#Cost sweeps

import pickle
import numpy as np
import matplotlib.pyplot as plt
import glob
import matplotlib.ticker as ticker
import pickle
import numpy as np
import matplotlib.pyplot as plt
import glob
import matplotlib.ticker as ticker
import csv
import pandas as pd

#%% Plot Settings


#tech_list[0] is demand
#tech_list[1] is curtainment
#tech_list[2] is solar
#techlist[3] is wind
#techlist[4] is battery
#techlist[5] is to_PGP
#techlist[6] is PGP_storage
#technlist[7] is from_PGP

#======================================================
def get_cost_contributions(base):
    #mulitply var cost by dispatch
    #multiply fixed cost by capacity
    info = base[0]
#    print(info)
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
#        print(tech.keys())
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
    
def getdata(path, techidx, var):
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
        par_list.append((inputs[techidx][var], base))
#    print(par_list)
#    par_list_sorted = sorted(par_list)
    par_list.sort(key=lambda x:x[0])
    par_list_sorted = par_list
#    par_list_sorted = sorted(par_list)
#    print(par_list_sorted)
    
    varlist = [i[0] for i in par_list_sorted]
    baselist = [i[1] for i in par_list_sorted]
    
    sun_cost=[]
    wind_cost=[]
    batt_cost=[]
    pgp_cost=[]
    elec_cap = []
    sys_cost = []
    topgp_cost = []
    storagepgp_cost =[]
    frompgp_cost = []
    ng_cost = []
    for base in baselist:
#        print(base)
        info = base[0]
        inputs = base[0][1]
        results = base[1]
        sys_cost.append(results[0]['system_cost'])
        elec_cap.append(results[1]['to_PGP capacity'])
#        print(results[1])
        dic = get_cost_contributions(base)
        sun_cost.append(dic['PV'])
        wind_cost.append(dic['wind'])
        batt_cost.append(dic['battery'])
        pgp_cost.append(dic['to_PGP']+dic['PGP_storage']+dic['from_PGP'])
        topgp_cost.append(dic['to_PGP'])
        storagepgp_cost.append(dic['PGP_storage'])
        frompgp_cost.append(dic['from_PGP'])
        ng_cost.append(dic['natgas'])
    data = (varlist, wind_cost, sun_cost, batt_cost, pgp_cost, elec_cap, sys_cost, topgp_cost, storagepgp_cost,frompgp_cost, ng_cost)
    return data

def get_impr(xbase, xperf):
    #min(myList, key=lambda x:abs(x-myNumber))
    close_base = min(x, key=lambda z:abs(z-xbase))
    print('close_base', close_base)
    
    close_perf = min(x, key=lambda z:abs(z-xperf))
    
    print(len(x),len(sys_cost))
    for i in range(0, len(sys_cost)):
        if x[i] == close_base:
            print('x of close base', x[i])
            base_cost = sys_cost[i]
        if x[i] == close_perf:
            print('x of close perf', x[i])
            perf_cost = sys_cost[i]
    impr = (base_cost - perf_cost)/base_cost*100
    print('impr', impr)
    return impr, close_base, base_cost, close_perf, perf_cost
#======================================================
    

##==============================================
plt.rcParams.update({'axes.titlesize': 'large'})
plt.rcParams.update({'axes.labelsize': 'large'})

import matplotlib.pylab as pylab
params = {'legend.fontsize': 'medium',
          'figure.figsize': (10, 10),
         'axes.labelsize': 'large',
         'axes.titlesize':'large',
         'xtick.labelsize':'large',
         'ytick.labelsize':'large'}
pylab.rcParams.update(params)

fig = plt.figure()


#======================================================
path = '/Users/jacquelinedowling/MEM/Output_Data/toPGPeff_5pctNG'

data = getdata(path, 5, 'efficiency')
varlist = data[0]
wind_cost = data[1]
sun_cost = data[2]
batt_cost = data[3]
pgp_cost = data[4]
elec_cap = data[5]
sys_cost = data[6]

topgp_cost = data[7]
storagepgp_cost =data[8]
frompgp_cost = data[9]
ng_cost = data[10]

x = np.array(varlist)*100 #for efficiencies turn into percent
#y = np.vstack([wind_cost, sun_cost, batt_cost, pgp_cost])
#pal = ['blue', 'orange', 'purple', 'pink']
#labels = ["Wind", "Solar", "Battery", "PGP"]

y = np.vstack([wind_cost, sun_cost, batt_cost, topgp_cost, storagepgp_cost,frompgp_cost, ng_cost])
pal = ['blue', 'orange', 'purple', 'pink','tab:pink','m', 'saddlebrown']
labels = ["Wind", "Solar", "Battery", "topgp_cost", "storagepgp_cost","frompgp_cost", 'natgas']


    
impr, close_base, base_cost, close_perf, perf_cost = get_impr(50, 100)


#for i in range(0, len(x)):
#    if x[i] == axline:
#        print(sys_cost[i-1])
#        print(x[i-1])
#        axline = x[i-1]
#        break

#plotting Linear
#ax3 = plt.subplot2grid((2, 3), (0, 0), colspan=2, rowspan=1)
ax1 = plt.subplot2grid((3, 2), (0, 1), colspan=1, rowspan=1)
#ax1.text(10, .12, "Max system cost\nimprovement:\n" + str(round(impr, 0)) + "%")

ax1.stackplot(x, y, colors=pal, labels=labels)
ax1.axvline(x=50, color='k', linestyle='-', linewidth=1.5, label='PEM electrolyzer\n$1,706/kW\n50% efficient')
#ax1.text(axline+18, .1, str(round(sys_cost[70], 0))+ '%')

#ax3.legend(loc='upper center', bbox_to_anchor=(1.25, 1.03))
#chartBox = ax3.get_position()
#ax3.set_position([chartBox.x0, chartBox.y0, chartBox.width, chartBox.height])
#ax1.plot(x, elec_cap, color='red', linestyle='-', label = 'Electryolyzer\ncapacity')
ax1.set_xlim(0, 100)
ax1.set_ylim(0, 0.08)
ax1.yaxis.set_major_locator(ticker.MultipleLocator(0.04))
#ax3.xaxis.set_major_locator(ticker.MultipleLocator(.1))
#ax3.xaxis.set_minor_locator(ticker.MultipleLocator(0.5))
#ax3.xaxis.set_major_formatter(FormatStrFormatter('%gx'))
ax1.xaxis.set_major_formatter(ticker.PercentFormatter())
#ax.set_title('Contribution of each technology\nto total system cost \n vs. PGP costs')
#ax1.set_title('Sensitivity to\nEfficiency\n', fontweight='bold')
#ax1.set_ylabel('System cost ($/kWh)') #,color='white'
ax1.set_xlabel('Power-to-H$_{2}$\nefficiency (%)')

ax1.scatter(close_base, base_cost, marker='o', color = 'black')
ax1.scatter(close_perf, perf_cost, marker='o', facecolors='none', edgecolors='k') 
#ax1.text(close_perf, base_cost+.01, str(round(impr, 0)) + "%",fontweight='bold', horizontalalignment='center')
ax1.annotate('{:.0f}'.format(impr) + "%", xy=(1.15, 0.582), xycoords='axes fraction',weight='bold')
ax1.annotate('', xy=(1.1, .673), xycoords='axes fraction', weight='bold', xytext=(1.1, 0.491), arrowprops=dict(arrowstyle="<-", color='k'))

ax1.legend(loc='upper left', bbox_to_anchor=(1.35, 1.03))
chartBox = ax1.get_position()
ax1.set_position([chartBox.x0, chartBox.y0, chartBox.width*1, chartBox.height])
ax1.set_title('Efficiency sensitivity')

#======================================================
path = '/Users/jacquelinedowling/MEM/Output_Data/fromPGPeff_5pctNG'

data = getdata(path, 7 , 'efficiency')
varlist = data[0]
wind_cost = data[1]
sun_cost = data[2]
batt_cost = data[3]
pgp_cost = data[4]
sys_cost = data[6]

topgp_cost = data[7]
storagepgp_cost =data[8]
frompgp_cost = data[9]
ng_cost = data[10]

x = np.array(varlist)*100 #for efficiencies turn into percent
#y = np.vstack([wind_cost, sun_cost, batt_cost, pgp_cost])
#pal = ['blue', 'orange', 'purple', 'pink']
#labels = ["Wind", "Solar", "Battery", "PGP"]

y = np.vstack([wind_cost, sun_cost, batt_cost, topgp_cost, storagepgp_cost,frompgp_cost, ng_cost])
pal = ['blue', 'orange', 'purple', 'pink','tab:pink','m', 'saddlebrown']
labels = ["Wind", "Solar", "Battery", "topgp_cost", "storagepgp_cost","frompgp_cost", 'natgas']
#pink','tab:pink','hotpink'
impr, close_base, base_cost, close_perf, perf_cost = get_impr(71, 100)


#plotting Linear
#ax3 = plt.subplot2grid((2, 3), (0, 0), colspan=2, rowspan=1)
ax6 = plt.subplot2grid((3, 2), (2, 1), colspan=1, rowspan=1)
stacks = ax6.stackplot(x, y, colors=pal, labels=labels)

#hatches=["\\", "//","+"]
#hatches=['', '', '', "\\","O", "//"]
#for stack, hatch in zip(stacks, hatches):
#    stack.set_hatch(hatch)

#ax6.axvline(x=50, color='gray', linestyle='-.', linewidth=1.5, label='H2 turbines\n(50%) ')
#ax6.axvline(x=70, color='gray', linestyle='--', linewidth=1.5, label='MC-CHP\nfuel cells\n(70%) ')
ax6.axvline(x=71, color='k', linestyle='-', linewidth=1.5, label='PEM fuel cell\n$1,414/kW\n71% efficient ')
#ax6.text(80, .1, str(round(impr, 4)))
#ax6.text(10, .12, "Max system cost\nimprovement:\n" + str(round(impr, 0)) + "%")

ax6.annotate('{:.0f}'.format(impr) + "%", xy=(1.15, 0.582), xycoords='axes fraction',weight='bold')
ax6.annotate('', xy=(1.1, .673), xycoords='axes fraction', weight='bold', xytext=(1.1, 0.491), arrowprops=dict(arrowstyle="<-", color='k'))

#ax3.legend(loc='upper center', bbox_to_anchor=(1.25, 1.03))
#chartBox = ax3.get_position()
#ax3.set_position([chartBox.x0, chartBox.y0, chartBox.width, chartBox.height])
ax6.set_xlim(0, 100)
ax6.set_ylim(0, 0.08)
ax6.yaxis.set_major_locator(ticker.MultipleLocator(0.04))
#ax3.xaxis.set_major_locator(ticker.MultipleLocator(.1))
#ax3.xaxis.set_minor_locator(ticker.MultipleLocator(0.5))
#ax3.xaxis.set_major_formatter(FormatStrFormatter('%gx'))
ax6.xaxis.set_major_formatter(ticker.PercentFormatter())
#ax.set_title('Contribution of each technology\nto total system cost \n vs. PGP costs')
#ax6.set_ylabel('System cost ($/kWh)') #,color='white'
ax6.set_xlabel('H$_{2}$-to-Power\nefficiency (%)')
ax6.scatter(close_base, base_cost, marker='o', color = 'black')
ax6.scatter(close_perf, perf_cost, marker='o', facecolors='none', edgecolors='k') 

ax6.legend(loc='upper left', bbox_to_anchor=(1.35, 1.03))
chartBox = ax6.get_position()
ax6.set_position([chartBox.x0, chartBox.y0, chartBox.width*1, chartBox.height])
ax6.set_title('Efficiency sensitivity')

#======================================================
path = '/Users/jacquelinedowling/MEM/Output_Data/toPGPcost_5pctNG'

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


data = getdata(path, 5 , 'fixed_cost')
varlist = data[0] #toPGP fixed cost
wind_cost = data[1]
sun_cost = data[2]
batt_cost = data[3]
pgp_cost = data[4]
sys_cost = data[6]

topgp_cost = data[7]
storagepgp_cost =data[8]
frompgp_cost = data[9]
ng_cost = data[10]

#x = [((i * hours_per_year) - batt_fixed_om) / batt_crc for i in batt_fixed_cost]
x = [((i * hours_per_year) - toPGP_fixed_om) / toPGP_crf for i in varlist]

#x = varlist
#y = np.vstack([wind_cost, sun_cost, batt_cost, pgp_cost])
#pal = ['blue', 'orange', 'purple', 'pink']
#labels = ["Wind", "Solar", "Battery", "PGP"]
y = np.vstack([wind_cost, sun_cost, batt_cost, topgp_cost, storagepgp_cost,frompgp_cost, ng_cost])
pal = ['blue', 'orange', 'purple', 'pink','tab:pink','m', 'saddlebrown']
labels = ["Wind", "Solar", "Battery", "topgp_cost", "storagepgp_cost","frompgp_cost", 'natgas']


#print(x)
impr, close_base, base_cost, close_perf, perf_cost = get_impr(toPGP_base_capitalcost, 0)

#plotting Linear
#ax3 = plt.subplot2grid((2, 3), (0, 0), colspan=2, rowspan=1)
ax5 = plt.subplot2grid((3, 2), (0, 0), colspan=1, rowspan=1)
ax5.stackplot(x, y, colors=pal, labels=labels)
#ax5.axvline(x=0.034609374, color='k', linestyle='-', linewidth=1.5, label='Electrolyzers\n($1,000/kW) ')
ax5.axvline(x=toPGP_base_capitalcost, color='k', linestyle='-', linewidth=1.5, label='Electrolyzers\n($1,706/kW) ')

#ax6.axvline(x=70, color='k', linestyle='--', linewidth=1.5, label='Fuel cells (70%) ')
#ax3.legend(loc='upper center', bbox_to_anchor=(1.25, 1.03))
#chartBox = ax3.get_position()
#ax3.set_position([chartBox.x0, chartBox.y0, chartBox.width, chartBox.height])
#ax5.text(0.03, .1, str(round(impr, 4)))
#ax5.text(0.135, .12, "Max system cost\nimprovement:\n" + str(round(impr, 0)) + "%",fontweight='bold')

ax5.set_xlim(0, 8000)
#ax5.invert_xaxis()
ax5.set_ylim(0, 0.08)
ax5.yaxis.set_major_locator(ticker.MultipleLocator(0.04))
#ax3.xaxis.set_major_locator(ticker.MultipleLocator(.1))
#ax3.xaxis.set_minor_locator(ticker.MultipleLocator(0.5))
#ax5.xaxis.set_major_formatter(FormatStrFormatter('%gx'))
#ax5.xaxis.set_major_formatter(ticker.PercentFormatter())
#ax5.set_title('Sensitivity to\nCapital Cost\n', fontweight='bold')
ax5.set_ylabel('System cost ($/kWh)') #,color='white'
ax5.set_xlabel('Power-to-H$_{2}$\ncapital cost ($/kW)')
ax5.scatter(close_base, base_cost, marker='o', color = 'black')
ax5.scatter(close_perf, perf_cost, marker='o', facecolors='none', edgecolors='k') 

ax5.annotate('{:.0f}'.format(impr) + "%", xy=(1.15, 0.582), xycoords='axes fraction',weight='bold')
ax5.annotate('', xy=(1.1, .673), xycoords='axes fraction', weight='bold', xytext=(1.1, 0.491), arrowprops=dict(arrowstyle="<-", color='k'))

#ax5.arrow(x=close_perf, y=base_cost, dx=0, dy=perf_cost-base_cost, width=.003, facecolor='black', edgecolor='none', length_includes_head = 'True') 


#ax5.legend(loc='upper center', bbox_to_anchor=(1.35, 1.03))
chartBox = ax5.get_position()
ax5.set_position([chartBox.x0, chartBox.y0, chartBox.width*1, chartBox.height])
ax5.set_title('Capital cost sensitivity')
#======================================================
path = '/Users/jacquelinedowling/MEM/Output_Data/fromPGPcost_5pctNG'

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

data = getdata(path, 7 , 'fixed_cost')
varlist = data[0]
wind_cost = data[1]
sun_cost = data[2]
batt_cost = data[3]
pgp_cost = data[4]
sys_cost = data[6]

topgp_cost = data[7]
storagepgp_cost =data[8]
frompgp_cost = data[9]
ng_cost = data[10]

x = [((i * hours_per_year) - fromPGP_fixed_om) / fromPGP_crf for i in varlist]
#x = varlist
#y = np.vstack([wind_cost, sun_cost, batt_cost, pgp_cost])
#pal = ['blue', 'orange', 'purple', 'pink']
#labels = ["Wind", "Solar", "Battery", "PGP"]
y = np.vstack([wind_cost, sun_cost, batt_cost, topgp_cost, storagepgp_cost,frompgp_cost, ng_cost])
pal = ['blue', 'orange', 'purple', 'pink','tab:pink','m', 'saddlebrown']
labels = ["Wind", "Solar", "Battery", "topgp_cost", "storagepgp_cost","frompgp_cost", 'natgas']


impr, close_base, base_cost, close_perf, perf_cost = get_impr(fromPGP_base_capitalcost, 0)

#plotting Linear
#ax3 = plt.subplot2grid((2, 3), (0, 0), colspan=2, rowspan=1)
ax5 = plt.subplot2grid((3, 2), (2, 0), colspan=1, rowspan=1)
ax5.stackplot(x, y, colors=pal, labels=labels)
#ax5.axvline(x=0.058464, color='gray', linestyle='--', linewidth=1.5, label='MC-CHP\nfuel cells\n($6,000/kW) ')
ax5.axvline(x=fromPGP_base_capitalcost, color='k', linestyle='-', linewidth=1.5, label='PEM fuel cells\n($1,414/kW) ')

#ax5.axvline(x=2.69207E-02, color='k', linestyle='-', linewidth=1.5, label='PEM-CHP\nfuel cells\n($2,000/kW) ')
#ax5.axvline(x=1.07683E-02, color='gray', linestyle='-.', linewidth=1.5, label='H2 turbines\n($1,000/kW) ')
#ax5.text(0.03, .1, str(round(impr, 4)))
#ax5.text(0.135, .12, "Max system cost\nimprovement:\n" + str(round(impr, 0)) + "%",fontweight='bold')


#ax6.axvline(x=70, color='k', linestyle='--', linewidth=1.5, label='Fuel cells (70%) ')
#ax3.legend(loc='upper center', bbox_to_anchor=(1.25, 1.03))
#chartBox = ax3.get_position()
#ax3.set_position([chartBox.x0, chartBox.y0, chartBox.width, chartBox.height])
ax5.set_xlim(0, 8000)
#ax5.invert_xaxis()
ax5.set_ylim(0, 0.08)
ax5.yaxis.set_major_locator(ticker.MultipleLocator(0.04))
#ax3.xaxis.set_major_locator(ticker.MultipleLocator(.1))
#ax3.xaxis.set_minor_locator(ticker.MultipleLocator(0.5))
#ax5.xaxis.set_major_formatter(FormatStrFormatter('%gx'))
#ax5.xaxis.set_major_formatter(ticker.PercentFormatter())
#ax.set_title('Contribution of each technology\nto total system cost \n vs. PGP costs')
ax5.set_ylabel('System cost ($/kWh)') #,color='white'
ax5.set_xlabel('H$_{2}$-to-Power\ncapital cost ($/kW)')

#ax5.legend(loc='upper center', bbox_to_anchor=(1.35, 1.03))
chartBox = ax5.get_position()
ax5.set_position([chartBox.x0, chartBox.y0, chartBox.width*1, chartBox.height])
#ax5.annotate('{:.0f}'.format(impr) + "%", xy=(1.15, (perf_cost+base_cost)/2/.12), xycoords='axes fraction',weight='bold')
#ax5.annotate('', xy=(1.1, base_cost/.12), xycoords='axes fraction', weight='bold', xytext=(1.1, perf_cost/.12), 
#            arrowprops=dict(arrowstyle="<-", color='k'))


ax5.annotate('{:.0f}'.format(impr) + "%", xy=(1.15, 0.582), xycoords='axes fraction',weight='bold')
ax5.annotate('', xy=(1.1, .673), xycoords='axes fraction', weight='bold', xytext=(1.1, 0.491), arrowprops=dict(arrowstyle="<-", color='k'))


ax5.scatter(close_base, base_cost, marker='o', color = 'black')
ax5.scatter(close_perf, perf_cost, marker='o', facecolors='none', edgecolors='k') 
#ax5.arrow(x=close_perf, y=base_cost, dx=0, dy=perf_cost-base_cost, width=.003, facecolor='black', edgecolor='none', shape = 'right', length_includes_head = 'True') 
ax5.set_title('Capital cost sensitivity')
#======================================================
path = '/Users/jacquelinedowling/MEM/Output_Data/storagePGPcost_5pctNG'

storagePGP_base_capitalcost = 1.9992
storagePGP_crf = 0.080586404
storagePGP_fixed_om = 0.029988 #1.50% of capital cost
hours_per_year = 8760
#c_fixed_base = (0.080586404 * 1706.46 + 13.056) / 8760
c_fixed_base = storagePGP_crf * (storagePGP_base_capitalcost + storagePGP_fixed_om) / hours_per_year
print('c_fixed_base', c_fixed_base)

#base_capitalcost = annual_capitalcost * hours_per_year / toPGP_crf
base_overnightcapital = ((c_fixed_base * hours_per_year) - storagePGP_fixed_om)  / storagePGP_crf
print('base_overnightcapital', base_overnightcapital)


data = getdata(path, 6 , 'fixed_cost')
varlist = data[0]
wind_cost = data[1]
sun_cost = data[2]
batt_cost = data[3]
pgp_cost = data[4]
sys_cost = data[6]

topgp_cost = data[7]
storagepgp_cost =data[8]
frompgp_cost = data[9]
ng_cost = data[10]

#We change the equation here because o&m cost from Hunter 2021 is a percentage of capital cost.
x = [((i * hours_per_year) / storagePGP_crf) - storagePGP_fixed_om for i in varlist]
#x = varlist
#y = np.vstack([wind_cost, sun_cost, batt_cost, pgp_cost])
#pal = ['blue', 'orange', 'purple', 'pink']
#labels = ["Wind", "Solar", "Battery", "PGP"]
y = np.vstack([wind_cost, sun_cost, batt_cost, topgp_cost, storagepgp_cost,frompgp_cost, ng_cost])
pal = ['blue', 'orange', 'purple', 'pink','tab:pink','m', 'saddlebrown']
labels = ["Wind", "Solar", "Battery", "topgp_cost", "storagepgp_cost","frompgp_cost", 'natgas']


impr, close_base, base_cost, close_perf, perf_cost = get_impr(storagePGP_base_capitalcost, 1e-9)

#plotting Linear
#ax3 = plt.subplot2grid((2, 3), (0, 0), colspan=2, rowspan=1)
ax5 = plt.subplot2grid((3, 2), (1, 0), colspan=1, rowspan=1)
ax5.stackplot(x, y, colors=pal, labels=labels)
#ax5.axvline(x=1.61524E-04, color='gray', linestyle='--', linewidth=1.5, label='Tanks\n($15/kWh) ')
ax5.axvline(x=storagePGP_base_capitalcost, color='k', linestyle='-', linewidth=1.5, label='Salt caverns\n($2/kWh) ')
#ax5.axvline(x=3.73E-06, color='k', linestyle='-', linewidth=1.5, label='Salt caverns\n($0.16/kWh) ')
#ax5.axvline(x=1.83865E-08, color='gray', linestyle='-.', linewidth=1.5, label='Depleted\nreservoirs\n($0.002/kWh) ')

#ax5.text(3.73E-06, .1, str(round(impr, 4)))
#ax5.text(2E-3, .12, "Max system cost\nimprovement:\n" + str(round(impr, 0)) + "%")

ax5.set_xlim(0, 8)
#ax5.xaxis.set_major_locator(ticker.MultipleLocator(4))

#ax6.axvline(x=70, color='k', linestyle='--', linewidth=1.5, label='Fuel cells (70%) ')
#ax3.legend(loc='upper center', bbox_to_anchor=(1.25, 1.03))
#chartBox = ax3.get_position()
#ax3.set_position([chartBox.x0, chartBox.y0, chartBox.width, chartBox.height])
#ax5.set_xscale('log')
#ax5.invert_xaxis()
#ax5.set_xlim(5e-6, 1e-9)
#ax5.set_xlim(1e-9,5e-6)
#ax5.ticklabel_format(axis='x', style='', scilimits=(5,6), useOffset=None, useLocale=None, useMathText=None)
ax5.set_ylim(0, 0.08)
ax5.yaxis.set_major_locator(ticker.MultipleLocator(0.04))

#f = ticker.ScalarFormatter(useOffset=False, useMathText=True)
#g = lambda x,pos : "${}$".format(f._formatSciNotation('%1.10e' % x))
#ax5.xaxis.set_major_formatter(ticker.FuncFormatter(g))
##ax5.set_xticklabels(rotation=45 )
#plt.xticks(rotation=45, ha="right")

#ax5.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.2e'))
#ax3.xaxis.set_major_locator(ticker.MultipleLocator(.1))
#ax3.xaxis.set_minor_locator(ticker.MultipleLocator(0.5))
#ax5.xaxis.set_major_formatter(FormatStrFormatter('%gx'))
#ax5.xaxis.set_major_formatter(ticker.PercentFormatter())
#ax.set_title('Contribution of each technology\nto total system cost \n vs. PGP costs')
ax5.set_ylabel('System cost ($/kWh)') #,color='white'
ax5.set_xlabel('H$_{2}$ Storage\ncapital cost ($/kWh)')

ax5.annotate('{:.0f}'.format(impr) + "%", xy=(1.15, 0.582), xycoords='axes fraction',weight='bold')
ax5.annotate('', xy=(1.1, .673), xycoords='axes fraction', weight='bold', xytext=(1.1, 0.491), arrowprops=dict(arrowstyle="<-", color='k'))

#ax5.legend(loc='upper center', bbox_to_anchor=(1.35, 1.03))
chartBox = ax5.get_position()
ax5.set_position([chartBox.x0, chartBox.y0, chartBox.width*1, chartBox.height])
ax5.scatter(close_base, base_cost, marker='o', color = 'black')
ax5.scatter(close_perf, perf_cost, marker='o', facecolors='none', edgecolors='k') 
ax5.set_title('Capital cost sensitivity')
 
#======================================================
path = '/Users/jacquelinedowling/MEM/Output_Data/storagePGPdecay_5pctNG'

data = getdata(path, 6 , 'decay_rate')
varlist = data[0]
wind_cost = data[1]
sun_cost = data[2]
batt_cost = data[3]
pgp_cost = data[4]
sys_cost = data[6]

topgp_cost = data[7]
storagepgp_cost =data[8]
frompgp_cost = data[9]
ng_cost = data[10]

x = [i * 100 * 8760 for i in varlist]

#x = varlist
#y = np.vstack([wind_cost, sun_cost, batt_cost, pgp_cost])
#print('decay rate x',x)
#print('decay rate y',sys_cost)
#pal = ['blue', 'orange', 'purple', 'pink']
#labels = ["Wind", "Solar", "Battery", "PGP"]
y = np.vstack([wind_cost, sun_cost, batt_cost, topgp_cost, storagepgp_cost,frompgp_cost, ng_cost])
pal = ['blue', 'orange', 'purple', 'pink','tab:pink','m', 'saddlebrown']
labels = ["Wind", "Solar", "Battery", "topgp_cost", "storagepgp_cost","frompgp_cost", 'natgas']


#impr, close_base, base_cost, close_perf, perf_cost = get_impr(1.14E-08, 1e-9)
impr, close_base, base_cost, close_perf, perf_cost = get_impr(0.01, 1e-9* 100 * 8760)


#plotting Linear
#ax3 = plt.subplot2grid((2, 3), (0, 0), colspan=2, rowspan=1)
ax5 = plt.subplot2grid((3, 2), (1, 1), colspan=1, rowspan=1)
ax5.stackplot(x, y, colors=pal, labels=labels)
#ax5.axvline(x=1.38E-05, color='gray', linestyle='--', linewidth=1.5, label='Battery\n(1%/month) ')
#ax5.axvline(x=(3.996133068895347e-08), color='gray', linestyle='-.', linewidth=1.5, label='Depleted\nreservoirs\n(0.035%/year)')
#ax5.axvline(x=1.14E-08, color='k', linestyle='-', linewidth=1.5, label='Salt caverns\n(0.01%/year) ')
#ax5.axvline(x=1.14E-08, color='k', linestyle='-', linewidth=1.5, label='Salt caverns\n(0.01%/year) ')
#ax5.axvline(x=close_base, color='k', linestyle='-', linewidth=1.5, label='Salt caverns\n$0.16/kWh\n0.01%/year\ndecay rate')
ax5.axvline(x=0.01, color='k', linestyle='-', linewidth=1.5, label='Salt caverns\n$2/kWh\n0.01%/year\ndecay rate')


#ax5.text(1.14E-08, .1, str(round(impr, 7)))
#ax5.text(0.8E-7, .12, "Max system cost\nimprovement:\n" + str(round(impr, 0)) + "%")


#ax5.axvline(x=, color='k', linestyle='--', linewidth=1.5, label='Dep. Reservoirs\n($0.002/kWh) ')

#ax6.axvline(x=70, color='k', linestyle='--', linewidth=1.5, label='Fuel cells (70%) ')
#ax3.legend(loc='upper center', bbox_to_anchor=(1.25, 1.03))
#chartBox = ax3.get_position()
#ax3.set_position([chartBox.x0, chartBox.y0, chartBox.width, chartBox.height])
#ax5.set_xscale('log')
ax5.set_xscale('linear')
#ax5.invert_xaxis()
#ax5.set_xlim(1.14E-08, 10e-10)
#ax5.set_xlim(.0000001, close_perf)
#ax5.set_xlim(.00000001, .000000001)
#ax5.set_xlim(.000000001,.00000001 )
#ax5.set_xlim(.0000001,.000001 )
ax5.set_xlim(.0,.06 )
#ax5.ticklabel_format(axis='x', style='', scilimits=(5,6), useOffset=None, useLocale=None, useMathText=None)
ax5.set_ylim(0, 0.08)
ax5.yaxis.set_major_locator(ticker.MultipleLocator(0.04))

#f = ticker.ScalarFormatter(useOffset=False, useMathText=True)
#g = lambda x,pos : "${}$".format(f._formatSciNotation('%1.10e' % x))
#ax5.xaxis.set_major_formatter(ticker.FuncFormatter(g))

#ax3.xaxis.set_major_locator(ticker.MultipleLocator(.1))
#ax3.xaxis.set_minor_locator(ticker.MultipleLocator(0.5))
#ax5.xaxis.set_major_formatter(FormatStrFormatter('%gx'))
#ax5.xaxis.set_major_formatter(ticker.PercentFormatter())
#ax.set_title('Contribution of each technology\nto total system cost \n vs. PGP costs')
#ax5.set_ylabel('System cost ($/kWh)') #,color='white'
ax5.set_xlabel(r'$\bf{H$_{2}$ Storage}$' + '\nloss rate (% per year)')
ax5.set_xlabel('H$_{2}$ Storage\nloss rate (% per year)')

ax5.legend(loc='upper left', bbox_to_anchor=(1.35, 1.03))
chartBox = ax5.get_position()
ax5.set_position([chartBox.x0, chartBox.y0, chartBox.width*1, chartBox.height])
ax5.scatter(close_base, base_cost, color='k')
ax5.scatter(close_perf, perf_cost, marker='o', facecolors='none', edgecolors='k') 

ax5.annotate('{:.0f}'.format(impr) + "%", xy=(1.15, 0.582), xycoords='axes fraction',weight='bold')
ax5.annotate('', xy=(1.1, .673), xycoords='axes fraction', weight='bold', xytext=(1.1, 0.491), arrowprops=dict(arrowstyle="<-", color='k'))
ax5.set_title('Loss rate sensitivity')


#======================================================
#fig.text(.32, 0.88, 'Power-to-Gas', size='large',fontweight='bold')
#fig.text(.32, 0.57, 'Gas Storage', size='large',fontweight='bold')
#fig.text(.32, 0.33, 'Gas-to-Power', size='large',fontweight='bold')

#fig.text(.32, 0.64, 'Power-to-Gas', size='x-large',fontweight='bold')
#fig.text(.32, 0.33, 'Gas Storage', size='x-large',fontweight='bold')
#fig.text(.32, 0.02, 'Gas-to-Power', size='x-large',fontweight='bold')

#fig.text(.32, 0.935, 'Power-to-Gas', size='x-large',fontweight='bold')
#fig.text(.32, 0.63, 'Gas Storage', size='x-large',fontweight='bold')
#fig.text(.32, 0.33, 'Gas-to-Power', size='x-large',fontweight='bold')

#fig.text(.16, 0.99, 'Capital Cost', size='large',fontweight='bold')
#fig.text(.58, 0.99, 'Efficiency', size='large',fontweight='bold')

#fig.text(.3, 0.02, '--> Direction of Innovation -->', size='large',fontweight='bold')
#fig.text(.05, 0.00, 'Annoated values are max possible system cost improvements ($/kWh) from the base case (circle marker to square marker).', size='medium')


plt.tight_layout()
plt.savefig('val_innovation_pem_ng5pct.pdf', bbox_inches='tight')
plt.savefig('val_innovation_pem_ng5pct.png', bbox_inches='tight')
plt.savefig('val_innovation_pem_ng5pct.svg', bbox_inches='tight')

plt.show()


