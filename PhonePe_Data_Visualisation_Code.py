import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

#Import all the files into dataframes
aggregated_transactions_state_data=pd.read_csv(
    r'Extracted Data\aggregated_transactions_state_data.csv'
    )
aggregated_transactions_state_data['Year_Quarter']=(
    aggregated_transactions_state_data['Year'].astype(str)
    +'-Q'
    +aggregated_transactions_state_data['Quarter'].astype(str)
    )

aggregated_users_state_data=pd.read_csv(
    r'Extracted Data\aggregated_users_state_data.csv'
    )
aggregated_users_state_data['Year_Quarter']=(
    aggregated_users_state_data['Year'].astype(str)
    +'-Q'
    +aggregated_users_state_data['Quarter'].astype(str)
    )

aggregated_users_state_data_summary=pd.read_csv(
    r'Extracted Data\aggregated_users_state_data_summary.csv'
    )
aggregated_users_state_data_summary['Year_Quarter']=(
    aggregated_users_state_data_summary['Year'].astype(str)
    +'-Q'
    +aggregated_users_state_data_summary['Quarter'].astype(str)
    )

map_transactions_state_data=pd.read_csv(
    r'Extracted Data\map_transactions_state_data.csv'
    )
map_transactions_state_data['Year_Quarter']=(
    map_transactions_state_data['Year'].astype(str)
    +'-Q'
    +map_transactions_state_data['Quarter'].astype(str)
    )

map_users_state_data=pd.read_csv(
    r'Extracted Data\map_users_state_data.csv'
    )
map_users_state_data['Year_Quarter']=(
    map_users_state_data['Year'].astype(str)
    +'-Q'
    +map_users_state_data['Quarter'].astype(str)
    )

district_coordinates=pd.read_csv(
    r'Extracted Data\districts_longitude_latitude_data.csv'
    )
district_coordinates=district_coordinates.drop(['State'],axis=1)

state_coordinates=pd.read_csv(
    r'Extracted Data\states_longitude_latitude_data.csv'
    )
state_coordinates=state_coordinates.drop(['code'],axis=1)
state_coordinates=state_coordinates.sort_values(
    by='state',ascending=True
    )
state_coordinates=state_coordinates.reset_index(drop=True)

#Initialize various lists that will be helpful later on
Transaction_types=list(set(aggregated_transactions_state_data['Type']))
States=list(set(aggregated_transactions_state_data['State']))
States.sort()
Brands=list(set(aggregated_users_state_data['Brand']))
Districts=list(set(map_users_state_data['District']))
Years=list(set(aggregated_transactions_state_data['Year']))
Years.sort()
Quarters=[1,2,3,4]

st. set_page_config(layout="wide")
st.title('PhonePe Pulse Analysis')

#Code for the Geomap
st.write('## Geomap for PhonePe Count based on Total Transaction counts')

year=st.selectbox(
    'Select the Year for Geomap:',tuple(Years)
    )
quarter=st.selectbox(
    'Select the Quarter for Geomap:',tuple(Quarters)
    )

#Refine the dataframes
#District data
transactions=map_transactions_state_data[
    (map_transactions_state_data['Year']==year) &
    (map_transactions_state_data['Quarter']==quarter)
    ]
users=map_users_state_data[
    (map_users_state_data['Year']==year) &
    (map_users_state_data['Quarter']==quarter)
    ]
district_transactions=transactions.drop(
    ['Year','Quarter','Year_Quarter'],axis=1
    )
district_users=users.drop(
    ['Year','Quarter','Year_Quarter','State'],axis=1
    )
district_data=pd.merge(
    district_transactions,
    district_users,
    on='District',
    how='inner'
    )
district_data=pd.merge(
    district_data,
    district_coordinates,
    on='District',
    how='inner'
    )
district_data['aux_count']=district_data['Count']

#State data
state_transactions=transactions.drop(
    ['Year','Quarter','Year_Quarter','District'],axis=1
    )
state_transactions['aux_state']=state_transactions['State']
state_transactions=pd.pivot_table(
    state_transactions,
    index='aux_state',
    values=['State','Count','Amount'],
    aggfunc={
        'State':lambda x: list(set(x))[0],
        'Count':np.sum,
        'Amount':np.sum
        }
    )
state_users=users.drop(
    ['Year','Quarter','Year_Quarter','District'],axis=1
    )
