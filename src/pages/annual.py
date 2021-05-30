import streamlit as st
import altair as alt

from src.pages.utils.data import basins_names
from src.pages.utils.load_time_series import compute_yr_accum

def plot_ts_yr(dfs, basin):

    curr_df = dfs.filter(['date', basin, 'OBS'], axis="columns")

    curr_df = curr_df.rename(columns={basin: 'curr_basin'})

    highlight = alt.selection(type='single', on='mouseover',
                              fields=['OBS'], nearest=True)

    basin_name = basin.upper()

    base = alt.Chart(curr_df).encode(
        x=alt.X('year(date):O', title="ANOS"),
        y=alt.Y('curr_basin:Q', title=basin_name),
        color='OBS:N'
        ).properties(
            title=f'ACUMULADO ANUAL - 1981-2016 ({basin_name})'
        )

    points = base.mark_circle().encode(
        opacity=alt.value(0),
        tooltip=[
            alt.Tooltip('OBS:N', title='Nome'),
            alt.Tooltip('year(date):O', title='Ano'),
            alt.Tooltip('curr_basin:Q', title='Valor')
        ]
    ).add_selection(
        highlight
    ).properties(
        width=700,
        height=350
    )

    lines = base.mark_line().encode(
        size=alt.condition(~highlight, alt.value(1), alt.value(3))
    )

    return (points + lines)


def main():

    st.markdown("<h2 style='text-align: center; color: red;'>ACUMULADO ANUAL PARA TODAS AS BACIAS</h2><br/>", unsafe_allow_html=True)

    df_yr_accum = compute_yr_accum()

    with st.spinner('Espere um instante ...'):
        for b in basins_names():
            points_lines = plot_ts_yr(df_yr_accum, b)
            st.write(points_lines)

    #TODO: adicionar opção para remover bases
    # show_df = st.checkbox('Display Data')
    # if show_df:
    #     st.write(df_yr_accum.filter(['date', basin, 'OBS'], axis="columns"))
