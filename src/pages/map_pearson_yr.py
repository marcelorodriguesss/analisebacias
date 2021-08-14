import shapely
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import cartopy as cart
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import matplotlib.patches as mpatches

from src.pages.utils.data import basins_names, dbobs_names
from src.pages.utils.load_time_series import compute_yr_accum

def compute_pearson_mon():

    obs_names = dbobs_names()

    basins = basins_names()

    dfs = compute_yr_accum()

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

        correl[b] = np.around(corr_data.values, 2)

    # dicionário onde a base de dados
    dd = {}
    for i, obs in enumerate(obs_names[1:]):
        dd[obs] = {}
        for k, v in correl.items():
            # st.write(k)
            # st.write(v)
            dd[obs][k] = v[i]

    return dd


def asc_to_polygon():

    # ref: https://stackoverflow.com/questions/30457089/how-to-create-a-shapely-polygon-from-a-list-of-shapely-points

    polygons = {}
    for basin in basins_names():
        curr_basin = f'./data/shapes/{basin}.asc'
        with open(curr_basin, 'r') as f:
            point_list = []
            for i in f.readlines():
                aux = i.split(',')
                point = shapely.geometry.Point(float(aux[0]), float(aux[1]))
                point_list.append(point)
            poly = shapely.geometry.Polygon([[p.x, p.y] for p in point_list])
        polygons[basin] = poly

    return polygons


