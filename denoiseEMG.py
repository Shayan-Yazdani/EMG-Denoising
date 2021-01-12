# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 13:53:08 2020

@author: Shayan Yazdani Sangdeh
"""

import scipy
import numpy as np
from scipy import io
from scipy import signal
import matplotlib.pyplot as plt
from PyEMD import EEMD


def EMGden(EMG, fs):
    fs=int(fs)
    len_pre=len(EMG)
    if fs!= 1024:
        EMGe=signal.resample(EMG, round(len(EMG)*(fs/1024)))
    else:
        EMGe=EMG
    out=[]
    win2=4000
    for st in range(int(len(EMGe)/win2)):
        win_st=st*win2
        win_end=win_st+win2
        if (win_end+4001)>len(EMGe):
            win_end=len(EMGe)
        temp_out = main_part(EMGe[win_st:win_end])
        out=np.concatenate((out,temp_out), axis=None)
    if len(out)!=len_pre:
        out=signal.resample(out, len_pre)
    EMGclean=EMG-out
    return out, EMGclean

def main_part(EMG):
    R=PeakDetection(EMG)
    IMFs=EEMD_DEC(EMG)
    if len(R)>1:
        winsz=50
        for jj in range(0,4):
            a=0
            b=0
            ec=0
            IMFs1 = np.pad(IMFs[jj,:], (winsz, winsz), 'symmetric')
            R1=(R+50).astype(int)
            for i in range(0,(len(R1)-1)):
                a=np.mean(np.abs(IMFs1[R1[i]-winsz:R1[i]+winsz])+a)
            for i in range(0,(len(R1)-1)):
                b=np.mean(np.abs(IMFs1[R1[i]+winsz:R1[i+1]-winsz])+b)
            if a>(3*b):
                IMFs[jj,:]=0
                ec=ec+1
        if ec==0: 
            IMFs[3,:]=0
        win1=100
        EMG1=EMG-np.sum(IMFs,axis=0)
        b, a = signal.butter(10, 14/512,'highpass')
        xx = signal.filtfilt(b, a, EMG1)
        sd=np.std(xx[R[0]+win1:R[1]-win1])
        y=[]
        y1 = PID(EMG1[0:R[1]],sd)
        y=np.concatenate((y,y1), axis=None)
        
        if len(R)>2:
            for jj in range(1,len(R)-2):
                sd=np.std(xx[R[jj]+win1:R[jj+1]-win1])
                y1 = PID(EMG1[R[jj]:R[jj+1]],sd)
                y=np.concatenate((y,y1), axis=None)
            sd=np.std(xx[R[-2]+win1:R[-1]-win1])
            y1 = PID(EMG1[R[-2]:len(EMG1)+1],sd)
            y=np.concatenate((y,y1), axis=None)
    else:
        IMFs[3,:]=0
        EMG1=EMG-np.sum(IMFs,axis=0)
        y=[]
        win2=2000
        b, a = signal.butter(10, 14/512,'highpass') 
        xx = signal.filtfilt(b, a, EMG1)
        for st in range(int(len(EMG1)/win2)):
            win_st=st*win2
            win_end=win_st+win2
            if (win_end+2001)>len(EMG):
                win_end=len(EMG)
            sd=np.std(xx[win_st:win_end])
            y1 = PID(EMG1[win_st:win_end],sd)
            y=np.concatenate((y,y1), axis=None)
    return y

def PeakDetection(EMG):
    b, a = signal.butter(10, 20/(512),'low')
    EMG_filt = signal.filtfilt(b, a, EMG)
    padsz=30
    EMG_pad=np.pad(EMG_filt, (30, 30), 'symmetric')
    x=[]
    for i in range(0,len(EMG_filt)):
        ii=i+padsz
        x.append(np.mean(np.abs(EMG_pad[ii-padsz:ii+padsz])))
    x=np.array(x)
    T=2.5*np.sqrt(np.mean(x ** 2))
    m=0;
    j=1;
    R=[];
    while j<len(x):
        k=0
        if (x[j]>=T):
            while (x[j+k]>= T):
                if j+k+1<len(x):
                    k=k+1;
                else:
                        break
            w_2=j+k+1
            R_loc=np.argwhere(x[j:w_2]==max(x[j:w_2]))+j-1
            if m==0:
                R=np.append(R,R_loc)
            elif R_loc-R[m]>300:
                R=np.append(R,R_loc)           
                m=m+1
            j=w_2+1
        else:
            j=j+1
    if len(R)>0:
        R=R.astype(int)
    return R

def EEMD_DEC (EMG):
    emd = EEMD()
    T = np.arange(0,len(EMG),1)
    max_imf=3
    eemd = EEMD()
    eemd.trials = 200
    #eemd.noise_seed(12345)
    IMFs = eemd.eemd(EMG,T, max_imf)
    return IMFs

def PID(y,sigma2):
    N = 30
    r = 50
    sigma_s = 100
    gamma_r = 998.5
    gamma_s = 0.22
    alpha   = 1.533
    lmbd  = np.log(alpha) * 0.567
    dx      = np.linspace(-r,r,2*r+1)
    r2      = dx**2 ;
    x = y;
    sigma2=(5*sigma2)**2
    for i in range(0,N):
        xp = np.pad(x, (r, r), 'symmetric')
        for q in range(0,len(x)):
            p=q+r
            # Spatial Domain
            d = xp[p-r:p+r+1] - x[q]  
            T = sigma2* gamma_r * (alpha**(-i)) 
            S = (sigma_s**2) * gamma_s * (alpha**(i/2))
            k = np.multiply(np.exp(- (d**2) / T) , np.exp(- r2 / S)) 
            # Fourier Domain
            D = np.fft.fft(np.fft.ifftshift(np.multiply(d,k)))      
            V = sigma2 * np.sum(k**2)             
            K = np.exp(-np.abs(D)**2 / V)        
            n = np.dot(D,K)/len(K)     
            x[q] = x[q] - lmbd * np.real(n)
                 
    return x

