import diffractsim
diffractsim.set_backend("CPU") #Change the string to "CUDA" to use GPU acceleration
from diffractsim import MonochromaticField, nm, mm, cm, um, BinaryGrating, Lens, CylindricalLensX, CylindricalLensY, ApertureFromArray, ApertureFromImage
from diffractsim import MonochromaticField, mm, nm, cm, CustomPhaseRetrieval, ApertureFromImage, ApertureFromArray
import sys
import matplotlib.pyplot as plt
import numpy as np


def plot_field(Field, title):
     plt.figure()
     I1 = np.log(1 + Field)
     plt.imshow(I1)
     if title != None:
          plt.title(title)
     plt.colorbar()


F = MonochromaticField(
    wavelength = 1500 * nm, extent_x=30. * mm, extent_y=30. * mm, Nx=2048, Ny=2048, intensity = 0.05
)


# Plane wave
F.add(ApertureFromImage(
     amplitude_mask_path= "/Users/jakubkostial/Documents/phd/code/dsim/diffractsim/examples/apertures/white_background.png", simulation = F)
)

distance = 10*cm
F.propagate(distance)

F.add(ApertureFromArray(
     phase_mask = "/Users/jakubkostial/Documents/phd/code/slm_matrix_gen-main/matrices_dsim_scaling/l2/phase_pattern_l2_20gfx-36gfy_1_0.1_0.8_0.3_0_0.6.npy", image_size=(15360 * um, 8640 * um), simulation = F)
)

# take Fourier transform
F.propagate(5*cm)
F.add(Lens(f = 10*cm))
F.propagate(10*cm)


I1 = F.get_intensity()
I1 = np.log(1 + I1)
plot_field(I1, "Holo 1 output")



plt.show()
sys.exit()




