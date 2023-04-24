# PLEASE NOTE THAT THIS CODE IS GOING TO TAKE A WHILE TO EXECUTE

import pandas as pd
import numpy as np
from datetime import datetime,timedelta


"""
Specify the range of the **loop**. The dataset is from *(Person)* 1 to 35, the start is the number you want the dataset to run from, and the end is the last number minus 1

For example: if your start is 4 and the end is 11, the processed dataset will be from dataset number 4 to 10.

You can adjust the start and save to your desire number. max is 36 which starts for the 35th person.
"""
start = 1
end = 36


"""
Within the loop, the `globals()` function is used to dynamically access and update variables in the global namespace. Specifically, the globals() function is used to get a reference to a variable with a specific name, based on the current value of i. Using the string format syntax `acc%sm` for example, when i is 1, the code will access the variable named acc1.
"""

# Reading the 35 dataset into variables
for i in range(start, end):
    if i < 10:
        acc = 'https://raw.githubusercontent.com/italha-d/Stress-Predict-Dataset/main/Raw_data/S0' + str(i) + '/ACC.csv'
        bvp = 'https://raw.githubusercontent.com/italha-d/Stress-Predict-Dataset/main/Raw_data/S0' + str(i) + '/BVP.csv'
        eda = 'https://raw.githubusercontent.com/italha-d/Stress-Predict-Dataset/main/Raw_data/S0' + str(i) + '/EDA.csv'
        temp = 'https://raw.githubusercontent.com/italha-d/Stress-Predict-Dataset/main/Raw_data/S0' + str(i) + '/TEMP.csv'
    else:
        acc = 'https://raw.githubusercontent.com/italha-d/Stress-Predict-Dataset/main/Raw_data/S' + str(i) + '/ACC.csv'
        bvp = 'https://raw.githubusercontent.com/italha-d/Stress-Predict-Dataset/main/Raw_data/S' + str(i) + '/BVP.csv'
        eda = 'https://raw.githubusercontent.com/italha-d/Stress-Predict-Dataset/main/Raw_data/S' + str(i) + '/EDA.csv'
        temp = 'https://raw.githubusercontent.com/italha-d/Stress-Predict-Dataset/main/Raw_data/S' + str(i) + '/TEMP.csv'
    globals()['acc%s'%i]= pd.read_csv(acc, header=None, names=['x', 'y', 'z'])
    globals()['bvp%s'%i]= pd.read_csv(bvp, header=None, names=['bvp'])
    globals()['eda%s'%i]= pd.read_csv(eda, header=None, names=['eda'])
    globals()['temp%s'%i]= pd.read_csv(temp, header=None, names=['temp'])




### Adding date to the dataset using the information provided in the first and second row of the respecitive datatset

# ACC
    globals()['acc%s'%i]["Datetime"] = datetime.utcfromtimestamp(globals()['acc%s'%i].loc[0,"x"])
    freq_acc = globals()['acc%s'%i].loc[1,"x"]
    globals()['acc%s'%i] = globals()['acc%s'%i].reset_index(drop=True)
    
    for k,v in globals()['acc%s'%i].iterrows():
        globals()['acc%s'%i]["Datetime"].iloc[k] = globals()['acc%s'%i]["Datetime"].iloc[k] + timedelta(seconds = k*(1/freq_acc))


# BVP
    globals()['bvp%s'%i]["Datetime"] = datetime.utcfromtimestamp(globals()['bvp%s'%i].loc[0,"bvp"])
    freq_bvp = globals()['bvp%s'%i].loc[1,"bvp"]
    globals()['bvp%s'%i] = globals()['bvp%s'%i].reset_index(drop=True)
    
    for k,v in globals()['bvp%s'%i].iterrows():
        globals()['bvp%s'%i]["Datetime"].iloc[k] = globals()['bvp%s'%i]["Datetime"].iloc[k] + timedelta(seconds = k*(1/freq_bvp))