state_users['aux_state']=state_users['State']
state_users=pd.pivot_table(
    state_users,
    index='aux_state',
    values=['State','RegisteredUsers','AppOpenings'],
    aggfunc={
        'State':lambda x: list(set(x))[0],
        'RegisteredUsers':np.sum,
        'AppOpenings':np.sum
        }
    )
state_data=pd.merge(
    state_transactions,
    state_users,
    on='State',
    how='outer'
    )

state_data['Latitude']=state_coordinates['Latitude']
state_data['Longitude']=state_coordinates['Longitude']
state_data['State']=state_coordinates['state']

#Geoplot based on Transaction Count
fig0=px.scatter_geo(
    district_data,
    lon='Longitude',
    lat='Latitude',
    color=district_data['aux_count'],
    size=district_data['aux_count'],
    hover_name='District',
    hover_data=['Amount','Count','RegisteredUsers','AppOpenings','State'],
    )
fig0.update_traces(marker={'color':'red','line_width':1})

fig1=px.scatter_geo(
    state_data,
    lon='Longitude',
    lat='Latitude',
    hover_name='State',
    hover_data=['Amount','Count','RegisteredUsers','AppOpenings']
    )
fig1.update_traces(marker={'color':'black','size':0.0001})

fig_final=px.choropleth(
                    state_data,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',                
                    locations='State',
                    color="Count",
                    color_continuous_scale='magenta'
                    )
fig_final.update_geos(fitbounds="locations", visible=False)

fig_final.add_trace(fig1.data[0])
fig_final.add_trace(fig0.data[0])

col1,col2=st.columns([0.6,0.4])

with col1:
    st.plotly_chart(fig_final)

with col2:
    st.write('Details of the Geomap')
    st.info(
        """
        - This map shows the transaction counts over the whole country
        - Darker color represents higher transaction count in selected quarter
        - Lighter color represents lower transaction count in selected quarter
        - Red circles represent a similar data but for districts
        - Larger circles represent a higher transaction count
        - Smaller circles reprsent a lower transaction count
        - Other details can be viewed by hovering on the districts
        """
        )

#Transactions analysis
st.write('## Transactions analysis')
tab1, tab2, tab3, tab4 = st.tabs(
    ['Country-wide analysis',
     'State-wise analysis',
     'District-wise analysis',
     'Year-wise analysis']
    )

#Country wide analysis
with tab1:
    Payment_mode1=st.selectbox(
            'Select the Payment mode for country wide analysis:',
            tuple(Transaction_types)
        )
    df_type_wise=aggregated_transactions_state_data[
        aggregated_transactions_state_data['Type']==Payment_mode1
        ]
    df_pivot=pd.pivot_table(
        df_type_wise,
        index=['Year','Quarter'],
        values=['Count','Amount','Year_Quarter'],
        aggfunc={
            'Count':np.sum,
            'Amount':np.sum,
            'Year_Quarter':lambda x: list(set(x))[0]
            }
        )
    Transaction_data=px.bar(df_pivot, x='Year_Quarter', y='Count')
    st.write('### Total transactions count in every quarter')
    st.plotly_chart(Transaction_data)
    
    Transaction_data=px.bar(df_pivot, x='Year_Quarter', y='Amount')
    st.write('### Total transactions amount in every quarter')
    st.plotly_chart(Transaction_data)

#State wise analysis
with tab2:
    Payment_mode2=st.selectbox(
        'Select the Payment mode for state wise analysis:'
        ,tuple(Transaction_types)
        )
    State=st.selectbox(
        'Select the State for state wise analysis:',tuple(States)
        )
    df_type_and_state_wise=aggregated_transactions_state_data[
        (aggregated_transactions_state_data['Type']==Payment_mode2) &
        (aggregated_transactions_state_data['State']==State)
        ]
    df_pivot=pd.pivot_table(
        df_type_and_state_wise,
        index=['Year','Quarter'],
        values=['Count','Amount','Year_Quarter'],
        aggfunc={
            'Count':np.sum,
            'Amount':np.sum,
            'Year_Quarter':lambda x: list(set(x))[0]
            }
        )
    Transaction_data=px.bar(df_pivot, x='Year_Quarter', y='Count')
    st.write('### Total transactions count in every quarter')
    st.plotly_chart(Transaction_data)
    
    Transaction_data=px.bar(df_pivot, x='Year_Quarter', y='Amount')
    st.write('### Total transactions amount in every quarter')
    st.plotly_chart(Transaction_data)

