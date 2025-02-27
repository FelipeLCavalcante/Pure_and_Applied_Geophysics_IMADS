#!/usr/bin/python3

import numpy as np
import multiprocessing as mp

from func_Inv import inv

"""
======================================================================
Nome do Script: 5R_PyDyke_inv.py
Autor: Felipe Lisbona Cavalcante
Data: 27/02/2025
Versão: 1.0
======================================================================
DESCRIÇÃO:
    Este script calcula o problema inverso.

    A execução do script depende da leitura de um arquivo de parâmetros
    (prog_param_{index}.dat) contendo os seguintes parâmetros:
      - index: Identificador do arquivo de dados 
      - index2: Identificador do arquivo de limites 
      - first_solution: Indicador de primeira solução
      - Fh: Altura de voo (m) 
      - I: Inclinação do campo geomagnético local (°)
      - D: Declinação do campo gemognético local (°) 
      - F: Intensidade do campo magnético local (nT)
      - Kmid: Susceptibilidade magnética 
      - Tk_max: Espessura máxima dos diques (m) 
      - strk: Strike da lâmina (ajustado para referência do modelo) 
      - aj: Resíduo limite para etapa 1 da inversão 
      - aj2: Resíduo limite para etapa 2 da inversão (Não implementado !!)
      - type: Tipo de problema inverso (r: real, nome do arquivo de parâmetros: sintético )

USO:
    Execute o script utilizando Python 3:
        python 5R_PyDyke_inv.py

SAÍDAS:
    - calculado_fc1*.dat: Arquivo contendo a resposta da etapa 1 da inversão
    - calculado_I*.dat: Arquivo contendo a resposta da final da inversão
    - exitmod_I_*.dat: Arquivo contendo o modelo final da inversão
    - FDA_*.dat: Arquivo contendo a função de distribuição acumulada dos intervalos
    - solucoes_I_*.dat: Arquivo contendo as soluções de todas as rodadas da inversão

OBSERVACOES:
    A função func_inv.py contém uma área de ajustes específicos para a inversão que podem ser modificados:
    
    rounds:     Quantidade de rodadas da inversão
    init_sol:   Quantidade de soluções iniciais
    inv_type:   Seleção de algoritmo de minimização - 1:  minimização gradiente, 2: minimização global
======================================================================
"""

if __name__ == "__main__":

    # Area de ajustes ====================================================
    index = 'M1'
    param_file = open(f'Input/prog_param_{index}.dat')
    # Area de ajustes ====================================================
    prog_param = np.genfromtxt(
        param_file, dtype='str', delimiter=' ', skip_header=0)

    inv(prog_param[0], prog_param[1], prog_param[2], int(prog_param[3]),
        float(prog_param[4]), float(prog_param[5]), float(
        prog_param[6]), float(prog_param[7]),
        int(prog_param[8]), int(prog_param[9]), int(prog_param[10]), int(prog_param[11]))

    param_file.close()
