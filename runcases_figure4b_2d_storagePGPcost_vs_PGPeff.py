# Code to loop through cost values for two different technologies to create a contour plot

from Preprocess_Input import preprocess_input
from Run_Core_Model import run_model_main_fun
import numpy as np
import math as m
from operator import add

#%% Set Up

# Input File
#case_input_path_filename = 'C:\\Users\\Anna\\Documents\\MEM-master\\rfb_pgp_model_capacity_knobs_no_unmet_dem_form_case.csv'
case_input_path_filename = '/Users/jacquelinedowling/MEM/PGP_basecase_14Oct2022.csv'
#STORAGE

### Pre-processing
print ('Macro_Energy_Model: Pre-processing input')
case_dic,tech_list = preprocess_input(case_input_path_filename)

case_name_orig = case_dic['case_name']
output_path_orig = case_dic['output_path']

#%% Define Functions

# run_two_techs: runs the model by specifying the two technologies, variables to change, and the range over which to change that variable

# tech1 = 1st technology to run the model for
# var1 = variable of 1st technology to vary
# range1 = range over which to vary the variable of 1st technology

# tech2 = 2nd technology to run the model for
# var2 = variable of 2nd technology to vary
# range2 = range over which to vary the variable of 2nd technology

#def run_two_techs(tech1, tech2, var1, var2, range1, range2, case_name_orig, output_path_orig):
#
#    case_name_default = case_name_orig
#    output_path_default = output_path_orig
#    case_dic['output_path'] = output_path_default + '/' + tech1 + tech2
#    
#    knob1_idx = [i for i, j in enumerate(tech_list) if tech_list[i]['tech_name'] == tech1][0]
#    knob2_idx = [i for i, j in enumerate(tech_list) if tech_list[i]['tech_name'] == tech2][0]
#    
#    for i, val in enumerate(range1):
#        
#        x1 = range1[i]
#        tech_list[knob1_idx][var1] = val
#        
#        for i, val in enumerate(range2):
#            x2 = range2[i]
#            tech_list[knob2_idx][var2] = val
#            case_dic['case_name'] = case_name_default + '_' + tech1 + '_' + var1 + '_' + str(x1) + '_' + tech2 + '_' + var2 + '_' + str(x2) 
#            run_model_main_fun(case_dic, tech_list)
#### Find values
for idx in range(len(tech_list)):
    name = tech_list[idx]['tech_name']
    if name == 'to_PGP': to_PGP_idx = idx
    if name == 'from_PGP': from_PGP_idx = idx
    if name == 'PGP_storage': storage_PGP_idx = idx

case_name_orig = case_dic['case_name']
output_path_orig = case_dic['output_path']

toPGPeff_orig = tech_list[to_PGP_idx]['efficiency']
fromPGPeff_orig = tech_list[from_PGP_idx]['efficiency']
storagePGPdecay_orig = tech_list[storage_PGP_idx]['decay_rate']

toPGPcost_orig = tech_list[to_PGP_idx]['fixed_cost']
fromPGPcost_orig = tech_list[from_PGP_idx]['fixed_cost']
storagePGPcost_orig = tech_list[storage_PGP_idx]['fixed_cost']


def reset_to_orig(tech_list):
    tech_list[to_PGP_idx]['efficiency'] = toPGPeff_orig
    tech_list[from_PGP_idx]['efficiency'] = fromPGPeff_orig
    tech_list[storage_PGP_idx]['decay_rate'] = storagePGPdecay_orig
    
    tech_list[to_PGP_idx]['fixed_cost'] = toPGPcost_orig
    tech_list[from_PGP_idx]['fixed_cost'] = fromPGPcost_orig
    tech_list[storage_PGP_idx]['fixed_cost'] = storagePGPcost_orig

