#!/usr/bin/env python3

import pandas as pd
import numpy as np

"""
======================================================================
Nome do Script: 7_PyDyke_STD.py
Autor: Felipe Lisbona Cavalcante
Data: 27/02/2025
Versão: 1.0
======================================================================
DESCRIÇÃO:
    Este script calcula os desvios padrão dos parâmetros A0, im, x0 e z0 para cada prisma.
    
    As etapas realizadas são:
      - Leitura dos dados do arquivo "solucoes_I_fwd_r_{f_name}.dat"
      - Cálculo, para cada prisma, do desvio padrão dos parâmetros 'A0', 'im', 'x0' e 'z0'
        utilizando o método std() do Pandas.
      
USO:
    Defina a variável f_name (ex.: f_name = 'M1') e execute o script com Python 3:
        python 7_PyDyke_STD.py

SAÍDAS:
    - Output/STD_fwd_r_{f_name}.dat : Arquivo CSV contendo os desvios padrão de cada 
      parâmetro para cada prisma, organizados nas colunas:
          'prism', 'std_A0', 'std_im', 'std_x0' e 'std_z0'.
======================================================================
"""

# Area de ajustes ====================================================
f_name = 'M1_cut_0.07'
# Area de ajustes ====================================================

sols_path = f'Output/solucoes_I_fwd_r_{f_name}.dat'
save_path = f'Output/STD_fwd_r_{f_name}.dat'

df = pd.read_csv(sols_path, sep=' ')

df = df.astype({'prism': 'int'})

# gera dataframe para desvios
feature_list = ['prism', 'std_A0', 'std_im', 'std_x0', 'std_z0']
df2 = pd.DataFrame(0, index=np.arange(np.max(df.prism)), columns=feature_list)
df2.prism = np.arange(1, np.max(df.prism)+1)

# preenche dataframe com desvios por prisma
for i in range(1, np.max(df.prism)+1):
    df2.std_A0[i-1] = df.loc[df['prism'] == i]['A0'].std()
    df2.std_im[i-1] = df.loc[df['prism'] == i]['im'].std()
    df2.std_x0[i-1] = df.loc[df['prism'] == i]['x0'].std()
    df2.std_z0[i-1] = df.loc[df['prism'] == i]['z0'].std()

df2.to_csv(save_path, index=None)
