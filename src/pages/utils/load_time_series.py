import pandas as pd
import streamlit as st
# from datetime import datetime

from src.pages.utils.data import dbobs_names

# @st.cache()
def load_time_series(start_date: str = '1981-01', end_date:str = '2016-12') -> pd.DataFrame:
    dfs = pd.DataFrame()
    for n in dbobs_names():
        csv_file = f'data/month/{n}_bacias.csv'
        df = pd.read_csv(csv_file, sep=';')
        df['OBS'] = n.upper()
        df['date'] = pd.to_datetime(df['date'], format="%Y/%m/%d")
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        dfs = dfs.append(df.loc[mask])
    return dfs


# @st.cache()
def compute_yr_accum(start_date: str = '1981-01', end_date:str = '2016-12') -> pd.DataFrame:
    dfs = pd.DataFrame()
    for n in dbobs_names():
        csv_file = f'data/month/{n}_bacias.csv'
        # custom_date_parser = lambda x: datetime.strptime(x, "%Y-%m-%d")
        df = pd.read_csv(
            csv_file,
            sep=';',
            # parse_dates=['date'],
            # index_col=['date'],
            # date_parser=custom_date_parser
        )
        df['date'] = pd.to_datetime(df['date'], format="%Y/%m/%d")
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        df = df.loc[mask]
        df.set_index(df['date'], inplace=True)
        df = df.resample('Y').sum()
        df.reset_index(level=0, inplace=True)
        df['OBS'] = n.upper()
        col_obs = df.pop('OBS')
        df.insert(1, 'OBS', col_obs)
        dfs = dfs.append(df)
    
    return dfs
