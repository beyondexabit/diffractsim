import matplotlib.pyplot as plt
import numpy as np


def plot_field(Field, title):
    plt.figure()
    I1 = np.log(1 + Field)
    plt.imshow(I1)
    if title != None:
        plt.title(title)
    plt.colorbar()




