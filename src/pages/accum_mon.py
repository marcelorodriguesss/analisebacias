import pandas as pd
import altair as alt
import streamlit as st

from src.pages.utils.load_time_series import load_time_series
from src.pages.utils.data import basins_names

def load_ts():
    return load_time_series()


# @st.cache
def plot_ts(dfs, basin, start_date, end_date):
    mask = (dfs['date'] >= start_date) & (dfs['date'] <= end_date)
    curr_df = dfs.loc[mask]
    curr_df = curr_df.filter(['date', basin, 'OBS'], axis="columns")
    curr_df = curr_df.rename(columns={basin: 'curr_basin'})
    highlight = alt.selection(type='single', on='mouseover',
                            fields=['OBS'], nearest=True)
    base = alt.Chart(curr_df).encode(
        x=alt.X('date:T', title="Date", axis=alt.Axis(format='%b/%Y')),
        y=alt.Y('curr_basin:Q', title=f'{basin}'),
        color='OBS:N'
    ).transform_timeunit(
        month='month(date)'
    )
    points = base.mark_circle().encode(
        opacity=alt.value(0),
        tooltip=[
            alt.Tooltip('OBS:N', title='OBS')
        ]
    ).add_selection(
        highlight
    ).properties(
        width=700,
        height=250
    )
    lines = base.mark_line().encode(
        size=alt.condition(~highlight, alt.value(1), alt.value(3))
    )
    return (points + lines)


def main():
    dfs = load_ts()
    basin = st.sidebar.selectbox('Select Basin', basins_names())
    st.subheader('1981 - 2016')
    with st.spinner('Rendering charts ...'):
        for y in range(1981, 2017):
            points_lines = plot_ts(dfs, basin, f'{y}-01', f'{y}-12')
            st.write(points_lines)
    show_df = st.checkbox('Display Data')
    if show_df:
        st.write(dfs.filter(['date', basin, 'OBS'], axis="columns"))
