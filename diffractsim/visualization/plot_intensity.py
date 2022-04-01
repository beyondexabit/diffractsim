import matplotlib.pyplot as plt
import numpy as np
from ..util.constants import *


def plot_intensity(self, I, square_root = False, figsize=(7, 6), 
                  xlim=None, ylim=None, grid = False, text = None, units = mm,
                  slice_y_pos = None):
    """visualize the diffraction pattern intesity with matplotlib"""
    
    from ..util.backend_functions import backend as bd
    plt.style.use("dark_background")

    if square_root == False:
        if bd != np:
            print("hola")
            I = I.get()
        else:
            I = I

    else:
        if bd != np:
            I = np.sqrt(I.get())
        else:
            I = np.sqrt(I)


    fig = plt.figure(figsize=figsize)

    if slice_y_pos == None:
        ax = fig.add_subplot(1, 1, 1)
    else:
        ax = fig.add_subplot(1, 2, 1)

    


    if grid == True:
        ax.grid(alpha =0.2)

    if xlim != None:
        ax.set_xlim(np.array(xlim)/units)

    if ylim != None:
        ax.set_ylim(np.array(ylim)/units)

    if units == mm:
        ax.set_xlabel("[mm]")
        ax.set_ylabel("[mm]")
    elif units == um:
        ax.set_xlabel("[um]")
        ax.set_ylabel("[um]")
    elif units == cm:
        ax.set_xlabel("[cm]")
        ax.set_ylabel("[cm]")
    elif units == nm:
        ax.set_xlabel("[nm]")
        ax.set_ylabel("[nm]")
    elif units == m:
        ax.set_xlabel("[m]")
        ax.set_ylabel("[m]")


    if text == None:
        ax.set_title("Screen distance = " + str(self.z * 100) + " cm")
    else: 
        ax.set_title(text)





    im = ax.imshow(
        I, cmap= 'inferno',
        extent=[
            float(self.x[0]) / units,
            float(self.x[-1] + self.dx) / units,
            float(self.y[0] )/ units,
            float(self.y[-1] + self.dy) / units,
        ],
        interpolation="spline36", origin = "lower"
    )

    
    cb = fig.colorbar(im, orientation = 'vertical')

    if square_root == False:
        cb.set_label(r'Intensity $\left[W / m^2 \right]$', fontsize=10, labelpad =  10 )
    else:
        cb.set_label(r'Square Root Intensity $\left[ \sqrt{W / m^2 } \right]$', fontsize=10, labelpad =  10 )
    ax.set_aspect('equal')
    


    if slice_y_pos != None:
        ax_slice = fig.add_subplot(1, 2, 2)
        plt.subplots_adjust(wspace=0.3)
        ax_slice.set_title("X slice")
        #plt.subplots_adjust(right=2)

        ax_slice.plot(self.y/units, I[np.argmin(abs(self.y-slice_y_pos)),:]**2)
        ax_slice.set_ylabel(r'Intensity $\left[W / m^2 \right]$')

        if grid == True:
            ax_slice.grid(alpha =0.2)

        if xlim != None:
            ax_slice.set_xlim(np.array(xlim)/units)

        if units == mm:
            ax_slice.set_xlabel("[mm]")
        elif units == um:
            ax_slice.set_xlabel("[um]")
        elif units == cm:
            ax_slice.set_xlabel("[cm]")
        elif units == nm:
            ax_slice.set_xlabel("[nm]")
        elif units == m:
            ax_slice.set_xlabel("[m]")

    plt.show()
