import numpy as np
import pandas as pd
from backgammon import backgammon
import random

# Instantiate the backgammon object
game = backgammon()

# Iterate over the moves until a winner is determined
while game.get_winner() is None:
    # Iterate over the moves directly from the moves attribute
    for move in game.moves:
        # Randomly generate a scalar value
        score = random.random()

        # Call the store_move function to store the move and scalar value
        game.score_move(move, score)

    # Check if a winner is determined after each iteration
    if game.get_winner() is not None:
        break


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def sigmoid_derivative(z):
    return z * (1 - z)


def normalize(data):
    for i in range(data.shape[1]):
        data[:, i] = (data[:, i] - np.mean(data[:, i])) / np.std(data[:, i])

    return data


def train_mlp(inputs, outputs, hidden_neurons, epochs, learning_rate):
    input_neurons, output_neurons = inputs.shape[1], outputs.shape[1]
    weights_input_hidden = np.random.uniform(size=(input_neurons, hidden_neurons))
    weights_hidden_output = np.random.uniform(size=(hidden_neurons, output_neurons))

    for _ in range(epochs):
        hidden_layer_activation = sigmoid(np.dot(inputs, weights_input_hidden))
        output_layer_activation = sigmoid(np.dot(hidden_layer_activation, weights_hidden_output))
        output_error = outputs - output_layer_activation
        output_delta = output_error * sigmoid_derivative(output_layer_activation)
        hidden_error = np.dot(output_delta, weights_hidden_output.T)
        hidden_delta = hidden_error * sigmoid_derivative(hidden_layer_activation)
        weights_hidden_output += learning_rate * np.dot(hidden_layer_activation.T, output_delta)
        weights_input_hidden += learning_rate * np.dot(inputs.T, hidden_delta)

    return weights_input_hidden, weights_hidden_output


def predict(input_data, weights_input_hidden, weights_hidden_output):
    hidden_layer_activation = sigmoid(np.dot(input_data, weights_input_hidden))
    output_layer_activation = sigmoid(np.dot(hidden_layer_activation, weights_hidden_output))
    return np.eye(output_layer_activation.shape[1])[np.argmax(output_layer_activation, axis=1)]


def main(args):
    input_features, output_classes, hidden_neurons, epochs, train_file, test_file = args
    train_data = pd.read_csv(train_file, header=None).values
    test_data = pd.read_csv(test_file, header=None).values
    train_inputs, train_outputs = train_data[:, :input_features], train_data[:, input_features:]
    test_inputs, test_outputs = test_data[:, :input_features], test_data[:, input_features:]
    train_inputs, test_inputs = normalize(train_inputs), normalize(test_inputs)
    weights_input_hidden, weights_hidden_output = train_mlp(train_inputs, train_outputs, hidden_neurons, epochs, 0.01)
    predictions = predict(test_inputs, weights_input_hidden, weights_hidden_output)
    correct_predictions = np.sum(np.all(predictions == test_outputs, axis=1))

    print(f'Accuracy: {correct_predictions / test_outputs.shape[0] * 100:.2f}%')

    output_file = f'B00841761.csv'

    np.savetxt(output_file, predictions, delimiter=',', fmt='%d')


if __name__ == '__main__':
    main([4, 3, 5, 10000, 'train_data.csv', 'test_data.csv'])


