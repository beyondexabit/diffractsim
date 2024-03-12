import diffractsim
diffractsim.set_backend("CPU") #Change the string to "CUDA" to use GPU acceleration

from diffractsim import MonochromaticField, ApertureFromImage, Lens, nm, mm, cm

F = MonochromaticField(
    wavelength=488 * nm, extent_x=27. * mm, extent_y=27. * mm, Nx=2000, Ny=2000,intensity = 0.2
)

F.add(ApertureFromImage("/Users/jakubkostial/Documents/phd/code/dsim/diffractsim/examples/apertures/QWT.png", image_size=(15 * mm, 15 * mm), simulation = F))


distance = 10


for i in range(5):
    F.add(Lens(f = distance*cm))
    F.propagate(distance*cm)

    I = F.get_intensity()
    F.plot_intensity(I, square_root = True, units = mm, grid = True, figsize = (14,5), slice_y_pos = 0*mm)



'''
F.add(Lens(f = distance*cm))
F.propagate(distance*cm)

I = F.get_intensity()
F.plot_intensity(I, square_root = True, units = mm, grid = True, figsize = (14,5), slice_y_pos = 0*mm)
'''


#rgb = F.get_colors()
#F.plot_colors(rgb, xlim=[-8*mm,8*mm], ylim=[-8*mm,8*mm])


