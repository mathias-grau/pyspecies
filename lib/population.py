from lib.animation import Animate
from lib.euler import BackwardEuler
from lib.utils import UVtoX
import numpy as np


class Population:

    Xlist = []

    def __init__(self, Space: np.ndarray, u0: function, v0: function, D: np.ndarray):
        self.D = D
        self.Space = Space
        X0 = UVtoX(u0(Space), v0(Space))
        self.Xlist = [X0, X0]
        self.Tlist = np.array([0, 0])

    def simulate(self, duration: float, N=100):
        Time = np.linspace(0, duration, N)
        self.Tlist = np.append(self.Tlist,
                               2 * self.Tlist[-1] - self.Tlist[-2] + Time)
        X0 = self.Xlist[-1].copy()
        self.Xlist = self.Xlist + BackwardEuler(X0, Time, self.Space, self.D)

    def animate(self, length=10, filename=None):
        K, N = len(self.Space), len(self.Tlist)
        txt = 'D={}, K={}, N={}'.format(
            str(self.D).replace('\n', ''), K, N - 2)
        Animate(self.Space,
                self.Xlist,
                self.Tlist,
                length=length,
                text=txt,
                filename=filename)
