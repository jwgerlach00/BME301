import scipy.io
import matplotlib.pyplot as plt
import bme301_utils as bme
import os
from math import radians

if __name__ == '__main__':
    for file in os.listdir('cochlear_files'):

        # Ignore hidden files
        if not file.startswith('.'):

            # Load in target angles and prediction angles from .mat files
            mat = scipy.io.loadmat(os.path.join('cochlear_files', file))
            predictions = mat['angresp'].flatten().tolist()
            targets = mat['angreal'].flatten().tolist()

            # Compute absolute error between real angle and prediction
            errors = [bme.compute_angle_error(p, t) for p, t in zip(predictions, targets)]

            # Plot in polar
            fig = plt.figure()
            ax = fig.add_subplot(projection='polar')
            ax.scatter(list(map(radians, targets)), errors, c=targets, s=[10*e for e in errors],
                       cmap='cool', alpha=0.75)
            ax.set_rticks([0, 15, 30, 45, 60, 75, 90])
            ax.set_thetamin(min(targets))
            ax.set_thetamax(max(targets))
            ax.set_theta_zero_location('N')
            plt.show()
