#!/usr/bin/env python3

import pandas as pd
import numpy as np

"""
======================================================================
Nome do Script: 8_PyDyke_join_exit_std.py
Autor: Felipe Lisbona Cavalcante
Data: 27/02/2025
Versão: 1.0
======================================================================
DESCRIÇÃO:
    Este script integra e organiza os dados de saída do modelo de prismas para gerar 
    uma tabela resumida (formato CSV) contendo parâmetros calculados e seus respectivos desvios. 

    O processamento realiza as seguintes etapas:
      - Leitura de três arquivos de entrada:
            * "Output/exitmod_I_fwd_r_M1_cut_0.07.dat": contém os parâmetros do modelo 
              (ex.: A0, im, x0, z0) calculados para cada prisma.
            * "Output/STD_fwd_r_M1_cut_0.07.dat": contém os desvios padrão dos parâmetros 
              para cada prisma.
            * "Input/lims_M1.txt": contém limites e delta e P.
      - Criação de um DataFrame com as colunas:
            ['prism', 'delta', 'P', 'A0', 'std_A0', 'im', 'std_im', 'x0', 'std_x0', 'z0', 'std_z0'].

USO:
    Execute o script utilizando Python 3. Exemplo:
        python 8_PyDyke_join_exit_std.py

SAÍDAS:
    - Output/TAB_fwd_r_M1.csv : Tabela consolidada com os parâmetros e desvios padrão para 
      cada prisma, contendo as colunas: prism, delta, P, A0, std_A0, im, std_im, x0, 
      std_x0, z0, std_z0.
======================================================================
"""

# Area de ajustes ====================================================
f_name = 'M1_cut_0.07'
f_name2 = 'M1'
# Area de ajustes ====================================================

exit_path = f'Output/exitmod_I_fwd_r_{f_name}.dat'
std_path = f'Output/STD_fwd_r_{f_name}.dat'
lim_path = f'Input/lims_{f_name2}.txt'

save_path = f'Output/TAB_fwd_r_{f_name2}.csv'

df = pd.read_csv(exit_path, sep=' ')
df2 = pd.read_csv(std_path)
df3 = pd.read_csv(lim_path, sep=' ')

feature_list = ['prism', 'delta', 'P', 'A0', 'std_A0',
                'im', 'std_im', 'x0', 'std_x0', 'z0', 'std_z0']
df4 = pd.DataFrame(0, index=np.arange(np.max(df2.prism)), columns=feature_list)

df4.prism = df2.prism
df4.delta = df3.delta
df4.P = df3.P
df4.A0 = df.A0
df4.std_A0 = df2.std_A0
df4.im = df.im
df4.std_im = df2.std_im
df4.x0 = df.x0
df4.std_x0 = df2.std_x0
df4.z0 = df.z0
df4.std_z0 = df2.std_z0

df4 = df4.astype('int')
df4.to_csv(save_path, index=None)
