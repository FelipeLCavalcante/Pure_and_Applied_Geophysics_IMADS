#!/usr/bin/python3

import numpy as np
from numpy import linalg as LA
from func_fwd import fwd


def fobj(p, *args):
    # fobj - funcao utilizada para minimizar o funcional Q

    T = args[0]
    B = args[1]
    flag = args[2]
    X = args[3]
    prism = args[4]
    alpha = args[5]
    I = args[6]

    f = fwd(p, X, prism, alpha, I)

    if flag == 1:
        r = B - f[:, 1]
    elif flag == 2:
        r = T - f[:, 0]

    Q = np.array(LA.norm(r, ord=2))

    return Q
