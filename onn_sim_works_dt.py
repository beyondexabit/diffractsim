import diffractsim
diffractsim.set_backend("CPU") #Change the string to "CUDA" to use GPU acceleration

from diffractsim import MonochromaticField, nm, mm, cm, um, BinaryGrating, Lens, CylindricalLensX, CylindricalLensY, ApertureFromArray, ApertureFromImage
from diffractsim import MonochromaticField, mm, nm, cm, CustomPhaseRetrieval, ApertureFromImage, ApertureFromArray

import sys
import matplotlib.pyplot as plt
import numpy as np


F = MonochromaticField(
    wavelength = 1500 * nm, extent_x=30. * mm, extent_y=30. * mm, Nx=2048, Ny=2048, intensity = 2.
)


# slm pitch: 8.0 um  ////  8* (54 * 4 = 216) = 1728 um ////1920 x 1080
# dmd pitch: 10.8 um //// 10.8* (40 * 4 = 160) = 1728 um  ////1280 x 800  

# dmd
# macropixel_width = 160
# macropixel_seperation = 80 

# 13824um * 8640

# slm
# macropixel_width = 216
# macropixel_seperation = 108

# 15360 * 8640

# for layer 2:
# 2* 1.3mm = 2.6mm 
# height of slm : 8.64mm 
# 8.64 /3 = 2.88mm / 2 = 1.44mm
# 1080/3 = 360pixels
# need 0.2 mm seperation
# 15360 = 1920
# 2000 = 250pixel seperation


# Plane wave
F.add(ApertureFromImage(
     amplitude_mask_path= "/Users/jakubkostial/Documents/phd/code/dsim/diffractsim/examples/apertures/white_background.png", simulation = F)
)

distance = 10*cm
F.propagate(distance)

# DMD
F.add(ApertureFromArray(
     amplitude_mask = "/Users/jakubkostial/Documents/phd/code/dsim/myholos/testgrating_ti.npy", image_size=(13854 * um, 8640 * um), simulation = F)
)

# 4f system
F.propagate(5*cm)
F.add(Lens(f = 10*cm))
F.propagate(20*cm)
F.add(Lens(f = 10*cm))
F.propagate(5*cm)

# SLM
F.add(ApertureFromArray(
     phase_mask = "/Users/jakubkostial/Documents/phd/code/dsim/myholos/saw_test_phase_pattern_216mp_20gfx_36gfytest.npy", image_size=(15360 * um, 8640 * um), simulation = F)
)

# take Fourier transform
F.propagate(5*cm)
F.add(Lens(f = 10*cm))
F.propagate(10*cm)


# aperture
F.add(ApertureFromArray(
     amplitude_mask = "/Users/jakubkostial/Documents/phd/code/dsim/myholos/aperture1_l.npy", image_size=(30 * mm, 30 * mm), simulation = F)
)


# Centring first order diffractions
F.centre_field(-174, 0)# by pixels

# Cylinder lens summation
F.add(CylindricalLensX(f = 5*cm))
F.propagate(3*cm)

# Centring first order diffractions
F.centre_field(-28, 0)# by pixels

# SESAM skip for now
#F.add(Sesam(tau = 10e-12, Fsat = 1e-3, pulse_length = 10e-10))
# beam splitter / attenuation


# Cylinder lens for expansion
F.add(CylindricalLensX(f = 5*cm))
F.propagate(7.5*cm)
# Centring first order diffractions
F.centre_field(-48, 0)# by pixels


# SLM
F.add(ApertureFromArray(
     phase_mask = "/Users/jakubkostial/Documents/phd/code/dsim/myholos/saw_test_phase_pattern_216mp_20gfx_36gfy_l2t.npy", image_size=(15360 * um, 8640 * um), simulation = F)
)
# take Fourier transform
F.propagate(5*cm)
F.add(Lens(f = 10*cm))
F.propagate(10*cm)

F.centre_field(170, 0)# by pixels


# Cylinder lens summation
F.add(CylindricalLensY(f = 5*cm))
F.propagate(3*cm)

# aperture
F.add(ApertureFromArray(
     amplitude_mask = "/Users/jakubkostial/Documents/phd/code/dsim/myholos/aperture2_l.npy", image_size=(30 * mm, 30 * mm), simulation = F)
)


I1 = F.get_intensity()
# plot the diffraction pattern
I1 = np.log(1 + I1)
F.plot_intensity(I1, square_root = True, units = mm, grid = True, figsize = (14,5), use_log_scale = True)


plt.show()

sys.exit()


'''
# 4f system
F.propagate(5*cm)
F.add(Lens(f = 10*cm))
F.propagate(20*cm)
F.add(Lens(f = 10*cm))
F.propagate(5*cm)
'''

# Field
# DMD
# 4f system: 2x lens
# SLM
# Cylinder lens
# 4f system: 2x lens
# SESAM
# Beam splitter
# SLM 
# CYlinder lens
# 4f system: 2x lens
# CCD



