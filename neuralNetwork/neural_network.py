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
        
    def predict(self, x):
        # Forward pass
        hidden_layer_input = np.dot(x, self.weights_input_hidden)
        hidden_layer_output = self.sigmoid(hidden_layer_input)
        output_layer_input = np.dot(hidden_layer_output, self.weights_hidden_output)
        output = self.sigmoid(output_layer_input)
        
        # Ensure output has at least two elements
        if output.size < 2:
            output = np.append(output, [0] * (2 - output.size))
        
        return output

    
class CarController:
    def __init__(self, road_simulation):
        self.road_simulation = road_simulation
        self.neural_network = NeuralNetwork(input_size=2, hidden_size=5, output_size=2)
        self.vision_radius = 50
        self.vision_color = (0, 255, 0, 50)
        self.last_state = None
        self.last_action = None
        self.total_reward = 0
        self.learning_rate = 0.1
        self.discount_factor = 0.9

    def update(self):
        vision_data = self.road_simulation.get_vision_data()
        control_signals = self.neural_network.predict(vision_data)
        self.road_simulation.controllable_car.update(control_signals[0], control_signals[1])

        # Check for collisions
        collision = any(self.road_simulation.controllable_car.rect.colliderect(other_car.rect) for other_car in self.road_simulation.other_cars)

        # Calculate reward
        reward = -1 if collision else 1

        # Update Q-values
        if self.last_state is not None:
            self.total_reward += reward
            new_state = vision_data
            new_action = control_signals

            if not collision:
                # Update Q-value using Q-learning update rule
                q_value = self.neural_network.forward(np.array([self.last_state]))[0]
                max_q_value = np.max(self.neural_network.forward(np.array([new_state]))[0])
                target_q_value = reward + self.discount_factor * max_q_value
                q_value[self.last_action] += self.learning_rate * (target_q_value - q_value[self.last_action])
                self.neural_network.set_weights(q_value)

            self.last_state = new_state
            self.last_action = new_action

        # Reset if collision
        if collision:
            self.reset()

        # Update display
        car_center_x, car_center_y = self.road_simulation.controllable_car.rect.center
        vision_circle = pygame.Surface((self.vision_radius * 2, self.vision_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(vision_circle, self.vision_color, (self.vision_radius, self.vision_radius), self.vision_radius)
        self.road_simulation.screen.blit(vision_circle, (car_center_x - self.vision_radius, car_center_y - self.vision_radius))

    def reset(self):
        self.last_state = None
        self.last_action = None
        self.total_reward = 0
