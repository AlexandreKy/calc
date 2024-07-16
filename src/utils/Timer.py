import logging
import time


class Timer:
    
    def __init__(self, log_file: str) -> None:
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

        self._durations = []
        self.fps_list = []
        self._current_fps = 0.
        self._t_start = None
        self._t_end = None

    def sample_before(self) -> None:
        self._t_start = time.time()
    
    def sample_after(self) -> None:
        self._t_end = time.time()
        self._durations.append(self._t_end - self._t_start)
        if len(self._durations) >= 10:
            durations_mean = sum(self._durations) / len(self._durations)
            self._current_fps = 1. / durations_mean
            self.fps_list.append(self._current_fps)
            self._durations.clear()
            self.logger.info("current_fps= %f", self._current_fps)

    def get_avg_fps(self) -> float:
        return sum(self.fps_list) / len(self.fps_list)
