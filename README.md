# PhonePe Data Analysis project
Streamlit app link : https://akash0973-phonepe-data-a-phonepe-data-visualisation-code-wpjdgz.streamlit.app/

This project is made using the data from PhonePe Github repository (https://github.com/PhonePe/pulse)

# Project execution:
 
    1 Download the data from PhonePe repository in local machine
    
    2 Use the python code Data_extraction.py to transform the JSON data into easily readable CSV files
      - Note that the paths in lines 35 to 38 will have to changed accordingly depending on where data from step 1 is saved
      - In my case, the data was stored in C Drive in a folder named "Guvi Capstone Project 2"
      - This needs to be altered in the code before running it
    
    3 Use the python code Data_into_SQL_Database.py to save the CSV data into a SQL Database.
      - Again, depending on where the transformed CSV data is stored, paths in lines 55, 70, 85, 100, 115 needs to be altered first
      - In my case, these files are saved in another folder "Extracted Data" in the folder "Guvi Capstone Project 2"
      - After running the code, the code will ask for hostname, username and password to connect to the SQL Database
      - After these details are entered, the code will create a database named phonepe_database where all the CSV data will be stored
      - The part of the code from line 128 onwards will now read these SQL tables and convert them back into Dataframes for easy analysis of data
    
    NOTE: The only purpose of step 3 is to create a connection between SQL and python. However, in the main code in the next step we will be directly reading the data into Dataframe without connecting to SQL Database at all
    
    4 Now, Using the main code PhonePe_Data_Visualisation_Code.py using streamlit run in command promt, we can now view the dashboard
    
Following link is the output of above code: https://akash0973-phonepe-data-a-phonepe-data-visualisation-code-wpjdgz.streamlit.app/
  
# Dashboard explaination:

## 1 Geo-visualization using plotly express
    
    - The map colours the sates based on the total transaction count in the selected quarter
    - Darker color means higher transaction count
    - By hovering over the circles one can also see various details such as total transaction amount, total registered users and total app openings of differect districts
    - The size of the circles is determined by total transction count in that district

## 2 Transaction Analysis:

This part has 4 tabs:

    2.1 Country-wide analysis: This tab shows the quarter on quarter increase of transaction count as well as transaction amount of selected mode of payment in the entire country
    
    2.2 State-wise analysis: This tab shows the quarter on quarter increase of transaction count as well as transaction amount of selected mode of payment and state
    
    2.3 District-wise analysis: This tab shows the transaction count as well as transaction amount of all the districts in the selected state in the selected quarter
    
    2.4 Year-wise analysis: This tab shows a pie chart showcasing the transaction count as well as transaction amount in all years from 2018 to 2022
    
## 3 Users Analysis:

This part has 4 tabs:

    3.1 Country-wide analysis: This tab shows the quarter on quarter data of new registered usres as well as app openings
    
    3.2 State-wise analysis: This tab shows the quarter on quarter data of new registered usres as well as app openings of the selected state
    
    3.3 District-wise analysis: This tab shows the data of new registered usres as well as app openings of all the districts in the selected state in the selected quarter
    
    3.4 Year-wise analysis: This tab shows a pie chart showcasing the data of new registered usres as well as app openings in all years from 2018 to 2022

## 4 Phome brand analysis:

This part has 2 tabs:

    4.1 Country-wide analysis: This tab shows the total registered users of different phone brands in the selected quarter in the whole country
    
    4.2 State-wise analysis: This tab shows the total registered users of different phone brands in the selected quarter and selected state

## 5 Top 10 states:

This section shows the top 10 states in total transaction amount, count, registered users ad app openings in the selected quarter

Lindekin link for demo video of this project: <insert link>
