"""
# Code to loop through different carbon emission reduction constraints;
# Give input table, region of interest, and year;
# Run the code as: >> python Run_Case_Example.py Case_AdvancedNuclear.csv US 2018
# Uploaded by Lei Duan on Febrary 08, 2020.
"""

from Preprocess_Input import preprocess_input
from Run_Core_Model import run_model_main_fun
import numpy as np
#from FindRegion import GetCFsName, update_series, update_timenum


case_input_path_filename = '/Users/jacquelinedowling/MEM/PGP_basecase_14Oct2022.csv'


### Pre-processing
print ('Macro_Energy_Model: Pre-processing input')
case_dic,tech_list = preprocess_input(case_input_path_filename)

#### Find values
for idx in range(len(tech_list)):
    name = tech_list[idx]['tech_name']
    if name == 'to_PGP': to_PGP_idx = idx
    if name == 'from_PGP': from_PGP_idx = idx
    if name == 'PGP_storage': storage_PGP_idx = idx


tech_list[from_PGP_idx]['efficiency'] = 0.5

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
    
    

#tech_list[0] is demand
#tech_list[1] is curtainment
#tech_list[2] is solar
#techlist[3] is wind
#techlist[4] is battery
#techlist[5] is to_PGP
#techlist[6] is PGP_storage
#technlist[7] is from_PGP
    



##One knob
#def run_condition(knob, idx, var, therange, case_name_orig, output_path_orig):
#    case_name_default = case_name_orig
#    output_path_default = output_path_orig
#    case_dic['output_path'] = output_path_default + '/' + knob
#    for val in therange:
#    #set this index for correct tech and knob!
#        tech_list[idx][var] = val 
#        case_dic['case_name'] = case_name_default + '_'+ knob + '_' + str(val)
#        run_model_main_fun(case_dic, tech_list)
        
#Two knobs for RTE   
def run_condition(knob, idx1, idx2, var, therange, case_name_orig, output_path_orig):
    case_name_default = case_name_orig
    output_path_default = output_path_orig
    case_dic['output_path'] = output_path_default + '/' + knob
    for val in therange:
    #set this index for correct tech and knob!
        tech_list[idx1][var] = val 
        tech_list[idx2][var] = val 
        case_dic['case_name'] = case_name_default + '_'+ knob + '_' + str(val)
        run_model_main_fun(case_dic, tech_list)
  
#Run various coniditions in a row
#-----------------------------------------------------------------------

#RTE Efficiency
reset_to_orig(tech_list)
tech_list[to_PGP_idx]['fixed_cost'] = 0
tech_list[from_PGP_idx]['fixed_cost'] = 0
tech_list[storage_PGP_idx]['fixed_cost'] = 0
rte = [1e-6] + [.1/100] + [36/100] + [1/100] + list(np.linspace(5/100, 100/100, 20)) + [99/100]
# rte = [36/100]
therange = np.sqrt(rte)
# therange = [.6]
print(therange)
run_condition('rtePGPeff_freestorage', to_PGP_idx, from_PGP_idx,'efficiency',  therange, case_name_orig, output_path_orig)

      
#Efficiency knobs
#reset_to_orig(tech_list)
#therange = [toPGPeff_orig] + [1e-6] + [1/100] + list(np.linspace(5/100, 100/100, 20))
#run_condition('toPGPeff', to_PGP_idx, 'efficiency',  therange, case_name_orig, output_path_orig)
#
#reset_to_orig(tech_list)
#therange = [fromPGPeff_orig] + [1e-6] + [1/100] + list(np.linspace(5/100, 100/100, 20))
#run_condition('fromPGPeff', from_PGP_idx, 'efficiency',  therange, case_name_orig, output_path_orig)

#reset_to_orig(tech_list)
##therange = list(np.array(np.logspace(-5, -1, 10)))
###therange = list(np.linspace(0*base, 1000*base, 11)) + list(np.linspace(0*base, 1*base, 11)) + list(np.array(np.logspace(-4, 4, 20)*base))
#therange = [storagePGPdecay_orig] + list(np.array(np.logspace(-9, -5, 10)))+ list(np.array(np.logspace(-1, 0, 3)))
#run_condition('storagePGPdecay', storage_PGP_idx, 'decay_rate',  therange, case_name_orig, output_path_orig)


##Cost knobs
#reset_to_orig(tech_list)
#base = toPGPcost_orig
#therange = [toPGPcost_orig] + list(np.linspace(0*base, 1*base, 20)) + list(np.linspace(1*base, 10*base, 10)) + list(np.array(np.logspace(-3, 2, 20)*base))
#run_condition('toPGPcost', to_PGP_idx, 'fixed_cost',  therange, case_name_orig, output_path_orig)
#
#reset_to_orig(tech_list)
#base = fromPGPcost_orig
#therange = list(np.linspace(0*base, 1*base, 20)) + list(np.linspace(1*base, 10*base, 10)) + list(np.array(np.logspace(-3, 2, 20)*base))
#therange = [fromPGPcost_orig] + list(np.linspace(0.05, 0.125, 20))
#run_condition('fromPGPcost', from_PGP_idx, 'fixed_cost',  therange, case_name_orig, output_path_orig)
#
#reset_to_orig(tech_list)
#base = storagePGPcost_orig
#therange = list(np.logspace(-4,-2, 10))
#therange = [storagePGPcost_orig] + list(np.linspace(0*base, 1000*base, 11)) + list(np.linspace(0*base, 1*base, 11)) + list(np.array(np.logspace(-4, 4, 20)*base))
#run_condition('storagePGPcost', storage_PGP_idx, 'fixed_cost',  therange, case_name_orig, output_path_orig)

#       