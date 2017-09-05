import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path
from matplotlib import colors as mcolors
import matplotlib.patches as patches

from Line import Line

PI = np.pi
GRID_COLORS = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
COLORS = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)

class nMultiGrid(object):
    def __init__(self, n, gammas):
        self.n = n
        self.gammas = gammas

        assert(len(self.gammas) == self.n)

        self.grid_color_repeat = (self.n - 1) / len(GRID_COLORS) + 1

        self.lines = [self.get_lines(j, 5) for j in range(self.n)]

        self.intersection_points = self.get_intersection_points()
        
    def eval_eqn(self, a, b, c, d, x):
        if b == 0:
            return None
        return (d - c - a*x) / b

    def get_lines(self, j, N_range):
        arg = 2*j*PI / self.n
        return [Line(np.cos(arg), np.sin(arg), self.gammas[j] - N)
                for N in range(-N_range, N_range + 1)]
    
    def plot_lines(self):
        for lines, color in zip(self.lines, GRID_COLORS*self.grid_color_repeat):
            for line in lines:
                line.plot(5, color)
        plt.xlim(-self.n, self.n)
        plt.ylim(-self.n, self.n)
        plt.gca().set_aspect('equal', adjustable='box')
        
    def get_intersection_points(self):
        all_points = []
        for i in range(self.n):
            for j in range(i + 1, self.n):
                for k in range(len(self.lines[i])):
                    for m in range(len(self.lines[j])):
                        all_points.append([self.lines[i][k].intersect(self.lines[j][m]), [i, j]])
        return all_points

    def plot_intersection_points(self):
        for pt in self.intersection_points:
            plt.plot([pt[0][0]], [pt[0][1]], 'ko')

    def plot_tiles(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for pt, dims in self.intersection_points:
            k = self.K(*pt)
            new_pts = [k,
                       k[:dims[0]] + [k[dims[0]] + 1] + k[dims[0] + 1:],
                       k[:min(dims)] + [k[min(dims)] + 1] +
                       k[min(dims) + 1:max(dims)] +
                       [k[max(dims)] + 1] + k[max(dims) + 1:],
                       k[:dims[1]] + [k[dims[1]] + 1] + k[dims[1] + 1:]]
            verts = [self.phi(x) for x in new_pts] + [(0,0)]
            codes = [Path.MOVETO,
                     Path.LINETO,
                     Path.LINETO,
                     Path.LINETO,
                     Path.CLOSEPOLY]
            path = Path(verts, codes)
            patch = patches.PathPatch(path, facecolor='papayawhip', lw=0.5)
            ax.add_patch(patch)
        ax.set_xlim(-10,10)
        ax.set_ylim(-10,10)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

    

    def K(self, x, y):
        return [np.ceil(x*np.cos(2*j*PI/self.n) +
                        y*np.sin(2*j*PI/self.n) +
                        self.gammas[j] - 0.00001) for j in range(0, self.n)]

    def phi(self, k):
        x_res = np.sum([k[j]*np.cos(2*j*PI/self.n) for j in range(0, self.n)])
        y_res = np.sum([k[j]*np.sin(2*j*PI/self.n) for j in range(0, self.n)])
        return (x_res, y_res)

if __name__=="__main__":
    try:
        N = int(sys.argv[1])
        n = nMultiGrid(N, [x*1./(N+1) for x in range(N)])
        n.plot_lines()
        n.plot_intersection_points()
        plt.show()
        n.plot_tiles()
    except IndexError:
        print("Usage: python nMultiGrid.py <number of dimensions>")
#N = 5
#n = nMultiGrid(N, [x*1./(N+1) for x in range(N)])
#n.plot_lines()
#n.plot_intersection_points()
#plt.show()
#n.plot_tiles()
#print(COLORS)
#for i in range(3, 12):
#    n = nMultiGrid(i, [x*1./(i+1) for x in range(i)])
#    n.plot_lines()
#    P1 = [1, 1]
#    P2 = [1, 2]
#    plt.plot([P1[0]], [P1[1]], 'ko')
#    plt.plot([P2[0]], [P2[1]], 'bo')
#    P1_prime = n.phi_comp_K(*P1)
#    P2_prime = n.phi_comp_K(*P2)
#    print(P1_prime)
#    print(P2_prime)
#    plt.plot([P1_prime[0]], [P1_prime[1]], 'kd')
#    plt.plot([P2_prime[0]], [P2_prime[1]], 'bd')
#    plt.show()
