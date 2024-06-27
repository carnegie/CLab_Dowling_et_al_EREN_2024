#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 15:58:44 2023

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

#case_input_path_filename = '/Users/jacquelinedowling/MEM/PGP_basecase_14Oct2022.csv'
# case_input_path_filename = '/Users/jacquelinedowling/MEM/PGP_basecase_14Oct2022_natgas.csv'
#case_input_path_filename = '/Users/jacquelinedowling/MEM/PGP_basecase_14Oct2022_nopgp.csv'
# case_input_path_filename = '/Users/jacquelinedowling/MEM/PGP_basecase_14Oct2022_natgas_nostorage.csv'
# case_input_path_filename = '/Users/jacquelinedowling/MEM/PGP_basecase_14Oct2022_natgas_nostorage_RI.csv'
case_input_path_filename = '/Users/jacquelinedowling/MEM/PGP_basecase_14Oct2022_natgas_storage_RI.csv'


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


def run():

    case_dic['output_path'] = output_path_default + '/NG_windsolar_storage_RI'
    # case_dic['output_path'] = output_path_default + '/NG_windsolar_nostorage'
#    case_dic['output_path'] = output_path_default + '/combos_allng_' + knob1 + '_'+ knob2
#    case_dic['output_path'] = output_path_default + '/combos_nopgp_' + knob1 + '_'+ knob2
#    case_dic['output_path'] = output_path_default + '/combos_' + knob1 + '_'+ knob2
 
    
    #===============
    #Set pgp values
    
    for idx in range(len(tech_list)):
        name = tech_list[idx]['tech_name']
        if name == 'to_PGP': to_PGP_idx = idx
        if name == 'from_PGP': from_PGP_idx = idx
        if name == 'PGP_storage': storage_PGP_idx = idx
 
    
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
        case_dic['case_name'] = case_name_default + '_'+ 'ng_' + str(val)+ '__'
#        case_dic['case_name'] = case_name_default + '_'+ 'combos_' + knob1 + '_'+ knob2
        
        run_model_main_fun(case_dic, tech_list)
    
    #===============
    #Run sweep
#    therange = [4038.36]
#    therange = [0]
    #Natural gas unconstrained is when CO2 constraint = 4038.36
    # therange = [0.1*4038.36, 0.2*4038.36, 0.3*4038.36]
    # therange = [0.001*4038.36, 0.0001*4038.36, 0.00001*4038.36]
    # therange = [0.01*4038.36,.02*4038.36, .03*4038.36, .04*4038.36, .04*4038.36, .05*4038.36]
    therange = [0.00001*4038.36, 0.0001*4038.36, 0.001*4038.36, 0.01*4038.36,.02*4038.36, .03*4038.36, .04*4038.36, .05*4038.36]
    # therange = [0.37*4038.36,.36*4038.36, .35*4038.36, .34*4038.36, .33*4038.36, .32*4038.36]
    # therange = list(np.array(np.linspace(0, 4038.36, 20)))
#    to see the percentages therange = list(np.linspace(0, 807.672*(1/4038.36), 21)) 
#    therange = list(np.linspace(0, 807.672, 21))
#    therange = list(np.array(np.linspace(0, 1000, 10)))
    for i in range(0,len(therange)):
        case_name_default = case_name_orig
        try:
            run_sweep(therange[i])
        except:
            pass
run()

    # raise cvx.error.SolverError
#run('salt','pemfc')
#run('na','na')
    
#knob1_list = ['tank','salt','dpr']
#knob2_list = ['mcfc', 'pemfc', 'h2tur']
#
#for i in knob1_list:
#    for j in knob2_list:
#        knob1 = i
#        knob2 = j
#        print (i,j)
#        run(knob1,knob2)
        


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

