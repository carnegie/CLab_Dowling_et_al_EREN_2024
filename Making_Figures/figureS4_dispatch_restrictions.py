#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 15:42:05 2023

@author: jacquelinedowling
"""

#Plot duty cycle of unrestricted salt cavern storage.

import pickle
import numpy as np
import matplotlib.pyplot as plt
import glob
import matplotlib.ticker as ticker

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
    time = []

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
        # print(results)
        demand_source.append(1*(results['demand potential']))
        wind_source.append(1*(results['wind potential']))
        solar_source.append(1*(results['PV potential']))
        batt_source.append(1*(results['battery dispatch']))
        pgp_source.append(1*(results['from_PGP dispatch']))
        
        demand_sink.append(-1*(input_series['demand series']))
        batt_sink.append(-1*(results['battery in dispatch']))
        pgp_sink.append(-1*(results['to_PGP in dispatch']))
        
        curt_avg.append(-1*(results['main_curtailment dispatch']))
        time.append(1*(results['time_index']))
        

    data = (pgp_source, pgp_sink, time)
    return data



#======================================================
fig = plt.figure()
##===========================================================================================================
# (Figure 1a: Energy in storage)

# Plotting code
##============================================================================================================
path = '/Users/jacquelinedowling/MEM/Output_Data/restrict_norestricts_salt_pemfc'

file = glob.glob(path + '/*.pickle')
pickle_in = open(file[0],"rb")
base = pickle.load(pickle_in)
info = base[0][0]
inputs = base[0][1]
results = base[1][2]
input_series = base[0][2]
# print(results)

pgp_eng = results['PGP_storage stored']
x = results['time_index']

ax3 = plt.subplot2grid((3, 3), (0, 0), colspan=1, rowspan=1)

ax3.plot(x, pgp_eng, '-', color='tab:pink', linewidth=1)

ax3.set_ylabel('Energy in storage\n (h of mean U.S. demand)')
ax3.set_xlabel('Hour in year 2017')
ax3.fill_between(x, 0, pgp_eng, color='tab:pink')
ax3.set_title('Salt Cavern\n Unrestricted H${_2}$')
ax3.set_ylim(0,700)

##============================================================================================================
path = '/Users/jacquelinedowling/MEM/Output_Data/restrict_eng_restrict_salt_pemfc'

file = glob.glob(path + '/*.pickle')
pickle_in = open(file[0],"rb")
base = pickle.load(pickle_in)
info = base[0][0]
inputs = base[0][1]
results = base[1][2]
input_series = base[0][2]
# print(results)

pgp_eng = results['PGP_storage stored']
x = results['time_index']

ax3 = plt.subplot2grid((3, 3), (0, 1), colspan=1, rowspan=1)

ax3.plot(x, pgp_eng, '-', color='tab:pink', linewidth=1)
ax3.set_ylabel('Energy in storage\n (h of mean U.S. demand)')
ax3.set_xlabel('Hour in year 2017')
ax3.fill_between(x, 0, pgp_eng, color='tab:pink')

ax3.set_title('Salt Cavern\nH${_2}$ volume restricted')
ax3.set_ylim(0,700)
ax3.axhline(y=77, linestyle ='--')
##============================================================================================================
path = '/Users/jacquelinedowling/MEM/Output_Data/restrict_pwr_restrict_salt_pemfc'

file = glob.glob(path + '/*.pickle')
pickle_in = open(file[0],"rb")
base = pickle.load(pickle_in)
info = base[0][0]
inputs = base[0][1]
results = base[1][2]
input_series = base[0][2]
# print(results)

pgp_eng = results['PGP_storage stored']
x = results['time_index']

ax3 = plt.subplot2grid((3, 3), (0, 2), colspan=1, rowspan=1)

ax3.plot(x, pgp_eng, '-', color='tab:pink', linewidth=1)
ax3.set_ylabel('Energy in storage\n (h of mean U.S. demand)')
ax3.set_xlabel('Hour in year 2017')
ax3.fill_between(x, 0, pgp_eng, color='tab:pink')

ax3.set_title('Salt Cavern\nH${_2}$ flow rate restricted')
ax3.set_ylim(0,700)

##============================================================================================================

##===========================================================================================================
# (Figure 1b: Charge/Discharge)

# Plotting code
##============================================================================================================
path = '/Users/jacquelinedowling/MEM/Output_Data/restrict_norestricts_salt_pemfc'

ax3 = plt.subplot2grid((3, 3), (1, 0), colspan=1, rowspan=1)
data = getdatadisp(path, 7 , 'efficiency')
pgp_source = data[0][0]
pgp_sink = data[1][0]
time = data[2][0]

x = time

y1 = np.vstack([pgp_source  ])
pal1 = ['m']
labels1 = ["H$_{2}$-to-Power"]

y2 = np.vstack([pgp_sink])
pal2 = ['pink']
labels2 = ['Power-to-H$_{2}$']

ax3.stackplot(x, y1, colors=pal1, labels=labels1)
ax3.stackplot(x, y2, colors=pal2, labels=labels2)
ax3.set_ylim(-1, 1)

ax3.yaxis.set_tick_params(direction='out', which='both')
ax3.set_ylabel('Electricity\nsources and sinks (kW)\n (1 = mean U.S. demand)')
ax3.set_xlabel('Hour in year 2017')
##============================================================================================================
path = '/Users/jacquelinedowling/MEM/Output_Data/restrict_eng_restrict_salt_pemfc'

ax3 = plt.subplot2grid((3, 3), (1, 1), colspan=1, rowspan=1)
data = getdatadisp(path, 7 , 'efficiency')
pgp_source = data[0][0]
pgp_sink = data[1][0]
time = data[2][0]

x = time

y1 = np.vstack([pgp_source  ])
pal1 = ['m']
labels1 = ["H$_{2}$-to-Power"]

y2 = np.vstack([pgp_sink])
pal2 = ['pink']
labels2 = ['Power-to-H$_{2}$']

ax3.stackplot(x, y1, colors=pal1, labels=labels1)
ax3.stackplot(x, y2, colors=pal2, labels=labels2)
ax3.set_ylim(-1, 1)

ax3.yaxis.set_tick_params(direction='out', which='both')
ax3.set_ylabel('Electricity\nsources and sinks (kW)\n (1 = mean U.S. demand)')
ax3.set_xlabel('Hour in year 2017')

##============================================================================================================
path = '/Users/jacquelinedowling/MEM/Output_Data/restrict_pwr_restrict_salt_pemfc'

ax3 = plt.subplot2grid((3, 3), (1, 2), colspan=1, rowspan=1)
data = getdatadisp(path, 7 , 'efficiency')
pgp_source = data[0][0]
pgp_sink = data[1][0]
time = data[2][0]

x = time

y1 = np.vstack([pgp_source  ])
pal1 = ['m']
labels1 = ["H$_{2}$-to-Power"]

y2 = np.vstack([pgp_sink])
pal2 = ['pink']
labels2 = ['Power-to-H$_{2}$']

ax3.stackplot(x, y1, colors=pal1, labels=labels1)
ax3.stackplot(x, y2, colors=pal2, labels=labels2)
ax3.set_ylim(-1, 1)

ax3.yaxis.set_tick_params(direction='out', which='both')
ax3.set_ylabel('Electricity\nsources and sinks (kW)\n (1 = mean U.S. demand)')
ax3.set_xlabel('Hour in year 2017')

ax3.axhline(y=-.069, linestyle ='--')
ax3.axhline(y=.19, linestyle ='--')
##============================================================================================================

plt.tight_layout()
plt.savefig('fig_restrictions_salt.pdf', bbox_inches='tight')
plt.show()














fig = plt.figure()
##===========================================================================================================
# (Figure 1a: Energy in storage)

# Plotting code
##============================================================================================================
path = '/Users/jacquelinedowling/MEM/Output_Data/restrict_norestricts_dpr_pemfc'

file = glob.glob(path + '/*.pickle')
pickle_in = open(file[0],"rb")
base = pickle.load(pickle_in)
info = base[0][0]
inputs = base[0][1]
results = base[1][2]
input_series = base[0][2]
# print(results)

pgp_eng = results['PGP_storage stored']
x = results['time_index']

ax3 = plt.subplot2grid((3, 3), (0, 0), colspan=1, rowspan=1)

ax3.plot(x, pgp_eng, '-', color='tab:pink', linewidth=1)

ax3.set_ylabel('Energy in storage\n (h of mean U.S. demand)')
ax3.set_xlabel('Hour in year 2017')
ax3.fill_between(x, 0, pgp_eng, color='tab:pink')
ax3.set_title('Depleted Reservoir\n Unrestricted H${_2}$')
ax3.set_ylim(0,700)
##============================================================================================================
path = '/Users/jacquelinedowling/MEM/Output_Data/restrict_eng_restrict_dpr_pemfc'

file = glob.glob(path + '/*.pickle')
pickle_in = open(file[0],"rb")
base = pickle.load(pickle_in)
info = base[0][0]
inputs = base[0][1]
results = base[1][2]
input_series = base[0][2]
# print(results)

pgp_eng = results['PGP_storage stored']
x = results['time_index']

ax3 = plt.subplot2grid((3, 3), (0, 1), colspan=1, rowspan=1)

ax3.plot(x, pgp_eng, '-', color='tab:pink', linewidth=1)
ax3.set_ylabel('Energy in storage\n (h of mean U.S. demand)')
ax3.set_xlabel('Hour in year 2017')
ax3.fill_between(x, 0, pgp_eng, color='tab:pink')

ax3.set_title('Depleted Reservoir\nH${_2}$ volume restricted')
ax3.set_ylim(0,700)
ax3.axhline(y=605, linestyle ='--')
##============================================================================================================
path = '/Users/jacquelinedowling/MEM/Output_Data/restrict_pwr_restrict_dpr_pemfc'

file = glob.glob(path + '/*.pickle')
pickle_in = open(file[0],"rb")
base = pickle.load(pickle_in)
info = base[0][0]
inputs = base[0][1]
results = base[1][2]
input_series = base[0][2]
# print(results)

pgp_eng = results['PGP_storage stored']
x = results['time_index']

ax3 = plt.subplot2grid((3, 3), (0, 2), colspan=1, rowspan=1)

ax3.plot(x, pgp_eng, '-', color='tab:pink', linewidth=1)
ax3.set_ylabel('Energy in storage\n (h of mean U.S. demand)')
ax3.set_xlabel('Hour in year 2017')
ax3.fill_between(x, 0, pgp_eng, color='tab:pink')

ax3.set_title('Depleted Reservoir\nH${_2}$ flow rate restricted')
ax3.set_ylim(0,700)
##===========================================================================================================
# (Figure 1b: Charge/Discharge)

# Plotting code
##============================================================================================================
path = '/Users/jacquelinedowling/MEM/Output_Data/restrict_norestricts_dpr_pemfc'

ax3 = plt.subplot2grid((3, 3), (1, 0), colspan=1, rowspan=1)
data = getdatadisp(path, 7 , 'efficiency')
pgp_source = data[0][0]
pgp_sink = data[1][0]
time = data[2][0]

x = time

y1 = np.vstack([pgp_source  ])
pal1 = ['m']
labels1 = ["H$_{2}$-to-Power"]

y2 = np.vstack([pgp_sink])
pal2 = ['pink']
labels2 = ['Power-to-H$_{2}$']

ax3.stackplot(x, y1, colors=pal1, labels=labels1)
ax3.stackplot(x, y2, colors=pal2, labels=labels2)
ax3.set_ylim(-1, 1)

ax3.yaxis.set_tick_params(direction='out', which='both')
ax3.set_ylabel('Electricity\nsources and sinks (kW)\n (1 = mean U.S. demand)')
ax3.set_xlabel('Hour in year 2017')
##============================================================================================================
path = '/Users/jacquelinedowling/MEM/Output_Data/restrict_eng_restrict_dpr_pemfc'

ax3 = plt.subplot2grid((3, 3), (1, 1), colspan=1, rowspan=1)
data = getdatadisp(path, 7 , 'efficiency')
pgp_source = data[0][0]
pgp_sink = data[1][0]
time = data[2][0]

x = time

y1 = np.vstack([pgp_source  ])
pal1 = ['m']
labels1 = ["H$_{2}$-to-Power"]

y2 = np.vstack([pgp_sink])
pal2 = ['pink']
labels2 = ['Power-to-H$_{2}$']

ax3.stackplot(x, y1, colors=pal1, labels=labels1)
ax3.stackplot(x, y2, colors=pal2, labels=labels2)
ax3.set_ylim(-1, 1)

ax3.yaxis.set_tick_params(direction='out', which='both')
ax3.set_ylabel('Electricity\nsources and sinks (kW)\n (1 = mean U.S. demand)')
ax3.set_xlabel('Hour in year 2017')

##============================================================================================================
path = '/Users/jacquelinedowling/MEM/Output_Data/restrict_pwr_restrict_dpr_pemfc'

ax3 = plt.subplot2grid((3, 3), (1, 2), colspan=1, rowspan=1)
data = getdatadisp(path, 7 , 'efficiency')
pgp_source = data[0][0]
pgp_sink = data[1][0]
time = data[2][0]

x = time

y1 = np.vstack([pgp_source  ])
pal1 = ['m']
labels1 = ["H$_{2}$-to-Power"]

y2 = np.vstack([pgp_sink])
pal2 = ['pink']
labels2 = ['Power-to-H$_{2}$']

ax3.stackplot(x, y1, colors=pal1, labels=labels1)
ax3.stackplot(x, y2, colors=pal2, labels=labels2)
ax3.set_ylim(-1, 1)

ax3.yaxis.set_tick_params(direction='out', which='both')
ax3.set_ylabel('Electricity\nsources and sinks (kW)\n (1 = mean U.S. demand)')
ax3.set_xlabel('Hour in year 2017')
ax3.axhline(y=-.069, linestyle ='--')
ax3.axhline(y=.19, linestyle ='--')
# ax3.set_xlim(0,8760)
# ax3.xaxis.set_major_locator(ticker.MultipleLocator(3000))
##============================================================================================================


plt.tight_layout()
plt.savefig('fig_restrictions_dpr.pdf', bbox_inches='tight')
plt.show()