# EDA
    globals()['eda%s'%i]["Datetime"] = datetime.utcfromtimestamp(globals()['eda%s'%i].loc[0,"eda"])
    freq_eda = globals()['eda%s'%i].loc[1,"eda"]
    globals()['eda%s'%i] = globals()['eda%s'%i].reset_index(drop=True)

    for k,v in globals()['eda%s'%i].iterrows():
        globals()['eda%s'%i]["Datetime"].iloc[k] = globals()['eda%s'%i]["Datetime"].iloc[k] + timedelta(seconds = k*(1/freq_eda))


# TEMP
    globals()['temp%s'%i]["Datetime"] = datetime.utcfromtimestamp(globals()['temp%s'%i].loc[0,"temp"])
    freq_temp = globals()['temp%s'%i].loc[1,"temp"]
    globals()['temp%s'%i] = globals()['temp%s'%i].reset_index(drop=True)
    
    for k,v in globals()['temp%s'%i].iterrows():
        globals()['temp%s'%i]["Datetime"].iloc[k] = globals()['temp%s'%i]["Datetime"].iloc[k] + timedelta(seconds = k*(1/freq_temp))


### READ TIME LOG XLSX
"""
This timelog from the link has been adjusted, the original file uses am and pm time type but the time added to the dataset is 24 hours time. so 1:14 was adjusted to 13:14, 3:15 to 15:15 and so on.
"""
log = pd.read_excel('https://www.dropbox.com/s/dmsj115f742esma/Time_logs%20mod.xlsx?dl=1', sheet_name=0)


# Picking a date from timelog and turn it to datetime value
# Time Function
def get_time_log(col,id):
    a = str(log.loc[log["S. ID."]==id,col].iloc[0])
    b = log.loc[log["S. ID."]==id,"Date"].dt.date.astype(str).iloc[0]
    return pd.to_datetime(b+" "+a,format="%Y-%m-%d %H:%M:%S.%f")


# Turning datetime value to timestamp value
# Get Time Stamp Value
def time_utc_timestamp_value(timval):
 #return datetime.timestamp(datetime.strptime(timval, '%Y-%m-%d %H:%M:%S.%f'))
    return datetime.timestamp(timval)



# Get Time Stamp Value
# timval = '2022-02-07 09:29:00.000000'
def utc_value(tim):
    return datetime.timestamp(datetime.strptime(tim, '%Y-%m-%d %H:%M:%S.%f'))

# Get Time Stamp Value
# timval = '2022-02-07 09:29:00.000000'
def utc_value(tim):
    return datetime.timestamp(datetime.strptime(tim, '%Y-%m-%d %H:%M:%S.%f'))


"""
Using Time frame start and end time to get Data that falls within a certain time range
"""
# Time frame start and end time to get Data to turn to Mean
def use_time_to_frame(dataframe, start_time, end_time):
    filtered = []
    for i, data in enumerate(dataframe.Datetime):
        if ((datetime.timestamp(data) >= start_time) and (datetime.timestamp(data) < end_time)):
            filtered.append(dataframe.loc[i])
            
    result = pd.DataFrame(filtered)
    return result


# Getting dataframe within a certain test range and assigning the respective label
# Get Class with Label for ACC
#result_acc1_ns = use_time_to_frame(acc1.Datetime, "2022-02-07 09:29:00.000000", "2022-02-07 09:34:00.000000")
def Label_Acc(result_df, person, label):
    result_df.index = result_df.Datetime
    result_df = result_df.drop("Datetime",axis=1)
    result_df["x"] = result_df["x"].resample('0.25S').mean()
    result_df["y"] = result_df["y"].resample('0.25S').mean()
    result_df["z"] = result_df["z"].resample('0.25S').mean()
    result_df.dropna(inplace=True)
    result_df['Person'] = person
    #result_df['Label'] = label
    
    return result_df


