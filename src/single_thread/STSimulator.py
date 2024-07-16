import logging
import numpy as np

from common.Simulator import Simulator


class STSimulator(Simulator):

    def step(self):

        distances_x = np.array([self.positions_x - self.positions_x[j] for j in range(len(self.positions_x))])
        distances_y = np.array([self.positions_y - self.positions_y[j] for j in range(len(self.positions_y))])
        distances_z = np.array([self.positions_z - self.positions_z[j] for j in range(len(self.positions_z))])

        for i in range(len(distances_x)):
            for j in range(len(distances_x)):
                if i == j:
                    distances_x[i, j] = np.nan

        distances = np.square(distances_x) + np.square(distances_y) + np.square(distances_z)

        distances = np.where(np.abs(distances) > 1. , (np.multiply(distances, np.sqrt(distances))), distances)
        distances = np.where((np.abs(distances) < 1.) & (distances != np.nan) , 1., distances)
        distances = 10./distances

        accelerations_x = np.multiply(distances_x, distances)
        accelerations_x = np.multiply(accelerations_x, self.masses)
        accelerations_y = np.multiply(distances_y, distances)
        accelerations_y = np.multiply(accelerations_y, self.masses)
        accelerations_z = np.multiply(distances_z, distances)
        accelerations_z = np.multiply(accelerations_z, self.masses)

        # Accelerations exerced on particle i by all the other particles 
        summed_accelerations_x = np.nansum(accelerations_x, axis = 1)
        summed_accelerations_y = np.nansum(accelerations_y, axis = 1)
        summed_accelerations_z = np.nansum(accelerations_z, axis = 1)

        # Update positions and speeds 
        self.velocities_x += summed_accelerations_x * 2.
        self.velocities_y += summed_accelerations_y * 2.
        self.velocities_z += summed_accelerations_z * 2.
        self.positions_x += self.velocities_x * 0.1
        self.positions_y += self.velocities_y * 0.1
        self.positions_z += self.velocities_z * 0.1
        
        self.logger.debug("velocities_x=\n{}".format(self.velocities_x))
        self.logger.debug("velocities_y=\n{}".format(self.velocities_y))
        self.logger.debug("velocities_z=\n{}".format(self.velocities_z))
        self.logger.debug("positions_x=\n{}".format(self.positions_x))
        self.logger.debug("positions_y=\n{}".format(self.positions_y))
        self.logger.debug("positions_z=\n{}".format(self.positions_z))
