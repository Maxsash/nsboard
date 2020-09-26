import getpass

import netsquid as ns
from netsquid_boardgames.protocols import TaskMasterProtocol, PlayerProtocol
from netsquid_boardgames.network import board_network

if __name__ == "__main__":
	
	board_size = int(input("Enter the size of the Main Memory: "))
	#Building the network
	network = board_network(board_size)

	#Get the ports from connections
	classical_ports_tm0 = network.get_connected_ports('TaskMasterNode', 'PlayerZeroNode', 'TMP0')
	classical_ports_tm1 = network.get_connected_ports('TaskMasterNode', 'PlayerOneNode', 'TMP1')
	quantum_ports_tm0 = network.get_connected_ports('TaskMasterNode', 'PlayerZeroNode', 'QTMP0')
	quantum_ports_tm1 = network.get_connected_ports('TaskMasterNode', 'PlayerOneNode', 'QTMP1')

	#Initialize Nodes with Protocols
	protocols = TaskMasterProtocol(network.nodes['TaskMasterNode'], board_size, classical_ports_tm0[0], quantum_ports_tm0[0], classical_ports_tm1[0], quantum_ports_tm1[0]).start()

	playerZero = PlayerProtocol(0, board_size, quantum_ports_tm0[1], classical_ports_tm0[1], network.nodes['PlayerZeroNode']).start()
	playerOne = PlayerProtocol(1, board_size, quantum_ports_tm1[1], classical_ports_tm1[1], network.nodes['PlayerOneNode']).start()

	ns.sim_run()

	print("Game finished. All moves played. Take a look at the measurements of the board.")

	score = 0
	for i in range(board_size):
		a = network.nodes['TaskMasterNode'].qmemory.measure(i)
		score += a[0][0] * a[1][0]
		print(a)
	print("The score is ", score)
	if score < board_size/2:
		print("Player Zero Wins")
	else:
		print("Player One Wins")
