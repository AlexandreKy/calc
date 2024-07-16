#!/usr/bin/env python3

import argparse
import logging

from parallel.DistributedSimulator import DistributedSimulator
from single_thread.STSimulator import STSimulator
from utils import Timer


def main(n: int, steps: int, parallelism: bool, data: str, log_file: str, compare: bool) -> None:
    # logs
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    stdout_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(log_file)
    stdout_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stdout_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)
    logger.addHandler(file_handler)

    # initialisation
    logger.info("INITIALISATION: start")
    if parallelism:
        simulator = DistributedSimulator(n, data, log_file)
    else:
        simulator = STSimulator(n, data, log_file)
    if compare:
        comparator = STSimulator(n, data, False)
    # simulator = STSimulator(n, data)
    timer = Timer.Timer(log_file)
    logger.info("INITIALISATION: end")

    # run
    for i in range(steps):
        timer.sample_before()
        logger.info("STEP %i: start", i)
        simulator.step()
        if compare:
            comparator.step()
        timer.sample_after()
        logger.info("STEP %i: end", i)
    logging.info("\n __________________ SIMULATION DONE __________________\n")
    if len(timer.fps_list) > 0:
        logging.info("avg_fps = %f", timer.get_avg_fps())

if __name__ == "__main__":

    # Initialize parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", required=True, type=int, help = "number of particles")
    parser.add_argument("-s", "--steps", default=50, type=int, help = "number of steps")
    parser.add_argument("-l", "--log_file", required=False, default="./logs/default.log", type=str, help = "log file path")
    parser.add_argument("-p", required=False, action='store_true', help = "use parallelism through dask")
    parser.add_argument("--data", required=False, type=str, default='./resources/particles.csv', help = "path to the csv file containing the system initial state")
    parser.add_argument("-c", "--compare", required=False, action='store_true', help = "compare chosen model's values with single_thread's values")
    args = parser.parse_args()

    main(args.n, args.steps, args.p, args.data, args.log_file, args.compare)
