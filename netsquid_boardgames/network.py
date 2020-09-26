import logging, sys
#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

from netsquid.nodes import Network
from netsquid.components import QuantumProcessor, QuantumChannel, Channel

def board_network(board_size):
	network = Network("Board")

	#Create nodes
	tm_node, p0_node, p1_node = network.add_nodes(["TaskMasterNode", "PlayerZeroNode", "PlayerOneNode"])
	logging.debug('nw: nodes created')

	#Add Memories
	tm_node.add_subcomponent(QuantumProcessor("TaskMasterMemory", num_positions=board_size))
	p0_node.add_subcomponent(QuantumProcessor("PlayerZeroMemory", num_postiions=1))
	p1_node.add_subcomponent(QuantumProcessor("PlayerOneMemory", num_positions=1))
	logging.debug('nw: added memories')

	#Quantum channels
	qchannel_tm0 = QuantumChannel("QChannelTMtoP0")
	qchannel_0tm = QuantumChannel("QChannelP0toTM")
	qchannel_tm1 = QuantumChannel("QChannelTMtoP1")
	qchannel_1tm = QuantumChannel("QChannelP1toTM")
	logging.debug('nw: created channels')
	
	#Quantum connections
	tm_port0, p0_port0 = network.add_connection(tm_node, p0_node, channel_to=qchannel_tm0, channel_from=qchannel_0tm, label="QTMP0")
	tm_port1, p1_port0 = network.add_connection(tm_node, p1_node, channel_to=qchannel_tm1, channel_from=qchannel_1tm, label="QTMP1")
	logging.debug('nw: created connections')

	#Port forwarding
	p0_node.qmemory.ports["qout"].forward_output(p0_node.ports[p0_port0])
	p0_node.ports[p0_port0].forward_input(p0_node.qmemory.ports["qin0"])

	p1_node.qmemory.ports["qout"].forward_output(p1_node.ports[p1_port0])
	p1_node.ports[p1_port0].forward_input(p1_node.qmemory.ports["qin0"])

	#Classical channels
	channel_0tm = Channel("ChannelP0toTM")
	channel_1tm = Channel("ChannelP1toTM")
	channel_tm0 = Channel("ChannelTMtoP0")
	channel_tm1 = Channel("ChannelTMtoP1")

	#Classical connections
	p0_port1, tm_port3 = network.add_connection(p0_node, tm_node, channel_to=channel_0tm, channel_from=channel_tm0, label="TMP0")
	p1_port1, tm_port4 = network.add_connection(p1_node, tm_node, channel_to=channel_1tm, channel_from=channel_tm1, label="TMP1")
	

	logging.debug('nw: port forwarding done. Network init complete.')
	
	return network
