from abc import ABC, abstractmethod
import logging

import numpy as np


class Simulator(ABC):
    def __init__(self, n: int, data: str, log_file: str) -> None:
        super().__init__()
        # logs
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        stdout_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(log_file)
        stdout_handler.setLevel(logging.INFO)
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stdout_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(stdout_handler)
        self.logger.addHandler(file_handler)

        # init state
        self.positions_x = np.loadtxt(data, delimiter=" ", max_rows=n, usecols=1, dtype='float') 
        self.positions_y = np.loadtxt(data, delimiter=" ", max_rows=n, usecols=2, dtype='float')
        self.positions_z = np.loadtxt(data, delimiter=" ", max_rows=n, usecols=3, dtype='float')
        self.velocities_x = np.loadtxt(data, delimiter=" ", max_rows=n, usecols=4, dtype='float')
        self.velocities_y = np.loadtxt(data, delimiter=" ", max_rows=n, usecols=5, dtype='float')
        self.velocities_z = np.loadtxt(data, delimiter=" ", max_rows=n, usecols=6, dtype='float')
        self.masses = np.loadtxt(data, delimiter=" ", max_rows=n, usecols=0, dtype='float')
        self.masses = self.masses[:, np.newaxis]
        
        self.logger.debug("velocities_x=\n{}".format(self.velocities_x))
        self.logger.debug("velocities_y=\n{}".format(self.velocities_y))
        self.logger.debug("velocities_z=\n{}".format(self.velocities_z))
        self.logger.debug("positions_x=\n{}".format(self.positions_x))
        self.logger.debug("positions_y=\n{}".format(self.positions_y))
        self.logger.debug("positions_z=\n{}".format(self.positions_z))

    @abstractmethod
    def step(self) -> None:
        pass
