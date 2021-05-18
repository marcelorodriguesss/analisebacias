import xarray as xr
import cartopy as cart
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap
from typing import List

from src.pages.utils.data import dbobs_names

def read_nc(dbobs_name: str, metric: str):
    nc_file = f'data/annual/{dbobs_name}.precip.1981-2016.{metric}_annual.nc'
    with xr.open_dataset(nc_file) as dset:
        return dset


def plotmap(arr, lon, lat, fig_title, pal='anom'):
    fig_map = plt.figure(figsize=(10, 7))
    proj = cart.crs.PlateCarree(central_longitude=0)  # -156
    ax = plt.axes(projection=proj)
    ax.add_feature(cart.feature.OCEAN, zorder=50, edgecolor='k', facecolor='white')
    if pal == 'std':
        # pal = ['#000044', '#0033FF', '#007FFF', '#0099FF', '#00B2FF',
        #        '#00CCFF', '#FFFFFF', '#FFCC00', '#FF9900', '#FF7F00',
        #        '#FF3300', '#A50000', '#B48C82']
        # clevs = [-3., -2.5, -2., -1.5, -1., -0.5, 0.5, 1., 1.5, 2., 2.5, 3.]
        # pal = ['#5B51A0', '#3388BB', '#64BAAC', '#AADDA7', '#EBFC99',
            #    '#FFFFC4', '#FEDD8A', '#FFAD61', '#F06F48', '#DD3445',
            #    '#990242']
        pal = ['#C0B4FF', '#8070EB', '#483CC8', '#2D1EA5', '#1464D2',
               '#2882F0', '#96D2FA', '#FFFAAA', '#FFC03C', '#FFA000',
               '#FF6000', '#E11400', '#A50000', '#F0DCD2', '#B48C82',
               '#785046'] 
        # clevs = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700]
        clevs = list(range(0, 701, 50))
        orient = 'vertical'
        shrink=0.9
        aspect=24
    elif pal == 'diff':
        pal = ('#0033FF', '#0099FF', '#FFFFFF', '#FFCC00', '#FF3300')
        clevs = [-1., -0.05, 0.05, 1.]
        orient = 'horizontal'
        shrink=0.3
        aspect=9
    else:
        pal = ['#D204A9', '#B605C1', '#9406DF', '#7907F7', '#5A45F9',
               '#368FFB', '#18CDFD', '#00F8E1', '#00E696', '#00D13C',
               '#0CC600', '#4CD500', '#99E700', '#D8F600', '#FFE900',
               '#FFB400', '#FF7400', '#FF3F00']
        clevs = list(range(100, 3400, 200))
        orient = 'vertical'
        shrink=0.9
        aspect=24
    ccols = ListedColormap(pal[1:-1])
    ccols.set_under(pal[0])
    ccols.set_over(pal[-1])
    norm = BoundaryNorm(clevs, ncolors=ccols.N, clip=False)
    img = ax.contourf(
        lon,
        lat,
        arr,
        cmap=ccols,
        levels=clevs,
        extend='both',
        norm=norm,
        transform=proj
    )
    # ax.gridlines(crs=proj, linewidth=1.5, color='black', alpha=0.5,
    #              linestyle='--', draw_labels=False)
    parallels = list(range(-180, 181, 10))
    meridians = list(range(-90, 91, 10))
    ax.set_xticks(parallels, crs=proj)
    ax.set_yticks(meridians, crs=proj)
    ax.set_xticklabels(parallels, rotation=0, fontsize=10, fontweight='bold')
    ax.set_yticklabels(meridians, rotation=0, fontsize=10, fontweight='bold')
    # ax.add_feature(
    #     cart.feature.LAND,
    #     zorder=50,
    #     edgecolor='k',  #808080
    #     facecolor='k'
    # )
    # contorno dos estados
    states = cart.feature.NaturalEarthFeature(
        category='cultural',
        scale='50m', facecolor='none',
        name='admin_1_states_provinces_shp'
    )
    ax.add_feature(states, edgecolor='k')
    # contorno dos países
    countries = cart.feature.NaturalEarthFeature(
        category='cultural',
        scale='50m', facecolor='none',
        name='admin_0_countries'
    )
    ax.add_feature(countries, edgecolor='k')
    ax.set_extent([-85, -30, -60, 15], proj)
    bar = fig_map.colorbar(
                img,
                pad=0.03,
                spacing='uniform',
                orientation=orient,
                extend='both',
                ax=ax,
                extendfrac='auto',
                ticks=clevs,
                shrink=shrink,
                aspect=aspect
            )
    bar.ax.tick_params(labelsize=11)
    # fig_map.canvas.flush_events()
    # ref: https://matplotlib.org/3.1.1/gallery/ticks_and_spines/colorbar_tick_labelling_demo.html
    # bar.ax.set_yticklabels(
    #     labels=bar.ax.get_yticklabels(),
    #     fontsize=50, weight='bold'
    # )
    bar.set_label(label="(mm)", size=11, weight='bold')
    ax.set_title(fig_title, fontsize=12, weight='bold', loc='center')
    return fig_map


def main():
    obs_names: List[str] = dbobs_names()
    metric = st.sidebar.radio('Metric:', ('Mean', 'STD'))
    with st.spinner('Rendering maps ...'):
        for obs_name in obs_names:
            dset = read_nc(obs_name, metric.lower())
            fig = plotmap(
                dset.precip.values[0],
                dset.lon.values,
                dset.lat.values,
                obs_name.upper(),
                pal=metric.lower()
            )
            st.write(fig)

