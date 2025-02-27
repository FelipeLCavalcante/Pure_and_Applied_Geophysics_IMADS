#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
# from matplotlib import cm
# from matplotlib.font_manager import FontProperties
from colour import Color
from collections import OrderedDict


def tabularS(X, dx, p, prism, index):

    # Prisms plotting -------------------------------------------------------------
    fig = plt.figure()
    axarr = fig.add_subplot(111)

    zf = 1.5*max(p[:, 3])
    # zf = 900
    lx = max(X)*0.01/2

    for i in range(prism):
        if p[i, 1] >= 0 and p[i, 0] >= 0.1:
            rect = Rectangle((p[i, 2]-(lx/2), zf), lx, (p[i, 3])-zf,
                             facecolor="blue", label="i$_{m}$ > 0", edgecolor="black")
            axarr.add_patch(rect)
            if i % 5 == 0:
                axarr.text(p[i, 2]-1, (p[i, 3])-1, r''+str(i+1), fontsize=12)
            handles, labels = axarr.get_legend_handles_labels()
            by_label = OrderedDict(zip(labels, handles))

        elif p[i, 1] < 0 and p[i, 0] >= 0.1:
            rect = Rectangle((p[i, 2]-(lx/2), zf), lx, (p[i, 3])-zf,
                             facecolor="red", label="i$_{m}$ < 0", edgecolor="black")
            axarr.add_patch(rect)
            if i % 5 == 0:
                axarr.text(p[i, 2]-1, (p[i, 3])-1, r''+str(i+1), fontsize=12)
            handles, labels = axarr.get_legend_handles_labels()
            by_label = OrderedDict(zip(labels, handles))

        elif p[i, 0] < 0.1:
            rect = Rectangle((p[i, 2]-(lx/2), zf), lx, (p[i, 3])-zf,
                             facecolor="green", label="Me = 0", edgecolor="black")
            axarr.add_patch(rect)
            if i % 5 == 0:
                axarr.text(p[i, 2]-1, (p[i, 3])-1, r''+str(i+1), fontsize=12)
            handles, labels = axarr.get_legend_handles_labels()
            by_label = OrderedDict(zip(labels, handles))

    axarr.set_xlim([X[0], X[-1]])
    axarr.set_ylim([0, zf])
    axarr.invert_yaxis()
    axarr.set_ylabel('Profundidade (m)')
    axarr.set_xlabel('Posição (m)')
    axarr.legend(by_label.values(), by_label.keys(),
                 loc="lower right", prop={'size': 9})

    # axarr.set_title('e)', fontsize=12, fontweight="bold", position=(-0.08,0.85))
    plt.savefig('Output/'+index+'_prism.svg')
    plt.show()

    return
