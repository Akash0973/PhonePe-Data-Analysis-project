# PhonePe-Data-Analysis-project
Streamlit app link : https://akash0973-phonepe-data-a-phonepe-data-visualisation-code-wpjdgz.streamlit.app/

This project is made using the data from PhonePe Github repository (https://github.com/PhonePe/pulse)

## Project execution:
 
    1 Download the data from PhonePe repository in local machine
    2 Use the python code Data_extraction.py to transform the JSON data into easily readable CSV files
      - Note that the paths in lines 35 to 38 will have to changed accordingly depending on where data from step 1 is saved.
      - In my case, the data was stored in C Drive in a folder named "Guvi Capstone Project 2".
      - This needs to be altered in the code before running it
    3 Use the python code Data_into_SQL_Database.py to save the CSV data into a SQL Database.
      - Again, depending on where the transformed CSV data is stored, paths in lines 55, 70, 85, 100, 115 needs to be altered first
      - In my case, these files are saved in another folder "Extracted Data" in the folder "Guvi Capstone Project 2".
      - After running the code, the code will ask for hostname, username and password to connect to the SQL Database.
      - After these details are entered, the code will create a database named phnepe_database where all the CSV data will be stored.
      - The part of the code from line 128 onwards will now read these SQL tables and convert them back into Dataframes for easy analysis of data.
    NOTE: The 0nly purpose of step 3 is to create a connection between SQL and python. However, in the main code in the next step we will be directly reading the data into Dataframe without connecting to SQL Database at all
    4 Now, Using the main code PhonePe_Data_Visualisation_Code.py using streamlit.run in command promt, we can now view the dashboard.
    5 Following link is the output of above code: https://akash0973-phonepe-data-a-phonepe-data-visualisation-code-wpjdgz.streamlit.app/
  
## Dashboard explaination:
