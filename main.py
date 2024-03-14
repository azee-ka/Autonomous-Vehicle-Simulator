# main.py

import pygame
import sys
import random
from simulation.simulation import RoadSimulation
from neuralNetwork.neural_network import NeuralNetwork

def main():
    # Initialize the neural network
    input_size = 2  # Number of inputs (vision_data in this case)
    hidden_size = 5  # Number of neurons in the hidden layer
    output_size = 2  # Number of outputs (direction_x and direction_y)
    nn = NeuralNetwork(input_size, hidden_size, output_size)

    # Create the road simulation
    simulation = RoadSimulation()

    while True:
        # Get vision data from simulation
        vision_data = simulation.get_vision_data()

        # Use neural network to get controls
        controls = nn.predict(vision_data)
        direction_x = controls[0]
        direction_y = controls[1]

        # Update simulation with controls
        simulation.controllable_car.update(direction_x, direction_y)

        # Run the simulation
        simulation.run()

if __name__ == "__main__":
    main()
