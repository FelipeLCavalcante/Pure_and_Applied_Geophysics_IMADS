#!/usr/bin/env python3

import numpy as np
import multiprocessing as mp
import time

def dique(p,X,I,alpha,prism):

	Tx=np.array([0.]) # VERIFICAR MATLAB PQ ALOCAR VETOR
	Tz = Tx
	
	P=p.reshape(prism,4) # CONVERTE VETOR PARA MATRIZ

	for k in range(prism):
        
		Mt = P[k,0]
		inc = P[k,1]
		x0 = P[k,2]
		z0 = P[k,3]

		cosseno=np.cos(np.radians(inc))
		seno=np.sin(np.radians(inc))

		Jx=100*cosseno
		Jz=100*seno

		wx=X-x0
		wn=wx**2+z0**2
		Tx=Tx-2*Mt*(Jx*z0+Jz*wx)/wn
		Tz=Tz+2*Mt*(Jz*z0-Jx*wx)/wn

	cosseno=np.cos(I*np.pi/180.)
	seno1=np.sin(I*np.pi/180.)
	seno2=np.sin(alpha*np.pi/180.)
	Tt=cosseno*seno2*Tx+seno1*Tz

	f = np.array(np.column_stack((Tx,Tz,Tt)))
	
	return f
