import os
import pandas as pd
import time

start=time.time()

#Initializing the empty dataframes

#Stores state wise transactions count and amount
aggregated_transactions_state_data=pd.DataFrame(
    columns=['State','Year','Quarter','Type','Count','Amount']
    )

#Stores state wise users phone brand and count
aggregated_users_state_data=pd.DataFrame(
    columns=['State','Year','Quarter','Brand','Count','Percentage']
    )

#Stores state wise registered users and App Opennings
aggregated_users_state_data_summary=pd.DataFrame(
    columns=['State','Year','Quarter','RegisteredUsers','AppOpenings']
    )

#Stores district wise transactions count and amount
map_transactions_state_data=pd.DataFrame(
    columns=['State','Year','Quarter','District','Count','Amount']
    )

#Stores district wise registered users and App Opennings
map_users_state_data=pd.DataFrame(
    columns=['State','Year','Quarter','District','RegisteredUsers','AppOpenings']
    )

#Paths of data required for extraction
path_aggregated_transactions=r'C:\\Guvi Capstone Project 2\\data\\aggregated\\transaction\\country\\india\\state'
path_aggregated_users=r'C:\\Guvi Capstone Project 2\\data\\aggregated\\user\\country\\india\\state'
path_map_transactions=r'C:\\Guvi Capstone Project 2\\data\\map\\transaction\\hover\\country\\india\\state'
path_map_users=r'C:\\Guvi Capstone Project 2\\data\\map\\user\\hover\\country\\india\\state'

#Define functions to append a particular state's data into the dataframe
def aggregated_transactions_func(state,year,quarter,path):
    global aggregated_transactions_state_data
    data=pd.read_json(path)
    relevant_data=data['data']['transactionData']
    for entry in relevant_data:
        row_data={
            'State':state,
            'Year':year,
            'Quarter':quarter,
            'Type':entry['name'],
            'Count':entry['paymentInstruments'][0]['count'],
            'Amount':entry['paymentInstruments'][0]['amount']
            }
        #aggregated_transactions_state_data=aggregated_transactions_state_data.append(row_data,ignore_index=1)
        aggregated_transactions_state_data=pd.concat(
            [
                aggregated_transactions_state_data,
                pd.Series(row_data).to_frame().T
                ],
            ignore_index=1
            )

def aggregated_users_func(state,year,quarter,path):
    global aggregated_users_state_data
    global aggregated_users_state_data_summary
    data=pd.read_json(path)
    registered_users=data['data']['aggregated']['registeredUsers']
    appOpens=data['data']['aggregated']['appOpens']
    summary={
        'State':state,
        'Year':year,
        'Quarter':quarter,
        'RegisteredUsers':registered_users,
        'AppOpenings':appOpens
        }
    #aggregated_users_state_data_summary=aggregated_users_state_data_summary.append(summary,ignore_index=1)
    aggregated_users_state_data_summary=pd.concat(
        [
            aggregated_users_state_data_summary,
            pd.Series(summary).to_frame().T
            ],
        ignore_index=1
        )
    device_data=data['data']['usersByDevice']
    if device_data:
        for entry in device_data:
            row_data={
                'State':state,
                'Year':year,
                'Quarter':quarter,
                'Brand':entry['brand'],
                'Count':entry['count'],
                'Percentage':entry['percentage']
                }
            #aggregated_users_state_data=aggregated_users_state_data.append(row_data,ignore_index=1)
            aggregated_users_state_data=pd.concat(
                [
                    aggregated_users_state_data,
                    pd.Series(row_data).to_frame().T
                    ],
                ignore_index=1
                )

def map_transactions_func(state,year,quarter,path):
    global map_transactions_state_data
    data=pd.read_json(path)
    relevant_data=data['data']['hoverDataList']
    for entry in relevant_data:
        row_data={
            'State':state,
            'Year':year,
            'Quarter':quarter,
            'District':entry['name'],
            'Count':entry['metric'][0]['count'],
            'Amount':entry['metric'][0]['amount']
            }
        #map_transactions_state_data=map_transactions_state_data.append(row_data,ignore_index=1)
        map_transactions_state_data=pd.concat(
            [
                map_transactions_state_data,
                pd.Series(row_data).to_frame().T
                ],
            ignore_index=1
            )

