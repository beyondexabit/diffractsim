import numpy as np
from ..util.backend_functions import backend as bd
from .diffractive_element import DOE
from ..util.image_handling import convert_graymap_image_to_hsvmap_image, rescale_img_to_custom_coordinates, rescale_array_to_custom_coordinates
from PIL import Image
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


"""

MPL 2.0 License 

Copyright (c) 2022, Rafael de la Fuente
All rights reserved.

"""


class ApertureFromArray(DOE):
    def __init__(self, amplitude_mask = None, phase_mask= None, image_size = None, phase_mask_format = 'graymap', amplitude_mask_extent = [0,1], simulation = None):

        """
        Load the image specified at "amplitude_mask_path" as a numpy graymap array represeting the amplitude transmittance of the aperture. 
        The image is centered on the plane and its physical size is specified in image_size parameter as image_size = (float, float)

        - If image_size isn't specified, the image fills the entire aperture plane
        """

        
        global bd
        from ..util.backend_functions import backend as bd


        self.simulation = simulation
        self.amplitude_mask = amplitude_mask
        self.phase_mask = phase_mask
        self.image_size = image_size
        self.phase_mask_format = phase_mask_format
        
        t = 1.
        if self.amplitude_mask != None:
            
            #load the amplitude_mask image
            np_array = np.load(self.amplitude_mask)
            
            if len(np_array.shape) == 2:
                np_array = np.stack([np_array, np_array, np_array], axis = -1)

            min_val = np.min(np_array)
            max_val = np.max(np_array)
            np_array = 254 * (np_array - min_val) / (max_val - min_val)

            img = Image.fromarray(np_array.astype(np.uint8), 'RGB')
            #img = img.convert("RGB")

            rescaled_img = rescale_img_to_custom_coordinates(img, self.image_size , simulation.extent_x,simulation.extent_y, simulation.Nx, simulation.Ny)
            imgRGB = np.asarray(rescaled_img) / 255.0

            t = 0.2990 * imgRGB[:, :, 0] + 0.5870 * imgRGB[:, :, 1] + 0.1140 * imgRGB[:, :, 2]
            t = bd.array(np.flip(t, axis = 0))

            if amplitude_mask_extent != [0,1]:
                t = bd.where((bd.abs(simulation.xx) < image_size[0]/2)   &  (bd.abs(simulation.yy) < image_size[1]/2),   t*(amplitude_mask_extent[1] - amplitude_mask_extent[0]) + amplitude_mask_extent[0], bd.zeros(t.shape))

        if self.phase_mask != None:
            from matplotlib.colors import rgb_to_hsv
            
            #load the phase_mask image
            np_array = np.load(self.phase_mask)

            if len(np_array.shape) == 2:
                np_array = np.stack([np_array, np_array, np_array], axis = -1)
            
            img = Image.fromarray(np_array.astype(np.uint8), 'RGB')

            #img = img.convert("RGB")


            if self.phase_mask_format == 'graymap':
                img = convert_graymap_image_to_hsvmap_image(img)
                
            rescaled_img = rescale_img_to_custom_coordinates(img, self.image_size , simulation.extent_x,simulation.extent_y, simulation.Nx, simulation.Ny)

            imgRGB = np.asarray(rescaled_img) / 255.0

            h = rgb_to_hsv( np.moveaxis(np.array([imgRGB[:, :, 0],imgRGB[:, :, 1],imgRGB[:, :, 2]]) , 0, -1))[:,:,0]
            #h = imgRGB[:,:,0]
            phase_mask = bd.flip(bd.array(h) * 2 * bd.pi - bd.pi, axis = 0)
            t = t*bd.exp(1j *  phase_mask)

            '''
            print(np.shape(t))
            print(np.max(t))
            print(np.min(t))
            print(np.mean(t))

            plt.figure()
            plt.imshow(np.real(t))
            plt.colorbar()
            plt.show()
            '''

        self.t = t

        
    def get_transmittance(self, xx, yy, λ):

        return self.t