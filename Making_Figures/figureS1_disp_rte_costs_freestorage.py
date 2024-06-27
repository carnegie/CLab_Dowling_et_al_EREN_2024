#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 04:07:30 2023

@author: jacquelinedowling
"""

# fig_disp_rte_costs_freestorage


#Cost sweeps

import pickle
import numpy as np
import matplotlib.pyplot as plt
import glob
import matplotlib.ticker as ticker

#tech_list[0] is demand
#tech_list[1] is curtainment
#tech_list[2] is solar
#techlist[3] is wind
#techlist[4] is battery
#techlist[5] is to_PGP
#techlist[6] is PGP_storage
#technlist[7] is from_PGP


def getdataprice(path, techidx, var):
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
    
#    main_node_price = []
#    demand_potential = []
#    to_PGP_dispatch = []
#    from_PGP_dispatch = []
    
    cost_elec_to_main_demand = []
    cost_elec_to_PGP = []
    cost_elec_from_PGP = []

#    elec_cap = []
#    sys_cost = []
#    curt_avg = []
    for base in baselist:
#        print(base)
#        info = base[0]
#        inputs = base[0][1]
#        results = base[1]
        info = base[0][0]
        inputs = base[0][1]
        results = base[1][2]
        input_series = base[0][2]
#        print('RESULTS')
#        print(results)
        
        cost_elec_to_main_demand.append(np.mean(results['main_node price'] * results['demand potential']))
        cost_elec_to_PGP.append(np.mean(results['main_node price'] * results['to_PGP dispatch']))
        cost_elec_from_PGP.append(np.mean(results['main_node price'] * results['from_PGP dispatch']))

    data = (varlist, cost_elec_to_main_demand, cost_elec_to_PGP, cost_elec_from_PGP)
    return data



#======================================================

def getdatadisp(path, techidx, var):
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
    
    demand_source = []
    wind_source = []
    solar_source = []
    batt_source = []
    pgp_source = []
    
    demand_sink = []
    batt_sink = []
    pgp_sink = []
    
    curt_avg = []

#    elec_cap = []
#    sys_cost = []
#    curt_avg = []
    for base in baselist:
#        print(base)
#        info = base[0]
#        inputs = base[0][1]
#        results = base[1]
        info = base[0][0]
        inputs = base[0][1]
        results = base[1][2]
        input_series = base[0][2]
#        print('RESULTS')
#        print(results)
        demand_source.append(np.mean(results['demand potential']))
        wind_source.append(np.mean(results['wind potential']))
        solar_source.append(np.mean(results['PV potential']))
        batt_source.append(np.mean(results['battery dispatch']))
        pgp_source.append(np.mean(results['from_PGP dispatch']))
        
        demand_sink.append(-1*np.mean(input_series['demand series']))
        batt_sink.append(-1*np.mean(results['battery in dispatch']))
        pgp_sink.append(-1*np.mean(results['to_PGP in dispatch']))
        
        curt_avg.append(-1*np.mean(results['main_curtailment dispatch']))
        

    data = (varlist, demand_source, wind_source, solar_source, batt_source, pgp_source,
            demand_sink, batt_sink, pgp_sink, curt_avg)
    return data



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
        # print(results[1])
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
    curt_avg = []
    topgp_cost = []
    storagepgp_cost =[]
    frompgp_cost = []
    for base in baselist:
#        print(base)
        info = base[0]
        inputs = base[0][1]
        results = base[1]
#        print('RESULTS')
#        print(results)
        sys_cost.append(results[0]['system_cost'])
        elec_cap.append(results[1]['to_PGP capacity'])
        curt_avg.append(np.average(results[2]['main_curtailment dispatch']))
#        print(curt_avg)
        dic = get_cost_contributions(base)
        sun_cost.append(dic['PV'])
        wind_cost.append(dic['wind'])
        batt_cost.append(dic['battery'])
        pgp_cost.append(dic['to_PGP']+dic['PGP_storage']+dic['from_PGP'])
        topgp_cost.append(dic['to_PGP'])
        storagepgp_cost.append(dic['PGP_storage'])
        frompgp_cost.append(dic['from_PGP'])
    data = (varlist, wind_cost, sun_cost, batt_cost, pgp_cost, elec_cap, sys_cost, curt_avg, topgp_cost, storagepgp_cost,frompgp_cost)
    return data


#======================================================
def get_impr(xbase, xperf):
    #min(myList, key=lambda x:abs(x-myNumber))
    close_base = min(x, key=lambda z:abs(z-xbase))
#    print('close_base', close_base)
    
    close_perf = min(x, key=lambda z:abs(z-xperf))
    
#    print(len(x),len(sys_cost))
    for i in range(0, len(sys_cost)):
        if x[i] == close_base:
#            print('x of close base', x[i])
            base_cost = sys_cost[i]
        if x[i] == close_perf:
#            print('x of close perf', x[i])
            perf_cost = sys_cost[i]
    impr = (base_cost - perf_cost)*(1/base_cost)*100
#    print(impr)
    return impr, close_base, base_cost, close_perf, perf_cost
    
#impr, close_base, base_cost, close_perf, perf_cost = get_impr(70, 100)
##==============================================
plt.rcParams.update({'axes.titlesize': 'large'})
plt.rcParams.update({'axes.labelsize': 'large'})

import matplotlib.pylab as pylab
params = {'legend.fontsize': 'medium',
          'figure.figsize': (10, 8),
         'axes.labelsize': 'large',
         'axes.titlesize':'large',
         'xtick.labelsize':'large',
         'ytick.labelsize':'large'}
pylab.rcParams.update(params)

fig = plt.figure()


#======================================================
# (Figure 1a: Cost contributions)
#======================================================
path = '/Users/jacquelinedowling/MEM/Output_Data/rtePGPeff_freestorage'

#wind and solar
#path_nopgp='/Users/jacquelinedowling/MEM/Output_Data/combos_nopgp_na_na'
#data_npgp = getdata(path, 7 , 'efficiency')

data = getdata(path, 7 , 'efficiency')
varlist = data[0]
wind_cost = data[1]
sun_cost = data[2]
batt_cost = data[3]
pgp_cost = data[4]
sys_cost = data[6]
curt_series = data[7]

topgp_cost = data[8]
storagepgp_cost =data[9]
frompgp_cost = data[10]

x = np.array(varlist)*varlist*100 #for RT efficiency in percent
#y = np.vstack([wind_cost, sun_cost, batt_cost, pgp_cost])
#pal = ['blue', 'orange', 'purple', 'pink']
#labels = ["Wind", "Solar", "Battery", "PGP"]

y = np.vstack([wind_cost, sun_cost, batt_cost, topgp_cost, storagepgp_cost,frompgp_cost])
pal = ['blue', 'orange', 'purple', 'pink','tab:pink','m']
labels = ["Wind", "Solar", "Battery", "topgp_cost", "storagepgp_cost","frompgp_cost"]

#impr, close_base, base_cost, close_perf, perf_cost = get_impr(80, 100)

#plotting Linear
ax6 = plt.subplot2grid((3, 3), (0, 0), colspan=1, rowspan=1)
#ax6 = plt.subplot2grid((1, 2), (0, 0), colspan=1, rowspan=1)
ax6.stackplot(x, y, colors=pal, labels=labels)
ax6.axvline(x=36, color='k', linestyle='-', linewidth=1.5, label='Power-H$_{2}$-Power\n 36% round-trip efficiency')
impr, close_base, base_cost, close_perf, perf_cost = get_impr(36, 100)

ax6.scatter(close_base, base_cost, marker='o', color = 'black')
ax6.scatter(close_perf, perf_cost, marker='o', facecolors='none', edgecolors='k') 
#ax1.text(close_perf, base_cost+.01, str(round(impr, 0)) + "%",fontweight='bold', horizontalalignment='center')
ax6.annotate('{:.0f}'.format(impr) + "%", xy=(1.15, 0.582), xycoords='axes fraction',weight='bold')
ax6.annotate('', xy=(1.1, .673), xycoords='axes fraction', weight='bold', xytext=(1.1, 0.491), arrowprops=dict(arrowstyle="<-", color='k'))



#ax3.legend(loc='upper center', bbox_to_anchor=(1.25, 1.03))
#chartBox = ax3.get_position()
#ax3.set_position([chartBox.x0, chartBox.y0, chartBox.width, chartBox.height])
ax6.set_xlim(0, 100)
ax6.set_ylim(0, 0.12)
ax6.yaxis.set_major_locator(ticker.MultipleLocator(0.04))
#ax6.set_title('Wind + Solar')
#ax3.xaxis.set_major_locator(ticker.MultipleLocator(.1))
#ax3.xaxis.set_minor_locator(ticker.MultipleLocator(0.5))
#ax3.xaxis.set_major_formatter(FormatStrFormatter('%gx'))
ax6.xaxis.set_major_formatter(ticker.PercentFormatter())
#ax.set_title('Contribution of each technology\nto total system cost \n vs. PGP costs')
ax6.set_ylabel('System cost ($/kWh)') #,color='white'
ax6.set_xlabel('Power-H$_{2}$-Power\nround-trip efficiency')
#ax6.set_xlabel('PGP round-trip efficiency (%)')
#ax6.set_xlabel('RT PGP efficiency (%)')
#ax6.scatter(close_base, base_cost, marker='o', color = 'black')
#ax6.scatter(close_perf, perf_cost, marker='s', color = 'black')

#ax6.legend(loc='upper center', bbox_to_anchor=(1.7, 1))
#chartBox = ax6.get_position()
#ax6.set_position([chartBox.x0, chartBox.y0, chartBox.width*1, chartBox.height])

##===========================================================================================================
# (Figure 1b: Annual Dispatch Curve)

# Plotting code
##============================================================================================================
path = '/Users/jacquelinedowling/MEM/Output_Data/rtePGPeff_freestorage'


data = getdatadisp(path, 7 , 'efficiency')
varlist = data[0]
demand_source = data[1]
wind_source = data[2]
solar_source = data[3]
batt_source = data[4]
pgp_source = data[5]
demand_sink = data[6]
batt_sink = data[7]
pgp_sink = data[8]
curt_sink = data[9]


##Set colors
solar_c = 'orange' 
wind_c = 'blue'
pgp_c = 'pink' 
batt_c = 'purple'
dem_c = 'black'
curt_c = 'gray'

x = np.array(varlist)*varlist*100 #for RT efficiency in percent

y1 = np.vstack([wind_source, solar_source, batt_source, pgp_source  ])
pal1 = [wind_c, solar_c, batt_c, 'm']
labels1 = ["Wind", "Solar",  "Battery", "H$_{2}$-to-Power"]

y2 = np.vstack([demand_sink, pgp_sink, batt_sink,curt_sink])
pal2 = [dem_c, pgp_c, batt_c, curt_c ]
labels2 = ["Demand", 'Power-to-H$_{2}$', '', "Curtailment"]

#fig, ax = plt.subplots()
#fig, (ax1, ax2, ax3) = plt.subplots(2, 2, sharey=True)
#fig = plt.figure()
ax3 = plt.subplot2grid((3, 3), (0, 1), colspan=1, rowspan=1)
#ax3.plot(x, curt_series, color = 'gray', label = "Curtailment")

#ax3 = plt.subplot(211)
ax3.stackplot(x, y1, colors=pal1, labels=labels1)
ax3.stackplot(x, y2, colors=pal2, labels=labels2)
ax3.plot(x, demand_source, '-', color=dem_c, linewidth=1.2)
#ax3.set_xlim(quick_dates[0], quick_dates[-1])
ax3.set_ylim(-2.1, 2.1)
#ax3.legend(loc='upper center', bbox_to_anchor=(1.2, 1.04))
#chartBox = ax3.get_position()
#ax3.set_position([chartBox.x0, chartBox.y0, chartBox.width*1, chartBox.height])

#ax3.xaxis.set_major_locator(AutoDateLocator())
#ax3.xaxis.set_major_formatter(DateFormatter('%b'))
#ax3.xaxis.set_tick_params(direction='out', which='both')
ax3.yaxis.set_tick_params(direction='out', which='both')
ax3.set_ylabel('Mean electricity\nsources and sinks (kW)\n 1 = mean U.S. demand')
ax3.set_xlabel('Power-H$_{2}$-Power\nround-trip efficiency')
#ax3.set_xlabel('PGP round-trip efficiency')


ax3.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax3.xaxis.set_major_formatter(ticker.PercentFormatter())
ax3.set_xlim(0, 100)

#ax3.legend(loc='upper center', bbox_to_anchor=(1.3, .65))
#ax3.legend(loc='upper center', bbox_to_anchor=(1.6, 1.1))

#======================================================
# (Figure 1c: Meet instantaneous electricty cost)
#======================================================

path = '/Users/jacquelinedowling/MEM/Output_Data/rtePGPeff_freestorage'

data = getdataprice(path, 7, 'efficiency')
varlist = data[0]
cost_elec_to_main_demand = data[1]
cost_elec_to_PGP = data[2]
cost_elec_from_PGP = data[3]


x = np.array(varlist)*varlist*100 #for RT efficiency in percent

ax1 = plt.subplot2grid((3, 3), (0, 2), colspan=1, rowspan=1)

ax1.set_xlim(0, 100)
ax1.set_ylim(0, 0.12)
ax1.set_ylim(-.005, 0.12)
ax1.yaxis.set_major_locator(ticker.MultipleLocator(0.04))
#ax1.set_title('Solar Only')
ax1.plot(x, cost_elec_to_main_demand, color = 'black', label= "Main demand\nbuying",linewidth=2)
ax1.plot(x, cost_elec_to_PGP, color = 'pink', label = 'Power-to-H$_{2}$\nbuying',linewidth=2)
ax1.plot(x, cost_elec_from_PGP, color = 'm', label = 'H$_{2}$-to-Power\nselling',linewidth=2)


#ax3.xaxis.set_major_locator(ticker.MultipleLocator(.1))
#ax3.xaxis.set_minor_locator(ticker.MultipleLocator(0.5))
#ax3.xaxis.set_major_formatter(FormatStrFormatter('%gx'))
ax1.xaxis.set_major_formatter(ticker.PercentFormatter())
#ax.set_title('Contribution of each technology\nto total system cost \n vs. PGP costs')
#ax1.set_ylabel('PGP input elec cost/\n total cost of PGP elec') #,color='white'
ax1.set_ylabel('Mean instantaneous\nelectricity cost ($/kWh)')
ax1.set_xlabel('Power-H$_{2}$-Power\nround-trip efficiency')
#ax1.legend(loc='upper center', bbox_to_anchor=(1.8, 1.03))


#======================================================

#======================================================
#fig.text(.36, 0.99, 'Power-to-Gas', size='x-large',fontweight='bold')
#fig.text(.36, 0.66, 'Gas Storage', size='x-large',fontweight='bold')
#fig.text(.36, 0.33, 'Gas-to-Power', size='x-large',fontweight='bold')
#
#fig.text(.16, 0.99, 'Cost', size='large',fontweight='bold')
#fig.text(.65, 0.99, 'Efficiency', size='large',fontweight='bold')
#
#fig.text(.3, 0.02, '--> Direction of Innovation -->', size='large',fontweight='bold')
#fig.text(.05, 0.00, 'Annoated values are max possible system cost improvements ($/kWh) from the base case (circle marker to square marker).', size='medium')


plt.tight_layout()
plt.savefig('fig_disp_rte_costs_freestorage.pdf', bbox_inches='tight')
plt.show()