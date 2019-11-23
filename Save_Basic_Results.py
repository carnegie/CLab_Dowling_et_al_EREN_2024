# -*- coding: utf-8 -*-

"""

Save_Basic_Results.py

save basic results for the simple energy model
    
"""

# -----------------------------------------------------------------------------


import os
import copy
import numpy as np
import csv
import datetime
import contextlib
import pickle
import utilities
import cvxpy
import pandas as pd

       
#%%
# save scalar results for all cases
def save_basic_results(case_dic, tech_list, constraints,prob_dic,capacity_dic,dispatch_dic,stored_dic):
    
    """
    There is direct input, and results
    This can be per case, per technology, or per time step.
    
    This suggests a 9 item array:
        [input, results]  X [by_case, by_tech, by_timestep]
    
    """
    verbose = case_dic['verbose']  

    input_case_dic = case_dic  # one scalar item per element per case
    input_tech_list = copy.deepcopy( tech_list )
    for tech_dic in input_tech_list: # get rid of series in tech list
        if 'series' in tech_dic:
            del tech_dic['series']
    
    #--------------------------------------------------------------------------
    
    results_case_dic = {}        
    temp_dic = flatten_dic(meanify(prob_dic))
    for key in temp_dic:
        results_case_dic[key] = temp_dic[key]
   
    #--------------------------------------------------------------------------
    
    results_tech_dic = {}
    
    for tech_dic in tech_list:
        tech_name = tech_dic['tech_name']
        if 'series' in tech_dic:
            results_tech_dic[tech_name + ' series'] = np.average(tech_dic['series'])
        if tech_name in capacity_dic:
            results_tech_dic[tech_name + ' capacity'] = capacity_dic[tech_name]
        if tech_name in dispatch_dic:
            results_tech_dic[tech_name + ' dispatch'] = np.average(dispatch_dic[tech_name])
        if tech_name in stored_dic:
            results_tech_dic[tech_name + ' stored'] = np.average(stored_dic[tech_name])
        
            
  
    #--------------------------------------------------------------------------
    input_time_dic = {}
    results_time_dic = {} # one time vector per keyword

    num_time_periods = case_dic['num_time_periods']
    results_time_dic['time_index'] = np.array(range(num_time_periods))
    for item in tech_list:
        tech_name = item['tech_name']
        if 'series' in item:
            input_time_dic[tech_name + ' series'] = item['series']
            if tech_name in capacity_dic:
                factor = capacity_dic[tech_name]
            else:
                factor = 1.0
            results_time_dic[tech_name + ' potential'] = item['series']*factor
    node_price_dic = prob_dic['node_price']
    for node in node_price_dic:
        results_time_dic[node+' price'] = node_price_dic[node]
    for item in dispatch_dic:
        results_time_dic[item] = dispatch_dic[item]
    for item in stored_dic:
        results_time_dic[item] = stored_dic[item]
        
    

    #--------------------------------------------------------------------------
    
    input_case_df = pd.DataFrame(list(input_case_dic.items()))
    input_tech_df = pd.DataFrame(input_tech_list)
    input_time_df = pd.DataFrame(input_time_dic)
    results_case_df = pd.DataFrame(list(results_case_dic.items()))
    results_tech_df = pd.DataFrame(list(results_tech_dic.items()))
    results_time_df = pd.DataFrame(results_time_dic)
    
    output_path = case_dic['output_path']
    case_name = case_dic['case_name']
    output_folder = output_path + "/" + case_name
    today = datetime.datetime.now()
    todayString = str(today.year) + str(today.month).zfill(2) + str(today.day).zfill(2) + '-' + \
        str(today.hour).zfill(2) + str(today.minute).zfill(2) + str(today.second).zfill(2)
    
    output_file_name = case_name + '_'+ todayString
    output_file_path_name = output_folder + "/" + output_file_name
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    with open(output_file_path_name + '.pickle', 'wb') as f:
        pickle.dump([[input_case_dic,  input_tech_list,  input_time_dic],
                     [results_case_dic,results_tech_dic,results_time_dic]], f, protocol=pickle.HIGHEST_PROTOCOL)
    if verbose: 
        print ( 'pickle file written: ' + output_file_path_name + '.pickle' )
    
    writer = pd.ExcelWriter(output_file_path_name + '.xlsx', engine = 'xlsxwriter')
    input_case_df.to_excel(writer, sheet_name = 'case input')
    input_tech_df.to_excel(writer, sheet_name = 'tech input')
    input_time_df.to_excel(writer, sheet_name = 'time input')
    results_case_df.to_excel(writer, sheet_name = 'case results')
    results_tech_df.to_excel(writer, sheet_name = 'tech results')
    results_time_df.to_excel(writer, sheet_name = 'time results') 
    writer.save()
         
    if verbose: 
        print ( 'Excel file written: ' + output_file_path_name + '.xlsx' )
    
    return [[input_case_dic,  input_tech_list,  input_time_dic],
            [results_case_dic,results_tech_dic,results_time_dic]]

 
#%%
# flatten dictionary of dictionaries to dictionary (1 level)
def flatten_dic(dic_in):
    dic_out = {}
    for item in dic_in:
        if dict != type(dic_in[item]):
            dic_out[item] = dic_in[item]
        else: # type is dict
            for sub_item in dic_in[item]:
                dic_out[item + ' ' + sub_item ] = dic_in[item][sub_item]
    return dic_out
    

#%%
# take mean if vector else return value
        
def meanify(dic_in):
    dic_out = copy.deepcopy(dic_in)
    for item in dic_out:
        if np.ndarray == type(dic_out[item]):
            dic_out[item] = np.average(dic_out[item])
        elif dict == type(dic_out[item]):
            dic_out[item] = meanify(dic_out[item])
    return dic_out

#%%
def robust_dic(dic, key):
    if key in dic:
        res = dic[key]
    else:
        res = ""  # Default value if missing key
    return res



#%%  NOTE THAT THIS STILL DOESN'T WORK BECAUSE OF TIME STAMP
def read_pickle_raw_results( case_dic ):
    
    output_path = case_dic['OUTPUT_PATH']
    case_name = case_dic['case_name']
    
    output_folder = output_path + '/' + case_name
    
    output_file_name = case_name + '-' + case_name + '.pickle'
    
    with open(output_folder + "/" + output_file_name, 'rb') as db:
        [[input_case_dic,  input_tech_list,  input_time_dic],
            [results_case_dic,results_tech_dic,results_time_dic]] = pickle.load( db )
    
    return result_dic

