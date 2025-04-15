import numpy as np

def pad(P,N):
    padding = -np.flip(P[1:N])
    return np.append(padding, P)