#cost and eff ranges all need to be the same length
def run_3techs_2vars(tech1, tech2, tech3, cost, eff, costrange1, costrange2, costrange3, effrange, case_name_orig, output_path_orig):

    case_name_default = case_name_orig
    output_path_default = output_path_orig
    case_dic['output_path'] = output_path_default + '/' + '2d_storagePGPcost_vs_PGPeff'
    
    knob1_idx = [i for i, j in enumerate(tech_list) if tech_list[i]['tech_name'] == tech1][0]
    knob2_idx = [i for i, j in enumerate(tech_list) if tech_list[i]['tech_name'] == tech2][0]
    knob3_idx = [i for i, j in enumerate(tech_list) if tech_list[i]['tech_name'] == tech3][0]
    
    if len(costrange1) == len(costrange2):
        print("cost lengths", len(costrange1),len(costrange2),len(costrange3))
        print("eff length", len(effrange))
        for i in range(0, len(costrange2)):
            # x1 = costrange1[i] #for labeling purposes
            # tech_list[knob1_idx][cost] = costrange1[i]
            x1 = costrange2[i] #for labeling purposes
            tech_list[knob2_idx][cost] = costrange2[i]
            # tech_list[knob3_idx][cost] = costrange3[i]
            print('cost status:', i, '/', len(costrange1))
            
            for j in range(0, len(effrange)):
                x2 = effrange[j] #for labeling purposes
                tech_list[knob1_idx][eff] = effrange[j]
                tech_list[knob3_idx][eff] = effrange[j]
                print('eff status:', j, '/', len(effrange))
                case_dic['case_name'] = case_name_default + '_2d_storagePGPcost_vs_PGPeff___' + tech2  + cost +  str(x1) + '__' + tech1 + tech3 + eff + str(x2) 
                print(case_dic['case_name'])
                print('X eff:',effrange[j]* effrange[j])
                print('Y costs:', costrange1[i]+costrange2[i]+costrange3[i])
                run_model_main_fun(case_dic, tech_list)
            
#rte = [1e-6] + [.1/100] + [1/100] + list(np.linspace(5/100, 100/100, 21)) + [99/100]
# rte = [1e-6] + [.1/100] + [1/100] + [0.05  , 0.0975, 0.145 , 0.1925, 0.24  , 0.2875, 0.335 , 0.3825,
#        0.43  , 0.4775, 0.525 , 0.5725, 0.62  , 0.6675, 0.715 , 0.7625,
#        0.81  , 0.8575, 0.905 , 0.9525, 0.99, 1.    ]

# rte = [1e-6] + [.1/100] + [1/100] + [36/100] + [99/100]+ list(np.linspace(5/100, 100/100, 20))
rte = [1e-6] + [.1/100] + [1/100] + [36/100] + [99/100]+ list(np.linspace(5/100, 100/100, 10))
effrange = np.sqrt(rte)

#3 is for mc fuel cells, 7.5 is for tanks
pcts = [0, 0.001, 0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 1, 3, 7.5, 10, 25, 50, 100]

# pcts = [0, 0.01, 0.1, 0.5, 0.9, 1, 5, 10]

# my_new_list = [i * 5 for i in my_list]
reset_to_orig(tech_list)
# costrange1 = [i * toPGPcost_orig for i in rte]
# costrange2 = [i * storagePGPcost_orig for i in rte]
# costrange3 = [i * fromPGPcost_orig for i in rte]

costrange1 = [i * toPGPcost_orig for i in pcts]
costrange2 = [i * storagePGPcost_orig for i in pcts]
costrange3 = [i * fromPGPcost_orig for i in pcts]


z = [sum(x) for x in zip(costrange1, costrange2, costrange3)]
print(z)


run_3techs_2vars('to_PGP', 'PGP_storage', 'from_PGP', 'fixed_cost', 'efficiency', costrange1, costrange2, costrange3, effrange, case_name_orig, output_path_orig)           

# log_range: reates evenly spaced points on a log scale

# start = beginning of range
# stop = end of range
# numpoints = how many points spaced in the log range
# roundvalue = what decimal point to round the value to

# def log_range(start, stop, numpoints, roundvalue):
#     the_range = [round(i,roundvalue) for i in list(np.logspace(np.log10(start), np.log10(stop), numpoints, endpoint=True, base = 10.0))]
# #    the_range = [0] + the_range
#     print(the_range)
#     return the_range
  
# #%% Run Conditions

# #range1 = log_range(0.01, 1, 8, 6) #cost
# #range2 = log_range(0.1, 100, 8, 6) #efficiency

# range1 = log_range(0.001, .1, 10, 6) #cost #base is 0.0346094
# range2 = log_range(.01, 1, 10, 6) #efficiency 1% to 100%

#range1 = log_range(0.1, 1000, 15, 6)
#range2 = log_range(0.1, 1000, 15, 6)

#run_two_techs('to_PGP', 'to_PGP', 'fixed_cost', 'efficiency', range1, range2, case_name_orig, output_path_orig)
#run_two_techs('battery', 'battery', 'fixed_cost', 'efficiency', range1, range2, case_name_orig, output_path_orig)