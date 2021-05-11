import streamlit as st
import altair as alt

from src.pages.utils.data import basins_names
from src.pages.utils.load_time_series import compute_yr_accum

def plot_ts_yr(dfs, basin):
    curr_df = dfs.filter(['date', basin, 'OBS'], axis="columns")
    curr_df = curr_df.rename(columns={basin: 'curr_basin'})
    highlight = alt.selection(type='single', on='mouseover',
                            fields=['OBS'], nearest=True)
    base = alt.Chart(curr_df).encode(
        x=alt.X('year(date):O', title="Date"),
        y=alt.Y('curr_basin:Q', title=f'{basin}'),
        color='OBS:N'
        ).properties(
            title='Acumulado Anual: 1981 - 2016'
        )
    points = base.mark_circle().encode(
        opacity=alt.value(0),
        tooltip=[
            alt.Tooltip('OBS:N', title='Obs'),
            alt.Tooltip('date:T', title='Year'),
            alt.Tooltip('curr_basin:Q', title='Value')
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
    df_yr_accum = compute_yr_accum()
    basin = st.sidebar.selectbox('Select Basin', basins_names())
    # st.subheader('Acumulado Anual: 1981 - 2016')
    points_lines = plot_ts_yr(df_yr_accum, basin)
    st.write(points_lines)
    show_df = st.checkbox('Display Data')
    if show_df:
        st.write(df_yr_accum.filter(['date', basin, 'OBS'], axis="columns"))
