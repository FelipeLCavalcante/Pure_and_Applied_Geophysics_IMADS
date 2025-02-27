#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

import random
from func_dique import dique
from func_tabularS import tabularS

from scipy.signal import hilbert

"""
======================================================================
Nome do Script: 1_PyDyke_Extent_n_Disturb.py
Autor: Felipe Lisbona Cavalcante
Data: 27/02/2025
Versão: 1.0
======================================================================
DESCRIÇÃO:
    Este script calcula o problema direto para um modelo 2D de prismas. 
    Ele permite calcular os componentes do campo anômalo (Tx e Tz) assim 
    como a anomalia de campo total (TFA), a amplitude da anomalia 
    magnética (AMA) e a amplitude do sinal analítico (ASA). Além disso,
    ele extende o perfil para adicionar ruído de modo que os componentes
    possam ser calculados via transformada de Fourier. 
    
    As principais etapas do script são:
      - Leitura de modelo pré-existente.
      - Criação de modelo de prismas.
      - Cálculos das componentes do campo anômalo:
           * Geração do perfil (array X) com base na extensão e discretização.
           * Cálculo dos componentes magnéticos (Tx, Tz) e TFA (Tt)através de uma
             função externa "dique".
           * Cálculo da AMA (B) e inclusão de ruído (modelo noised).
           * Aplicação da Transformada de Fourier e de Hilbert para obter
             derivadas e reconstruir componentes (Tx_r, Tz_r).
      - Geração de arquivos de saída (em formato .dat e .csv) contendo:
           * Componentes do campo (original e reconstruído).
           * Valores de ASA (original e com ruído).
           * Resultados finais dos campos (TFA, AMA).
           * Dados de ruído e parâmetros dos prismas.
      - Plotagem de figuras para comparar os resultados do modelo original com os 
        resultados com ruído.

USO:
    Execute o script com Python 3. Exemplo:
        python 1_PyDyke_Extent_n_Disturb.py

    Os resultados serão salvos no diretório "Output" com nomes que incluem o 
    índice do modelo (ex.: "M1").


VARIÁVEIS PRINCIPAIS:
    index      : Identificador do modelo (ex.: 'M1')
    Fh         : Altura de voo (Flight Height)
    dd         : Discretização (em metros)
    I          : Inclinação do campo geomagnético local
    D          : Declinação do campo gemognético local
    F          : Intensidade do campo magnético local
    strk       : Strike da lâmina (ajustado para referência do modelo)
    alpha      : Ângulo de referência a partir do Norte magnético
    extent     : Valor da extensão do perfil (km)
    prof_end   : Extensão original do perfil (km)
    imp_mod    : Controle de importação do modelo (1 para importar; 2 para gerar)
    ns_control : Controle de ruído (1 para valor fixo; 2 para porcentagem)
    ns_nT      : Valor fixo de ruído (nT)
    ns_perc    : Porcentagem de ruído (ex.: 0.02 = 2%)
    
SAÍDAS GERADAS:
    - Output/components_M1.dat : Componentes do campo [Tx, Tz, Tx_r, Tz_r]
    - Output/ASA_M1.dat        : Valores ASA (original e com ruído)
    - Output/fwd_M1.dat        : Resultados dos campos [distância, TFA, AMA]
    - Output/fwd_r_M1.dat      : Resultados do campos com ruído [distância, TFA_r, AMA_r]
    - Output/noise_M1.dat      : Valores do ruído aplicado
    - Output/parametros_M1.dat : Parâmetros do modelo

======================================================================
"""
# Area de ajustes ====================================================
index = 'M1'

Fh = 100
dd = 5

I = -30
D = 0
F = 25986

strk = 145
strk = -(strk-180)

alpha = strk - D

extent = 300
prof_end = 30

imp_mod = 2
ns_control = 1

ns_nT = 1
ns_perc = 0.02

# Modelo ------------------------------------------------------------
if imp_mod == 1:
    arq = open("Input/parametros_M1.dat")
    p = np.loadtxt(arq, skiprows=1)
elif imp_mod == 2:
    p = np.array([[2*50, 30, 10000, 50],
                  [2*50, -30, 20000, 150]])
# Modelo ------------------------------------------------------------
# Area de ajustes ====================================================

X = np.array(range(-extent*1000, (prof_end+extent)*1000, dd))

p[:, 3] = p[:, 3] + Fh
ind = np.argsort(p[:, 2])
p = p[ind, :]
samples = len(p[:, 0])
pp = p.reshape(samples*4, 1)

components = dique(pp, X, dd, I, alpha, samples)

Tx = components[:, 0]
Tz = components[:, 1]
Tt = components[:, 2]

B = np.sqrt(Tx**2+Tz**2)

if ns_control == 1:
    ns = ns_nT
elif ns_control == 2:
    nsp = ns_perc
    ns = int(max(B))*nsp

