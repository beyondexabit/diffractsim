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
    wavelength = 1550 * nm, extent_x=30. * mm, extent_y=30. * mm, Nx=2048, Ny=2048, intensity = 0.05
)

#SMF amplitude mask
F.add(ApertureFromArray(
     amplitude_mask = "/Users/jakubkostial/Documents/phd/code/onn_simulation/smf_amplitude_mask.npy", image_size=(13854 * um, 8640 * um), simulation = F)
)

distance = 10*cm
#F.propagate(distance)

# SLM
F.add(ApertureFromArray(phase_mask = "/Users/jakubkostial/Documents/phd/code/slm_matrix_gen-main/matrices_dsim_scaling/l1/phase_pattern_l1_20gfx-46gfy_1_0.1_0.8_0.3_0_0.6.npy", image_size=(15360 * um, 8640 * um), simulation = F))
# F.add(ApertureFromArray(phase_mask = "/Users/jakubkostial/Documents/phd/code/slm_matrix_gen-main/matrices_dsim_scaling/l1/phase_pattern_l1_20gfx-46gfy_ones.npy", image_size=(15360 * um, 8640 * um), simulation = F))

# take Fourier transform
F.add(Lens(f = 10*cm))
F.propagate(10*cm)

# aperture, get 1st order
F.add(ApertureFromArray(amplitude_mask = "/Users/jakubkostial/Documents/phd/code/dsim/myholos/aperture1_l.npy", image_size=(30 * mm, 30 * mm), simulation = F))


I1 = F.get_intensity()
plot_field(I1, "First Holo 1 output")


F.add(CylindricalLensX(f = 10*cm))
F.propagate(10*cm)
F.centre_field(-182, 0)# by pixels


# aperture
#F.add(ApertureFromArray( amplitude_mask = "/Users/jakubkostial/Documents/phd/code/ff_project/matrix_generation_dmd/repo/narrow_slit_10pix.npy", image_size=(30 * mm, 30 * mm), simulation = F))

I1 = F.get_intensity()
plot_field(I1, "First Holo 1 output")

plt.show()
sys.exit()

F.propagate(10*cm)

I1 = F.get_intensity()
plot_field(I1, "First Holo 1 output")

F.propagate(10*cm)

I1 = F.get_intensity()
plot_field(I1, "First Holo 1 output")

plt.show()
sys.exit()



F.add(Lens(f = 10*cm))
F.propagate(10*cm)

F.propagate(10*cm)
# plot the diffraction pattern
I1 = F.get_intensity()
plot_field(I1, "First Holo 1 output")


F.add(CylindricalLensX(f = 10*cm))
F.propagate(10*cm)
# plot the diffraction pattern
I1 = F.get_intensity()
plot_field(I1, "First Holo 1 output")


plt.show()
sys.exit()

F.propagate(10*cm)
F.add(Lens(f = 10*cm))
F.propagate(10*cm)
# plot the diffraction pattern
I1 = F.get_intensity()
plot_field(I1, "First Holo 1 output")


F.add(CylindricalLensX(f = 10*cm))

for i in range(10):
     F.propagate(0.5*i*cm)
     # plot the diffraction pattern
     I1 = F.get_intensity()
     plot_field(I1, "First Holo 1 output")


plt.show()
sys.exit()

# Cylinder lens summation
F.add(CylindricalLensX(f = 10*cm))


F.propagate(10*cm)
I1 = F.get_intensity()
plot_field(I1, "summation")

#F.propagate(10*cm) # needs to be f1 + f2



# aperture
#F.add(ApertureFromArray( amplitude_mask = "/Users/jakubkostial/Documents/phd/code/ff_project/matrix_generation_dmd/repo/narrow_slit_2pix.npy", image_size=(30 * mm, 30 * mm), simulation = F))


F.propagate(1*cm) # needs to be f1 + f2


I1 = F.get_intensity()
plot_field(I1, "summation")

# Cylinder lens expansion
F.add(CylindricalLensX(f = 1*cm)) # - focal length of the lens, f2 = h2/h1*f1

F.propagate(10*cm)
I1 = F.get_intensity()
plot_field(I1, "prop")

F.propagate(10*cm)
I1 = F.get_intensity()
plot_field(I1, "prop")




plt.show()
sys.exit()




I1 = F.get_intensity()
plot_field(I1, "summation")

# Cylinder lens expansion
F.add(CylindricalLensX(f = 2*cm))

F.propagate(20*cm)
I1 = F.get_intensity()
plot_field(I1, "Expansion")

F.propagate(5*cm)
I1 = F.get_intensity()
#plot_field(I1, "summation")
