import connection
from layer import Layer
from neuron import Neuron
from network import Network

connection = connection.connection()

try:
    # Attempt to load the network from a file
    network = Network.load("test_binary.json")
except Exception as e:
    # On failure, recreate the network from scratch
    network = Network()
    network.add_layer(8, 8, Network.ACTIVATION_SIGMOID) # Hidden Layer, 10 Neurons, 8 inputs
    network.add_layer(2, 8, Network.ACTIVATION_SIGMOID) # Output Layer,  2 Neurons, 8 inputs  
    print("Creating Neural Network...")
    
  
ITERATIONS = 500  # Number of iterations per training session
LEARN_RATE = 0.03  # The rate the network learns on each iteration
THRESHOLD  = 0.001 # If this precision is reached, the training session is instantly complete

# Perform a quick training session
for i in range(0, ITERATIONS, 1):
    error = 0
    print("Learning to fly...")
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `NeuralNetwork` ORDER BY Date DESC LIMIT 150" 
        cursor.execute(sql, ())
        connection.commit()
        NeuralTraining = cursor.fetchall()
        
    for set in NeuralTraining:  
        print("Finding hidden Robots...")
        train = [
            set["DayOfWeek"],         set["TradingMonth"], 
            set["VolumeNormalized"],  set["AboveBigMoving"],
            set["BelowLittleMoving"], set["TweetsVolumeNormalized"], 
            set["Sentiment"],         set["Sentiment30"]
        ]
        Output1 = set["Output1"]
        Output2 = set["Output2"]
        error += network.train(train, [Output1, Output2], LEARN_RATE)

    # Check the error
    if error < THRESHOLD:
        break

with connection.cursor() as cursor:
    sql = "SELECT * FROM `NeuralNetwork` ORDER BY Date ASC LIMIT 50" 
    cursor.execute(sql, ())
    connection.commit()
    NeuralTesting = cursor.fetchall()

for test in NeuralTesting:  
    outputs = network.process([
            test["DayOfWeek"],         test["TradingMonth"], 
            test["VolumeNormalized"],  test["AboveBigMoving"],
            test["BelowLittleMoving"], test["TweetsVolumeNormalized"], 
            test["Sentiment"],         test["Sentiment30"]
    ])
    print("--------------------------------------------------")
    print("Correct ", test["Output1"], ",", test["Output2"] ,"")
    print("AI      ", outputs)
   
Network.save("test_binary.json", network)
print(outputs)
