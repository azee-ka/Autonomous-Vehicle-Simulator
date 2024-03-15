# main.py

import pygame
import sys
import random
from simulation.simulation import RoadSimulation
from neuralNetwork.neural_network import NeuralNetwork, CarController

def main():
    # Create the road simulation
    simulation = RoadSimulation()

    # Create the car controller
    car_controller = CarController(simulation)

    while True:
        # Update the car controller
        car_controller.update()

        # Run the simulation
        simulation.run()


if __name__ == "__main__":
    main()
