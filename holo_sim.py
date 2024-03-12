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

# plot the diffraction pattern
#I = F.get_intensity()
#F.plot_intensity(I, square_root = True, units = mm, grid = True, figsize = (14,5), slice_y_pos = 0*mm)


# load the hologram as a phase mask aperture
F.add(ApertureFromImage(
     #amplitude_mask_path= "/Users/jakubkostial/Documents/phd/code/dsim/diffractsim/examples/apertures/white_background.png", 
     phase_mask_path= "/Users/jakubkostial/Documents/phd/code/dsim/myholos/saw_test_phase_pattern_150mp_10gf_square.png", image_size=(10.0 * mm, 10.0 * mm), simulation = F)
)

#/Users/jakubkostial/Documents/phd/code/dsim/myholos/saw_test_phase_pattern_150mp_10gf_square.png
#/Users/jakubkostial/Documents/phd/code/dsim/myholos/snowflake_phase_hologram.png

#/Users/jakubkostial/Documents/phd/code/dsim/myholos/snowflake_phase_hologram_greyscale.png

distance = 10.01*cm
#F.propagate(distance)
# propagate the field
F.add(Lens(f = 10*cm))
F.propagate(distance)

# plot the diffraction pattern
I = F.get_intensity()
print(type(I))

I = np.log(1 + I)

#plt.figure()
#plt.imshow(I)
#plt.colorbar()
#plt.show()

F.plot_intensity(I, square_root = True, units = mm, grid = True, figsize = (14,5), use_log_scale = True)



