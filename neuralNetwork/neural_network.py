# neuralNetwork/neural_network.py

import pygame
import random
import sys
import numpy as np

# Define the neural network class
class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # Initialize weights and biases
        self.weights_input_hidden = np.random.randn(self.input_size, self.hidden_size)
        self.bias_input_hidden = np.zeros((1, self.hidden_size))
        self.weights_hidden_output = np.random.randn(self.hidden_size, self.output_size)
        self.bias_hidden_output = np.zeros((1, self.output_size))

    def forward(self, input_data):
        # Forward pass through the network
        hidden_layer_input = np.dot(input_data, self.weights_input_hidden) + self.bias_input_hidden
        hidden_layer_output = self.sigmoid(hidden_layer_input)
        output_layer_input = np.dot(hidden_layer_output, self.weights_hidden_output) + self.bias_hidden_output
        output = self.sigmoid(output_layer_input)
        return output

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def get_weights(self):
        return self.weights_input_hidden, self.bias_input_hidden, self.weights_hidden_output, self.bias_hidden_output

    def set_weights(self, weights_input_hidden, bias_input_hidden, weights_hidden_output, bias_hidden_output):
        self.weights_input_hidden = weights_input_hidden
        self.bias_input_hidden = bias_input_hidden
        self.weights_hidden_output = weights_hidden_output
        self.bias_hidden_output = bias_hidden_output

# Define the car controller class
class CarController:
    def __init__(self, road_simulation):
        self.road_simulation = road_simulation
        self.neural_network = NeuralNetwork(input_size=2, hidden_size=5, output_size=2)  # Input size: 2 (x, y), Output size: 2 (direction_x, direction_y)
        self.vision_radius = 50  # Radius of the vision circle
        self.vision_color = (0, 255, 0, 50)  # Green with transparency

    def update(self):
        # Get the position of the car
        car_center_x, car_center_y = self.road_simulation.controllable_car.rect.center

        # Create a vision circle around the car
        vision_circle = pygame.Surface((self.vision_radius * 2, self.vision_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(vision_circle, self.vision_color, (self.vision_radius, self.vision_radius), self.vision_radius)

        # Get the pixels within the vision circle
        vision_data = pygame.PixelArray(vision_circle)
        vision_pixels = np.array(vision_data)

        # Convert vision pixels to coordinates relative to the car's center
        vision_coordinates = np.argwhere(vision_pixels[:, :, 3] > 0) - [self.vision_radius, self.vision_radius]
        vision_coordinates += [car_center_x, car_center_y]

        # Normalize vision coordinates
        vision_coordinates_norm = vision_coordinates / self.road_simulation.HEIGHT

        # Forward pass through the neural network to get control signals
        control_signals = self.neural_network.forward(vision_coordinates_norm)

        # Update the controllable car based on the control signals
        self.road_simulation.controllable_car.update(control_signals[0, 0], control_signals[0, 1])

        # Update the display with the vision circle
        self.road_simulation.screen.blit(vision_circle, (car_center_x - self.vision_radius, car_center_y - self.vision_radius))
