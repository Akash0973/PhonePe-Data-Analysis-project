import pandas as pd
import mysql.connector as sql
from mysql.connector import Error

#create mySQL function to run the queries
def create_server_connection(host_name,user_name,user_password):
    connection=None
    try:
        connection=sql.connect(
            host=host_name,
            user=user_name,
            passwd=user_password)
    except Error:
        1
    return connection

def create_database(connection,query):
    mycursor=connection.cursor()
    try:
        mycursor.execute(query)
    except Error:
        1

def create_database_connection(host_name,user_name,user_password,db_name):
    connection=0
    try:
        connection=sql.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name)
    except Error:
        1
    return connection

#Connect to SQL Database
host=input('Provide host name to connect to SQL Database: ')
user=input('Provide user name to connect to SQL Database: ')
password=input('Provide user password to connect to SQL Database: ')
connection=create_server_connection(host,user,password)

db_name='phonepe_database'
database_query=f"create database {db_name}"
create_database(connection,database_query)

connection=create_database_connection(host,user,password,db_name)

mycursor=connection.cursor(buffered=True)

#Import all the files into dataframes and then into SQL Database
#Note that you will have to re-write the path as per your save location

#Dataframe no. 1
aggregated_transactions_state_data=pd.read_csv(
    r'C:\Guvi Capstone Project 2\Extracted Data\aggregated_transactions_state_data.csv'
    )

mycursor.execute(
    """create table aggregated_transactions_state_data(State varchar(100), Year int, Quarter int, Type varchar(35), Count bigint, Amount float)"""
    )
for row in aggregated_transactions_state_data.itertuples():
    mycursor.execute(
        """insert into aggregated_transactions_state_data(State, Year, Quarter, Type, Count, Amount) values(%s,%s,%s,%s,%s,%s)""",
        (row.State, row.Year, row.Quarter, row.Type, row.Count, row.Amount)
        )
connection.commit()

#Dataframe no. 2
aggregated_users_state_data=pd.read_csv(
    r'C:\Guvi Capstone Project 2\Extracted Data\aggregated_users_state_data.csv'
    )

mycursor.execute(
    """create table aggregated_users_state_data(State varchar(100), Year int, Quarter int, Brand varchar(35), Count bigint, Percentage float)"""
    )
for row in aggregated_users_state_data.itertuples():
    mycursor.execute(
        """insert into aggregated_users_state_data(State, Year, Quarter, Brand, Count, Percentage) values(%s,%s,%s,%s,%s,%s)""",
        (row.State, row.Year, row.Quarter, row.Brand, row.Count, row.Percentage)
        )
connection.commit()

#Dataframe no. 3
aggregated_users_state_data_summary=pd.read_csv(
    r'C:\Guvi Capstone Project 2\Extracted Data\aggregated_users_state_data_summary.csv'
    )

mycursor.execute(
    """create table aggregated_users_state_data_summary(State varchar(100), Year int, Quarter int, RegisteredUsers bigint, AppOpenings bigint)"""
    )
for row in aggregated_users_state_data_summary.itertuples():
    mycursor.execute(
        """insert into aggregated_users_state_data_summary(State, Year, Quarter, RegisteredUsers, AppOpenings) values(%s,%s,%s,%s,%s)""",
        (row.State, row.Year, row.Quarter, row.RegisteredUsers, row.AppOpenings)
        )
connection.commit()

#Dataframe no. 4
map_transactions_state_data=pd.read_csv(
    r'C:\Guvi Capstone Project 2\Extracted Data\map_transactions_state_data.csv'
    )

mycursor.execute(
    """create table map_transactions_state_data(State varchar(100), Year int, Quarter int, District varchar(100), Count bigint, Amount float)"""
    )
for row in map_transactions_state_data.itertuples():
    mycursor.execute(
        """insert into map_transactions_state_data(State, Year, Quarter, District, Count, Amount) values(%s,%s,%s,%s,%s,%s)""",
        (row.State, row.Year, row.Quarter, row.District, row.Count, row.Amount)
        )
connection.commit()

#Dataframe no. 5
map_users_state_data=pd.read_csv(
    r'C:\Guvi Capstone Project 2\Extracted Data\map_users_state_data.csv'
    )

mycursor.execute(
    """create table map_users_state_data(State varchar(100), Year int, Quarter int, District varchar(100), RegisteredUsers bigint, AppOpenings bigint)"""
    )
for row in map_users_state_data.itertuples():
    mycursor.execute(
        """insert into map_users_state_data(State, Year, Quarter, District, RegisteredUsers, AppOpenings) values(%s,%s,%s,%s,%s,%s)""",
        (row.State, row.Year, row.Quarter, row.District, row.RegisteredUsers, row.AppOpenings)
        )
connection.commit()

#Now to load the SQL Tables back into the dataframes
aggregated_transactions_state_data=pd.read_sql(
    sql="Select * from aggregated_transactions_state_data",con=connection
    )

aggregated_users_state_data=pd.read_sql(
    sql="Select * from aggregated_users_state_data",con=connection
    )

aggregated_users_state_data_summary=pd.read_sql(
    sql="Select * from aggregated_users_state_data_summary",con=connection
    )

map_transactions_state_data=pd.read_sql(
    sql="Select * from map_transactions_state_data",con=connection
    )

map_users_state_data=pd.read_sql(
    sql="Select * from map_users_state_data",con=connection
    )

connection.commit()