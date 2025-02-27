#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
======================================================================
Nome do Script: 2_PyDyke_cut_data.py
Autor: Felipe Lisbona Cavalcante
Data: 27/02/2025
Versão: 1.0
======================================================================
DESCRIÇÃO:
    Este script realiza o corte e a decimação de dados provenientes do 
    arquivo contendo os resultados de campo anômalo com ruído.
    
    As principais operações realizadas são:
      - Leitura do arquivo de dados com os resultados do modelo.
      - Seleção (corte) dos dados cujo valor da distância ("dist") esteja 
        entre um limite inferior (prof_ini) e um limite superior (prof_end).
      - Decimação dos dados (redução de amostras) utilizando um fator de 
        decimação definido (dec).
      - Salvamento dos dados decimados em um novo arquivo CSV.
      - Plotagem dos dados cortados (linha preta) e dos dados decimados (linha azul)
        para visualização comparativa.

VARIÁVEIS PRINCIPAIS:
    index      : Identificador do modelo (ex.: 'M1')
    prof_ini   : Limite inferior do corte (em metros)
    prof_end   : Limite superior do corte (em metros)
    dd         : Discretização (em metros)
    dec        : Fator de decimação
        
USO:
    Execute o script com Python 3. Por exemplo:
        python 2_PyDyke_cut_data.py

SAÍDAS GERADAS:
    - Um arquivo CSV contendo os dados decimados (save_path).
    - Um gráfico comparativo dos dados originais cortados e dos dados decimados.

======================================================================
"""

# Area de ajustes ====================================================
index = 'M1'

prof_ini = 0
prof_end = 30000
dec = 10
# Area de ajustes ====================================================

data_path = f'Output/fwd_r_{index}.dat'
save_path = f'Output/fwd_r_{index}_cut.dat'

df_data = pd.read_csv(data_path, sep=' ')
df_cut = df_data.query(f"dist >= {prof_ini} and dist <= {prof_end}")

idx = np.arange(0, len(df_cut['dist']), dec)
df_dec = df_cut.iloc[idx]

df_dec.to_csv(save_path, index=False)

plt.plot(df_cut.dist, df_cut.AMA_r, '-k')
plt.plot(df_dec.dist, df_dec.AMA_r, '-b')
plt.xlabel('Distance (m)')
plt.ylabel('AMA (nT)')
plt.legend(['original', 'noised'])
plt.show()
