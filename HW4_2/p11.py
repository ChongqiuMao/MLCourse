# -*- coding: utf-8 -*-
# @Author: yuchen
# @Date:   2019-05-01 09:49:48
# @Last Modified by:   yuchen
# @Last Modified time: 2019-05-01 17:31:35

import numpy as np
import numpy.random as nr
import scipy.linalg as linalg
import matplotlib.pyplot as plt
from IPython import embed

def dataset1(n, r1=5, r2=10):
    angle1 = nr.uniform(0.0, np.pi * 2, size=n)
    circle1 = np.vstack((r1 * np.cos(angle1), r1 * np.sin(angle1)))

    angle2 = nr.uniform(0.0, np.pi * 2, size=n).T
    circle2 = np.vstack((r2 * np.cos(angle2), r2 * np.sin(angle2)))

    def centergen():
        return nr.randn(2, 2) * (r1 + r2) / 2.

    return np.hstack((circle1, circle2)).T, centergen

def dataset2(n, r1=5, r2=10):

    def sample_sphere(n, r, dim=3):
        vec = nr.randn(dim, n)
        vec /= linalg.norm(vec, axis=0)
        return vec * r

    sphere1 = sample_sphere(n, r1)
    sphere2 = sample_sphere(n, r2)

    def centergen():
        return nr.randn(2, 3) * (r1 + r2) / 2.

    return np.hstack((sphere1, sphere2)).T, centergen

def iterator(dataset, centers):
    assignment = [np.argmin(np.sum((centers - datapoint) ** 2., axis=1)) for datapoint in dataset]
    pos = [[] for _ in centers]
    for i, cidx in enumerate(assignment):
        pos[cidx].append(dataset[i])
    for i, c in enumerate(pos):
        pos[i] = np.vstack(pos[i])
    newcenters = np.array([np.mean(pos[i], axis=0) for i in range(len(pos))])
    return newcenters, np.array(assignment)

def plot(dataset, centers, assignment, name="plt_1"):
    plt.clf()
    colors = ['b', 'g']
    for i in range(2):
        idx = (assignment == i)
        plt.scatter(dataset[idx, 0], dataset[idx, 1], marker='.', alpha=0.2, color=colors[i])
    plt.scatter(centers[0:1, 0], centers[0:1, 1], marker='x', color=colors[0])
    plt.scatter(centers[1:2, 0], centers[1:2, 1], marker='x', color=colors[1])
    plt.title(name)
    plt.savefig(name + ".png")

def plot3d(dataset, centers, assignment, name="plt_3d_1"):
    plt.clf()
    colors = ['b', 'g', 'r']
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(3):
        idx = (assignment == i)
        ax.scatter(dataset[idx, 0], dataset[idx, 1], dataset[idx, 2], marker='.', alpha=0.2, color=colors[i])
    ax.set_xlabel('dim1')
    ax.set_ylabel('dim2')
    ax.set_zlabel('dim3')
    plt.title(name)
    plt.show()
    plt.savefig(name + ".png")

def main():
    n = 1000            # #data
    k = 2               # k-means

    MAXITER = 500
    MAXTRIAL = 10       # In case of bad initialization of centers
    dataset, centergen = dataset2(n)

    for _ in range(MAXTRIAL):
        try:
            centers = centergen()
            for it in range(MAXITER):
                if it % 20 == 0:
                    print("Iteration {}".format(it))
                newcenters, assignment = iterator(dataset, centers)
                diff = np.sum((centers - newcenters) ** 2.)
                centers = newcenters
                if diff < 1e-9:
                    print("Stopped at iter {}".format(it))
                    break
            plot3d(dataset, centers, assignment)
            break
        except Exception as e:
            print(e)

    print("K-Means experiment concluded.")

if __name__ == "__main__":
    main()