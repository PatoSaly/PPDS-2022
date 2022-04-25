# Assignment 9

In assignment was our task to work with `numba` framework that has direct support
of cuda GPU programming by directly compiling a restricted subset of Python code into CUDA kernels
and device functions following the CUDA execution model. 

---

## Program

We implemented matrix multiplication. Two matrices are generated
with help from numpy library. Third matrix is filled with zeros and has the size needed to contain the result of the multiplication. 

```python
arr1 = np.arange(35).reshape(5, 7)
arr2 = np.arange(63).reshape(7, 9)
# output matrix rize
arr_out = np.zeros((arr1.shape[0], arr2.shape[1]))
```

In our program we used basic `Memory management` by
passing numpy arrays directly to device (kernel) function using
`cuda.to_device(arr)`.

While calling kernel function we used 1 block per grid
and two-dimensional array of output size as count of threads per block.

```python
block_per_grid = 1
treads_per_block = (5, 9)

multiply[block_per_grid, treads_per_block](matrix1, matrix2, matrix_out)
```

To calculate result we used basic function, that calculated value for each index in its thread.

---

## Result
After calculating multiplication of two matrices with different sizes. The duration of calculations in seconds is always similar.

<br>

Example 1 (input matrices -> (5, 7), (7, 9):
```
Time elapsed: 0.608100800000102

[[ 819.  840.  861.  882.  903.  924.  945.  966.  987.]
 [2142. 2212. 2282. 2352. 2422. 2492. 2562. 2632. 2702.]
 [3465. 3584. 3703. 3822. 3941. 4060. 4179. 4298. 4417.]
 [4788. 4956. 5124. 5292. 5460. 5628. 5796. 5964. 6132.]
 [6111. 6328. 6545. 6762. 6979. 7196. 7413. 7630. 7847.]]
 ```

<br>

Example 1 (input matrices -> (2, 3), (3, 4):
```
Time elapsed: 0.6016157000012754

[[20. 23. 26. 29.]
 [ 8.  9. 10. 11.]]
```

