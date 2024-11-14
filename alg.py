import numpy as np

path = "points.txt"

points = np.array([np.array(i.split(" ")[1:], dtype = np.float64) for i in open(path).readlines()])



tmp_A = []
for i in points:
    tmp_A.append([*i[0:2], 1])

A = np.matrix(tmp_A)
B = np.matrix(points[:, 2]).T

print(B.size, A.size)

fit = (A.T * A).I * A.T * B

# Extract the left singular vectors
print(fit)



