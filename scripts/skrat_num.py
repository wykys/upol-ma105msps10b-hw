#!/usr/bin/env python3

import numpy as np

RF1 = RF2 = 301
RG1 = 301
RG2 = 301
RCM = 4700
RT = 57.2

RS = 50
RL = 1000

Udd = 3.3
Uocm = Udd / 3
Uin = 1
Iin = Uin/RS

GF1 = 1/RF1
GF2 = 1/RF2
GG1 = 1/RG1
GG2 = 1/RG2

GS = 1/RS
GL = 1/RL
GT = 1/RT
GCM = 1/RCM

m = np.array([
    [GT+GG1, -GG1, 0, 0, 0],
    [-GG1, GG1+GF1+GCM, -GF1, 0, 0],
    [0, -GF1, GF1+GL, -GL, 0],
    [0, 0, -GL, GL+GF2, -GF2],
    [0, 0, 0, -GF2, GF2+GG2+GCM]
])


# Full OpAmp
# i m
m = np.insert(m, 5, [0, 0, 1, 0, 0], axis=1)
# i p
m = np.insert(m, 6, [0, 0, 0, -1, 0], axis=1)
# u in
m = np.insert(m, 5, [0, 1, 0, 0, -1, 0, 0], axis=0)
# u out
m = np.insert(m, 6, [0, 0, 1, 1, 0, 0, 0], axis=0)


m = np.matrix(m)


vec = np.matrix([Iin, 0, 0, 0, 0, 0, 0]).transpose()

det = np.linalg.det(m)

col = 1
tmp = m.copy()
tmp[:,col-1] = vec
det_1 = np.linalg.det(tmp)

col = 2
tmp = m.copy()
tmp[:, col-1] = vec
det_2 = np.linalg.det(tmp)

col = 3
tmp = m.copy()
tmp[:, col-1] = vec
det_3 = np.linalg.det(tmp)

col = 4
tmp = m.copy()
tmp[:, col-1] = vec
det_4 = np.linalg.det(tmp)

U10 = det_1/det
U20 = det_2/det
U30 = det_3/det
U40 = det_4/det

Rin = U10 / Iin

Kup = U40 / U10
Kum = U30 / U10

Udiff = U40 - U30

Ku = Udiff / U10

print(f'Rin:\t{Rin:.3f} Ω')
print(f'Kup:\t{Kup:.3f}')
print(f'Kum:\t{Kum:.3f}')
print(f'Ku:\t{Ku:.3f}')
print(f'U10:\t{U10:.3f} V')
print(f'U20:\t{U20:.3f} V')
print(f'U30:\t{U30:.3f} V')
print(f'U40:\t{U40:.3f} V')
print(f'Udiff:\t{Udiff:.3f} V')
