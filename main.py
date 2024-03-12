from simulator.simulator import Simulator
from neural_network.model import NeuralNetwork
from neural_network.training import Trainer

if __name__ == "__main__":
    # Initialize simulator, neural network, and trainer
    sim = Simulator()
    input_shape = (10,)  # Example input shape
    output_shape = 3     # Example output shape
    nn = NeuralNetwork(input_shape, output_shape)
    trainer = Trainer(nn, sim)

    # Run the simulator and train the neural network
    sim.run()
    trainer.train_model(num_samples=1000, epochs=10)