#District wise analysis
with tab3:
    year=st.selectbox(
        'Select the Year for District wise analysis:',tuple(Years)
        )
    quarter=st.selectbox(
        'Select the Quarter for District wise analysis:',tuple(Quarters)
        )
    State=st.selectbox(
        'Select the State for District wise analysis:',tuple(States)
        )
    df_district_wise=map_transactions_state_data[
        (map_transactions_state_data['Year']==year) &
        (map_transactions_state_data['Quarter']==quarter) & 
        (map_transactions_state_data['State']==State)
        ]
    df_district_wise=df_district_wise.sort_values(by='Count',ascending=False)
    Transaction_data=px.bar(df_district_wise, x='District', y='Count')
    st.write('### Total transactions count in every district')
    st.plotly_chart(Transaction_data)
    
    df_district_wise=df_district_wise.sort_values(by='Amount',ascending=False)
    Transaction_data=px.bar(df_district_wise, x='District', y='Amount')
    st.write('### Total transactions amount in every district')
    st.plotly_chart(Transaction_data)

#Year wise analysis
with tab4:
    col1, col2 = st.columns([0.7,0.3])
    with col1:
        Transaction_data=px.pie(
            aggregated_transactions_state_data, values='Count', names='Year'
            )
        st.write('### Total transactions count')
        st.plotly_chart(Transaction_data)
    
        Transaction_data=px.pie(
            aggregated_transactions_state_data, values='Amount', names='Year'
            )
        st.write('### Total transactions amount')
        st.plotly_chart(Transaction_data)
    
    with col2:
        table=pd.pivot_table(
            aggregated_transactions_state_data,
            index='Year',
            values=['Count','Amount'],
            aggfunc={
                'Count':lambda x: str(
                    round(np.sum(x)/1000000000,2)
                    )+' Billion',
                'Amount':lambda x: str(
                    round(np.sum(x)/1000000000000,2)
                    )+' Trillion INR'
                }
            )
        st.markdown(table.to_html(), unsafe_allow_html=True)
    
#Users analysis
st.write('## Users analysis')
tab1, tab2, tab3, tab4 = st.tabs(
    ['Country-wide analysis',
     'State-wise analysis',
     'District-wise analysis',
     'Year-wise analysis']
    )

#Country wide analysis
with tab1:
    df_pivot=pd.pivot_table(
        aggregated_users_state_data_summary,
        index=['Year','Quarter'],
        values=['RegisteredUsers','AppOpenings','Year_Quarter'],
        aggfunc={
            'RegisteredUsers':np.sum,
            'AppOpenings':np.sum,
            'Year_Quarter':lambda x: list(set(x))[0]
            }
        )
    NewRegisteredUsers=(
        [list(df_pivot['RegisteredUsers'])[0]]
        +list(df_pivot['RegisteredUsers'])
        )
    NewRegisteredUsers.pop()
    df_pivot['NewRegisteredUsers']=NewRegisteredUsers
    df_pivot['NewRegisteredUsers']=(
        df_pivot['RegisteredUsers']-df_pivot['NewRegisteredUsers']
        )
    
    User_data=px.bar(df_pivot, x='Year_Quarter', y='NewRegisteredUsers')
    st.write('### Total Registered users by every quarter')
    st.plotly_chart(User_data)
    
    User_data=px.bar(df_pivot, x='Year_Quarter', y='AppOpenings')
    st.write('### Total App Openings by every quarter')
    st.plotly_chart(User_data)

#State wise analysis
with tab2:
    State=st.selectbox(
        'Select the State for state wise analysis for users:',tuple(States)
        )
    df_state_wise=aggregated_users_state_data_summary[
        aggregated_users_state_data_summary['State']==State
        ]
    df_pivot=pd.pivot_table(
        df_state_wise,
        index=['Year','Quarter'],
        values=['RegisteredUsers','AppOpenings','Year_Quarter'],
        aggfunc={
            'RegisteredUsers':np.sum,
            'AppOpenings':np.sum,
            'Year_Quarter':lambda x: list(set(x))[0]
            }
        )
    NewRegisteredUsers=(
        [list(df_pivot['RegisteredUsers'])[0]]
        +list(df_pivot['RegisteredUsers'])
        )
    NewRegisteredUsers.pop()
    df_pivot['NewRegisteredUsers']=NewRegisteredUsers
    df_pivot['NewRegisteredUsers']=(
        df_pivot['RegisteredUsers']-df_pivot['NewRegisteredUsers']
        )
    
    User_data=px.bar(df_pivot, x='Year_Quarter', y='NewRegisteredUsers')
    st.write('### Total Registered users by every quarter State wise')
    st.plotly_chart(User_data)
    
    User_data=px.bar(df_pivot, x='Year_Quarter', y='AppOpenings')
    st.write('### Total App Openings by every quarter State wise')
    st.plotly_chart(User_data)

