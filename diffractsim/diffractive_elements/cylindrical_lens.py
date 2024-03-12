import numpy as np
from ..util.backend_functions import backend as bd
from .diffractive_element import DOE
from ..util.scaled_FT import scaled_fourier_transform

class CylindricalLensX(DOE):
    def __init__(self, f, radius=None, aberration=None, axis='x'):
        """
        Creates a cylindrical lens with a focal length equal to f.

        Args:
            f (float): Focal length of the cylindrical lens.
            radius (float, optional): Physical radius of the lens.
            aberration (function, optional): Function of (x, y) describing optical path depth aberration.
            axis (str, optional): The axis along which the lens is cylindrical ('x' or 'y').
        """
        super().__init__()
        global bd
        from ..util.backend_functions import backend as bd

        self.f = f
        self.aberration = aberration
        self.radius = radius
        self.axis = axis.lower()  # Ensure lowercase for consistency

    def get_transmittance(self, xx, yy, λ):

        t = 1
        if self.aberration is not None:
            t = t * bd.exp(2j * bd.pi / λ * self.aberration(xx, yy))

        if self.radius is not None:
            if self.axis == 'x':
                t = bd.where(xx**2 < self.radius**2, t, bd.zeros_like(xx))
            else:
                t = bd.where(yy**2 < self.radius**2, t, bd.zeros_like(xx))

        self.t = t

        # Apply cylindrical phase factor only along the specified axis
        if self.axis == 'x':
            t = t * bd.exp(-1j * bd.pi / (λ * self.f) * xx**2)
        else:
            t = t * bd.exp(-1j * bd.pi / (λ * self.f) * yy**2)

        return t


class CylindricalLensY(DOE):
    def __init__(self, f, radius=None, aberration=None, axis='y'):
        """
        Creates a cylindrical lens with a focal length equal to f.

        Args:
            f (float): Focal length of the cylindrical lens.
            radius (float, optional): Physical radius of the lens.
            aberration (function, optional): Function of (x, y) describing optical path depth aberration.
            axis (str, optional): The axis along which the lens is cylindrical ('x' or 'y').
        """
        super().__init__()
        global bd
        from ..util.backend_functions import backend as bd

        self.f = f
        self.aberration = aberration
        self.radius = radius
        self.axis = axis.lower()  # Ensure lowercase for consistency

    def get_transmittance(self, xx, yy, λ):

        t = 1
        if self.aberration is not None:
            t = t * bd.exp(2j * bd.pi / λ * self.aberration(xx, yy))

        if self.radius is not None:
            if self.axis == 'x':
                t = bd.where(xx**2 < self.radius**2, t, bd.zeros_like(xx))
            else:
                t = bd.where(yy**2 < self.radius**2, t, bd.zeros_like(xx))

        self.t = t

        # Apply cylindrical phase factor only along the specified axis
        if self.axis == 'x':
            t = t * bd.exp(-1j * bd.pi / (λ * self.f) * xx**2)
        else:
            t = t * bd.exp(-1j * bd.pi / (λ * self.f) * yy**2)

        return t
