#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.signal import find_peaks as fp
from matplotlib.widgets import MultiCursor
from matplotlib import collections as mc
from math import atan2

"""
======================================================================
Nome do Script: 3_PyDyke_lims.py
Autor: Felipe Lisbona Cavalcante
Data: 27/02/2025
Versão: 1.0
======================================================================
DESCRIÇÃO:
    Este script realiza o processamento e a extração de parâmetros a partir dos
    dados de um modelo magnético de prismas. Com base na segunda derivada do sinal
    filtrado (TFA_r_filt), o script identifica picos (mínimos locais) e, a partir
    deles, calcula parâmetros importantes do modelo, tais como:
      - Za: profundidade associada aos mínimos, ajustada pela altura de voo (FH);
      - A0: parâmetro derivado do campo magnético filtrado;
      - im: ângulo de inclinação modificado, convertido para graus e ajustado ao
            referencial trigonométrico.
      
    Além disso, o script determina intervalos (xi e xf) correspondentes a cada prisma,
    corrige intervalos colapsados e sobrepostos, e calcula uma função de distribuição
    acumulada (FDA) dos intervalos. Os resultados são salvos em arquivos de texto e
    também são visualizados por meio de diversos gráficos que comparam os sinais
    originais e filtrados, exibem os intervalos identificados e anotam os mínimos
    locais.

VARIÁVEIS PRINCIPAIS:
    index      : Identificador do modelo (ex.: 'M1')
    FH         : Altura de voo (em metros)
    I          : Inclinação do campo geomagnético local
    D          : Declinação do campo gemognético local
    strk       : Strike da lâmina (ajustado para referência do modelo)
    alpha      : Ângulo de referência a partir do Norte magnético
    cut_pike   : Limite de corte para identificação de picos
    prof_ini   : Limite inferior do corte (em metros)
    prof_end   : Limite superior do corte (em metros)
    dd         : Discretização (em metros)
    dec        : Fator de decimação

USO:
    Execute o script com Python 3. Por exemplo:
        python 3_PyDyke_lims.py

SAÍDAS:
    - Input/lims_M1_mins.txt: Arquivo de texto com os valores dos mínimos locais (h_pks).
    - Input/lims_M1.txt: Arquivo de texto com os parâmetros extraídos (com cabeçalho
      "P xi xf A0 z0 im x0 delta").
    - Várias figuras que exibem:
         * Os sinais "TFA_r" (original) e "TFA_r_filt" (filtrado) em função da distância;
         * Os sinais "AMA_r" e "AMA_r_filt", com os intervalos dos prismas destacados (usando
           LineCollection) e a numeração dos picos;
         * A segunda derivada dos sinais (d2T_orig e d2T) com os mínimos locais identificados;
         * Uma interface interativa (MultiCursor) para facilitar a análise gráfica.
======================================================================
"""


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    out = [array[idx], idx]
    return out


# Area de ajustes ====================================================
index = 'M1'

FH = 100
I = -30
D = 0
strk = 135
strk = -(strk-180)
alpha = strk - D
cut_pike = 5E-4
# Area de ajustes ====================================================

file_path1 = f"Input/fwd_r_{index}_cut.csv"  # dado original

lim_name = f"lims_{index}"

df = pd.read_csv(file_path1)  # dado completo

d2x_aux = df.d2x.to_numpy()
d2x = d2x_aux[1:-1]  # elimina derivadas dos extremos
d2T_aux = df.d2y_AMA_r_filt.to_numpy()
d2T = d2T_aux[1:-1]  # elimina derivadas dos extremos
d2T_orig_aux = df.d2y_AMA_r.to_numpy()
d2T_orig = d2T_orig_aux[1:-1]

pks = fp(-d2T, height=cut_pike)
pos_pks = d2x[pks[0]]
h_pks = pks[1]['peak_heights']

idx = pks[0]

idx = idx.astype(int)

Za = np.sqrt(-df['AMA_r_filt'][idx]/d2T[idx])
Za = Za.to_numpy()

# mu0 = 4*np.pi*1e-7 # (N/A²)
mu0 = 1.2566*1e3  # (nT.m/A)
frac = mu0/(2*np.pi)
# frac = mu0/(4*np.pi)
A0 = ((df['AMA_r_filt'][idx])*Za)/frac
A0 = A0.to_numpy()

