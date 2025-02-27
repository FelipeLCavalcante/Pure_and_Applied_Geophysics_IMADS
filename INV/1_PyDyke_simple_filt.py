#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

"""
======================================================================
Nome do Script: 1_PyDyke_simple_filt.py
Autor: Felipe Lisbona Cavalcante
Data: 27/02/2025
Versão: 1.0
======================================================================
DESCRIÇÃO:
    Este script aplica um filtro passa-baixa do tipo Butterworth aos dados. 
    O filtro é utilizado para suavizar os sinais "AMA_r" e "TFA_r".

    As etapas do processamento incluem:
      - Definição de uma função (butter_lowpass_filter) que aplica o filtro passa‐baixa,
        utilizando as funções "butter" e "filtfilt" da biblioteca SciPy.
      - Leitura dos dados de um arquivo (Input/fwd_r_M1_cut.dat) via Pandas.
      - Conversão das colunas relevantes ("AMA_r", "TFA_r" e "dist") para arrays NumPy.
      - Cálculo dos parâmetros do filtro, como a frequência de corte (f_cut) e 
        a frequência de Nyquist (nyq), com base no intervalo de amostragem (dd).
      - Aplicação do filtro aos sinais "AMA_r" e "TFA_r", gerando "AMA_r_filtered" 
        e "TFA_r_filtered".
      - Armazenamento dos sinais filtrados em novas colunas do DataFrame e salvamento 
        dos resultados em um arquivo CSV.
      - Geração de gráficos comparando os sinais originais e filtrados, apresentados em 
        dois subplots (um para cada sinal).

VARIÁVEIS PRINCIPAIS:
    index      : Identificador do modelo (ex.: 'M1')
    dd         : Discretização (em metros)
    freq_val   : Frequência de referência do filtro (em Hz)
    order      : Ordem do filtro

USO:
    Execute o script com Python 3. Exemplo:
        python 1_PyDyke_simple_filt.py

SAÍDAS GERADAS:
    - Um arquivo CSV contendo os dados originais e os sinais filtrados.
    - Uma figura com dois subplots comparando os sinais "AMA_r" e "TFA_r" 
      antes e depois da aplicação do filtro.

======================================================================
"""


def butter_lowpass_filter(data, cutoff, order):
    # normal_cutoff = cutoff / nyq
    # Get the filter coefficients
    # b, a = butter(order, normal_cutoff, btype='low', analog=False)
    b, a = butter(order, cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y


# Area de ajustes ====================================================
index = 'M1'

dd = 50

order = 2
freq_val = 0.00165
# Area de ajustes ====================================================

input_path = f"Input/fwd_r_{index}_cut.dat"
output_path = f"Input/fwd_r_{index}_cut.csv"

nyq = 1/(2*dd)
print(nyq)

f_cut = freq_val/(nyq/2)


df = pd.read_csv(input_path)

AMA_r = df.AMA_r.to_numpy()
dist = df.dist.to_numpy()
TFA_r = df.TFA_r.to_numpy()


AMA_r_filtered = butter_lowpass_filter(AMA_r, f_cut, order)
TFA_r_filtered = butter_lowpass_filter(TFA_r, f_cut, order)

df["AMA_r_filt"] = AMA_r_filtered
df["TFA_r_filt"] = TFA_r_filtered

df.to_csv(output_path, index=False)
np.set_printoptions(precision=4)

fig, (ax, ax2) = plt.subplots(2, 1, figsize=[8, 8])
ax.plot(dist, AMA_r, 'k-', linewidth=1, label='not filtered')
ax.plot(dist, AMA_r_filtered, 'r-', linewidth=1, label='filtered')
ax.set_ylabel("AMA_r (nT)")
ax.grid()
ax.legend()

ax2.plot(dist, TFA_r, 'k-', linewidth=1, label='not filtered')
ax2.plot(dist, TFA_r_filtered, 'r-', linewidth=1, label='filtered')
ax2.set_ylabel("TFA_r (nT)")
ax2.set_xlabel('distance [m]')
ax2.grid()
ax2.legend()
plt.show()