def Label_BVP_EDA_TEMP(result_dff, col_name, label):
    result_dff.index = result_dff.Datetime
    result_dff = result_dff.drop("Datetime",axis=1)
    result_dff[col_name] = result_dff[col_name].resample('0.25S').mean()
    result_dff.dropna(inplace=True)
    #result_dff['Label'] = label
    
    return result_dff
    
#Label_Acc(result_acc1_ns, 'S01', 'No Stress')



    if i < 10:
        globals()['s_id%s'%i] = 'S0' + str(i)
    else:
        globals()['s_id%s'%i] = 'S' + str(i)
        
# STROOP TEST 
    globals()['timestamp_str_start_S%s'%i] = time_utc_timestamp_value(get_time_log("Stroop Test", globals()['s_id%s'%i]))
    globals()['timestamp_str_end_S%s'%i] = time_utc_timestamp_value(get_time_log("Unnamed: 9", globals()['s_id%s'%i]))

    globals()['str_frm_acc%s'%i] = use_time_to_frame(globals()['acc%s'%i], globals()['timestamp_str_start_S%s'%i], globals()['timestamp_str_end_S%s'%i])

    globals()['str_frm_bvp%s'%i] = use_time_to_frame(globals()['bvp%s'%i], globals()['timestamp_str_start_S%s'%i], globals()['timestamp_str_end_S%s'%i])

    globals()['str_frm_eda%s'%i] = use_time_to_frame(globals()['eda%s'%i], globals()['timestamp_str_start_S%s'%i], globals()['timestamp_str_end_S%s'%i])

    globals()['str_frm_temp%s'%i] = use_time_to_frame(globals()['temp%s'%i], globals()['timestamp_str_start_S%s'%i], globals()['timestamp_str_end_S%s'%i])

"""
Resampling the dataframe by finding the mean of data in each secs, joining the columns and adding a label

The mean turns data from 64 to 4, 32 to 4 by finding their mean using the Function stated in the function section.
"""



stress = 'Stress'
for i in range(start, end):
    if i < 10:
        globals()['s_id%s'%i] = 'S0' + str(i)
    else:
        globals()['s_id%s'%i] = 'S' + str(i)
        
    globals()['str_df_acc%s'%i] = Label_Acc(globals()['str_frm_acc%s'%i], globals()['s_id%s'%i], stress)
    globals()['str_df_bvp%s'%i] = Label_BVP_EDA_TEMP(globals()['str_frm_bvp%s'%i], 'bvp', stress)
    globals()['str_df_eda%s'%i] = Label_BVP_EDA_TEMP(globals()['str_frm_eda%s'%i], 'eda', stress)
    globals()['str_df_temp%s'%i] = Label_BVP_EDA_TEMP(globals()['str_frm_temp%s'%i], 'temp', stress)

    globals()['str_df_%s'%i] = pd.concat([globals()['str_df_acc%s'%i] , globals()['str_df_bvp%s'%i], globals()['str_df_eda%s'%i], globals()['str_df_temp%s'%i]], axis=1)
    globals()['str_df_%s'%i]['Label'] = stress

        
