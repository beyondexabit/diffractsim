import diffractsim
diffractsim.set_backend("CPU") #Change the string to "CUDA" to use GPU acceleration
from diffractsim import MonochromaticField, nm, mm, cm, um, BinaryGrating, Lens, CylindricalLensX, CylindricalLensY, ApertureFromArray, ApertureFromImage
from diffractsim import MonochromaticField, mm, nm, cm, CustomPhaseRetrieval, ApertureFromImage, ApertureFromArray
import sys
import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import fft2, fftshift, ifft2 # Python DFT

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
#F.add(ApertureFromArray(amplitude_mask = "/Users/jakubkostial/Documents/phd/code/onn_simulation/smf_amplitude_mask.npy", image_size=(13854 * um, 8640 * um), simulation = F))
F.add(ApertureFromImage(amplitude_mask_path= "/Users/jakubkostial/Documents/phd/code/dsim/diffractsim/examples/apertures/white_background.png", simulation = F))

distance = 10*cm
#F.propagate(distance)

# SLM
F.add(ApertureFromArray(phase_mask = "/Users/jakubkostial/Documents/phd/code/slm_matrix_gen-main/matrices_dsim_scaling/l1/phase_pattern_l1_20gfx-46gfy_ones.npy", image_size=(15360 * um, 8640 * um), simulation = F))
# F.add(ApertureFromArray(phase_mask = "/Users/jakubkostial/Documents/phd/code/slm_matrix_gen-main/matrices_dsim_scaling/l1/phase_pattern_l1_20gfx-46gfy_ones.npy", image_size=(15360 * um, 8640 * um), simulation = F))

F.propagate(10*cm)
# take Fourier transform
F.add(Lens(f = 10*cm))
F.propagate(10*cm)

holo = np.load("/Users/jakubkostial/Documents/phd/code/slm_matrix_gen-main/matrices_dsim_scaling/l1/phase_pattern_l1_20gfx-46gfy_ones.npy")
plot_field(holo, "First Holo 1 output")


# aperture, get 1st order
F.add(ApertureFromArray(amplitude_mask = "/Users/jakubkostial/Documents/phd/code/dsim/myholos/aperture1_l.npy", image_size=(30 * mm, 30 * mm), simulation = F))

I1 = F.get_intensity()
plot_field(I1, "First Holo 1 output")

#Field = fft2(I1)                         
#Field = fftshift(Field)
#P = np.abs(Field)  


#plot_field(, "FFT of First Holo 1 output")


#F.propagate(10*cm)

# Corrective holograms
F.add(ApertureFromArray(phase_mask = "/Users/jakubkostial/Documents/phd/code/dsim/good_holos/fft_corrective.npy", image_size=(15360 * um, 8640 * um), simulation = F))

F.add(Lens(f = 10*cm))
# take Fourier transform
F.propagate(10*cm)
I1 = F.get_intensity()
plot_field(I1, "Corrective Holo 1 output")

F.propagate(10*cm)
I1 = F.get_intensity()
plot_field(I1, "Corrective Holo 1 output")


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