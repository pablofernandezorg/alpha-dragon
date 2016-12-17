from layer import Layer
from neuron import Neuron

import json
import math

class Network(object):
    """
        A neural network which contains multiple layers
        Note:
        
            The first layer is called the input layer
            The last layer is called the output layer
            All the layers inbetween are called hidden layers
        
        @static (Function) ACTIVATION_LINEAR - An activation function that does nothing
        @static (Function) ACTIVATION_TANH - The tanh activation function
        @static (Function) ACTIVATION_SIGMOID - The sigmoid activation function
        @static (Function) ACTIVATION_STEP - The unit step activation function (range 0 to 1)
        @static (Function) DERIVATIVE_LINEAR - The derivative of the linear activation function
        @static (Function) DERIVATIVE_TANH - The derivative of the tanh activation function
        @static (Function) DERIVATIVE_SIGMOID - The derivative of the sigmoid activation function
        @static (Function) DERIVATIVE_STEP - The derivative of the unit step activation function
        @static (Number) LINEAR - Represents the linear activation function. Used for File I/O.
        @static (Number) TANH - Represents the tanh activation function. Used for File I/O.
        @static (Number) SIGMOID - Represents the sigmoid activation function. Used for File I/O.
        @static (Number) STEP - Represents the unit step activation function. Used for File I/O.
        @property (Array<Layer>) layers - The layers of the neural network
    """
    LINEAR = 0
    TANH = 1
    SIGMOID = 2
    STEP = 3
    
    ACTIVATION_LINEAR = lambda x: x
    ACTIVATION_TANH = lambda x: math.tanh(x)
    ACTIVATION_SIGMOID = lambda x: 1.0 / (1.0 + math.exp(-x))
    ACTIVATION_STEP = lambda x: 1 if x >= 0 else 0

    DERIVATIVE_LINEAR = lambda x: 1
    DERIVATIVE_TANH = lambda x: 1.0 - x ** 2
    DERIVATIVE_SIGMOID = lambda x: x * (1.0 - x)
    DERIVATIVE_STEP = lambda x: 0 if abs(x) < 10 ** -4 else 1

    def __init__(self):
        """
            Initializes the neural network
            @param (Network) self - The neural network to initialize
        """
        self.layers = []

    def process(self, _inputs):
        """
            Processes a set of inputs (the length of inputs must be the same as the number of inputs for the input layer)
            @param (Network) self - The neural network to process the inputs with
            @param (Array<Number>) _inputs - The inputs for the input layer
            @returns (Array<Number>) - The output of the output layer
        """
        outputs = None
        inputs = _inputs
        
        for layer in self.layers:
            outputs = layer.process(inputs)
            inputs = outputs

        return outputs

    def add_layer(self, num_neurons, num_inputs=None, activation=None):
        """
            Adds a layer to the neural network
            @param (Network) self - The network to add the layer to
            @param (Number) - The number of neurons of the layer
            @param (Number) [num_inputs=None] - The number of inputs of the layer
            @param (Function) [activation=None] - The activation function to use for this layer
            
            Note:
                If num_inputs is not specified it is the same as the number of inputs of the last layer added
                If activation is not specified it defaults to ACTIVATION_SIGMOID
                The only accepted values for activation are:
                    - ACTIVATION_LINEAR
                    - ACTIVATION_SIGMOID
                    - ACTIVATION_TANH
                    - ACTIVATION_STEP
        """

        # Check if then number of inputs wasn't specified
        if num_inputs == None:
            last_layer = self.layers[-1]
            num_inputs = len(last_layer.neurons)

        # Check if the activation function wasn't specified
        if activation == None:
            activation = Network.ACTIVATION_SIGMOID

        # Check which activation function was chosen (to choose a derivative)
        derivative = None
        if activation == Network.ACTIVATION_LINEAR:     derivative = Network.DERIVATIVE_LINEAR
        elif activation == Network.ACTIVATION_SIGMOID:  derivative = Network.DERIVATIVE_SIGMOID
        elif activation == Network.ACTIVATION_TANH:     derivative = Network.DERIVATIVE_TANH
        elif activation == Network.ACTIVATION_STEP:     derivative = Network.DERIVATIVE_STEP

        self.layers.append(Layer(num_neurons, num_inputs, activation, derivative))
    
    def train(self, inputs, targets, learn_rate):
        """
            Trains the neural network with an example
            @param (Network) self - The network to train
            @param (Array<Number>) inputs - The inputs of the example
            @param (Array<Number>) targets - The target values of the example
            @param (Number) learn_rate - The rate to learn at
            @returns (Number) - The mean squared error
        """
        output_layer = self.layers[-1]
        error = 0
        
        # Run the example through the neural network
        outputs = self.process(inputs)

        # For every neuron in the output layer ...
        for k in range(0, len(output_layer.neurons), 1):
            # Calculate the error of the neuron
            neuron = output_layer.neurons[k]
            neuron.error = targets[k] - outputs[k]
            error += 0.5 * neuron.error ** 2

            neuron.delta = neuron.derive(neuron.last_output) * neuron.error
        
        # For every other layer (backwards) ...
        for k in range(len(self.layers) - 2, 0 - 1, -1):
            layer = self.layers[k]
            layer_next = self.layers[k + 1]
            
            # For every neuron in this layer ...
            for l in range(0, len(layer.neurons), 1):
                # Calculate the error on the neuron
                neuron_l = layer.neurons[l]
                neuron_l.error = sum([neuron.weights[l] * neuron.delta for neuron in layer_next.neurons])

                # Use newtons method for later improvement of the result
                neuron_l.delta = neuron.derive(neuron.last_output) * neuron_l.error

                # For every neuron in the next layer
                for m in range(0, len(layer_next.neurons), 1):
                    neuron_m = layer_next.neurons[m]

                    # For all the weights of the neuron
                    for n in range(0, len(neuron_m.weights), 1):
                        # Improve the neuron by a factor of the learning rate
                        neuron_m.weights[n] += learn_rate * neuron_m.last_input[n] * neuron_m.error # neuron_l.delta

                    # Improve this neuron using the previous newtons method information
                    neuron_m.bias += learn_rate * neuron_m.delta

        return error
    
    @staticmethod
    def save(path, network):
        """
            Saves a neural network to a json file
            @param (String) path - The path to save the network to
            @param (Network) network - The network to save to a file
            @returns
        """
        network_data = dict()

        # For every layer in the network ...
        layers_data = []
        for layer in network.layers:
            layer_data = dict()
            layer_neurons = []
            
            # For every neuron in the layer ...
            for neuron in layer.neurons:
                weights = neuron.weights
                bias = neuron.bias

                # "Convert" the functions into their number counterparts
                enum = None
                if neuron.activation == Network.ACTIVATION_LINEAR:      enum = Network.LINEAR
                elif neuron.activation == Network.ACTIVATION_SIGMOID:   enum = Network.SIGMOID
                elif neuron.activation == Network.ACTIVATION_TANH:      enum = Network.TANH
                elif neuron.activation == Network.ACTIVATION_STEP:      enum = Network.STEP

                # Save the neuron data to a dictionary
                neuron_data = dict()
                neuron_data["weights"] = weights
                neuron_data["bias"] = bias
                neuron_data["activation"] = enum

                # Add the neuron to the collection
                layer_neurons.append(neuron_data)

            # Add the layer to the collection
            layer_data["neurons"] = layer_neurons
            layers_data.append(layer_data)

        # Add the layer data to the network data
        network_data["layers"] = layers_data

        # Convert the object to json (TODO: Formatting)
        network_json = json.dumps(network_data, sort_keys=False, indent=4)
        
        # Write the json data to the file
        with open(path, "w+") as f:
            f.write(network_json)

    @staticmethod
    def load(path):
        """
            Loads a neural network from a json file
            @param (String) path - The path to load the neural network from
            @returns (Network) - The neural network that was loaded
        """
        network = Network()

        try:
            with open(path, "r+") as f:
                network_data = "\n".join(f.readlines())
                network_json = json.loads(network_data)
                layers = network_json["layers"]
                
                # For every layer in the network ...
                for layer in layers:
                    neurons = []

                    # For every neuron in the layer ...
                    for neuron in layer["neurons"]:
                        weights = neuron["weights"]
                        bias = neuron["bias"]
                        activation = neuron["activation"]

                        # Choose the proper activation function and corresponding derivative
                        activation_func = None
                        derivative_func = None
                        if activation == Network.LINEAR:
                            activation_func = Network.ACTIVATION_LINEAR
                            derivative_func = Network.DERIVATIVE_LINEAR
                        elif activation == Network.SIGMOID:
                            activation_func = Network.ACTIVATION_SIGMOID
                            derivative_func = Network.DERIVATIVE_SIGMOID
                        elif activation == Network.TANH:
                            activation_func = Network.ACTIVATION_TANH
                            derivative_func = Network.DERIVATIVE_TANH
                        elif activation == Network.STEP:
                            activation_func = Network.ACTIVATION_STEP
                            derivative_func = Network.DERIVATIVE_STEP

                        # Create a neuron with the desired info
                        neuron = Neuron(0, activation_func, derivative_func)
                        neuron.weights = weights
                        neuron.bias = bias
                        
                        # Add the processed neuron to the collection
                        neurons.append(neuron)

                    # Create a layer with the desired neurons
                    layer = Layer(0, 0, None, None)
                    layer.neurons = neurons
                    
                    # Add the processed layer to the collection
                    network.layers.append(layer)
        except:
            raise Exception("Invalid Neural Network File @ {}!".format(path))

        return network
