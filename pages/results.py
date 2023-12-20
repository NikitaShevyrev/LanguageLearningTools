import streamlit as st
from page_supplementaries import get_sidebar, get_footer
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import numpy as np
from datetime import datetime

url = 'https://docs.google.com/spreadsheets/d/1BnTx2pRWDICfhw77z8IlOzk1R7uKhEd8nw9H1Buq-dU/edit?usp=sharing'

get_sidebar()

def get_unique_vals(df: pd.DataFrame, key: str) -> np.ndarray:
    vals = pd.unique(df[key])
    return vals[vals != 'none']

def retreive_records(df: pd.DataFrame, key: str, sort_options: dict) -> pd.DataFrame:
    if len(sort_options[key]) > 0:
        condn_mask = df[key] == sort_options[key][0]
        for i in range(1, len(sort_options[key])):
            condn_mask |= (df[key] == sort_options[key][i])
        df = df[condn_mask]
    return df

conn = st.connection("gsheets", type=GSheetsConnection)
try:
    df = conn.read(spreadsheet=url, usecols=[0,1,2,3,4,5,6,7,8,9])
    
    df['Отметка времени'] = pd.to_datetime(df['Отметка времени'], format='%d.%m.%Y %H:%M:%S')
    
    df['Attempt - Total Time Spent, sec'] = df['Attempt - Time Spent, sec']
    df['Attempt - Time Spent, sec'] = pd.to_timedelta(df['Attempt - Time Spent, sec'], unit='seconds')
    df['Attempt - Time Spent, sec'] = df['Attempt - Time Spent, sec'].astype(str)
    df['Attempt - Time Spent, sec'] = df['Attempt - Time Spent, sec'].apply(lambda x: x.split(' ')[-1])
    df.rename(columns={'Attempt - Time Spent, sec': 'Attempt - Time Spent, HH:MM:SS'}, inplace=True)
    df = df.iloc[:,[0,1,10,2,3,4,5,6,7,8,9]]

    df.rename(columns={'Отметка времени': "Timestamp"}, inplace=True)
    
    columns = [col for col in df.columns if not col.startswith('Attempt')]

    # choose filtering by column
    sort_by = st.multiselect("Select column(-s) for sorting by:", columns)

    sort_options = {}
    # add filtering
    if 'Timestamp' in sort_by:
        min_val = df['Timestamp'].min()
        max_val = df['Timestamp'].max()
        accepted_time_interval = (min_val, max_val)
        (min_date_choice, max_date_choice) = st.date_input(
            "Select time interval to find records:", value=accepted_time_interval, min_value=min_val, max_value=max_val
        )
        min_date_choice = pd.Timestamp(min_date_choice)
        max_date_choice = pd.Timestamp(year=max_date_choice.year, month=max_date_choice.month, day=max_date_choice.day, hour=23, minute=59, second=59)
        df = df[(pd.Timestamp(min_date_choice) <= df['Timestamp']) & (df['Timestamp'] <= pd.Timestamp(max_date_choice))]

    if 'User Name' in sort_by:
        sort_options['User Name'] = st.multiselect("Select user(-s) to find records:", get_unique_vals(df, 'User Name'))
        df = retreive_records(df, 'User Name', sort_options)
    
    if 'Task Type' in sort_by:
        sort_options['Task Type'] = st.multiselect("Select task type(-s) to find records:", get_unique_vals(df, 'Task Type'))
        df = retreive_records(df, 'Task Type', sort_options)
    
    if 'Target Language' in sort_by:
        sort_options['Target Language'] = st.multiselect("Select target language(-s) to find records:", get_unique_vals(df, 'Target Language'))
        df = retreive_records(df, 'Target Language', sort_options)
    
    if 'Fluent Language' in sort_by:
        sort_options['Fluent Language'] = st.multiselect("Select fluent language(-s) to find records:", get_unique_vals(df, 'Fluent Language'))
        df = retreive_records(df, 'Fluent Language', sort_options)
    
    if 'Video choice' in sort_by:
        sort_options['Video choice'] = st.multiselect("Select video name(-s) to find records:", get_unique_vals(df, 'Video choice'))
        df = retreive_records(df, 'Video choice', sort_options)

    if 'Proficiency Level' in sort_by:
        sort_options['Proficiency Level'] = st.multiselect("Select proficiency level(-s) to find records:", get_unique_vals(df, 'Proficiency Level'))
        df = retreive_records(df, 'Proficiency Level', sort_options)

    if 'Unit choice' in sort_by:
        sort_options['Unit choice'] = st.multiselect("Select unit(-s) to find records:", get_unique_vals(df, 'Unit choice'))
        df = retreive_records(df, 'Unit choice', sort_options)
    
    if 'Exercise choice' in sort_by:
        sort_options['Exercise choice'] = st.multiselect("Select exercise(-s) to find records:", get_unique_vals(df, 'Exercise choice'))
        df = retreive_records(df, 'Exercise choice', sort_options)

    st.dataframe(df, hide_index=True)

except:
    st.warning('Something went wrong')

get_footer()