#District wise analysis
with tab3:
    year=st.selectbox(
        'Select the Year for district wise analysis for users :',
        tuple(Years)
        )
    quarter=st.selectbox(
        'Select the Quarter for district wise analysis for users :',
        tuple(Quarters)
        )
    State=st.selectbox(
        'Select the State for district wise analysis for users:',
        tuple(States)
        )
    df_district_wise=map_users_state_data[
        (map_users_state_data['Year']==year) &
        (map_users_state_data['Quarter']==quarter) & 
        (map_users_state_data['State']==State)
        ]
    df_district_wise=df_district_wise.sort_values(
        by='RegisteredUsers',ascending=False
        )
    User_data=px.bar(df_district_wise, x='District', y='RegisteredUsers')
    st.write('### Total Registered users by selected quarter in every district')
    st.plotly_chart(User_data)
    
    df_district_wise=df_district_wise.sort_values(
        by='AppOpenings',ascending=False
        )
    User_data=px.bar(df_district_wise, x='District', y='AppOpenings')
    st.write('### Total App opens by selected quarter in every district')
    st.plotly_chart(User_data)

#Year wise analysis
with tab4:
    col1, col2 = st.columns([0.7,0.3])
    with col1:
        df_pivot=pd.pivot_table(
            aggregated_users_state_data_summary,
            index=['Year','Quarter'],
            values=['RegisteredUsers','AppOpenings','Year_Quarter'],
            aggfunc={
                'RegisteredUsers':np.sum,
                'AppOpenings':np.sum,
                'Year_Quarter':lambda x: list(set(x))[0]
                }
            )
        NewRegisteredUsers=(
            [list(df_pivot['RegisteredUsers'])[0]]
            +list(df_pivot['RegisteredUsers'])
            )
        NewRegisteredUsers.pop()
        df_pivot['NewRegisteredUsers']=NewRegisteredUsers
        df_pivot['NewRegisteredUsers']=(
            df_pivot['RegisteredUsers']-df_pivot['NewRegisteredUsers']
            )
        Y=[]
        for Y_Q in df_pivot['Year_Quarter']:
            Y.append(Y_Q[:4])
        df_pivot['Year.']=Y
        
        User_data=px.pie(df_pivot, values='NewRegisteredUsers', names='Year.')
        st.write('### Total registered users')
        st.plotly_chart(User_data)
    
        User_data=px.pie(df_pivot, values='AppOpenings', names='Year.')
        st.write('### Total app openings')
        st.plotly_chart(User_data)
    
    with col2:
        table=pd.pivot_table(
            df_pivot,
            index='Year',
            values=['NewRegisteredUsers','AppOpenings'],
            aggfunc={
                'NewRegisteredUsers':lambda x: str(
                    round(np.sum(x)/1000000,2)
                    )+' Million',
                'AppOpenings':lambda x: str(
                    round(np.sum(x)/1000000000,2)
                    )+' Billion'
                }
            )
        st.markdown(table.to_html(), unsafe_allow_html=True)
        
#Phone Brand Analysis
st.write('## Phone Brand analysis')
tab1, tab2, = st.tabs(
    ['Country-wide analysis',
     'State-wise analysis']
    )

