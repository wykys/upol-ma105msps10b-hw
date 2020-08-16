#!/usr/bin/env python3

import sympy as sp
sp.init_printing()

IIN = sp.Symbol('Iin')

RF = sp.Symbol('RF')
RG1 = sp.Symbol('RG1')
RG2 = sp.Symbol('RG2')

RS = sp.Symbol('RS')
RL = sp.Symbol('RL')
RT = sp.Symbol('RT')

RIN = sp.Symbol('Ri')
KU = sp.Symbol('K')

GF = 1/RF
GG1 = 1/RG1
GG2 = 1/RG2
GS = 1/RS
GL = 1/RL
GT = 1/RT

class FullOpAmp(object):
    def __init__(self):
        self.create_matrix()
        self.create_equations()

    def create_matrix(self):

        mat = sp.Matrix([
            [GT+GG1, -GG1, 0, 0, 0],
            [-GG1, GG1+GF, -GF, 0, 0],
            [0, -GF, GF+GL, -GL, 0],
            [0, 0, -GL, GL+GF, -GF],
            [0, 0, 0, -GF, GF+GG2]
        ])

        #sp.pprint(mat)

        # i m
        mat = mat.col_insert(7, sp.Matrix([0, 0, 1, 0, 0]))
        # i p
        mat = mat.col_insert(8, sp.Matrix([0, 0, 0, -1, 0]))
        # u in
        mat = mat.row_insert(7, sp.Matrix([[0, 1, 0, 0, -1, 0, 0]]))
        # u out
        mat = mat.row_insert(8, sp.Matrix([[0, 0, 1, 1, 0, 0, 0]]))

        vec = sp.Matrix([
            [IIN],
            [0],
            [0],
            [0],
            [0],
            [0],
            [0]
        ])

        self.mat = mat
        self.vec = vec

    def calculate_subdet(self, col):
        mat = self.mat.copy()
        mat.col_del(col-1)
        mat = mat.col_insert(col-1, self.vec)
        return mat.det()

    def create_equations(self):
        det = self.mat.det()
        det_10 = self.calculate_subdet(1)
        det_20 = self.calculate_subdet(2)
        det_30 = self.calculate_subdet(3)
        det_40 = self.calculate_subdet(4)
        U10 = sp.simplify(det_10/det)
        U30 = sp.simplify(det_30/det)
        U40 = sp.simplify(det_40/det)

        Rin = sp.simplify(U10 / IIN)
        Ku = sp.simplify((U40 - U30) / U10)

        print('Ku:')
        sp.pprint(Ku)
        print('-'*30)

        print('Rin:')
        sp.pprint(Rin)
        print('-'*30)

        rg1_a = sp.solve(Ku-KU, RG1)[0]
        rg1_b = sp.solve(Rin-RIN, RG1)[0]
        rg2 = sp.simplify(sp.solve(rg1_a-rg1_b, RG2)[0])
        rg1 = sp.simplify(rg1_a.subs(RG2, rg2))

        self.ku_eq = str(Ku)
        self.rin_eq = str(Rin)
        self.rg1_eq = str(rg1)
        self.rg2_eq = str(rg2)

    def test(self, RF, RG1, RG2, RT):
        Ku = eval(self.ku_eq)
        Ri = eval(self.rin_eq)

        print(f'Rin = {Ri:.0f} Ω')
        print(f'Ku = {Ku:.1f}')

    def solve(self, K, Ri, RF=301):
        print('Solver start')

        RT = 1000*Ri + 1
        RG1 = 0
        RG2 = 0

        while RG1 < 50 or RG2 < 50:

            RT -= 1

            RG1 = eval(self.rg1_eq)
            RG2 = eval(self.rg2_eq)


            print('#'*40)

            print(f'RG1 = {RG1:.0f} Ω')
            print(f'RG2 = {RG2:.0f} Ω')
            print(f'RT = {RT:.0f} Ω')
            print(f'RF = {RF:.0f} Ω')

            self.test(RF, RG1, RG2, RT)


if __name__ == '__main__':
    amp = FullOpAmp()
    amp.solve(0.5, 50)