# INTERVIEW     
    globals()['timestamp_int_start_S%s'%i] = time_utc_timestamp_value(get_time_log("Interview", globals()['s_id%s'%i]))
    globals()['timestamp_int_end_S%s'%i] = time_utc_timestamp_value(get_time_log("Unnamed: 13", globals()['s_id%s'%i]))

    globals()['int_frm_acc%s'%i] = use_time_to_frame(globals()['acc%s'%i], globals()['timestamp_int_start_S%s'%i], globals()['timestamp_int_end_S%s'%i])

    globals()['int_frm_bvp%s'%i] = use_time_to_frame(globals()['bvp%s'%i], globals()['timestamp_int_start_S%s'%i], globals()['timestamp_int_end_S%s'%i])

    globals()['int_frm_eda%s'%i] = use_time_to_frame(globals()['eda%s'%i], globals()['timestamp_int_start_S%s'%i], globals()['timestamp_int_end_S%s'%i])

    globals()['int_frm_temp%s'%i] = use_time_to_frame(globals()['temp%s'%i], globals()['timestamp_int_start_S%s'%i], globals()['timestamp_int_end_S%s'%i])



    globals()['int_df_acc%s'%i] = Label_Acc(globals()['int_frm_acc%s'%i], globals()['s_id%s'%i], stress)
    globals()['int_df_bvp%s'%i] = Label_BVP_EDA_TEMP(globals()['int_frm_bvp%s'%i], 'bvp', stress)
    globals()['int_df_eda%s'%i] = Label_BVP_EDA_TEMP(globals()['int_frm_eda%s'%i], 'eda', stress)
    globals()['int_df_temp%s'%i] = Label_BVP_EDA_TEMP(globals()['int_frm_temp%s'%i], 'temp', stress)

    globals()['int_df_%s'%i] = pd.concat([globals()['int_df_acc%s'%i] , globals()['int_df_bvp%s'%i], globals()['int_df_eda%s'%i], globals()['int_df_temp%s'%i]], axis=1)
    globals()['int_df_%s'%i]['Label'] = stress



# HYPERVENTILATION  
    globals()['timestamp_hyp_start_S%s'%i] = time_utc_timestamp_value(get_time_log("Hyperventilation", globals()['s_id%s'%i]))
    globals()['timestamp_hyp_end_S%s'%i] = time_utc_timestamp_value(get_time_log("Unnamed: 17", globals()['s_id%s'%i]))

    globals()['hyp_frm_acc%s'%i] = use_time_to_frame(globals()['acc%s'%i], globals()['timestamp_hyp_start_S%s'%i], globals()['timestamp_hyp_end_S%s'%i])

    globals()['hyp_frm_bvp%s'%i] = use_time_to_frame(globals()['bvp%s'%i], globals()['timestamp_hyp_start_S%s'%i], globals()['timestamp_hyp_end_S%s'%i])

    globals()['hyp_frm_eda%s'%i] = use_time_to_frame(globals()['eda%s'%i], globals()['timestamp_hyp_start_S%s'%i], globals()['timestamp_hyp_end_S%s'%i])

    globals()['hyp_frm_temp%s'%i] = use_time_to_frame(globals()['temp%s'%i], globals()['timestamp_hyp_start_S%s'%i], globals()['timestamp_hyp_end_S%s'%i])



# NORMAL/RELAXING
    globals()['hyp_df_acc%s'%i] = Label_Acc(globals()['hyp_frm_acc%s'%i], globals()['s_id%s'%i], stress)
    globals()['hyp_df_bvp%s'%i] = Label_BVP_EDA_TEMP(globals()['hyp_frm_bvp%s'%i], 'bvp', stress)
    globals()['hyp_df_eda%s'%i] = Label_BVP_EDA_TEMP(globals()['hyp_frm_eda%s'%i], 'eda', stress)
    globals()['hyp_df_temp%s'%i] = Label_BVP_EDA_TEMP(globals()['hyp_frm_temp%s'%i], 'temp', stress)

    globals()['hyp_df_%s'%i] = pd.concat([globals()['hyp_df_acc%s'%i] , globals()['hyp_df_bvp%s'%i], globals()['hyp_df_eda%s'%i], globals()['hyp_df_temp%s'%i]], axis=1)
    globals()['hyp_df_%s'%i]['Label'] = stress



