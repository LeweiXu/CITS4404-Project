import numpy as np

def pad(P,N):
    padding = -np.flip(P[1:N])
    return np.append(padding, P)

def wma(P, N, kernel):
    padded = pad(P, N)
    return np.convolve(padded, kernel, mode='valid')