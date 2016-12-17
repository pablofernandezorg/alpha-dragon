from neuron import Neuron

class Layer(object):
    """
        A layer is a layer of neurons in a neural network (sometimes called Synapses)
        @property (Array<Neuron>) neurons - The neurons in the layer
    """
    def __init__(self, num_neurons, num_inputs, activation, derivative):
        """
            Initializes a layer of neurons
            @param (Number) num_neurons - The number of neurons in the layer
            @param (Number) num_inputs - The number of inputs of each neuron in the layer
            @param (Function) activation - The activation function to be used
            @param (Function) derivative - The derivative of the activation function
            @returns (Layer)
        """
        self.neurons = [Neuron(num_inputs, activation, derivative) for i in range(0, num_neurons, 1)]

    def process(self, inputs):
        """
            Processes a set of inputs
            @param (Array<Number>) inputs - The inputs to process
            @returns (Array<Number>) - The output of the layer
        """
        return [neuron.process(inputs) for neuron in self.neurons]
