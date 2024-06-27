"""
# Code to loop through different carbon emission reduction constraints;
# Give input table, region of interest, and year;
# Run the code as: >> python Run_Case_Example.py Case_AdvancedNuclear.csv US 2018
# Uploaded by Lei Duan on Febrary 08, 2020.
"""

from Preprocess_Input import preprocess_input
from Run_Core_Model import run_model_main_fun
import numpy as np
import copy as copy
#from FindRegion import GetCFsName, update_series, update_timenum


#case_input_path_filename = '/Users/jacquelinedowling/MEM/PGP_basecase_08July2021.csv'
case_input_path_filename = '/Users/jacquelinedowling/MEM/PGP_basecase_16Aug2021.csv'
#case_input_path_filename = '/Users/jacquelinedowling/MEM/PGP_basecase_16Aug2021_natgas.csv'


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


def run(genknob, tech_list):
    tech_list = copy.deepcopy(tech_list)
    case_dic['output_path'] = output_path_default + '/fixedgenRTE_' + knob1
    
    
    #===============
    #Set pgp values
    
    for idx in range(len(tech_list)):
        name = tech_list[idx]['tech_name']
        if name == 'to_PGP': to_PGP_idx = idx
        if name == 'from_PGP': from_PGP_idx = idx
        if name == 'PGP_storage': storage_PGP_idx = idx
        if name == 'wind': wind_idx = idx
        if name == 'PV': PV_idx = idx
    
        
    if knob1== 'windonly':
        if tech_list[wind_idx]:
            tech_list[PV_idx]['capacity'] = 0
        else:
            print("no wind")
        
    if knob1== 'solaronly':
        if tech_list[PV_idx]:
            tech_list[wind_idx]['capacity'] = 0
        else:
            print("no wind")
        
    if knob1== 'windandsolar':
        if tech_list[wind_idx] and tech_list[PV_idx]:
            pass
        else:
            print('no wind and solar')
          
    
    #===============
    #Set ng sweep
    def run_sweep(val):
            
#        print("before tech_list[to_PGP_idx]['efficiency']", tech_list[to_PGP_idx]['efficiency'])
#        print("before tech_list[from_PGP_idx]['efficiency']", tech_list[from_PGP_idx]['efficiency'])
#        tech_list[to_PGP_idx]['efficiency'] = val
#        tech_list[from_PGP_idx]['efficiency'] = val
#        print("after tech_list[to_PGP_idx]['efficiency']", tech_list[to_PGP_idx]['efficiency'])
#        print("after tech_list[from_PGP_idx]['efficiency']", tech_list[from_PGP_idx]['efficiency'])
#        
#        print("before tech_list[wind_idx]['max_capacity']", tech_list[wind_idx]['max_capacity'])
        tech_list[wind_idx]['capacity'] = val
        print("after tech_list[wind_idx]['capacity']", tech_list[wind_idx]['capacity'])
        
        
            
        case_dic['case_name'] = case_name_default + '_'+ 'fixedwindcap_' + knob1 + '_' + str(val)+ '__'
        run_model_main_fun(case_dic, tech_list)
        print(case_dic['case_name'])
    
    #===============
    #Run sweep
    
#    #RT efficiency range:
#    x = np.linspace(0.0, 1, 21)
#    #PGP input efficiency, PGP output efficiency
#    y = np.sqrt(x)
    
    # Fixed capacity range
    x = np.linspace(0.0, 10, 21)
    print(x)
    therange = list(x)
    for i in range(0,len(therange)):
        case_name_default = case_name_orig
        run_sweep(therange[i])

    

#knob1_list = ['windandsolar','windonly','solaronly']

knob1_list = ['windandsolar']

for i in knob1_list:
    knob1 = i
    print (i)
    run(knob1, tech_list)

        

