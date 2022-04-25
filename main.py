"""
Authors:
    Mgr. Ing. Matúš Jókay, PhD.
Example implementation of matrix multiplication from lecture.
Resources:
"""

import numpy as np
from numba import cuda
from math import ceil


@cuda.jit
def my_kernel(i_data):
    x, y = cuda.grid(2)
    x_max, y_max = data.shape
    if x < x_max and y < y_max:
        i_data[x][y] *= 5


# Create the data array - usually initialized some other way
data = np.ones((17, 17))

# Set the number of threads in a block
threadsperblock = (16, 16)

# Calculate the number of thread blocks in the grid
blockspergridX = ceil(data.shape[0] / threadsperblock[0])
blockspergridY = ceil(data.shape[1] / threadsperblock[1])

# Now start the kernel
my_kernel[(blockspergridX, blockspergridX), threadsperblock](data)

# Print the result
print(data)
