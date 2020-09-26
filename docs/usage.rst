Usage
-----

The user has to specify the size of QuantumMemory that will be used as the board, this initializes the network with three nodes. Each player will get as many turns as the size of the QuantumMemory. At each turn, player can choose to operate on the qubit and then specify the index of qubit that will be sent to the other player. At the end of all the turns, the result after measuring all the qubits in the QuantumMemory will be presented and a score based on the value of qubit and its probability will be calculated. If the score is more than half the size of QuantumMemory, Player One wins; else Player Zero wins.
