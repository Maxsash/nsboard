import random

import netsquid as ns
from netsquid.nodes import Node

def main():
	ns.sim_reset()
	tm_node = Node(name="TaskMaster")
	p1_node = Node(name="PlayerOne")
	p0_node = Node(name="PlayerZero")

	from netsquid.components import QuantumChannel, Channel
	cht0q = QuantumChannel(name="qchannel[tm to p0]")
	cht1q = QuantumChannel(name="qchannel[tm to p1]")
	ch0tq = QuantumChannel(name="qchannel[p0 to tm]")
	ch1tq = QuantumChannel(name="qchannel[p1 to tm]")

	ch0tc = Channel(name="channel[p0 to tm]")
	ch1tc = Channel(name="channel[p1 to tm]")

	tm_node.add_ports('cIO0')
	tm_node.add_ports('cIO1')
	p0_node.add_ports('cPtoTM')
	p1_node.add_ports('cPtoTM')

	ch0tc.ports['send'].connect(p0_node.ports['cPtoTM'])
	ch0tc.ports['recv'].connect(tm_node.ports['cIO0'])
	ch1tc.ports['send'].connect(p1_node.ports['cPtoTM'])
	ch1tc.ports['recv'].connect(tm_node.ports['cIO1'])

	from netsquid.nodes import DirectConnection
	qconnection0 = DirectConnection(name="qconn[tm|p0]", channel_AtoB=cht0q, channel_BtoA=ch0tq)
	qconnection1 = DirectConnection(name="qconn[tm|p1]", channel_AtoB=cht1q, channel_BtoA=ch1tq)

	tm_node.connect_to(remote_node=p0_node, connection=qconnection0, local_port_name="IOp0", remote_port_name="qubitIO")
	tm_node.connect_to(remote_node=p1_node, connection=qconnection1, local_port_name="IOp1", remote_port_name="qubitIO")


	tm_protocol = TaskMasterProtocol(tm_node, 25)
	p0_protocol = PlayerProtocol(p0_node, 0)
	p1_protocol = PlayerProtocol(p1_node, 1)

	p0_protocol.start()
	p1_protocol.start()
	tm_protocol.start()

	ns.sim_run()

if __name__ == "__main__":
     main()