def map_users_func(state,year,quarter,path):
    global map_users_state_data
    global relevant_data
    data=pd.read_json(path)
    relevant_data=data['data']['hoverData']
    for district,entry in relevant_data.items():
        row_data={
            'State':state,
            'Year':year,
            'Quarter':quarter,
            'District':district,
            'RegisteredUsers':entry['registeredUsers'],
            'AppOpenings':entry['appOpens']
            }
        #map_users_state_data=map_users_state_data.append(row_data,ignore_index=1)
        map_users_state_data=pd.concat(
            [
                map_users_state_data,
                pd.Series(row_data).to_frame().T
                ],
            ignore_index=1
            )

#List of states in the folders
aggregated_transactions_list=os.listdir(path_aggregated_transactions)
aggregated_users_list=os.listdir(path_aggregated_users)
map_transactions_list=os.listdir(path_map_transactions)
map_users_list=os.listdir(path_map_users)

#Begin statewise, yearwise, and quarterwise addition of data into the dataframes
for state in aggregated_transactions_list:
    nested_path1=path_aggregated_transactions+'\\'+state
    year_list=os.listdir(nested_path1)
    for year in year_list:
        nested_path2=nested_path1+'\\'+year
        quarter_list=os.listdir(nested_path2)
        for quarter_file in quarter_list:
            final_path=nested_path2+'\\'+quarter_file
            quarter=quarter_file[:quarter_file.index('.')]
            aggregated_transactions_func(state,year,quarter,final_path)

for state in aggregated_users_list:
    nested_path1=path_aggregated_users+'\\'+state
    year_list=os.listdir(nested_path1)
    for year in year_list:
        nested_path2=nested_path1+'\\'+year
        quarter_list=os.listdir(nested_path2)
        for quarter_file in quarter_list:
            final_path=nested_path2+'\\'+quarter_file
            quarter=quarter_file[:quarter_file.index('.')]
            aggregated_users_func(state,year,quarter,final_path)

for state in map_transactions_list:
    nested_path1=path_map_transactions+'\\'+state
    year_list=os.listdir(nested_path1)
    for year in year_list:
        nested_path2=nested_path1+'\\'+year
        quarter_list=os.listdir(nested_path2)
        for quarter_file in quarter_list:
            final_path=nested_path2+'\\'+quarter_file
            quarter=quarter_file[:quarter_file.index('.')]
            map_transactions_func(state,year,quarter,final_path)

for state in map_users_list:
    nested_path1=path_map_users+'\\'+state
    year_list=os.listdir(nested_path1)
    for year in year_list:
        nested_path2=nested_path1+'\\'+year
        quarter_list=os.listdir(nested_path2)
        for quarter_file in quarter_list:
            final_path=nested_path2+'\\'+quarter_file
            quarter=quarter_file[:quarter_file.index('.')]
            map_users_func(state,year,quarter,final_path)

#Download the csv files
aggregated_transactions_state_data.to_csv(
    r'C:\Guvi Capstone Project 2\Extracted Data\aggregated_transactions_state_data.csv',
    index=False
    )

aggregated_users_state_data.to_csv(
    r'C:\Guvi Capstone Project 2\Extracted Data\aggregated_users_state_data.csv',
    index=False
    )

aggregated_users_state_data_summary.to_csv(
    r'C:\Guvi Capstone Project 2\Extracted Data\aggregated_users_state_data_summary.csv',
    index=False
    )

map_transactions_state_data.to_csv(
    r'C:\Guvi Capstone Project 2\Extracted Data\map_transactions_state_data.csv',
    index=False
    )

map_users_state_data.to_csv(
    r'C:\Guvi Capstone Project 2\Extracted Data\map_users_state_data.csv',
    index=False
    )

end=time.time()
print('Execution time:',end-start)