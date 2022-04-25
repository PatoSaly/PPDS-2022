"""
Authors:
    Bc. Patrik Saly
Implementation of two matrices multiplication.
Resources:
    https://www.programiz.com/python-programming/examples/multiply-matrix
    https://nyu-cds.github.io/python-numba/05-cuda/
"""

import time
from numba import cuda
import numpy as np


@cuda.jit
def multiply(mat1, mat2, out):
    """
    Function to count value on given index (grid(2))
    Parameters:
        mat1: First matrix
        mat2: Second matrix
        out: output matrix
    """
    x, y = cuda.grid(2)
    suma = 0
    for i in range(mat1.shape[1]):
        suma += mat1[x][i] * mat2[i][y]
    out[x, y] = suma


def main():
    arr1 = np.arange(6).reshape(2, 3)
    arr2 = np.arange(12).reshape(3, 4)
    # output matrix rize
    arr_out = np.zeros((arr1.shape[0], arr2.shape[1]))

    # start timer
    time1 = time.perf_counter()

    matrix1 = cuda.to_device(arr1)
    matrix2 = cuda.to_device(arr2)
    matrix_out = cuda.to_device(arr_out)

    block_per_grid = 1
    treads_per_block = (5, 9)

    multiply[block_per_grid, treads_per_block](matrix1, matrix2, matrix_out)

    # end timer
    print(f'\nTime elapsed: {time.perf_counter() - time1}\n')

    print(matrix_out.copy_to_host())


if __name__ == '__main__':
    main()
