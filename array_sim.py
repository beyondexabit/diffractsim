import diffractsim
diffractsim.set_backend("CPU") #Change the string to "CUDA" to use GPU acceleration

from diffractsim import MonochromaticField, nm, mm, cm, BinaryGrating, Lens
from diffractsim import MonochromaticField, mm, nm, cm, CustomPhaseRetrieval, ApertureFromImage, ApertureFromArray
import sys
import matplotlib.pyplot as plt
import numpy as np


F = MonochromaticField(
    wavelength = 1500 * nm, extent_x=30. * mm, extent_y=30. * mm, Nx=2048, Ny=2048, intensity = 2.
)


'''
# load the hologram as a phase mask aperture
F.add(ApertureFromArray(
     phase_mask = "/Users/jakubkostial/Documents/phd/code/dsim/myholos/saw_test_phase_pattern_150mp_10gf.npy", image_size=(10.0 * mm, 10.0 * mm), simulation = F)
)

'''
F.add(ApertureFromArray(
    amplitude_mask = "/Users/jakubkostial/Documents/phd/code/dsim/myholos/dmdtestgrating.npy", image_size = (10 * mm, 10 * mm), simulation = F)
)


distance = 10.01*cm
F.propagate(distance)

#F.add(Lens(f = 10*cm))
F.propagate(distance)

# plot the diffraction pattern
I = F.get_intensity()

I = np.log(1 + I)
F.plot_intensity(I, square_root = True, units = mm, grid = True, figsize = (14,5), use_log_scale = True)
