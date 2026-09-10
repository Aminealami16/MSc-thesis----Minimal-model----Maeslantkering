# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 13:37:51 2026

@author: dwbtermeulen
"""


import numpy as np 
import scipy.signal as sig
import matplotlib.pyplot as plt


def FDD(time, data, f1f2, layer, nFFT, nOverlap, window):
    """
    Function that identifies modal properties (natural frequencies and mode shapes) from a dataset using FDD
    
    Input:
        time            = Array containing time corresponding to the collected data [s] 
        data            = Preprocessed data of DP900 (every column corresponds to a channel) [g]  
        f1f2            = Frequency band in which the peak is located [Hz] (size:[nP x 2] - nP: number of peaks)
        layer           = Singular value layer in which the peak is located [-] (size: [nP] - nP: number of peaks)
        nFFT            = Length of each segment [-] (choose 2^x)
        nOverlap        = Amount of overlap between two segments [%] 
        window          = Window to use (see scipy.signal.get_window)
        
    Output:
        f_seg           = Frequency vector [Hz] [nFFT/2+1]
        s_value         = Singular values [nFFT/2+1, nChannels] 
        FDD_nF          = Natural frequencies FDD [Hz] [nP]
        FDD_phi         = Normalized modeshapes FDD [-] [nChannels x nP]
    """
    
    nChannels           = data[0,:].size
    dt                  = time[1] - time[0]
    fs                  = 1 / dt
    nSpec               = int(nFFT/2+1)
    
    Sdd                 = np.zeros((nSpec, nChannels, nChannels), dtype = 'complex')
    for j in range(nChannels):
        for k in range(nChannels):
            f_seg, Sdd[:,j,k]                   = sig.csd(data[:,j], 
                                                          data[:,k], 
                                                          fs, 
                                                          window = window, 
                                                          nperseg = nFFT, 
                                                          noverlap = nOverlap/100*nFFT, 
                                                          scaling ='density', 
                                                          detrend = None, 
                                                          return_onesided = True)
    
    s_value             = np.zeros((nSpec, nChannels))
    U_vector            = np.zeros((nSpec, nChannels, nChannels), dtype = 'complex')
    for i in range(nSpec):
        U_vector[i,:,:], s_value[i,:], _        = np.linalg.svd(Sdd[i,:,:])
    
    FDD_nF              = np.zeros(layer.size)
    FDD_phi             = np.zeros((nChannels, layer.size), dtype = 'complex')
    for i in range(layer.size):
        k               = int(layer[i]-1)
        freq_band       = (f_seg>=f1f2[i,0]) & (f_seg<=f1f2[i,1])
        idx_band        = np.argmax(s_value[freq_band, k])
        idx             = np.where(freq_band)[0][idx_band]
        FDD_nF[i]       = f_seg[idx]
        FDD_phi[:,i]    = U_vector[idx, :, k]
    
    return f_seg, s_value, FDD_nF, FDD_phi


def SVD_plot(f_seg, s_value, xlim, ylim, nF = [], f1f2 = []):
    """
    Function that plots the singular value diagram. 

    Input:    
        f_seg               = Frequency vector [Hz] [nFFT/2+1]
        s_value             = Singular values [nFFT/2+1, nChannels]
        xlim                = Boundaries x-axis
        ylim                = Boundaries y-axis
        nF                  = Natural frequency estimations [Hz]
        f1f2                = Frequency band [Hz]
    """
    
    plt.figure(figsize = (10,10), constrained_layout = True)
    plt.xlabel('Frequency [Hz]', fontsize = 16, fontweight = 'bold')
    plt.xticks(fontsize = 14)
    plt.ylabel('Amplitude [dB]', fontsize = 16, fontweight = 'bold')
    plt.yticks(fontsize = 14)
    plt.xlim(xlim)
    plt.ylim(ylim)

    clr     = 'black', 'dimgray', 'darkgray'
        
    for i in range(3):
        lbl     = 'Singular value {}'.format(i+1)
        plt.plot(f_seg, 10*np.log10(s_value[:,i]/s_value[0,0]), label = lbl, color = clr[i])
    
    if len(nF) != 0:
        plt.vlines(nF, ylim[0], ylim[1], label = 'Natural frequency', color = 'red', linestyle = (0, (4, 2)), linewidth = 2)  
    
    if len(f1f2) != 0:
        plt.vlines(f1f2, ylim[0], ylim[1], label = 'Frequency band', color = 'lightcoral', linestyle = 'dotted')
       
    plt.legend(fontsize = 16, loc = 'best', framealpha = 1) 


def compute_mac(A, B, n_modes=4):
    MAC = np.zeros((n_modes, n_modes))

    for i in range(n_modes):
        for j in range(n_modes):

            phi_i = np.asarray(A[:, i]).ravel()
            phi_j = np.asarray(B[:, j]).ravel()

            num = np.abs(np.vdot(phi_i, phi_j))**2
            den = np.vdot(phi_i, phi_i) * np.vdot(phi_j, phi_j)

            MAC[i, j] = num / den

    return MAC



def plot_mac(MAC, title, xlabel, ylabel):
    plt.figure(figsize=(5, 4))
    plt.imshow(MAC, cmap='viridis', vmin=0, vmax=1)
    plt.colorbar(label='MAC value')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title, fontweight='bold')

    # Axis labels start at 1
    plt.xticks(
        ticks=range(MAC.shape[1]),
        labels=range(1, MAC.shape[1] + 1)
    )
    plt.yticks(
        ticks=range(MAC.shape[0]),
        labels=range(1, MAC.shape[0] + 1)
    )

    # Add MAC values inside the cells
    for i in range(MAC.shape[0]):
        for j in range(MAC.shape[1]):
            value = MAC[i, j]
            plt.text(
                j, i,
                f"{value:.2f}",
                ha='center',
                va='center',
                color='white' if value < 0.5 else 'black',
                fontsize=10
            )

    plt.tight_layout()