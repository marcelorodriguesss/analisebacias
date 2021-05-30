import altair as alt
import streamlit as st

from src.pages.utils.load_time_series import compute_clim_mon
from src.pages.utils.data import basins_names

def plot_clim_mon(dfs, basin):

    curr_df = dfs.filter(['date', basin, 'OBS'], axis="columns")

    curr_df = curr_df.rename(columns={basin: 'curr_basin'})

    highlight = alt.selection(type='single', on='mouseover',
                              fields=['OBS'], nearest=True)

    basin_name = basin.upper()

    base = alt.Chart(curr_df).encode(
        x=alt.X('date:Q', title="MESES DA CLIMATOLOGIA", scale=alt.Scale(zero=False)),
        y=alt.Y('curr_basin:Q', title='mm'),
        color='OBS:N'
        ).properties(
            title=f'CLIMATOLOGIA MENSAL - 1981-2016 ({basin_name})'
        )

    points = base.mark_circle().encode(
        opacity=alt.value(0),
        tooltip=[
            alt.Tooltip('OBS:N', title='Nome'),
            alt.Tooltip('date:Q', title='Mês'),
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

    st.markdown("<h2 style='text-align: center; color: red;'>CLIMATOLOGIA MENSAL (1981-2016)</h2><br/>", unsafe_allow_html=True)

    dfs = compute_clim_mon()

    with st.spinner('Espere um instante ...'):
        for b in basins_names():
            points_lines = plot_clim_mon(dfs, b)
            st.write(points_lines)

    show_df = st.checkbox('Mostrar dados ?')
    if show_df:
        st.table(dfs)