#Country wide analysis
with tab1:
    year=st.selectbox(
        'Select the Year for country wide analysis of phone brands:',
        tuple(Years)
        )
    quarter=st.selectbox(
        'Select the Quarter for country wide analysis of phone brands:',
        tuple(Quarters)
        )
    df_brand=aggregated_users_state_data[
        (aggregated_users_state_data['Year']==year) &
        (aggregated_users_state_data['Quarter']==quarter)
        ]
    df_brand['Phone_Brand']=df_brand['Brand']
    df_pivot=pd.pivot_table(
        df_brand,
        index='Brand',
        values=['Count','Phone_Brand'],
        aggfunc={
            'Count':np.sum,
            'Phone_Brand':lambda x: list(set(x))[0]}
        )    
    df_pivot=df_pivot.sort_values(
        by='Count',ascending=False
        )
    Brand_data=px.bar(df_pivot,x='Phone_Brand', y='Count')
    st.write('### Total Registered users as per phone brand')
    st.plotly_chart(Brand_data)

#State wise analysis
with tab2:
    year=st.selectbox(
        'Select the Year for state wise analysis of phone brands:',
        tuple(Years)
        )
    quarter=st.selectbox(
        'Select the Quarter for state wise analysis of phone brands:',
        tuple(Quarters)
        )
    state=st.selectbox(
        'Select the State:        ',tuple(States))
    df_brand=aggregated_users_state_data[
        (aggregated_users_state_data['Year']==year) &
        (aggregated_users_state_data['Quarter']==quarter) &
        (aggregated_users_state_data['State']==state)
        ]
    df_brand['Phone_Brand']=df_brand['Brand']
    df_pivot=pd.pivot_table(
        df_brand,
        index='Brand',
        values=['Count','Phone_Brand'],
        aggfunc={
            'Count':np.sum,
            'Phone_Brand':lambda x: list(set(x))[0]}
        )    
    df_pivot=df_pivot.sort_values(
        by='Count',ascending=False
        )
    Brand_data=px.bar(df_pivot,x='Phone_Brand', y='Count')
    st.write('### Total Registered users as per phone brand')
    st.plotly_chart(Brand_data)

#Top 10 states in transaction amount, transaction count, users, App openings
st.write('## Top 10 states')

year=st.selectbox(
    'Select the Year for top 10 states:',tuple(Years)
    )
quarter=st.selectbox(
    'Select the Quarter for top 10 states:',tuple(Quarters)
    )

col1, col2, col3, col4 = st.columns([0.25,0.25,0.25,0.25])
with col1:
    st.write('### By Transaction amount: ')
    Transaction_amount_df=pd.pivot_table(
        aggregated_transactions_state_data[
            (aggregated_transactions_state_data['Year']==year) &
            (aggregated_transactions_state_data['Quarter']==quarter)
            ],
        index='State',
        values=['Amount'],
        aggfunc={
            'Amount':lambda x: round(np.sum(x),0)
            }
        )
    Transaction_amount_df=Transaction_amount_df.sort_values(
        by='Amount',ascending=False
        )
    st.dataframe(Transaction_amount_df.head(10))

with col2:
    st.write('### By Transaction count: ')
    Transaction_count_df=pd.pivot_table(
        aggregated_transactions_state_data[
            (aggregated_transactions_state_data['Year']==year) &
            (aggregated_transactions_state_data['Quarter']==quarter)
            ],
        index='State',
        values=['Count'],
        aggfunc={
            'Count':np.sum
            }
        )
    Transaction_count_df=Transaction_count_df.sort_values(
        by='Count',ascending=False
        )
    st.dataframe(Transaction_count_df.head(10))
    
with col3:
    st.write('### By registered users: ')
    Registered_df=aggregated_users_state_data_summary[
        (aggregated_users_state_data_summary['Year']==year) &
        (aggregated_users_state_data_summary['Quarter']==quarter)
        ]
    
    Registered_df=pd.pivot_table(
        Registered_df,
        index='State',
        values='RegisteredUsers',
        aggfunc={
            'RegisteredUsers':np.sum
            }
        )
    
    Registered_df=Registered_df.sort_values(
        by='RegisteredUsers',ascending=False
        )
    
    st.dataframe(Registered_df.head(10))
    
with col4:
    st.write('### By app openings: ')
    Appopens_df=aggregated_users_state_data_summary[
        (aggregated_users_state_data_summary['Year']==year) &
        (aggregated_users_state_data_summary['Quarter']==quarter)
        ]
    
    Appopens_df=pd.pivot_table(
        Appopens_df,
        index='State',
        values='AppOpenings',
        aggfunc={
            'AppOpenings':np.sum
            }
        )
    
    Appopens_df=Appopens_df.sort_values(
        by='AppOpenings',ascending=False
        )
    
    st.dataframe(Appopens_df.head(10))