import random
import math

class Neuron(object):
    """
        A neuron is a stage of a neural network (sometimes called Nodes)
        @static (Number) WEIGHT_RANGE - The value at which the weight is scaled at when randomized
        @static (Number) BIAS_RANGE - The value at which the bias is scaled at when randomized
        @property (Array<Number>) weights - The weights of the neuron
        @property (Array<Number>) bias - The bias of the neuron (sometimes thought of as a special weight)
        @property (Array<Number>) last_output - The last output produced by the neuron (used for training)
        @property (Array<Number>) last_input - The last inputs processed by this neuron (used for training)
        @property (Number) error - The error of the neuron (target - output)
        @property (Number) delta - The amount that the weights and biases must be adjusted by to closer approximate the test values
        @property (Function) activation - The activation function to be used to calculate the output
        @property (Function) derive - The derivative of the activation function
    """
    WEIGHT_RANGE = 0.2
    BIAS_RANGE = 0.2
    
    def __init__(self, num_inputs, activation, derivative):
        """
            Initializes a neuron
            @param (Neuron) self - The neuron to initialize
            @param (Integer) num_inputs - The number of inputs of this neuron
            @param (Function) activation - The activation function to be used to calculate the output
            @param (Function) derivative - The derivative of the activation function
            @returns (Neuron)
        """
        self.weights = [random.uniform(-Neuron.WEIGHT_RANGE, Neuron.WEIGHT_RANGE) for i in range(0, num_inputs, 1)]
        self.bias = random.uniform(-Neuron.BIAS_RANGE, Neuron.BIAS_RANGE)
        self.activation = activation
        self.derive = derivative
        self.last_output = None
        self.last_input = None
        self.error = None
        self.delta = None

    def process(self, inputs):
        """
            Processes a set of inputs
            @param (Neuron) self - The neuron to process the inputs
            @param (Array<Number>) inputs - The inputs to process
            @returns (Number) - The output of the neuron
        """
        self.last_input = inputs
        self.last_output = sum([self.weights[i] * inputs[i] for i in range(0, len(inputs), 1)])
        self.last_output += self.bias
        self.last_output = self.activation(self.last_output)
        
        return self.last_output
