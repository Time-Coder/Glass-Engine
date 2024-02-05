import math
import numpy as np
from abc import ABC, abstractmethod


class WeightedIntegrator(ABC):

    def __init__(self):
        self.__ortho_polys = {0: np.array([1])}
        self.__nodes = {0: np.array([])}
        self.__weights = {0: np.array([])}

    @abstractmethod
    def integral_base_with_weight(self, n):
        pass

    def integral_func_with_weight(self, func, n):
        x = self.nodes(n)
        w = self.weights(n)
        result = 0
        for i in range(n):
            result += w[i] * func(x[i])

        return result

    def nodes(self, n):
        if n in self.__nodes:
            return self.__nodes[n]

        self.__nodes[n] = np.sort(np.real(np.roots(self._ortho_poly(n))))
        return self.__nodes[n]

    def weights(self, n):
        if n in self.__weights:
            return self.__weights[n]

        I = []
        for i in range(n):
            I.append(self.integral_base_with_weight(i))
        I = np.array(I)

        x = self.nodes(n)
        V = np.vander(x, increasing=True).T
        invV = np.linalg.inv(V)
        self.__weights[n] = np.dot(invV, I)
        return self.__weights[n]

    def _ortho_poly(self, n):
        if n in self.__ortho_polys:
            return self.__ortho_polys[n]

        xn = np.array([1] + [0] * n)
        poly = xn
        for i in range(n):
            pi = self._ortho_poly(i)
            item_num = np.polymul(xn, pi)
            num = 0
            for j in range(len(item_num)):
                num += item_num[j] * self.integral_base_with_weight(
                    len(item_num) - j - 1
                )

            item_dem = np.polymul(pi, pi)
            dem = 0
            for j in range(len(item_dem)):
                dem += item_dem[j] * self.integral_base_with_weight(
                    len(item_dem) - j - 1
                )

            poly = np.polysub(poly, num / dem * pi)

        self.__ortho_polys[n] = poly
        return poly


class cosxIntegrator(WeightedIntegrator):

    def __init__(self):
        WeightedIntegrator.__init__(self)
        self.__I2n_values = {0: 2}

    def integral_base_with_weight(self, n):
        if n & 1:
            return 0

        half_n = n // 2
        if half_n in self.__I2n_values:
            return self.__I2n_values[half_n]

        self.__I2n_values[half_n] = 2 * (math.pi / 2) ** n - n * (
            n - 1
        ) * self.integral_base_with_weight(n - 2)
        return self.__I2n_values[half_n]
