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

def func(x):
     a = 0.13435333 
     b = 0.68009031
     return a * np.log(x) + b

def sesam_approx(Field):
     # Vectorize the function for element-wise operation
     # Fsat = 0.5j/m2
     # Returns transmission values
     ratios = Field / 0.5
     vfunc = np.vectorize(func)
     # Apply the function to the array
     transmittances = vfunc(ratios)  # Pass additional arguments for a and b
     # Replace negative values with 0
     transmittances[transmittances < 0] = 0
     if (transmittances > 1).any():
          print('\n Input Power Too High !!!\n')
          sys.exit()
     return transmittances


F = MonochromaticField(
    wavelength = 1550 * nm, extent_x=30. * mm, extent_y=30. * mm, Nx=2048, Ny=2048, intensity = 0.05
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


#for i in range(10):


F = MonochromaticField(
     wavelength = 1550 * nm, extent_x=30. * mm, extent_y=30. * mm, Nx=2048, Ny=2048, intensity = 0.05
)

# Plane wave
#F.add(ApertureFromImage(amplitude_mask_path= "/Users/jakubkostial/Documents/phd/code/dsim/diffractsim/examples/apertures/white_background.png", simulation = F))


#SMF amplitude mask
F.add(ApertureFromArray(
     amplitude_mask = "/Users/jakubkostial/Documents/phd/code/onn_simulation/smf_amplitude_mask.npy", image_size=(13854 * um, 8640 * um), simulation = F)
)

distance = 10*cm
#F.propagate(distance)

# DMD
F.add(ApertureFromArray(
     amplitude_mask = "/Users/jakubkostial/Documents/phd/code/dsim/myholos/testgrating_ti.npy", image_size=(13854 * um, 8640 * um), simulation = F)
)

# 4f system

'''
F.propagate(5*cm)
F.add(Lens(f = 10*cm))
F.propagate(20*cm)
F.add(Lens(f = 10*cm))
F.propagate(5*cm) 
'''


# SLM
F.add(ApertureFromArray(phase_mask = "/Users/jakubkostial/Documents/phd/code/slm_matrix_gen-main/matrices_dsim_scaling/l1/phase_pattern_l1_20gfx-46gfy_1_0.1_0.8_0.3_0_0.6.npy", image_size=(15360 * um, 8640 * um), simulation = F))
# F.add(ApertureFromArray(phase_mask = "/Users/jakubkostial/Documents/phd/code/slm_matrix_gen-main/matrices_dsim_scaling/l1/phase_pattern_l1_20gfx-46gfy_ones.npy", image_size=(15360 * um, 8640 * um), simulation = F))

# take Fourier transform
# F.propagate(5*cm)
F.add(Lens(f = 10*cm))
F.propagate(10*cm)



# aperture
F.add(ApertureFromArray(
     amplitude_mask = "/Users/jakubkostial/Documents/phd/code/dsim/myholos/aperture1_l.npy", image_size=(30 * mm, 30 * mm), simulation = F)
)

I1 = F.get_intensity()
#plot_field(I1, "Fourier Transform")


# Centring first order diffractions
F.centre_field(-162, 0)# by pixels
I1 = F.get_intensity()
plot_field(I1, "after centering")


# Cylinder lens summation
#F.add(CylindricalLensX(f = 10*cm))


F.propagate(10*cm)

#F.centre_field(-135, 0)# by pixels

I1 = F.get_intensity()
plot_field(I1, "summation before aperture")


# aperture
#F.add(ApertureFromArray(     amplitude_mask = "/Users/jakubkostial/Documents/phd/code/ff_project/matrix_generation_dmd/repo/narrow_slit_30pix.npy", image_size=(30 * mm, 30 * mm), simulation = F))

F.propagate(20*cm)
I1 = F.get_intensity()
plot_field(I1, "summation after aperture")




plt.show()
sys.exit()     




F.propagate(3*cm)
F.add(Lens(f = (3.0)*cm))
#I1 = np.log(1 + I1)
I1 = F.get_intensity()
#plot_field(I1, "propagation")

F.propagate(5*cm)

I1 = F.get_intensity()
#I1 = np.log(1 + I1)
plot_field(I1, "propagation")


plt.show()
sys.exit()





F.centre_field(-24, 0)# by pixels
# plot the diffraction pattern
I1 = F.get_intensity()
plot_field(I1, "First Matmul")


# Cylinder lens 
F.add(CylindricalLensX(f = -0.0001*cm))
F.propagate(5*cm)
# plot the diffraction pattern
I1 = F.get_intensity()
I1 = np.log(1 + I1)
plot_field(I1, "Summation")



plt.show()
sys.exit()





# Pixels are already in W/m2
F.plot_intensity(I1, square_root = True, units = mm, grid = True, figsize = (14,5), use_log_scale = True)

np.seterr(invalid='ignore')  # Suppress warnings about invalid values in log
# Apply the function to the array
sesam_field = sesam_approx(I1) 
F.update_field(sesam_field)


I1 = F.get_intensity()
#plot_field(I1, "Sesam Approximation")



#I1 = np.log(1 + I1)
F.plot_intensity(I1, square_root = True, units = mm, grid = True, figsize = (14,5), use_log_scale = True)
# beam splitter / attenuation

# Cylinder lens for expansion
F.add(CylindricalLensX(f = 5*cm))
F.propagate(7.5*cm)
# Centring first order diffractions
F.centre_field(-48, 0)# by pixels

I1 = F.get_intensity()
plot_field(I1, "pre holo 2 expansion")


# SLM - second matmul
F.add(ApertureFromArray(
     phase_mask = "/Users/jakubkostial/Documents/phd/code/dsim/good_holos/saw_test_phase_pattern_216mp_20gfx_36gfy_l2t.npy", image_size=(15360 * um, 8640 * um), simulation = F)
)


# take Fourier transform
F.propagate(5*cm)

F.add(Lens(f = 10*cm))

F.propagate(10*cm)
F.centre_field(170, 0)# by pixels

#I1 = F.get_intensity()
#plot_field(I1, "Post Holo 2 Lens F transform")


# Cylinder lens summation
F.add(CylindricalLensY(f = 5*cm))


#for i in range(20):
#F.propagate(0.5*cm)

F.propagate(3*cm)
# aperture
F.add(ApertureFromArray( amplitude_mask = "/Users/jakubkostial/Documents/phd/code/dsim/myholos/aperture2_l.npy", image_size=(30 * mm, 30 * mm), simulation = F))


I1 = F.get_intensity()
# plot the diffraction pattern
#I1 = np.log(1 + I1)
#F.plot_intensity(I1, square_root = True, units = mm, grid = True, figsize = (14,5), use_log_scale = True)
plot_field(I1, "Output ")

#plot_field(I1[1005:1045, 800:840], "Output 1 ")
#plot_field(I1[1005:1045, 1160:1200], "Output 2")
#plot_field(I1[row_start:row_end, column_start:column_end], "Output ")


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