def plot_regions(corr_values, fig_title='My Title'):

    # ref: https://stackoverflow.com/questions/57229425/cartopy-incorrectly-filling-outside-of-shapely-polygon

    fig = plt.figure(figsize=(10, 10))

    proj = cart.crs.PlateCarree(central_longitude=0)  # -156

    ax = plt.axes(projection=proj)

    shp_file_bound = './data/shapes/ne_50m_admin_1_br/brasil_contorno_sem_estados.shp'

    shape_feature = ShapelyFeature(Reader(shp_file_bound).geometries(),
                                   cart.crs.PlateCarree(), facecolor='none')

    ax.add_feature(shape_feature, edgecolor='k')

    # colorbar

    # paralelos e meridianos

    parallels = list(range(-180, 181, 5))

    meridians = list(range(-90, 91, 5))

    ax.set_xticks(parallels, crs=proj)

    ax.set_yticks(meridians, crs=proj)

    ax.set_xticklabels(parallels, rotation=0, fontsize=10, fontweight='bold')

    ax.set_yticklabels(meridians, rotation=0, fontsize=10, fontweight='bold')

    # ax.add_feature(cart.feature.OCEAN, zorder=50, edgecolor='k', facecolor='white')

    # contorno dos estados
    # states = cart.feature.NaturalEarthFeature(
    #     category='cultural',
    #     scale='50m', facecolor='none',
    #     name='admin_1_states_provinces_shp'
    # )
    # ax.add_feature(states, edgecolor='k')

    # contorno dos países
    # countries = cart.feature.NaturalEarthFeature(
    #     category='cultural',
    #     scale='50m', facecolor='none',
    #     name='admin_0_countries'
    # )
    # ax.add_feature(countries, edgecolor='k')

    ax.set_extent([-75, -33, -35, 6], proj)  # brasil

    dict_polygons = asc_to_polygon()

    for key in dict_polygons.keys():

        p = dict_polygons[key]

        # print(p.is_valid)

        px = p.exterior

        if px.is_ccw==False:
            px.coords = list(px.coords)[::-1]

        if corr_values[key] < 0:
            facecolor = '#ae000c'
        elif corr_values[key] > 0 and corr_values[key] <= 0.2:
            facecolor = '#ff0219'
        elif corr_values[key] > 0.2 and corr_values[key] <= 0.4:
            facecolor = '#ff5f26'
        elif corr_values[key] > 0.4 and corr_values[key] <= 0.6:
            facecolor = '#ff9d37'
        elif corr_values[key] > 0.6 and corr_values[key] <= 0.7:
            facecolor = '#fbe78a'
        elif corr_values[key] > 0.7 and corr_values[key] <= 0.8:
            facecolor = '#b0f0f7'
        elif corr_values[key] > 0.8 and corr_values[key] <= 0.9:
            facecolor = '#76bbf3'
        elif corr_values[key] > 0.9 and corr_values[key] <= 1.:
            facecolor = '#2372c9'
        else:
            corr_values[key] = 'green'

        shape_feature = ShapelyFeature(
                [p],
                cart.crs.PlateCarree(),
                edgecolor='black',
                facecolor=facecolor
            )

        ax.add_feature(shape_feature)

    ax.set_title(fig_title)

    # leg lado direito

    labels = ['< 0',
        '0 - 0.2',
        '0.2 - 0.4',
        '0.4 - 0.6',
        '0.6 - 0.7',
        '0.7 - 0.8',
        '0.8 - 0.9',
        '0.9 - 1',
        # 'NaN',
    ]

    interval1 = mpatches.Rectangle((0, 0), 1, 1, facecolor="#ae000c")
    interval2 = mpatches.Rectangle((0, 0), 1, 1, facecolor="#ff0219")
    interval3 = mpatches.Rectangle((0, 0), 1, 1, facecolor="#ff5f26")
    interval4 = mpatches.Rectangle((0, 0), 1, 1, facecolor="#ff9d37")
    interval5 = mpatches.Rectangle((0, 0), 1, 1, facecolor="#fbe78a")
    interval6 = mpatches.Rectangle((0, 0), 1, 1, facecolor="#b0f0f7")
    interval7 = mpatches.Rectangle((0, 0), 1, 1, facecolor="#76bbf3")
    interval8 = mpatches.Rectangle((0, 0), 1, 1, facecolor="#2372c9")
    # interval9 = mpatches.Rectangle((0, 0), 1, 1, facecolor="green")

    lst_intervals = [
        interval1,
        interval2,
        interval3,
        interval4,
        interval5,
        interval6,
        interval7,
        interval8,
        # interval9
    ]

    legend1 = ax.legend(lst_intervals, labels, loc='upper right',
                        fancybox=True, fontsize='small')

    # # leg lado esquerdo

    # labels = ['1: Santo Antonio', '2', '3', '4', '5', '6', '7', '8', '9', '10',
    #           '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
    #           '21', '22', '23', '24']

    # lst_leg = []

    # for i in range(len(labels)):
    #     lst_leg.append(mpatches.Rectangle((0, 0), 1, 1, facecolor="k"))

    # ax.legend(lst_leg, labels, fontsize='small',
    #           loc='upper right', fancybox=True, bbox_to_anchor=(-0.05, 1.02))

    # plt.gca().add_artist(legend1)

    # '1': (-65, -15),
    dict_pos = {
        '1': (-57, -7),
        '2': (-53.5, -7),
        '3': (-49, -7),
        '4': (-40, -9),
        '5': (-44.5, -15),
        '6': (-48, -13),
        '7': (-49, -15.1),
        '8': (-55.5, -10.5),
        '9': (-50.5, -18),
        '10': (-52.3, -20.5),
        '11': (-48.5, -20.5),
        '12': (-50.3, -23.5),
        '13': (-54.3, -23.5),
    }

    for key in dict_pos.keys():

        plt.annotate(key, xy=dict_pos[key], xycoords='data',
                      color='white', backgroundcolor='black', size='small')

    plt.annotate('14', xy=(-48.8, -17), xycoords='data', textcoords='data',
                 xytext=(-38, -16), color='white', backgroundcolor='black', size='small',
                 arrowprops=dict(arrowstyle= '<|-|>',
                             color='gray',
                             lw=1.,
                             ls='--'))

    plt.annotate('15', xy=(-47.8, -18), xycoords='data', textcoords='data',
                 xytext=(-38, -17.5), color='white', backgroundcolor='black', size='small',
                 arrowprops=dict(arrowstyle= '<|-|>',
                             color='gray',
                             lw=1.,
                             ls='--'))

    plt.annotate('16', xy=(-47.3, -19.7), xycoords='data', textcoords='data',
                xytext=(-38.5, -19), color='white', backgroundcolor='black', size='small',
                arrowprops=dict(arrowstyle= '<|-|>',
                            color='gray',
                            lw=1.,
                            ls='--'))

    plt.annotate('17', xy=(-45, -19.9), xycoords='data', textcoords='data',
                xytext=(-39, -20.5), color='white', backgroundcolor='black', size='small',
                arrowprops=dict(arrowstyle= '<|-|>',
                            color='gray',
                            lw=1.,
                            ls='--'))

    plt.annotate('18', xy=(-45, -21.3), xycoords='data', textcoords='data',
                xytext=(-40, -22), color='white', backgroundcolor='black', size='small',
                arrowprops=dict(arrowstyle= '<|-|>',
                            color='gray',
                            lw=1.,
                            ls='--'))

    plt.annotate('19', xy=(-45.8, -23), xycoords='data', textcoords='data',
                xytext=(-43, -24), color='white', backgroundcolor='black', size='small',
                arrowprops=dict(arrowstyle= '<|-|>',
                            color='gray',
                            lw=1.,
                            ls='--'))

    plt.annotate('20', xy=(-48, -23), xycoords='data', textcoords='data',
                xytext=(-45, -25), color='white', backgroundcolor='black', size='small',
                arrowprops=dict(arrowstyle= '<|-|>',
                            color='gray',
                            lw=1.,
                            ls='--'))

    plt.annotate('21', xy=(-50, -26), xycoords='data', textcoords='data',
                xytext=(-47, -27), color='white', backgroundcolor='black', size='small',
                arrowprops=dict(arrowstyle= '<|-|>',
                            color='gray',
                            lw=1.,
                            ls='--'))

    plt.annotate('22', xy=(-50.5, -28), xycoords='data', textcoords='data',
                xytext=(-48, -29), color='white', backgroundcolor='black', size='small',
                arrowprops=dict(arrowstyle= '<|-|>',
                            color='gray',
                            lw=1.,
                            ls='--'))

    plt.annotate('23', xy=(-53.5, -29), xycoords='data', textcoords='data',
                xytext=(-49, -30.5), color='white', backgroundcolor='black', size='small',
                arrowprops=dict(arrowstyle= '<|-|>',
                            color='gray',
                            lw=1.,
                            ls='--'))

    # plt.show()

    return fig


def main():
    pearson = compute_pearson_mon()
    # st.write(pearson)
    with st.spinner('Espere um segundo...'):
        obs_names = dbobs_names()
        for obs in obs_names[1:]:
            map = plot_regions(pearson[obs], obs.upper())
            st.write(map)

