#!/usr/bin/python3

import numpy as np

def fwd(p,X,prism,alpha,I):
    """ Tx=np.array([0.]) 
    Tz=np.array([0.]) """
    Tx = np.zeros(len(X))
    Tz = np.zeros(len(X)) 

    P=p.reshape(prism,4)

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
        #print(f' Mt: {Mt} z0: {z0} x0: {x0} inc: {inc}')
        #print(f'Tx: {Tx} Jx: {Jx}  Jz: {Jz} wx: {wx} wn: {wn}')
        #input("FWD PAUSE")
        Tx=Tx-2*Mt*(Jx*z0+Jz*wx)/wn
        Tz=Tz+2*Mt*(Jz*z0-Jx*wx)/wn

    cosseno=np.cos(I*np.pi/180.)
    seno1=np.sin(I*np.pi/180.)
    seno2=np.sin(alpha*np.pi/180.)
    Tt=cosseno*seno2*Tx+seno1*Tz 

    B=np.sqrt(Tx**2+Tz**2)
    A=np.degrees(np.arctan2(Tz,Tx))
    f=np.array(np.column_stack((Tt,B,A)))
    
    return f
