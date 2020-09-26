#import random

import netsquid as ns
#from netsquid.nodes import Node
#from netsquid.components import QuantumChannel, Channel
#from netsquid.nodes import DirectConnection
from netsquid_boardgames.protocols import TaskMasterProtocol, PlayerProtocol
from netsquid_boardgames.network import board_network

if __name__ == "__main__":
	board_size = 10
	network = board_network(board_size)

	classical_ports_tm0 = network.get_connected_ports('TaskMasterNode', 'PlayerZeroNode', 'TMP0')
	classical_ports_tm1 = network.get_connected_ports('TaskMasterNode', 'PlayerOneNode', 'TMP1')
	quantum_ports_tm0 = network.get_connected_ports('TaskMasterNode', 'PlayerZeroNode', 'QTMP0')
	quantum_ports_tm1 = network.get_connected_ports('TaskMasterNode', 'PlayerOneNode', 'QTMP1')

	protocols = TaskMasterProtocol(network.nodes['TaskMasterNode'], board_size, classical_ports_tm0[0], quantum_ports_tm0[0], classical_ports_tm1[0], quantum_ports_tm1[0]).start()

	playerZero = PlayerProtocol(0, quantum_ports_tm0[1], classical_ports_tm0[1], network.nodes['PlayerZeroNode']).start()
	playerOne = PlayerProtocol(1, quantum_ports_tm1[1], classical_ports_tm1[1], network.nodes['PlayerOneNode']).start()
	#print(network.nodes['TaskMasterNode'].subcomponents['BufferMemoryZero'])
	ns.sim_run()

