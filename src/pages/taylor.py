import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist.grid_finder as gf
import mpl_toolkits.axisartist.floating_axes as fa
from matplotlib.projections import PolarAxes

from src.pages.utils.load_time_series import load_time_series
from src.pages.utils.data import basins_names, dbobs_names

class TaylorDiagram(object):
    """
    Taylor diagram.

    Plot model standard deviation and correlation to reference (data)
    sample in a single-quadrant polar plot, with r=stddev and
    theta=arccos(correlation).
    """

    def __init__(self, refstd,
                 fig=None, rect=111, label='_', srange=(0, 1.5), extend=False):
        """
        Set up Taylor diagram axes, i.e. single quadrant polar
        plot, using `mpl_toolkits.axisartist.floating_axes`.

        Parameters:

        * refstd: reference standard deviation to be compared to
        * fig: input Figure or None
        * rect: subplot definition
        * label: reference label
        * srange: stddev axis extension, in units of *refstd*
        * extend: extend diagram to negative correlations
        """

        self.refstd = refstd            # Reference standard deviation

        tr = PolarAxes.PolarTransform()

        # Correlation labels
        rlocs = np.array([0, 0.2, 0.4, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 1])
        if extend:
            # Diagram extended to negative correlations
            self.tmax = np.pi
            rlocs = np.concatenate((-rlocs[:0:-1], rlocs))
        else:
            # Diagram limited to positive correlations
            self.tmax = np.pi/2
        tlocs = np.arccos(rlocs)        # Conversion to polar angles
        gl1 = gf.FixedLocator(tlocs)    # Positions
        tf1 = gf.DictFormatter(dict(zip(tlocs, map(str, rlocs))))

        # Standard deviation axis extent (in units of reference stddev)
        self.smin = srange[0] * self.refstd
        self.smax = srange[1] * self.refstd

        ghelper = fa.GridHelperCurveLinear(
            tr,
            extremes=(0, self.tmax, self.smin, self.smax),
            grid_locator1=gl1, tick_formatter1=tf1)

        if fig is None:
            fig = plt.figure()

        ax = fa.FloatingSubplot(fig, rect, grid_helper=ghelper)
        fig.add_subplot(ax)

        # Adjust axes
        ax.axis["top"].set_axis_direction("bottom")   # "Angle axis"
        ax.axis["top"].toggle(ticklabels=True, label=True)
        ax.axis["top"].major_ticklabels.set_axis_direction("top")
        ax.axis["top"].label.set_axis_direction("top")
        ax.axis["top"].label.set_text('CORRELAÇÃO')
        ax.axis["top"].label.set_fontsize(10)

        ax.axis["left"].set_axis_direction("bottom")  # "X axis"
        ax.axis["left"].label.set_text("DESVIO PADRÃO")
        ax.axis["left"].label.set_fontsize(10)

        ax.axis["right"].set_axis_direction("top")    # "Y-axis"
        ax.axis["right"].toggle(ticklabels=True)
        ax.axis["right"].major_ticklabels.set_axis_direction(
            "bottom" if extend else "left")

        if self.smin:
            ax.axis["bottom"].toggle(ticklabels=False, label=False)
        else:
            ax.axis["bottom"].set_visible(False)          # Unused

        self._ax = ax                   # Graphical axes
        self.ax = ax.get_aux_axes(tr)   # Polar coordinates

        # Add reference point and stddev contour
        l, = self.ax.plot([0], self.refstd, 'k*',
                          ls='', ms=10, label=label)
        t = np.linspace(0, self.tmax)
        r = np.zeros_like(t) + self.refstd
        self.ax.plot(t, r, 'k--', label='_')

        # Collect sample points for latter use (e.g. legend)
        self.samplePoints = [l]

    def add_sample(self, stddev, corrcoef, *args, **kwargs):
        """
        Add sample (*stddev*, *corrcoeff*) to the Taylor
        diagram. *args* and *kwargs* are directly propagated to the
        `Figure.plot` command.
        """

        l, = self.ax.plot(np.arccos(corrcoef), stddev,
                          *args, **kwargs)  # (theta, radius)
        self.samplePoints.append(l)

        return l

    def add_grid(self, *args, **kwargs):
        """Add a grid."""

        self._ax.grid(*args, **kwargs)

    def add_contours(self, levels=5, **kwargs):
        """
        Add constant centered RMS difference contours, defined by *levels*.
        """

        rs, ts = np.meshgrid(np.linspace(self.smin, self.smax),
                             np.linspace(0, self.tmax))
        # Compute centered RMS difference
        rms = np.sqrt(self.refstd ** 2 + rs ** 2 - 2 * self.refstd * rs * np.cos(ts))

        contours = self.ax.contour(ts, rs, rms, levels, **kwargs)

        return contours


def main():
    dfs = load_time_series()

    obs_names = dbobs_names()

    taylor_obs_names = obs_names[1:]

    basins = basins_names()

    with st.spinner('Rendering charts ...'):

        for b in basins:

            data = []

            for obs in obs_names:
                df_curr = dfs[(dfs.OBS == obs.upper())]
                df_curr = df_curr[b]
                df_curr.reset_index(drop=True, inplace=True)
                data.append(df_curr)

            df3 = pd.concat(data, axis=1, keys=obs_names)

            std_bases = df3.std(ddof=1).values.tolist()

            stdref, std_bases = std_bases[0], std_bases[1:]

            corr_data = df3.corr().iloc[1:, 0].values.tolist()

            samples = []
            for i, t in enumerate(taylor_obs_names):
                samples.append([std_bases[i], corr_data[i], t])

            # samples = np.c_[std_bases, corr_data]

            fig = plt.figure(figsize=(3, 3))

            dia = TaylorDiagram(stdref, fig=fig, label='reference', extend=False)

            dia.samplePoints[0].set_color('r')  # Mark reference point as a red star

            # Add models to Taylor diagram
            for i, (stddev, corrcoef, name) in enumerate(samples):
                dia.add_sample(stddev, corrcoef, marker='$%d$' % (i+1), ms=7,
                            ls='', label=name)  # mec='k', mfc='k',

            # Add RMS contours, and label them
            # contours = dia.add_contours(levels=5, colors='0.5')  # 5 levels in grey
            # plt.clabel(contours, inline=1, fontsize=10, fmt='%.0f')

            dia.add_grid()  # Add grid

            dia._ax.axis[:].major_ticks.set_tick_out(True)  # Put ticks outward

            # Add a figure legend and title
            fig.legend(
                dia.samplePoints,
                [ p.get_label() for p in dia.samplePoints ],
                numpoints=1, prop=dict(size='8'), loc='upper right'
            )

            fig.suptitle(b.upper(), size='small')  # Figure title

            st.write(fig)

            st.stop()

            plt.close()
