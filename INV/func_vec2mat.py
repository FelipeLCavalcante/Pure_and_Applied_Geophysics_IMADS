#!/usr/bin/python3

import numpy as np

def vec2mat(vec,prism):

    mat = vec.reshape(prism,4)
    posit = np.argsort(mat[:,2])
    mat = mat[posit,:]

    return mat