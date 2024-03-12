import numpy as np
from ..util.backend_functions import backend as bd
from .diffractive_element import DOE
from ..util.scaled_FT import scaled_fourier_transform

class Sesam(DOE):
    def __init__(self,f, radius = None, aberration = None):
        """
        Creates a thin lens with a focal length equal to f. 

        Radius is a physical circular boundary of the lens.

        Aberration is a function of (x, y) which describes the optical
        path depth aberration of the lens. This is applied along with
        any focal length given by `f`.
        """
        global bd
        from ..util.backend_functions import backend as bd



    def get_transmittance(self, xx, yy, λ):

        t = 1
        if self.aberration != None:
            t = t*bd.exp(2j * bd.pi / λ * self.aberration(xx, yy))

        if self.radius != None:
            t = bd.where((xx**2 + yy**2) < self.radius**2, t, bd.zeros_like(xx))

        self.t = t

        t = self.t * bd.exp(-1j*bd.pi/(λ*self.f) * (xx**2 + yy**2))
        return t


