# Code to loop through cost values for two different technologies to create a contour plot

from Preprocess_Input import preprocess_input
from Run_Core_Model import run_model_main_fun
import numpy as np
import math as m

#%% Set Up

# Input File
#case_input_path_filename = 'C:\\Users\\Anna\\Documents\\MEM-master\\rfb_pgp_model_capacity_knobs_no_unmet_dem_form_case.csv'
case_input_path_filename = '/Users/jacquelinedowling/MEM/PGP_basecase_16Aug2021.csv'
# case_input_path_filename = '/Users/jacquelinedowling/MEM/PGP_basecase_14Oct2022.csv' #NEED TO RERUN

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

def run_two_techs(tech1, tech2, var1, var2, range1, range2, case_name_orig, output_path_orig):

    case_name_default = case_name_orig
    output_path_default = output_path_orig
    case_dic['output_path'] = output_path_default + '/' + tech1 + tech2
    
    knob1_idx = [i for i, j in enumerate(tech_list) if tech_list[i]['tech_name'] == tech1][0]
    knob2_idx = [i for i, j in enumerate(tech_list) if tech_list[i]['tech_name'] == tech2][0]
    
    for i, val in enumerate(range1):
        
        x1 = range1[i]
        tech_list[knob1_idx][var1] = val
        
        for i, val in enumerate(range2):
            x2 = range2[i]
            tech_list[knob2_idx][var2] = val
            case_dic['case_name'] = case_name_default + '_' + tech1 + '_' + var1 + '_' + str(x1) + '_' + tech2 + '_' + var2 + '_' + str(x2) 
            run_model_main_fun(case_dic, tech_list)
            

# log_range: reates evenly spaced points on a log scale

# start = beginning of range
# stop = end of range
# numpoints = how many points spaced in the log range
# roundvalue = what decimal point to round the value to

def log_range(start, stop, numpoints, roundvalue):
    the_range = [round(i,roundvalue) for i in list(np.logspace(np.log10(start), np.log10(stop), numpoints, endpoint=True, base = 10.0))]
#    the_range = [0] + the_range
    print(the_range)
    return the_range
  
#%% Run Conditions

#range1 = log_range(0.01, 1, 8, 6) #cost
#range2 = log_range(0.1, 100, 8, 6) #efficiency

range1 = log_range(0.001, .1, 10, 6) #cost #base is 0.023461168
range2 = log_range(.01, 1, 10, 6) #efficiency 1% to 100%


#range1 = log_range(0.1, 1000, 15, 6)
#range2 = log_range(0.1, 1000, 15, 6)

run_two_techs('from_PGP', 'from_PGP', 'fixed_cost', 'efficiency', range1, range2, case_name_orig, output_path_orig)