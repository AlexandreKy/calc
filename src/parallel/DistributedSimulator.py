import dask.array as da
import numpy as np

from common.Simulator import Simulator


class DistributedSimulator(Simulator):

    def __init__(self, n: int, data: str, log_file: str) -> None:
        super().__init__(n, data, log_file)
        # Converting the numpy arrays into dask arrays
        self.positions_x = da.from_array(self.positions_x, chunks=5)
        self.positions_y = da.from_array(self.positions_y, chunks=5)
        self.positions_z = da.from_array(self.positions_z, chunks=5)
        self.velocities_x = da.from_array(self.velocities_x, chunks=5)
        self.velocities_y = da.from_array(self.velocities_y, chunks=5)
        self.velocities_z = da.from_array(self.velocities_z, chunks=5)
        self.masses = da.from_array(self.masses, chunks=5)

        self.logger.debug("velocities_x=\n{}".format(self.velocities_x))
        self.logger.debug("velocities_y=\n{}".format(self.velocities_y))
        self.logger.debug("velocities_z=\n{}".format(self.velocities_z))
        self.logger.debug("positions_x=\n{}".format(self.positions_x))
        self.logger.debug("positions_y=\n{}".format(self.positions_y))
        self.logger.debug("positions_z=\n{}".format(self.positions_z))
        self.logger.debug("masses=\n{}".format(self.masses))
    
    def step(self) -> None:
        distances_x = [self.positions_x - self.positions_x[j] for j in range(len(self.positions_x))]
        distances_y = [self.positions_y - self.positions_y[j] for j in range(len(self.positions_y))]
        distances_z = [self.positions_z - self.positions_z[j] for j in range(len(self.positions_z))]

        distances_x = da.stack(distances_x, axis=0)
        distances_y = da.stack(distances_y, axis=0)
        distances_z = da.stack(distances_z, axis=0)

        for i in range(len(distances_x)):
            for j in range(len(distances_x)):
                if i == j:
                    distances_x[i, j] = np.nan

        distances = da.square(distances_x) + da.square(distances_y) + da.square(distances_z)

        distances = da.where(da.abs(distances) > 1. , (da.multiply(distances, da.sqrt(distances))), distances)
        distances = da.where((da.abs(distances) < 1.) & (distances != np.nan) , 1., distances)
        distances = 10./distances

        accelerations_x = da.multiply(distances_x, distances)
        accelerations_x = da.multiply(accelerations_x, self.masses)
        accelerations_y = da.multiply(distances_y, distances)
        accelerations_y = da.multiply(accelerations_y, self.masses)
        accelerations_z = da.multiply(distances_z, distances)
        accelerations_z = da.multiply(accelerations_z, self.masses)

        # Accelerations exerced on particle i by all the other particles 
        summed_accelerations_x = da.nansum(accelerations_x, axis = 1)
        summed_accelerations_y = da.nansum(accelerations_y, axis = 1)
        summed_accelerations_z = da.nansum(accelerations_z, axis = 1)

        # Update positions and speeds 
        self.velocities_x += summed_accelerations_x * 2.
        self.velocities_y += summed_accelerations_y * 2.
        self.velocities_z += summed_accelerations_z * 2.
        self.positions_x += self.velocities_x * 0.1
        self.positions_y += self.velocities_y * 0.1
        self.positions_z += self.velocities_z * 0.1

        self.positions_x.compute()
        self.positions_y.compute()
        self.positions_z.compute()