I_aux = np.deg2rad(I)
alpha_aux = np.deg2rad(alpha)
D_aux = np.deg2rad(D)
Ip = np.arctan2(np.tan(I_aux), np.sin(alpha_aux-D_aux))
im_p = I_aux-np.arcsin(df['TFA_r_filt'][idx]/df['AMA_r_filt'][idx])
im = np.rad2deg(im_p)
im = im.to_numpy()+90  # referencial do círculo trigonométrico

s = np.zeros((len(idx), 2))

eps = 1  # precisao para checar se os intervalos são iguais

for i in range(len(idx)):  # inicia xi e xf
    s[i, 0] = d2x[0]
    s[i, 1] = d2x[-1]
    # s[i,2] = d2x[idx[i]]

for i in range(len(idx)):  # define intervalos
    if idx[i] == 0:
        j = 1
        # print(f"Oi0 {i}")
        s[i, 0] = d2x[0]
        while idx[i]+j < len(d2x):
            if d2T[idx[i]+j] > 0:
                s[i, 1] = d2x[idx[i]+j-1]
                break
            j += 1

    elif idx[i] == len(d2x)-1:
        j = 1
        # print(f"Oi-1 {i}")
        s[i, 1] = d2x[-1]
        while idx[i]-j > 0:
            if d2T[idx[i]-j] > 0:
                s[i, 1] = d2x[idx[i]+j-1]
                break
            j += 1

    else:
        j = 1
        while idx[i]+j < len(d2x):  # direita
            # print(f"Oi1 {i}")
            if d2T[idx[i]+j] > 0:
                s[i, 1] = d2x[idx[i]+j-1]
                break
            j += 1

        j = 1
        while idx[i]-j > 0:  # esquerda
            # print(f"Oi2 {i}")
            if d2T[idx[i]-j] > 0:
                s[i, 0] = d2x[idx[i]-j+1]
                break
            j += 1

s, idx_uniq = np.unique(s, axis=0, return_index=True)
Za = Za[idx_uniq]-FH
A0 = A0[idx_uniq]
im = im[idx_uniq]
pos_pks = pos_pks[idx_uniq]

idx = idx[idx_uniq]
h_pks = h_pks[idx_uniq]

for i in range(len(s[:0])):  # checa limites colapsados
    if abs(s[i, 0] - s[i, 1]) < eps:
        if i > 0 and i < len(idx)-1:  # valores interiores
            if s[i, 0] - FH < s[i-1, 1]:  # olhar esquerda
                mid_val = (s[i, 0]+s[i-1, 1])/2
                s[i, 0] = mid_val
            else:
                s[i, 0] = s[i, 0] - FH

            if s[i, 1] + FH > s[i+1, 0]:  # olhar direita
                mid_val = (s[i, 1]+s[i+1, 0])/2
                s[i, 1] = mid_val
            else:
                s[i, 1] = s[i, 1] + FH
            """ if s[i-1,1]+FH < d2x[idx[i]]:
                s[i,0] = s[i-1,1]+FH
            else:
                s[i,0] = s[i-1,1]

            if s[i+1,0]-FH > d2x[idx[i]]:
                s[i,1] = s[i+1,0]-FH
            else:
                s[i,1] = s[i+1,0] """

        elif i == 0:  # extremo esquerdo
            # if s[i+1,0]-FH > d2x[idx[i]]:
            if idx[0] > 0:
                # s[i,0] = d2x[0]; s[i,1] = s[i+1,0]-FH
                s[i, 0] = df['dist'][idx[0]-1]

                if s[i, 1] + FH < s[i+1, 0]:
                    s[i, 1] = s[i, 1] + FH
                else:
                    mid_val = (s[i, 1] + s[i+1, 0]-FH)/2
                    s[i, 1] = mid_val
            else:
                s[i, 0] = d2x[0]

                if s[i, 1] + FH < s[i+1, 0]:
                    s[i, 1] = s[i, 1] + FH
                else:
                    mid_val = (s[i, 1] + s[i+1, 0])/2
                    s[i, 1] = mid_val

        elif i == len(idx)-1:  # extremo direito
            if idx[i] < df['dist'].iloc[-1]:
                # if s[i-1,1]+FH < d2x[idx[i]]:
                s[i, 1] = df['dist'][idx[-1]+1]

                if s[i, 0] - FH > s[i-1, 1]:
                    s[i, 0] = s[i, 0] - FH
                else:
                    mid_val = (s[i, 0] + s[i-1, 1])/2
                    s[i, 0] = mid_val
            else:
                s[i, 1] = d2x[-1]

                if s[i, 0] - FH > s[i-1, 1]:
                    s[i, 0] = s[i, 0] - FH
                else:
                    mid_val = (s[i, 0] + s[i-1, 1])/2
                    s[i, 0] = mid_val

