import tensorflow as tf
from keras import layers

class NeuralNetwork:
    def __init__(self, input_shape, output_shape):
        self.input_shape = input_shape
        self.output_shape = output_shape
        self.model = self.build_model()

    def build_model(self):
        model = tf.keras.Sequential([
            layers.Dense(64, activation='relu', input_shape=self.input_shape),
            layers.Dense(64, activation='relu'),
            layers.Dense(self.output_shape, activation='softmax')
        ])
        model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
        return model

    def train(self, X_train, y_train, epochs=10):
        self.model.fit(X_train, y_train, epochs=epochs)

    def predict(self, X):
        return self.model.predict(X)

if __name__ == "__main__":
    input_shape = (10,)  # Example input shape
    output_shape = 3     # Example output shape
    nn = NeuralNetwork(input_shape, output_shape)
