#!/usr/bin/env python3

import numpy as np
import pandas as pd

"""
======================================================================
Nome do Script: 2_PyDyke_d2T.py
Autor: Felipe Lisbona Cavalcante
Data: 27/02/2025
Versão: 1.0
======================================================================
DESCRIÇÃO:
    Este script calcula a segunda derivada (aproximada) de dois sinais presentes 
    em um arquivo CSV, utilizando uma aproximação central. Os sinais processados 
    são "AMA_r" e "AMA_r_filt", que representam a AMA (original e filtrada).

    O processamento envolve:
      - Leitura dos dados do arquivo CSV (Input/fwd_r_M1_cut.csv) contendo as 
        colunas "dist", "AMA_r" e "AMA_r_filt".
      - Preparação dos vetores de dados (com "padding" nas bordas) para reduzir 
      artefatos de borda.
      - Cálculo da segunda derivada usando a fórmula:
            d²y/dx² ≈ (y[i+1] - 2*y[i] + y[i-1]) / dx²
      - Adição dos resultados como novas colunas no DataFrame:
            * "d2x": posições associadas (excetuando as bordas)
            * "d2y_AMA_r": segunda derivada do sinal "AMA_r"
            * "d2y_AMA_r_filt": segunda derivada do sinal "AMA_r_filt"
      - Salvamento do DataFrame atualizado no mesmo arquivo CSV de entrada.

VARIÁVEIS PRINCIPAIS:
    index      : Identificador do modelo (ex.: 'M1')
    dd         : Discretização (em metros)

USO:
    Execute o script com Python 3. Exemplo:
        python 2_PyDyke_d2T.py

SAÍDAS:
    - Atualização do arquivo CSV de entrada, que passará a conter as colunas:
          "d2x", "d2y_AMA_r" e "d2y_AMA_r_filt", correspondentes às posições e 
          às segundas derivadas dos sinais.
======================================================================
"""


def derivative(x, y, dd):
    d2y = np.zeros(len(y)-2)
    d2x = np.zeros(len(y)-2)

    j = 1
    for i in range(len(d2y)):
        d2y[i] = (y[j+1] - 2*y[j] + y[j-1])/dd**2
        d2x[i] = x[j]
        j += 1

    return d2x, d2y


# Area de ajustes ====================================================
index = 'M1'

dd = 50
# Area de ajustes ====================================================

file_path = f"Input/fwd_r_{index}_cut.csv"

df = pd.read_csv(file_path)

data_head = "AMA_r"

y = np.zeros(len(df[data_head])+2)
x = np.zeros_like(y)
aux_y = df[data_head].to_numpy()
aux_x = df["dist"].to_numpy()

y[0] = aux_y[0]
y[-1] = aux_y[-1]
x[0] = aux_x[0]
x[-1] = aux_x[-1]
y[1:-1] = aux_y
x[1:-1] = aux_x

d2x, d2y = derivative(x, y, dd)

df["d2x"] = d2x
df["d2y_AMA_r"] = d2y

data_head = "AMA_r_filt"
aux_y = df[data_head].to_numpy()

y[0] = aux_y[0]
y[-1] = aux_y[-1]
y[1:-1] = aux_y

d2x, d2y = derivative(x, y, dd)

df["d2y_AMA_r_filt"] = d2y

df.to_csv(file_path, index=False)
