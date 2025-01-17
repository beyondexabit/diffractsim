import diffractsim
diffractsim.set_backend("CPU")

from diffractsim import MonochromaticField, mm, nm, cm, CustomPhaseRetrieval, ApertureFromImage, FourierPhaseRetrieval
import sys

#Note: CustomPhaseRetrieval requires autograd which is not installed by default with diffractsim. 
# To install autograd, type: 'pip install autograd'


'''
# Generate a 30cm plane phase hologram
distance = 30*cm
PR = FourierPhaseRetrieval(wavelength=532 * nm, z = distance, extent_x=30 * mm, extent_y=30 * mm, Nx=2048, Ny=2048)

PR.set_source_amplitude(amplitude_mask_path= "/Users/jakubkostial/Documents/phd/code/dsim/diffractsim/examples/apertures/white_background.png", image_size=(15.0 * mm, 15.0 * mm))
PR.set_target_amplitude(amplitude_mask_path= "/Users/jakubkostial/Documents/phd/code/dsim/diffractsim/examples/apertures/USAF_test.png", image_size=(15.0 * mm, 15.0 * mm))

PR.retrieve_phase_mask(max_iter = 15, method = 'Adam-Optimizer')
'''
# Generate a Fourier plane phase hologram

PR = FourierPhaseRetrieval(target_amplitude_path = '/Users/jakubkostial/Documents/phd/code/dsim/diffractsim/examples/apertures/snowflake.png', new_size= (400,400), pad = (200,200))
PR.retrieve_phase_mask(max_iter = 20, method = 'Gerchberg-Saxton')
PR.save_retrieved_phase_as_image('snowflake_phase_hologram_greyscale.png')


sys.exit()

PR.save_retrieved_phase_as_image('USAF_hologram.png')



#Add a plane wave

F = MonochromaticField(
    wavelength=532 * nm, extent_x=30 * mm, extent_y=30 * mm, Nx=2048, Ny=2048, intensity = 0.001
)


F.add(ApertureFromImage(
     amplitude_mask_path= "/Users/jakubkostial/Documents/phd/code/dsim/diffractsim/examples/apertures/white_background.png", 
     image_size=(15.0    * mm, 15.0  * mm), simulation = F)
)



F.add(ApertureFromImage(
     phase_mask_path= "USAF_hologram.png", 
     image_size=(30.0   * mm, 30.0 * mm), simulation = F)
)



# plot phase at z = 0
E = F.get_field()
F.plot_phase(E, grid = True, units = mm)

# propagate field 30*cm
F.propagate(distance)


# plot reconstructed image
rgb = F.get_colors()
F.plot_colors(rgb)