#---------------------------------------------------------
# Relax 1
#---------------------------------------------------------
    globals()['timestamp_rlx1_start_S%s'%i] = time_utc_timestamp_value(get_time_log("Relax", globals()['s_id%s'%i]))
    globals()['timestamp_rlx1_end_S%s'%i] = time_utc_timestamp_value(get_time_log("Unnamed: 11", globals()['s_id%s'%i]))

    
    globals()['rlx1_frm_acc%s'%i] = use_time_to_frame(globals()['acc%s'%i], globals()['timestamp_rlx1_start_S%s'%i], globals()['timestamp_rlx1_end_S%s'%i])

    globals()['rlx1_frm_bvp%s'%i] = use_time_to_frame(globals()['bvp%s'%i], globals()['timestamp_rlx1_start_S%s'%i], globals()['timestamp_rlx1_end_S%s'%i])

    globals()['rlx1_frm_eda%s'%i] = use_time_to_frame(globals()['eda%s'%i], globals()['timestamp_rlx1_start_S%s'%i], globals()['timestamp_rlx1_end_S%s'%i])

    globals()['rlx1_frm_temp%s'%i] = use_time_to_frame(globals()['temp%s'%i], globals()['timestamp_rlx1_start_S%s'%i], globals()['timestamp_rlx1_end_S%s'%i])


#---------------------------------------------------------
# Relax 2
#---------------------------------------------------------
    globals()['timestamp_rlx2_start_S%s'%i] = time_utc_timestamp_value(get_time_log("Relax.1", globals()['s_id%s'%i]))
    globals()['timestamp_rlx2_end_S%s'%i] = time_utc_timestamp_value(get_time_log("Unnamed: 15", globals()['s_id%s'%i]))
   
    globals()['rlx2_frm_acc%s'%i] = use_time_to_frame(globals()['acc%s'%i], globals()['timestamp_rlx2_start_S%s'%i], globals()['timestamp_rlx2_end_S%s'%i])

    globals()['rlx2_frm_bvp%s'%i] = use_time_to_frame(globals()['bvp%s'%i], globals()['timestamp_rlx2_start_S%s'%i], globals()['timestamp_rlx2_end_S%s'%i])

    globals()['rlx2_frm_eda%s'%i] = use_time_to_frame(globals()['eda%s'%i], globals()['timestamp_rlx2_start_S%s'%i], globals()['timestamp_rlx2_end_S%s'%i])

    globals()['rlx2_frm_temp%s'%i] = use_time_to_frame(globals()['temp%s'%i], globals()['timestamp_rlx2_start_S%s'%i], globals()['timestamp_rlx2_end_S%s'%i])


#---------------------------------------------------------
# Relax 3
#---------------------------------------------------------
    globals()['timestamp_rlx3_start_S%s'%i] = time_utc_timestamp_value(get_time_log("Relax.2", globals()['s_id%s'%i]))
    globals()['timestamp_rlx3_end_S%s'%i] = time_utc_timestamp_value(get_time_log("Unnamed: 19", globals()['s_id%s'%i]))
    
    globals()['rlx3_frm_acc%s'%i] = use_time_to_frame(globals()['acc%s'%i], globals()['timestamp_rlx3_start_S%s'%i], globals()['timestamp_rlx3_end_S%s'%i])

    globals()['rlx3_frm_bvp%s'%i] = use_time_to_frame(globals()['bvp%s'%i], globals()['timestamp_rlx3_start_S%s'%i], globals()['timestamp_rlx3_end_S%s'%i])

    globals()['rlx3_frm_eda%s'%i] = use_time_to_frame(globals()['eda%s'%i], globals()['timestamp_rlx3_start_S%s'%i], globals()['timestamp_rlx3_end_S%s'%i])

    globals()['rlx3_frm_temp%s'%i] = use_time_to_frame(globals()['temp%s'%i], globals()['timestamp_rlx3_start_S%s'%i], globals()['timestamp_rlx3_end_S%s'%i])


