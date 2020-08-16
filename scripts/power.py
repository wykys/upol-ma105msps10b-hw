#!/usr/bin/env python3

def pwr(Uin, Uout, Iout, Tmax=125, T=40):
    U = Uin - Uout
    P = U * Iout
    Rja = 100.2
    Ta = T
    Tj = Ta + Rja * P
    R = (Tmax - T) / P
    print(f'Uin: {Uin} V, Uout: {Uout} V, Iout: {Iout} A')
    print(f'U: {U*1e3:.0f} mV')
    print(f'P: {P*1e3:.0f} mW')
    print(f'R: {R:.0f} K/W')
    print(f'Tj: {Tj} °C')
    print('='*44)



if __name__ == '__main__':
    Ud = 0.8
    Vcc = 5 - Ud

    pwr(Vcc, 3.3, 777e-3)
    pwr(Vcc, 1.8, 50e-3)
    pwr(Vcc, 1, 217e-3)



