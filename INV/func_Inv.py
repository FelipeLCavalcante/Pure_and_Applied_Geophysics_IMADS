#!/usr/bin/env python3

# Inver calcula o problema inverso

import numpy as np
import multiprocessing as mp
import time
import sys
import pandas as pd
import logging

from random import random
from math import atan2
from math import e

from func_fwd import fwd
from func_minimiza import minimiza
from func_vec2mat import vec2mat
from scipy import optimize
from func_fobj import fobj


def inv(index, index2, first, Fh, I, D, F, Kmid, Tk_max, strk, aj, aj2):

    logging.basicConfig(filename='Output/'+index+'.log', filemode='w',
                        format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# Area de ajustes ====================================================
    rounds = 10  # 5
    init_sol = 10  # 10
    inv_type = 2  # 1: minimização gradiente, 2: minimização global
# Area de ajustes ====================================================

# Leitura de dados -----------------------------------------------------------
    df = pd.read_csv("Input/"+index+".csv")
    df2 = pd.read_csv("Input/"+index2+".txt", sep=' ')
    df2.z0 = df2.z0 + Fh
# Reorganize ------------------------------------------------------------------
    X = df['dist'].to_numpy()
    T = df['TFA_r_filt'].to_numpy()
    B = df['AMA_r_filt'].to_numpy()
    dens = len(df2.xi)/(X[-1]/1000)
    dens = float("{:.2f}".format(dens))
# Alpha calculation -----------------------------------------------------------
    strk = -(strk - 180)
    alpha = strk - D
# Dyke Magnetic Properties ---------------------------------------------------
    Kmax = Kmid*10

    # u0 = 4*np.pi*1e-7  # (N/A²)
    u0 = 1.2566*1e3  # (nT.m/A)
    Q = 4  # Koenigsberger ratio
    M_max = (1+Q)*Kmax*F/u0
    Mt_max = M_max*Tk_max
# Limites do modelo ----------------------------------------------------------
    if first == 'N' or first == 'n':

        prism = int(round((X[-1]/1000)*dens))

        lp = np.zeros(len(df2.xi)*2)
        j = 0
        for i in range(0, len(lp), 2):
            lp[i] = df2.xi[j]
            lp[i+1] = df2.xf[j]
            j += 1

        logging.info('\nprism: '+str(prism))

        C = np.array([0, -180, 0, Fh])  # Mt,inc,X0,Z0; inc = 90 invariance
        lb = np.array((C[0], C[1], C[2], C[3])*prism)
        D = np.array([Mt_max, 180, X[-1], 500])  # Mt,inc,X0,Z0; z0 = RAS_max
        ub = np.array((D[0], D[1], D[2], D[3])*prism)

        for i in range(prism):  # Xo limits
            lb[2+4*i] = df2.xi[i]
            ub[2+4*i] = df2.xf[i]
            if ~np.isnan(df2.z0[i]):  # limite aberto caso NaN na solucao inicial
                if df2.z0[i]*0.5 > Fh:
                    lb[3+4*i] = df2.z0[i]*0.5  # limits for z0
                ub[3+4*i] = df2.z0[i]*2

            if ~np.isnan(df2.A0[i]):  # limite aberto caso NaN na solucao inicial
                lb[0+4*i] = df2.A0[i]*0.5  # limits for A0
                ub[0+4*i] = df2.A0[i]*2

    else:
        dens = float(input("Original Density (prism/km):"))
        aux_lp = int(round((X[-1]/1000)*dens))
        lp = float((X[-1]-X[0])/aux_lp)

        arq_sol = open('Output/exitmod_I'+index+'SM_'+str(dens)+'.dat')
        sol_lim = np.loadtxt(arq_sol)
        sol_lim[:, 3] = sol_lim[:, 3] + Fh  # add flight high from saved data

        prism = len(sol_lim[:, 0])
        sol_lim = sol_lim.reshape(4*len(sol_lim[:, 0]))

        ub = sol_lim*1.1
        lb = sol_lim*0.9

    mybounds = list(zip(lb, ub))
    mybounds_init = mybounds

# Inversion - First Step -----------------------------------------------------
    aux1 = np.array(range(1, prism+1))  # VERIF QTDE ELEMENTOS

    error1 = 0

    for cont1 in range(rounds):  # Rounds of inversion
        flag = 1
        pass1 = 0

        count_quit = 0  # Max interations counter

        while pass1 == 0:  # Epsilon control
            start = time.time()

            if inv_type == 1:
                kick = np.random.uniform(lb, ub, len(lb))
                data = [(kick, mybounds, X, T, B, flag, prism, alpha, I)
                        for k in range(init_sol)]

                pool = mp.Pool()
                res = pool.starmap(minimiza, data)  # parallel minimization
                pool.close()
                pool.join()

                new_list = [item[1] for item in res]  # get fobj values
                # index for best model, minor fobj value
                indice = new_list.index(min(new_list))

                prism_mod = res[indice][0]  # best model
                fopt = res[indice][1]  # adjust for best model

            elif inv_type == 2:
                res = optimize.differential_evolution(func=fobj, bounds=mybounds, args=(T, B, flag, X,
                                                                                        prism, alpha, I), disp=False, workers=-1)

                fopt = res['fun']
                mod = res['x']

            logging.info('\ninteration: '+str(count_quit)
                         + '\nStep 1 adjust: %.2f' % fopt + ' aj: %.2f' % aj)

            if fopt <= aj:  # Check epsilon criteria
                if inv_type == 1:
                    new_lim = res[indice][0]  # best model
                    prism_mod = vec2mat(new_lim, prism)
                elif inv_type == 2:
                    new_lim = mod  # best model
                    prism_mod = vec2mat(mod, prism)
                pass1 = 1
                error1 = fopt
                count_quit = 0
            else:  # Reject model and quit program display
                pass1 = 0
                end = time.time()
                logging.info('\nBad Model'
                             + '\nElapsed time: %.2f' % ((end - start)/3600)+'h\n'
                             + "------------------------------------------------------")
                count_quit += 1
                if count_quit == 200:
                    logging.info(
                        '\nProgram ended by reach the maximum interations !!!')
                    sys.exit()
        fc1 = fwd(prism_mod, X, prism, alpha, I)
        # Inversion - Step 2 ---------------------------------------------------------
        lb = new_lim
        ub = new_lim

        ub = ub + ub*0.0001

        for cont2 in range(1, 4*prism, 4):  # Free the bounds to Inc
            lb[cont2] = -180
            ub[cont2] = 180
        flag = 2

        mybounds = list(zip(lb, ub))

        if inv_type == 1:
            data = [(np.random.uniform(lb, ub, len(lb)), mybounds, X, T, B, flag, prism, alpha, I)
                    # tuplets to feed the minimization function
                    for k in range(init_sol)]
            pool = mp.Pool()
            res = pool.starmap(minimiza, data)  # parallel minimization
            pool.close()
            pool.join()
            new_list = [item[1] for item in res]  # get fobj values
            # index for best model, minor fobj value
            indice = new_list.index(min(new_list))
            prism_mod2 = res[indice][0]
            fopt = res[indice][1]

        elif inv_type == 2:
            res = optimize.differential_evolution(func=fobj, bounds=mybounds, args=(T, B, flag, X,
                                                                                    prism, alpha, I), disp=False, workers=-1)

            fopt = res['fun']
            prism_mod2 = res['x']

        end = time.time()

        fc2 = fwd(prism_mod2, X, prism, alpha, I)

        prism_mod2 = vec2mat(prism_mod2, prism)

        for i in range(prism):  # Zero to surface
            prism_mod2[i, 3] = prism_mod2[i, 3] - Fh

        aux2 = np.array(np.column_stack((aux1, prism_mod2)))

        if cont1 == 0:  # Get first model accepted by the inversion criterias
            data_exit = aux2.copy()

        else:  # Appending accepted inversion models
            data_exit = np.concatenate((data_exit, aux2))

        if cont1 == 0:  # Get first epsilon and model accepted by the inversion criterias
            bestaj = error1
            bestmodel = prism_mod2  # matrix format
            bestFC = fc2  # fwd full output

        elif error1 < bestaj:  # Get the best epsilon and model accepted from the inversions
            bestaj = error1
            bestmodel = prism_mod2  # matrix format
            bestFC = fc2  # fwd full output

        logging.info('\nStep 2 adjust: %.2f' % fopt + ' aj: %.2f' % aj2
                     + '\nElapsed time: %.2f' % ((end - start)/3600) + 'h'
                     + '\nEnd of the round: %i' % (cont1)
                     + "\n------------------------------------------------------")

        mybounds = mybounds_init

    Z0 = bestmodel[:, 3]  # 1D-array for z0
    FDA = np.zeros(prism)
    j = 0
    for i in range(prism):  # Function of acumulative distribution
        FDA[i] = (2/np.pi)*atan2((lp[j+1]-lp[j])/2,
                                 Z0[i])  # calculada em função de lp
        j += 2

    logging.info('\nFDA: '+str(FDA))

    data_posit = np.argsort(data_exit[:, 0])
    data_exit = data_exit[data_posit, :]  # data organized by prisms

    # Save Results ---------------------------------------------------------------
    simple_prism = 0

    for i in range(prism):
        if bestmodel[i, 0] >= 4 and FDA[i] >= 0.5:
            simple_prism += 1

    simple_model = np.zeros((simple_prism, 4))

    j = 0
    for i in range(prism):
        if bestmodel[i, 0] >= 4 and FDA[i] >= 0.5:
            simple_model[j, :] = bestmodel[i, :]
            j += 1

    if first == 'n' or first == 'N':
        header_par = "A0 im x0 z0"
        header_FDA = "Probability for prisms"
        header_calc = "TFA (nT) IAVF (nT) INC (degree)"
        header_sols = "prism A0 im x0 z0"

        np.savetxt('Output/exitmod_I_'+index+'_'+str(dens)+'.dat',
                   bestmodel, header=header_par, comments='')

        if simple_prism > 0 and simple_prism < prism:
            np.savetxt('Output/exitmod_I_'+index+'SM_'+str(dens) +
                       '.dat', simple_model, header=header_par, comments='')

        np.savetxt('Output/FDA_'+index+'_'+str(dens)+'.dat',
                   FDA, header=header_FDA, comments='')
        np.savetxt('Output/calculado_I_'+index+'_'+str(dens) +
                   '.dat', bestFC, header=header_calc, comments='')
        np.savetxt('Output/calculado_fc1_'+index+'_'+str(dens) +
                   '.dat', fc1, header=header_calc, comments='')
        np.savetxt('Output/solucoes_I_'+index+'_'+str(dens)+'.dat',
                   data_exit, header=header_sols, comments='')

    else:
        np.savetxt('Output/exitmod_I_'+index+'_SM_'+str(dens) +
                   '.dat', bestmodel, header=header_par, comments='')

        if simple_prism > 0 and simple_prism < prism:
            np.savetxt('Output/exitmod_I_'+index+'SM_SM_'+str(dens) +
                       '.dat', simple_model, header=header_par, comments='')

        np.savetxt('Output/FDA_'+index+'_SM_'+str(dens) +
                   '.dat', FDA, header=header_FDA, comments='')
        np.savetxt('Output/calculado_I_'+index+'_SM_'+str(dens) +
                   '.dat', bestFC, header=header_calc, comments='')
        np.savetxt('Output/calculado_fc1_'+index+'_SM_'+str(dens) +
                   '.dat', fc1, header=header_calc, comments='')
        np.savetxt('Output/solucoes_I_'+index+'_SM_'+str(dens) +
                   '.dat', data_exit, header=header_sols, comments='')

    sys.modules[__name__].__dict__.clear()

    return
