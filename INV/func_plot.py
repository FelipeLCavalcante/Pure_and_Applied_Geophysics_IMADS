#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import cm
from matplotlib.font_manager import FontProperties
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from colour import Color
from sklearn.metrics import r2_score
from collections import OrderedDict
from matplotlib import collections as mc
from matplotlib import gridspec


def plot_res(X, T, B, cT, B0, T0, cB, p, prism, lp, FDA_vals, Fh, sint=None, initial=None, euler=None):

    fig = plt.figure(figsize=[6, 8])
    gs = gridspec.GridSpec(3, 1, width_ratios=[1], height_ratios=[
                           1, 1, 2], figure=fig)
    ax = plt.subplot(gs[0, :])
    ax2 = plt.subplot(gs[1, :])
    ax3 = plt.subplot(gs[2, :])

    max_yticks = 2

    # Graphic of AMA --------------------------------------------------------------

    ax.plot(X/1000, B0, '--k')
    ax.plot(X/1000, cB, '-b')
    ax.scatter(X/1000, B, s=10, linewidths=1,
               facecolors='none', edgecolors='y')
    ax.set_xlim([X[0]/1000, X[-1]/1000])
    ax.set_ylabel('AMA (nT)', fontsize=12)

    yloc = plt.MaxNLocator(max_yticks)
    ax.yaxis.set_major_locator(yloc)

    ax.legend(["Initial", "Inverted", "Measured"], loc="upper right",
              prop={'size': 10}, bbox_to_anchor=(1, 1.3), ncol=3)
    ax.set_title('a)', fontsize=12, fontweight="bold", position=(-0.08, 0.85))

    # Graphic of TFA ----------------------------------------------------------------

    ax2.plot(X/1000, T0, '--k')
    ax2.plot(X/1000, cT, '-b')
    ax2.scatter(X/1000, T, s=10, linewidths=1,
                facecolors='none', edgecolors='y')
    ax2.set_xlim([X[0]/1000, X[-1]/1000])
    ax2.set_ylabel('TFA (nT)', fontsize=12)

    yloc = plt.MaxNLocator(max_yticks)
    ax2.yaxis.set_major_locator(yloc)

    ax2.set_title('b)', fontsize=12, fontweight="bold", position=(-0.08, 0.85))

    # Prisms plotting -------------------------------------------------------------
    FDA_vals = FDA_vals*100
    FDA_vals = FDA_vals.astype(int)

    zmin = 0
    zmax = 1.3*max(p[:, 3])
    # zmax = 300
    x_width = 200
    half_width = x_width/2

    lp_zero = np.zeros(len(lp))
    lines = []
    for i in range(0, len(lp), 2):
        lines.append([(lp[i]/1000, 0), (lp[i+1]/1000, 0)])
    lc = mc.LineCollection(lines, colors="r", linewidths=4, zorder=0)
    lc.set_label(r'$\Delta_{i}$')  # Define o label na coleção
    ax3.add_collection(lc)

    th_offset = 200
    tv_offset = 10

    for i in range(len(p[:, 2])):
        if p[i, 1] > 0:  # polaridade normal hemisfério sul
            ax3.scatter(p[i, 2]/1000, p[i, 3], facecolors='None',
                        edgecolors='k', s=20, zorder=35, label='inv normal')

        else:
            ax3.scatter(p[i, 2]/1000, p[i, 3], facecolors='None',
                        edgecolors='b', s=20, zorder=35, label='inv reverse')

    if sint != None:
        arq = open(sint)
        sint_model = np.loadtxt(arq, skiprows=1)
        sint_model[:, 3] = sint_model[:, 3]

        if prism == 1:
            aux_mod = np.array([sint_model])
            sint_model = aux_mod
        for i in range(prism):
            if sint_model[i, 1] >= 0:
                ax3.axvline(sint_model[i, 2]/1000, ymin=0, ymax=(zmax-sint_model[i, 3])/(zmax-zmin),
                            color='k', zorder=15, label='true normal')

            elif sint_model[i, 1] < 0:
                ax3.axvline(sint_model[i, 2]/1000, ymin=0, ymax=(zmax-sint_model[i, 3])/(zmax-zmin),
                            color='b', zorder=15, label='true reverse')

        arq.close()

    for i in range(prism):
        if prism == 1:
            aux_FDA = np.array([FDA_vals])
            FDA_vals = aux_FDA
        ax3.text(p[i, 2]/1000-th_offset, (p[i, 3])-tv_offset, r'' +
                 str(FDA_vals[i])+"%", fontsize=6, zorder=45)

    for i in range(0, prism, 10):
        ax3.text(p[i, 2]/1000, -5, str(i+1), fontsize=8, color='r')

    if initial is not None:
        ax3.scatter(initial["x0"]/1000, initial["z0"], facecolors='r',
                    edgecolors='r', s=15, marker='x', zorder=30, label='Initial')

    ax3.set_xlim([X[0]/1000, X[-1]/1000])
    ax3.set_ylim([0, zmax])
    ax3.invert_yaxis()
    ax3.set_ylabel('Depth (m)', fontsize=12)
    ax3.set_xlabel('Distance (km)', fontsize=12)

    handles, labels = ax3.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax3.legend(by_label.values(), by_label.keys(), prop={
               'size': 9}, loc='upper right', ncol=2, bbox_to_anchor=(1, 0.95), columnspacing=0.5)

    ax3.set_title('c)', fontsize=12, fontweight="bold", position=(-0.08, 0.85))

    ytcks = np.arange(0, zmax, 100)  # real: 250
    ax3.set_yticks(ytcks)

    fig.tight_layout()
    plt.show()

    return