for i in range(len(s[:, 0])-1):  # checa sobreposicao
    if s[i, 1] > s[i+1, 0]:
        if s[i, 1]+FH < d2x[idx[i+1]]:
            s[i+1, 0] = s[i, 1]+FH
        else:
            s[i+1, 0] = s[i, 1]

header_label = "P xi xf A0 z0 im x0 delta"

prism = len(A0)
FDA = np.zeros(prism)
delta = s[:, 1] - s[:, 0]
for i in range(prism):  # Function of acumulative distribution
    FDA[i] = (2/np.pi)*atan2(delta[i]/2, Za[i])

FDA = FDA*100
FDA = FDA.astype(int)
print(FDA)

exit_data = np.c_[FDA, s[:, 0], s[:, 1], A0, Za, im, pos_pks, s[:, 1]-s[:, 0]]

aux_ind = np.argwhere(np.isnan(exit_data))

check_inc = np.argwhere(aux_ind == 5)
check_inc = check_inc[:, 0]
aux_inc = aux_ind[check_inc, 0]

exit_data[aux_inc, 5] = 0

cut_Pc = 0  # ARRUMAR !!
if cut_Pc == 1:
    Pc = 10
    exit_data = np.delete(exit_data, np.argwhere(
        exit_data[:, 0] < Pc)[0], axis=0)
    h_pks = np.delete(h_pks, np.argwhere(exit_data[:, 0] < Pc)[0], axis=0)
    s = np.delete(s, np.argwhere(exit_data[:, 0] < Pc)[0], axis=0)
    prism = len(exit_data[:, 0])

np.savetxt("Input/"+lim_name+"_mins.txt", -h_pks, header="mins", comments='')
np.savetxt("Input/"+lim_name+".txt", exit_data,
           header=header_label, comments='')

lp_zero = np.zeros(2*prism)

lines = []
for i in range(prism):
    lines.append([(exit_data[i, 1]/1000, 0), (exit_data[i, 2]/1000, 0)])
lc = mc.LineCollection(lines, colors="r", linewidths=3,
                       zorder=0, label=r"$\Delta_{i}$")  # ,label="intervals"
lp = np.reshape(s, (2*prism, 1))

fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, figsize=(8, 6))

ax1.plot(df["dist"]/1000, df["TFA_r"], '-b', linewidth=1, label="original")
ax1.plot(df["dist"]/1000, df["TFA_r_filt"],
         '-k', linewidth=1, label="filtered")
ax1.set_ylabel("TFA (nT)", fontsize=12)
ax1.legend(loc="upper right", fontsize=10)

ax2.plot(df["dist"]/1000, df["AMA_r"], '-b', linewidth=1)
ax2.plot(df["dist"]/1000, df["AMA_r_filt"], '-k', linewidth=1)
ax2.set_ylabel("AMA (nT)", fontsize=12)
ax2.add_collection(lc)
ax2.legend(loc="upper right", fontsize=10)
ax2.set_ylim([-5, max(df["AMA_r"])+5])

for i in range(0, prism, 10):
    ax2.text(exit_data[i, 6]/1000, 5, str(i+1), fontsize=8, color='r')

ax3.plot(d2x/1000, d2T_orig, '-b', linewidth=1, zorder=0)
ax3.plot(d2x/1000, d2T, '-k', linewidth=1, zorder=1)
ax3.scatter(exit_data[:, 6]/1000, -h_pks, facecolors='none',
            edgecolors='r', label='local minimum', linewidth=2, zorder=2)
ax3.set_ylabel(r"$|T(x)|''$ (nT/m²)", fontsize=12)
ax3.set_xlabel("Distance (km)", fontsize=12)

ax3.set_ylim([-3E-3, 3E-3])
ax3.set_xlim([min(df.dist/1000), max(df.dist/1000)])
ax3.legend(loc="upper center", fontsize=10, ncol=3)

multi = MultiCursor(fig.canvas, (ax1, ax2), color='r', lw=1)
fig.tight_layout()
plt.show()
