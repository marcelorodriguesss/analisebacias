import numpy as np
import streamlit as st
import pandas as pd

from src.pages.utils.load_time_series import compute_yr_accum, load_time_series
from src.pages.utils.data import basins_names, dbobs_names

def color_negative_red(value: float) -> str:
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


def nash_sut_coef(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Nash Sutcliffe efficiency coefficient

    input:
        x: simulated
        y: observed

    output:
        ns: Nash Sutcliffe efficient coefficient
    """

    return 1 - sum((x - y) ** 2) / sum((y - np.mean(y)) ** 2)


def main():

    obs_names = dbobs_names()

    basins = basins_names()

    dfs = load_time_series()

    nash = {}

    for b in basins:

        data = []

        for obs in obs_names:
            df_curr = dfs[(dfs.OBS == obs.upper())]
            df_curr = df_curr[b]
            df_curr.reset_index(drop=True, inplace=True)
            data.append(df_curr.values)

        d = {}

        for i, obs in enumerate(obs_names):

            if i > 0:

                d[obs] = nash_sut_coef(data[0], data[i])

        nash[b] = d

    st.markdown('### NASH - DADOS x REFERÊNCIA - 1981-2016 - MENSAL')

    st.table(pd.DataFrame(nash, index=obs_names[1:]).style.applymap(color_negative_red).format("{:.2}"))

    st.stop()

    dfs = compute_yr_accum()

    nash = {}

    for b in basins:

        data = []

        for obs in obs_names:
            df_curr = dfs[(dfs.OBS == obs.upper())]
            df_curr = df_curr[b]
            df_curr.reset_index(drop=True, inplace=True)
            data.append(df_curr.values)

        d = {}

        for i, obs in enumerate(obs_names):

            if i > 0:

                d[obs] = nash_sut_coef(data[0], data[i])

        nash[b] = d

    st.markdown('### NASH - DADOS x REFERÊNCIA - 1981-2016 - ANUAL')

    st.table(pd.DataFrame(nash, index=obs_names[1:]).style.applymap(color_negative_red).format("{:.2}"))
