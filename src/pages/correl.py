import pandas as pd
import streamlit as st

from src.pages.utils.load_time_series import compute_yr_accum, load_time_series
from src.pages.utils.data import basins_names, dbobs_names

def color_negative_red(value):
    """
    Colors elements in a dateframe
    green if positive and red if
    negative. Does not color NaN
    values.
    """

    if value < 0:
        color = '#ae000c'
    elif value > 0 and value <= 0.2:
        color = '#ff0219'
    elif value > 0.2 and value <= 0.4:
        color = '#ff5f26'
    elif value > 0.4 and value <= 0.6:
        color = '#ff9d37'
    elif value > 0.6 and value <= 0.7:
        color = '#fbe78a'
    elif value > 0.7 and value <= 0.8:
        color = '#b0f0f7'
    elif value > 0.8 and value <= 0.9:
        color = '#76bbf3'
    elif value > 0.9 and value <= 1.:
        color = '#2372c9'
    else:
        color = 'green'

    return 'color: %s' % color


def main():

    obs_names = dbobs_names()

    basins = basins_names()

    dfs = load_time_series()

    correl = {}

    for b in basins:

        data = []

        for obs in obs_names:
            df_curr = dfs[(dfs.OBS == obs.upper())]
            df_curr = df_curr[b]
            df_curr.reset_index(drop=True, inplace=True)
            data.append(df_curr)

        df3 = pd.concat(data, axis=1, keys=obs_names)

        corr_data = df3.corr().iloc[1:, 0]

        correl[b] = corr_data.values

    st.markdown("#### CORRELAÇÃO MENSAL ENTRE BASES DE DADOS x REFERÊNCIA")
    st.markdown('#### PERÍODO: 1981-2016')

    # st.write(pd.DataFrame(correl, index=obs_names[1:]))

    st.table(pd.DataFrame(correl, index=obs_names[1:]).style.applymap(color_negative_red).format("{:.2}"))

    dfs = compute_yr_accum()

    correl = {}

    for b in basins:

        data = []

        for obs in obs_names:
            df_curr = dfs[(dfs.OBS == obs.upper())]
            df_curr = df_curr[b]
            df_curr.reset_index(drop=True, inplace=True)
            # st.write(df_curr)
            data.append(df_curr)

        df3 = pd.concat(data, axis=1, keys=obs_names)

        corr_data = df3.corr().iloc[1:, 0]

        correl[b] = corr_data.values

    st.markdown("#### CORRELAÇÃO ANUAL ENTRE BASES DE DADOS x REFERÊNCIA")
    st.markdown('#### PERÍODO: 1981-2016')

    st.table(pd.DataFrame(correl, index=obs_names[1:]).style.applymap(color_negative_red).format("{:.2}"))
