#!/usr/bin/env python3
import _matrix
from pytest import approx
import numpy as np
import random
import time

class TestMatrix:

    def multiply_calculate(self, row, col1, col2, tsize):
        
        #ini
        r_a = np.random.rand(row, col1)
        r_b = np.random.rand(col1, col2)
        a = _matrix.Matrix(r_a)
        b = _matrix.Matrix(r_b)

        #naive
        time_start = time.time()
        ans_naive = _matrix.multiply_naive(a, b)
        time_end = time.time()
        naive = time_end - time_start

        #tile
        time_start = time.time()
        ans_tile = _matrix.multiply_tile(a, b, tsize)
        time_end = time.time()
        tile = time_end - time_start

        #mkl
        time_start = time.time()
        ans_mkl = _matrix.multiply_mkl(a, b)
        time_end = time.time()
        mkl = time_end - time_start

        #ground truth
        ans_numpy = np.matmul(r_a, r_b)

        #check
        for i in range(row):
            for j in range(col2):
                assert ans_numpy[i, j] == approx(ans_naive[i, j])
                assert ans_numpy[i, j] == approx(ans_tile[i, j])
                assert ans_numpy[i, j] == approx(ans_mkl[i, j])

        return naive, tile, mkl

    def write_file(self, naive_t, tile_t, mkl_t):
        with open('performance.txt', 'w') as f:
            f.write('mutiply_naive time: '+ str(naive_t) + " second\n")
            f.write('mutiply_tile: '+ str(tile_t) + " second\n")
            f.write('mutiply_mkl: '+ str(mkl_t) + " second\n")
            f.write('tile speeds up rate ( naive time / tile time) : '+ str(naive_t / tile_t) + "\n")
            f.write('MKL speeds up rate (naive time / mkl time) : '+ str(naive_t / mkl_t) + "\n")


    def test(self):
        # Rule in README.rst : the matrix size should be larger than or equal to 1000x1000
        naive_t, tile_t, mkl_t = self.multiply_calculate(1500, 1500, 1500, 2)
        for i in range(2,6):
            this_naive, this_tile, this_mkl = self.multiply_calculate(1500, 1500, 1500, 2**i)
            tile_t = min(this_tile, tile_t)
        self.write_file(naive_t, tile_t, mkl_t)