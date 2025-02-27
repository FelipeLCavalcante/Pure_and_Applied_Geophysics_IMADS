#!/usr/bin/python3

import numpy as np
import os
import time
from scipy import optimize
from random import random
from func_fobj import fobj
# from Pydyke_fobj import fobj
from math import e


def minimiza(kick, mybounds, X, T, B, flag, prism, alpha, I):

    results = optimize.fmin_l_bfgs_b(fobj, x0=kick, args=(T, B, flag, X,
                                                          prism, alpha, I), bounds=mybounds, approx_grad=True, pgtol=1e-1)

    return results
