#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 13:26:30 2023

@author: jacquelinedowling
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 22:04:51 2021

@author: jacquelinedowling
"""

#PGP restrict

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

#dict_keys(['tech_name', 'tech_type', 'node_to', 'series_file', 'fixed_cost'])
#dict_keys(['tech_name', 'tech_type', 'node_to', 'node_from', 'fixed_cost', 'var_cost', 'efficiency', 'charging_time', 'decay_rate'])
#dict_keys(['tech_name', 'tech_type', 'node_to', 'node_from', 'fixed_cost', 'var_cost', 'efficiency'])

##==============================================
plt.rcParams.update({'axes.titlesize': 'large'})
plt.rcParams.update({'axes.labelsize': 'large'})

import matplotlib.pylab as pylab
params = {'legend.fontsize': 'medium',
          'figure.figsize': (8, 4),
         'axes.labelsize': 'large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'large',
         'ytick.labelsize':'large'}
pylab.rcParams.update(params)

fig = plt.figure()


#======================================================

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
    
def getbardata(path):
    unsortedlist = glob.glob(path + '/*.pickle')
#    print(unsortedlist, path)
    pickle_in = open(unsortedlist[0],"rb")
#        print(unsortedlist[i])
    base = pickle.load(pickle_in)
    info = base[0]
    inputs = base[0][1]
    results = base[1]
    
    sun_cost=[]
    wind_cost=[]
    batt_cost=[]
    pgp_cost=[]
    ng_cost = []
    topgp_cost = []
    storagepgp_cost =[]
    frompgp_cost = []

    dic = get_cost_contributions(base)
    sun_cost.append(dic['PV'])
    wind_cost.append(dic['wind'])
    batt_cost.append(dic['battery'])
    if 'natgas' in dic:
        ng_cost.append(dic['natgas'])
    else:
        ng_cost.append(0.0)
    if 'to_PGP' in dic:
        pgp_cost.append(dic['to_PGP']+dic['PGP_storage']+dic['from_PGP'])
        topgp_cost.append(dic['to_PGP'])
        storagepgp_cost.append(dic['PGP_storage'])
        frompgp_cost.append(dic['from_PGP'])
    else:
        pgp_cost.append(0.0)
        topgp_cost.append(0.0)
        storagepgp_cost.append(0.0)
        frompgp_cost.append(0.0)
    data = (wind_cost,sun_cost,  batt_cost, topgp_cost, storagepgp_cost, frompgp_cost,  ng_cost)
    return data

#======================================================
path_ng='/Users/jacquelinedowling/MEM/Output_Data/combos_allng_salt_pemfc'

path_nopgp='/Users/jacquelinedowling/MEM/Output_Data/combos_nopgp_na_na'

path1 = '/Users/jacquelinedowling/MEM/Output_Data/restrict_norestricts_salt_pemfc'
path2 = '/Users/jacquelinedowling/MEM/Output_Data/restrict_eng_restrict_salt_pemfc'
path3 = '/Users/jacquelinedowling/MEM/Output_Data/restrict_pwr_restrict_salt_pemfc' 

path4 = '/Users/jacquelinedowling/MEM/Output_Data/restrict_norestricts_dpr_pemfc'
path5 = '/Users/jacquelinedowling/MEM/Output_Data/restrict_eng_restrict_dpr_pemfc'
path6 = '/Users/jacquelinedowling/MEM/Output_Data/restrict_pwr_restrict_dpr_pemfc'


pathlist = [path_ng, path_nopgp, path1,path2,path3,path4,path5,path6]

#===============================================================
#prep for bar plotting

wind_costs=[]
sun_costs=[]
batt_costs=[]
topgp_costs = []
storagepgp_costs =[]
frompgp_costs = []
ng_costs = []
for i in pathlist:
    data = getbardata(i)
    wind_costs.append(data[0])
    sun_costs.append(data[1])
    batt_costs.append(data[2])
    topgp_costs.append(data[3])
    storagepgp_costs.append(data[4])
    frompgp_costs.append(data[5])
    ng_costs.append(data[6])
    

data = (wind_costs, sun_costs,  batt_costs, topgp_costs, storagepgp_costs, frompgp_costs,  ng_costs)

#Add in white spaces in between groups of data 
newdata = []

for i in data:
    insert1 = np.insert(i, 2, 0)
    insert2 = np.insert(insert1, 6, 0)
#    insert3 = np.insert(insert2, 6, 0)
    newlist = insert2
    newdata.append(newlist)


N = 10
ind = np.arange(N)    # the x locations for the groups
width = 0.6       # the width of the bars: can also be len(x) sequence

dataset1 = np.array(newdata[0])
dataset2 = np.array(newdata[1])
dataset3 = np.array(newdata[2])
dataset4 = np.array(newdata[3])
dataset5 = np.array(newdata[4])
dataset6 = np.array(newdata[5])
dataset7 = np.array(newdata[6])

#===============================================================
#Plotting

fig = plt.figure()
ax = plt.subplot2grid((1, 1), (0, 0), colspan=1, rowspan=1)

solar_q = 'orange'
wind_q = 'blue'
pgp_t = 'pink'
pgp_s = 'tab:pink'
pgp_f = 'm'
batt_q = 'purple'

p1 = ax.bar(ind, dataset1, width, color=wind_q)
p2 = ax.bar(ind, dataset2, width, bottom=dataset1, color=solar_q)
p3 = ax.bar(ind, dataset3, width, bottom=dataset1+dataset2, color=batt_q)
p4 = ax.bar(ind, dataset4, width, bottom=dataset1+dataset2+dataset3,
             color='pink')
p5 = ax.bar(ind, dataset5, width, bottom=dataset1+dataset2+dataset3+dataset4,
             color='tab:pink')
p6 = ax.bar(ind, dataset6, width, bottom=dataset1+dataset2+dataset3+dataset4+dataset5,
             color='m')
p7 = ax.bar(ind, dataset7, width, bottom=dataset1+dataset2+dataset3+dataset4+dataset5+dataset6,
             color='saddlebrown')


ax.set_xticks(ind, ( 'Natural gas only','Wind solar battery only', 'Salt cavern',
                    'Unrestricted H${_2}$','H${_2}$ volume restricted','H${_2}$ flow rate restricted',
                 'Depleted reservoir',
                 'Unrestricted H${_2}$', 'H${_2}$ volume restricted', 'H${_2}$ flow rate restricted' ),
              rotation=90, ha='center')
# rotation=45, ha='right'
#plt.yticks(np.arange(0, 81, 10))
# ax.legend((p1[0], p2[0], p3[0], p4[0], p5[0], p6[0], p7[0]),
#            ('Wind','Solar', 'Battery','Power-H${_2}$','H${_2}$ storage', 'H${_2}$-Power','Natural\ngas' ),
#            loc='upper center', bbox_to_anchor=(1.15, 1.03))


# ax.set_ylabel('System cost ($/kWh) ')

xticks = ax.xaxis.get_major_ticks()
# xticks[2].set_visible(False)
# xticks[6].set_visible(False)
ax.set_ylim(0, 0.12)
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.04))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.02))
ax.yaxis.set_ticks_position('both')


ax2 = ax.twinx()
ax2.set_ylabel('System cost ($/kWh)')

ax2.set_ylim(0, 0.12)
ax2.yaxis.set_major_locator(ticker.MultipleLocator(0.04))
ax2.yaxis.set_minor_locator(ticker.MultipleLocator(0.02))

yticks = ax2.yaxis.get_major_ticks()
plt.yticks(rotation=90, va = 'center')

yticksleft = ax.yaxis.get_major_ticks()
for i in range(0,len(yticksleft)):
    yticksleft[i].set_visible(False)

yticksleft = ax.yaxis.get_minor_ticks()
for i in range(0,len(yticksleft)):
    yticksleft[i].set_visible(False)


# 
# ax2.set_yticks(yticks,rotation = 45)

#ax2.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))


#chartBox = ax2.get_position()
#ax2.set_position([chartBox.x0, chartBox.y0, chartBox.width*1, chartBox.height])
#ax2.legend(loc='upper center', bbox_to_anchor=(1.45, 1.02))

# Add xticks on the middle of the group bars
#plt.xlabel('Simulations\n Vary generation: Solar, Wind, Solar+Wind \nVary storage: PGP, Battery, PGP+Battery')
#fig.text(.14, 0.75, 'Natural\ngas only', size='medium')
#fig.text(.38, 0.75, 'PGP\nSalt caverns', size='medium',ha='center')
##fig.text(.49, 0.75, 'Salt\ncaverns', size='medium')
#fig.text(.64, 0.75, 'PGP\nDepleted fields', size='medium',ha='center')
#fig.text(.82, 0.75, 'No\nPGP', size='medium')

# fig.text(.34, 0.8, 'Salt cavern', size='medium')
# fig.text(.57, 0.8, 'Depleted reservoir', size='medium')



plt.savefig('barplot_pgprestrict.pdf', bbox_inches='tight')
plt.savefig('barplot_pgprestrict.png', bbox_inches='tight')
#plt.savefig('combos_h2turbines.eps', bbox_inches='tight')
plt.show()
    