r = np.random.uniform(-ns, ns, len(Tx))

Tt_r = Tt + r

T_dx = np.gradient(Tt, X)
T_dz = np.imag(hilbert(T_dx, 2*len(T_dx)))
T_dz = T_dz[0:len(T_dx)]
ASA = np.sqrt(T_dx**2 + T_dz**2)

Tr_dx = np.gradient(Tt_r, X)
Tr_dz = np.imag(hilbert(Tr_dx, 2*len(Tr_dx)))
Tr_dz = Tr_dz[0:len(Tr_dx)]
ASA_r = np.sqrt(Tr_dx**2 + Tr_dz**2)

# data padding
data_pad = np.zeros(len(Tx)+20)
data_pad[10:-10] = Tt_r

# wavenumber
Tt_fft = np.fft.fft(data_pad)
Kx = 2*np.pi*np.fft.fftfreq(Tt_fft.shape[0], dd)
K = np.sqrt(Kx**2)

# directional cosines and sines
I_rad = I*np.pi/180
D_rad = D*np.pi/180
L = np.cos(I_rad)*np.cos(D_rad)
N = np.sin(I_rad)
# component Tx

theta_x = (1j*Kx)/(N*K+1j*L*Kx)
theta_x[np.argwhere(np.isnan(theta_x))] = 0
Tx_r_pad_fft = Tt_fft*theta_x
Tx_r_pad = np.fft.ifft(Tx_r_pad_fft)
Tx_r = np.real(Tx_r_pad[10:-10])

# component Tz
theta_z = K/(N*K+1j*L*Kx)
theta_z[np.argwhere(np.isnan(theta_z))] = 0
Tz_r_pad_fft = Tt_fft*theta_z
Tz_r_pad = np.fft.ifft(Tz_r_pad_fft)
Tz_r = np.real(Tz_r_pad[10:-10])

B_r = np.sqrt(Tx_r**2+Tz_r**2)

components = np.c_[Tx, Tz, Tx_r, Tz_r]
data_ASA = np.c_[ASA, ASA_r]

results = np.array(np.column_stack((X, Tt, B)))
results_r = np.array(np.column_stack((X, Tt_r, B_r)))

for i in range(samples):
    p[i, 3] = p[i, 3] - Fh  # Zero to surface

header_comp = "Tx Tz Tx_r Tz_r"
header_par = "a im x0 z0"
header_ASA = "ASA ASA_r"
header_res = "dist TFA AMA"
header_res_r = "dist TFA_r AMA_r"
np.savetxt(f'Output/components_{index}.dat',
           components, header=header_comp, comments='')
np.savetxt(f'Output/ASA_{index}.dat', data_ASA,
           header=header_ASA, comments='')
np.savetxt(f'Output/fwd_{index}.dat', results, header=header_res, comments='')
np.savetxt(f'Output/fwd_r_{index}.dat', results_r,
           header=header_res_r, comments='')
np.savetxt(f'Output/noise_{index}.dat', r, header="noise (nT)", comments='')
np.savetxt(f'Output/parametros_{index}.dat',
           p, header=header_par, comments='')

# PLOTAGEM---------------------------------------------------
# AMA
plt.figure(1)
plt.plot(X, B, '-k', X, B_r, '-b')
plt.xlabel('Distance (m)')
plt.ylabel('AMA (nT)')
plt.title('Comparacao AMA')
plt.legend(['original', 'noised'])

# ASA
plt.figure(2)
plt.plot(X, ASA, '-k', ASA_r, B_r, '-b')
plt.xlabel('Distance (m)')
plt.ylabel('ASA (nT/m)')
plt.title('Comparacao ASA')
plt.legend(['original', 'noised'])

# Componentes
plt.figure(3)
plt.plot(X, Tx, label="Tx")
plt.plot(X, Tz, label="Tz")
plt.plot(X, Tt, label="Tt")
plt.title('Componentes do campo anomalo - Modelo de Prismas')
plt.xlabel('Posicao (m)')
plt.ylabel('nT')
plt.legend()

# Ruido
plt.figure(4)
plt.plot(X, r)
plt.title('Ruido')
plt.xlabel('Posicao (m)')
plt.ylabel('nT')

# Campo Anomalo e Modulo
f, axarr = plt.subplots(2, sharex=True)
axarr[0].plot(X, Tt, '-k', label='TFA')
axarr[0].set_xlim([X[0], X[-1]])
axarr[0].set_title('Campos Calculados pelo Modelo de prismas')
axarr[0].set_ylabel('TFA (nT)')

legend = axarr[0].legend()
axarr[1].plot(X, B, '-k', label='AMA')

axarr[1].set_xlim([X[0], X[-1]])
axarr[1].set_xlabel('Posicao(m)')
axarr[1].set_ylabel('AMA (nT)')
legend = axarr[1].legend()

# Prismas
tabularS(X, dd, p, samples, index)
