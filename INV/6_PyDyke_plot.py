#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import atan2

from func_plot import plot_res

"""
======================================================================
Nome do Script: 6_PyDyke_plot.py
Autor: Felipe Lisbona Cavalcante
Data: 27/02/2025
Versão: 1.0
======================================================================
DESCRIÇÃO:
    Este script processa os plota os resultados da inversão.

    As principais operações realizadas pelo script são:
      - Leitura dos parâmetros do programa a partir do arquivo
          "Input/prog_param_M1.dat", que define diversos parâmetros para o script.
      - Carregamento dos dados de entrada:
            * Dados do perfil magnético filtrado ("TFA_r_filt" e "AMA_r_filt").
            * Parâmetros dos prismas .
      - Leitura de arquivos de saída contendo resultados do modelo:
            * Dados FDA .
            * Arquivos calculados.
            * Arquivos de saída do modelo.
            * Dados iniciais.
      - Chamada da função "plot_res_R" para a geração da visualização dos resultados.

USO:
    Execute o script utilizando Python 3. Exemplo:
        python 6_PyDyke_plot.py
======================================================================
"""

# Area de ajustes ====================================================
f_name = 'M1'
f_name2 = '0.07'  # sufixo referente aos arquivos obtidos por inversao
# Area de ajustes ====================================================

param_file = open(f'Input/prog_param_{f_name}.dat')


prog_param = np.genfromtxt(param_file, dtype='str',
                           delimiter=' ', skip_header=0)

Fh = int(prog_param[3])

index = prog_param[0]
index2 = prog_param[1]

FDA_path = f"FDA_{index}_{f_name2}.dat"

df = pd.read_csv("Input/"+index+".csv")

X = df['dist'].to_numpy()
T = df['TFA_r_filt'].to_numpy()
B = df['AMA_r_filt'].to_numpy()

df2 = pd.read_csv("Input/"+index2+".txt", sep=' ')

df3 = df2[["A0", "im", "x0", "z0"]]

arq_FDA = open("Output/"+FDA_path)
FDA_vals = np.loadtxt(arq_FDA, skiprows=1)
dens = len(df3.A0)/(X[-1]/1000)
dens = float("{:.2f}".format(dens))
print(dens)

dx = len(X)

arq3 = open('Output/calculado_I_'+index+'_'+str(dens)+'.dat')
calc = np.loadtxt(arq3, skiprows=1)
arq4 = open('Output/exitmod_I_'+index+'_'+str(dens)+'.dat')
model = np.loadtxt(arq4, skiprows=1)

not_simple = 0
try:
    arq5 = open('Output/exitmod_I_'+index+'SM_'+str(dens)+'.dat')
    simple_model = np.loadtxt(arq5, skiprows=1)
except IOError:
    not_simple = 1

arq6 = open('Output/'+index+'_initial_'+str(dens)+'.dat')
calc0 = np.loadtxt(arq6, skiprows=1)
arq7 = open('Output/calculado_fc1_'+index+'_'+str(dens)+'.dat')
calc1 = np.loadtxt(arq7, skiprows=1)


prism = sum(1 for line in open('Output/exitmod_I_'+index +
            '_'+str(dens)+'.dat'))  # Count lines from txt
prism -= 1  # remove header count

if prism == 1:
    model = np.reshape(model, (1, 4))

lp = np.zeros(len(df2.A0)*2)
j = 0
for i in range(0, len(lp), 2):
    lp[i] = df2.xi[j]
    lp[i+1] = df2.xf[j]
    j += 1

if prog_param[12] != 'r':
    sint_path = "Input/"+prog_param[12]
    print(sint_path)
else:
    sint_path = None

plot_res(X, T, B, calc[:, 0], calc0[:, 1], calc0[:, 0], calc1[:, 1],
         model, prism, lp, FDA_vals, Fh, sint_path, initial=df3, euler=None)

arq3.close()
arq4.close()

if not_simple == 0:
    arq5.close()
