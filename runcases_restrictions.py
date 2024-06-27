#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 20:46:20 2021

@author: jacquelinedowling
"""

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


#case_input_path_filename = '/Users/jacquelinedowling/MEM/PGP_basecase_08July2021.csv'
#case_input_path_filename = '/Users/jacquelinedowling/MEM/PGP_basecase_16Aug2021.csv'
#case_input_path_filename = '/Users/jacquelinedowling/MEM/PGP_basecase_16Aug2021_natgas.csv'
#case_input_path_filename = '/Users/jacquelinedowling/MEM/PGP_basecase_16Aug2021_nopgp.csv'
case_input_path_filename = '/Users/jacquelinedowling/MEM/PGP_basecase_14Oct2022.csv'


### Pre-processing
print ('Macro_Energy_Model: Pre-processing input')
case_dic,tech_list = preprocess_input(case_input_path_filename)

#===============   
#Set case name

case_name_orig = case_dic['case_name']
output_path_orig = case_dic['output_path']
output_path_default = output_path_orig
#knob1 = 'dpr'
#knob2 = 'h2tur'


def run(knob1, knob2, knob3):

#    case_dic['output_path'] = output_path_default + '/NG_' + knob1 + '_'+ knob2
#    case_dic['output_path'] = output_path_default + '/combos_allng_' + knob1 + '_'+ knob2
    case_dic['output_path'] = output_path_default + '/restrict_'+ knob3 +'_'+ knob1 + '_'+ knob2
 
    
    #===============
    #Set pgp values
    
    for idx in range(len(tech_list)):
        name = tech_list[idx]['tech_name']
        if name == 'to_PGP': to_PGP_idx = idx
        if name == 'from_PGP': from_PGP_idx = idx
        if name == 'PGP_storage': storage_PGP_idx = idx
        
        
        
    if knob1 == 'tank': #tanks
        tech_list[storage_PGP_idx]['fixed_cost'] = 0.000140074 #($15/kWh) #1.61524E-04
        tech_list[storage_PGP_idx]['decay_rate'] = 1.14155E-08 #(0.01%/year)
        
    if knob1 == 'salt': #salt cavern #BASE CASE
        tech_list[storage_PGP_idx]['fixed_cost'] = 1.86672E-05 #($2/kWh)
        tech_list[storage_PGP_idx]['decay_rate'] = 1.14E-08 #(0.01%/year)
        if knob3 == 'eng_restrict':
            tech_list[storage_PGP_idx]['max_capacity'] = 77.0109418 #salt restricted
#            print(tech_list)
    if knob1 == 'dpr': #depleted reservior
        tech_list[storage_PGP_idx]['fixed_cost'] = 3.61392E-07 # ($0.038/kWh)
        tech_list[storage_PGP_idx]['decay_rate'] = 3.99543E-08 #(0.035%/year)
        if knob3 == 'eng_restrict':
            tech_list[storage_PGP_idx]['max_capacity'] = 605.4244808905064 #dpr storage restriction
        
    if knob2 == 'mcfc': #molten carbonate fuel cell
        tech_list[from_PGP_idx]['fixed_cost'] = 0.044442228 #($4,600/kW)
        tech_list[from_PGP_idx]['efficiency'] = 0.7
        
    if knob2 == 'pemfc': #PEM fuel cell #BASE CASE
        tech_list[from_PGP_idx]['fixed_cost'] = 0.014700336 #($1414.74/kW)
        tech_list[from_PGP_idx]['efficiency'] = 0.71
        if knob3 == 'pwr_restrict':
            tech_list[to_PGP_idx]['max_capacity'] = 0.069 # Input to storage restriction
            tech_list[from_PGP_idx]['max_capacity'] = 0.19 # Output from storage restriction

    
    if knob2 == 'h2tur': #hydrogen turbine
        tech_list[from_PGP_idx]['fixed_cost'] = 1.07683E-02 #($1000/kW)
        tech_list[from_PGP_idx]['efficiency'] = 0.5
    
    #===============
    #Set ng sweep
    def run_sweep(val):
        if case_dic.get('co2_constraint',-1) >= 0:
            
            print("before case_dic['co2_constraint']", case_dic['co2_constraint'])
            case_dic['co2_constraint'] = val
            case_dic['co2_constraint'] = case_dic['co2_constraint']
            print("after case_dic['co2_constraint']", case_dic['co2_constraint'])
            
        else:
            case_dic['co2_constraint'] = -1
        case_dic['case_name'] = case_name_default + '_'+ 'constraint_' + knob3 + '_'+ knob1 + '_'+ knob2 + '_' + str(val)+ '__'
        run_model_main_fun(case_dic, tech_list)
    
    #===============
    #Run sweep
    therange = [0]
    #Natural gas unconstrained is when CO2 constraint = 4038.36
#    therange = list(np.array(np.linspace(0, 4038.36, 20)))
#    therange = list(np.array(np.linspace(0, 1000, 10)))
    for i in range(0,len(therange)):
        case_name_default = case_name_orig
        run_sweep(therange[i])


#run('salt','pemfc')
#run('na','na')
   
knob3_list = ['norestricts','eng_restrict','pwr_restrict']
knob1_list = ['salt','dpr']
knob2_list = ['pemfc']

#
for i in knob3_list:
    for j in knob1_list:
        knob3 = i
        knob1 = j
        print (i,j)
        run(knob1,'pemfc',knob3)
        


#
#def run_condition(knob, idx, var, therange, case_name_orig, output_path_orig):
#    case_name_default = case_name_orig
#    output_path_default = output_path_orig
#    case_dic['output_path'] = output_path_default + '/' + knob
#    for val in therange:
#    #set this index for correct tech and knob!
#        tech_list[idx][var] = val 
#        case_dic['case_name'] = case_name_default + '_'+ knob + '_' + str(val)
#        run_model_main_fun(case_dic, tech_list)
#  
#Run various coniditions in a row
#-----------------------------------------------------------------------

      
#Efficiency knobs
#reset_to_orig(tech_list)
#therange = [1e-6] + [1/100] + list(np.linspace(5/100, 100/100, 20))
#run_condition('toPGPeff', to_PGP_idx, 'efficiency',  therange, case_name_orig, output_path_orig)
#
#reset_to_orig(tech_list)
#therange = [1e-6] + [1/100] + list(np.linspace(5/100, 100/100, 20))
#run_condition('fromPGPeff', from_PGP_idx, 'efficiency',  therange, case_name_orig, output_path_orig)
#
#reset_to_orig(tech_list)
##therange = list(np.array(np.logspace(-5, -1, 10)))
###therange = list(np.linspace(0*base, 1000*base, 11)) + list(np.linspace(0*base, 1*base, 11)) + list(np.array(np.logspace(-4, 4, 20)*base))
#therange = list(np.array(np.logspace(-9, -5, 10)))+ list(np.array(np.logspace(-1, 0, 3)))
#run_condition('storagePGPdecay', storage_PGP_idx, 'decay_rate',  therange, case_name_orig, output_path_orig)


#Cost knobs
#reset_to_orig(tech_list)
#base = toPGPcost_orig
#therange = list(np.linspace(0*base, 1*base, 20)) + list(np.linspace(1*base, 10*base, 10)) + list(np.array(np.logspace(-3, 2, 20)*base))
#run_condition('toPGPcost', to_PGP_idx, 'fixed_cost',  therange, case_name_orig, output_path_orig)
##
#reset_to_orig(tech_list)
#base = fromPGPcost_orig
##therange = list(np.linspace(0*base, 1*base, 20)) + list(np.linspace(1*base, 10*base, 10)) + list(np.array(np.logspace(-3, 2, 20)*base))
#therange = list(np.linspace(0.05, 0.125, 20))
#run_condition('fromPGPcost', from_PGP_idx, 'fixed_cost',  therange, case_name_orig, output_path_orig)
#
##reset_to_orig(tech_list)
#base = storagePGPcost_orig
##therange = list(np.logspace(-4,-2, 10))
#therange = list(np.linspace(0*base, 1000*base, 11)) + list(np.linspace(0*base, 1*base, 11)) + list(np.array(np.logspace(-4, 4, 20)*base))
#run_condition('storagePGPcost', storage_PGP_idx, 'fixed_cost',  therange, case_name_orig, output_path_orig)



##-----------------------------------------------------------------------

