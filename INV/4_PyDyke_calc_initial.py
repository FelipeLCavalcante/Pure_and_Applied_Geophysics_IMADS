#!/usr/bin/env python3

import numpy as np
import pandas as pd

from func_dique import dique

"""
======================================================================
Nome do Script: 4_PyDyke_calc_initial.py
Autor: Felipe Lisbona Cavalcante
Data: 27/02/2025
Versão: 1.0
======================================================================
DESCRIÇÃO:
    Este script calcula o problema direto com base nos parâmetros da solução
    inicial.
    A função principal, calc_initial, realiza as seguintes operações:
      - Lê os dados do perfil magnético a partir do arquivo
          "Input/fwd_r_M1_cut.csv" (contendo a coluna "dist");
      - Lê os limites e os parâmetros dos prismas a partir do arquivo
          "Input/lims_M1.txt" (os quais incluem as colunas "A0", "im", "x0" e "z0");
      - Ajusta a profundidade dos prismas adicionando a altura de voo (Fh);
      - Calcula a densidade dos prismas com base na extensão do perfil;
      - Extrai os parâmetros relevantes dos prismas e os converte em um array,
      - Chama a função externa "dique" para calcular os componentes do campo:
            * Tx, Tz e Tt (com Tt correspondendo ao campo anômalo, TFA);
      - Calcula o módulo do campo (AMA) a partir de Tx e Tz;
      - Salva os resultados (TFA e AMA) em um arquivo de saída cujo nome incorpora
        a densidade dos prismas.

VARIÁVEIS PRINCIPAIS:
    index      : Identificador do modelo (ex.: 'M1')

USO:
    Execute o script utilizando Python 3:
        python 4_PyDyke_calc_initial.py

SAÍDAS:
    - Output/fwd_r_M1_cut_initial_{dens}.dat : Arquivo de saída contendo os valores
      calculados para o campo anômalo (TFA, nT) e o módulo do campo (AMA, nT).
======================================================================
"""

# Area de ajustes ====================================================
f_name = 'M1'
# Area de ajustes ====================================================

file_path = f"Input/fwd_r_{f_name}_cut.csv"
index = f"fwd_r_{f_name}_cut"
file_path2 = f"Input/lims_{f_name}.txt"


def calc_initial(I, alpha, Fh):
    # Initial parameters ---------------------------------------------------
    df = pd.read_csv(file_path)
    X = df['dist'].to_numpy()

    df2 = pd.read_csv(file_path2, sep=' ')
    df2.z0 = df2.z0 + Fh
    dens = len(df2.xi)/(X[-1]/1000)
    dens = float("{:.2f}".format(dens))

    df3 = df2[["A0", "im", "x0", "z0"]]
    model = df3.to_numpy()

    prism = len(model[:, 0])

    pp = model.reshape(prism*4, 1)
    components = dique(pp, X, I, alpha, prism)

    Tx = components[:, 0]
    Tz = components[:, 1]
    Tt = components[:, 2]

    B = np.sqrt(Tx**2+Tz**2)

    exit_data = np.c_[Tt, B]

    header_calc = "TFA (nT) AMA (nT)"
    np.savetxt('Output/'+index+'_initial_'+str(dens)+'.dat',
               exit_data, header=header_calc, comments='')


if __name__ == "__main__":

    param_file = open(f'Input/prog_param_{f_name}.dat')

    prog_param = np.genfromtxt(
        param_file, dtype='str', delimiter=' ', skip_header=0)

    strk = -(int(prog_param[9]) - 180)
    alpha = strk - float(prog_param[5])
    calc_initial(float(prog_param[4]), alpha, int(prog_param[3]))

    param_file.close()
