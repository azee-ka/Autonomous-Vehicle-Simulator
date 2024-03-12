import numpy as np
from .model import NeuralNetwork
from simulator.simulator import Simulator

class Trainer:
    def __init__(self, model, simulator):
        self.model = model
        self.simulator = simulator

    def preprocess_data(self, data):
        normalized_data = (data - np.min(data)) / (np.max(data) - np.min(data))
        return normalized_data

    def generate_training_data(self, num_samples):
        X_train = []
        y_train = []
        for _ in range(num_samples):
            # Example: Get state from the simulator
            state = self.simulator.get_state()
            # Example: Get action from the simulator
            action = self.simulator.get_action()
            X_train.append(state)
            y_train.append(action)
        X_train = np.array(X_train).astype('float32')
        y_train = np.array([float(y) if y != 'none' else 0.0 for y in y_train]).astype('float32')
        return X_train, y_train

    def train_model(self, num_samples, epochs):
        for _ in range(epochs):
            X_train, y_train = self.generate_training_data(num_samples)
            X_train = self.preprocess_data(X_train)
            self.model.train(X_train, y_train)

if __name__ == "__main__":
    input_shape = (10,)  # Example input shape
    output_shape = 3     # Example output shape
    nn = NeuralNetwork(input_shape, output_shape)
    sim = Simulator()
    trainer = Trainer(nn, sim)
    trainer.train_model(num_samples=1000, epochs=10)