#---------------------------------------------------------
# Quest
#---------------------------------------------------------
    globals()['timestamp_quest_start_S%s'%i] = time_utc_timestamp_value(get_time_log("Questionniare", globals()['s_id%s'%i]))
    globals()['timestamp_quest_end_S%s'%i] = time_utc_timestamp_value(get_time_log("Unnamed: 21", globals()['s_id%s'%i]))
    
    globals()['quest_frm_acc%s'%i] = use_time_to_frame(globals()['acc%s'%i], globals()['timestamp_quest_start_S%s'%i], globals()['timestamp_quest_end_S%s'%i])

    globals()['quest_frm_bvp%s'%i] = use_time_to_frame(globals()['bvp%s'%i], globals()['timestamp_quest_start_S%s'%i], globals()['timestamp_quest_end_S%s'%i])

    globals()['quest_frm_eda%s'%i] = use_time_to_frame(globals()['eda%s'%i], globals()['timestamp_quest_start_S%s'%i], globals()['timestamp_quest_end_S%s'%i])

    globals()['quest_frm_temp%s'%i] = use_time_to_frame(globals()['temp%s'%i], globals()['timestamp_quest_start_S%s'%i], globals()['timestamp_quest_end_S%s'%i])

              
#---------------------------------------------------------
# Relax Base
#---------------------------------------------------------
    globals()['timestamp_rlxBase_start_S%s'%i] = time_utc_timestamp_value(get_time_log("Relax/Baseline", globals()['s_id%s'%i]))
    globals()['timestamp_rlxBase_end_S%s'%i] = time_utc_timestamp_value(get_time_log("Unnamed: 23", globals()['s_id%s'%i]))
    
    globals()['rlxBase_frm_acc%s'%i] = use_time_to_frame(globals()['acc%s'%i], globals()['timestamp_rlxBase_start_S%s'%i], globals()['timestamp_rlxBase_end_S%s'%i])

    globals()['rlxBase_frm_bvp%s'%i] = use_time_to_frame(globals()['bvp%s'%i], globals()['timestamp_rlxBase_start_S%s'%i], globals()['timestamp_rlxBase_end_S%s'%i])

    globals()['rlxBase_frm_eda%s'%i] = use_time_to_frame(globals()['eda%s'%i], globals()['timestamp_rlxBase_start_S%s'%i], globals()['timestamp_rlxBase_end_S%s'%i])

    globals()['rlxBase_frm_temp%s'%i] = use_time_to_frame(globals()['temp%s'%i], globals()['timestamp_rlxBase_start_S%s'%i], globals()['timestamp_rlxBase_end_S%s'%i])




normal = 'Normal'
for i in range(start, end):
    if i < 10:
        globals()['s_id%s'%i] = 'S0' + str(i)
    else:
        globals()['s_id%s'%i] = 'S' + str(i)
        
    globals()['rlx1_df_acc%s'%i] = Label_Acc(globals()['rlx1_frm_acc%s'%i], globals()['s_id%s'%i], normal)
    globals()['rlx1_df_bvp%s'%i] = Label_BVP_EDA_TEMP(globals()['rlx1_frm_bvp%s'%i], 'bvp', normal)
    globals()['rlx1_df_eda%s'%i] = Label_BVP_EDA_TEMP(globals()['rlx1_frm_eda%s'%i], 'eda', normal)
    globals()['rlx1_df_temp%s'%i] = Label_BVP_EDA_TEMP(globals()['rlx1_frm_temp%s'%i], 'temp', normal)

    globals()['rlx1_df_%s'%i] = pd.concat([globals()['rlx1_df_acc%s'%i], globals()['rlx1_df_bvp%s'%i], globals()['rlx1_df_eda%s'%i], globals()['rlx1_df_temp%s'%i]], axis=1)
    globals()['rlx1_df_%s'%i]['Label'] = normal


    globals()['rlx2_df_acc%s'%i] = Label_Acc(globals()['rlx2_frm_acc%s'%i], globals()['s_id%s'%i], normal)
    globals()['rlx2_df_bvp%s'%i] = Label_BVP_EDA_TEMP(globals()['rlx2_frm_bvp%s'%i], 'bvp', normal)
    globals()['rlx2_df_eda%s'%i] = Label_BVP_EDA_TEMP(globals()['rlx2_frm_eda%s'%i], 'eda', normal)
    globals()['rlx2_df_temp%s'%i] = Label_BVP_EDA_TEMP(globals()['rlx2_frm_temp%s'%i], 'temp', normal)

    globals()['rlx2_df_%s'%i] = pd.concat([globals()['rlx2_df_acc%s'%i], globals()['rlx2_df_bvp%s'%i], globals()['rlx2_df_eda%s'%i], globals()['rlx2_df_temp%s'%i]], axis=1)
    globals()['rlx2_df_%s'%i]['Label'] = normal



    globals()['rlx3_df_acc%s'%i] = Label_Acc(globals()['rlx3_frm_acc%s'%i], globals()['s_id%s'%i], normal)
    globals()['rlx3_df_bvp%s'%i] = Label_BVP_EDA_TEMP(globals()['rlx3_frm_bvp%s'%i], 'bvp', normal)
    globals()['rlx3_df_eda%s'%i] = Label_BVP_EDA_TEMP(globals()['rlx3_frm_eda%s'%i], 'eda', normal)
    globals()['rlx3_df_temp%s'%i] = Label_BVP_EDA_TEMP(globals()['rlx3_frm_temp%s'%i], 'temp', normal)

    globals()['rlx3_df_%s'%i] = pd.concat([globals()['rlx3_df_acc%s'%i], globals()['rlx3_df_bvp%s'%i], globals()['rlx3_df_eda%s'%i], globals()['rlx3_df_temp%s'%i]], axis=1)
    globals()['rlx3_df_%s'%i]['Label'] = normal



    globals()['quest_df_acc%s'%i] = Label_Acc(globals()['quest_frm_acc%s'%i], globals()['s_id%s'%i], normal)
    globals()['quest_df_bvp%s'%i] = Label_BVP_EDA_TEMP(globals()['quest_frm_bvp%s'%i], 'bvp', normal)
    globals()['quest_df_eda%s'%i] = Label_BVP_EDA_TEMP(globals()['quest_frm_eda%s'%i], 'eda', normal)
    globals()['quest_df_temp%s'%i] = Label_BVP_EDA_TEMP(globals()['quest_frm_temp%s'%i], 'temp', normal)

    globals()['quest_df_%s'%i] = pd.concat([globals()['quest_df_acc%s'%i], globals()['quest_df_bvp%s'%i], globals()['quest_df_eda%s'%i], globals()['quest_df_temp%s'%i]], axis=1)
    globals()['quest_df_%s'%i]['Label'] = normal



    globals()['rlxBase_df_acc%s'%i] = Label_Acc(globals()['rlxBase_frm_acc%s'%i], globals()['s_id%s'%i], normal)
    globals()['rlxBase_df_bvp%s'%i] = Label_BVP_EDA_TEMP(globals()['rlxBase_frm_bvp%s'%i], 'bvp', normal)
    globals()['rlxBase_df_eda%s'%i] = Label_BVP_EDA_TEMP(globals()['rlxBase_frm_eda%s'%i], 'eda', normal)
    globals()['rlxBase_df_temp%s'%i] = Label_BVP_EDA_TEMP(globals()['rlxBase_frm_temp%s'%i], 'temp', normal)

    globals()['rlxBase_df_%s'%i] = pd.concat([globals()['rlxBase_df_acc%s'%i], globals()['rlxBase_df_bvp%s'%i], globals()['rlxBase_df_eda%s'%i], globals()['rlxBase_df_temp%s'%i]], axis=1)
    globals()['rlxBase_df_%s'%i]['Label'] = normal


# Joining all the Stroop test, Interview with the others after assigning labels
    globals()['df%s'%i] = pd.concat([globals()['str_df_%s'%i], globals()['rlx1_df_%s'%i], globals()['int_df_%s'%i], globals()['rlx2_df_%s'%i], globals()['hyp_df_%s'%i], globals()['rlx3_df_%s'%i], globals()['quest_df_%s'%i], globals()['rlxBase_df_%s'%i]], axis=0)


# Resetting indexes and dropping na
    globals()['df%s'%i].reset_index(drop=True, inplace=True)
    globals()['df%s'%i].dropna(inplace=True)
    #globals()['df'%i]



