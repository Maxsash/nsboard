import logging, sys
#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

import random

import netsquid as ns
from netsquid.protocols import NodeProtocol
from netsquid.components import QuantumMemory
import netsquid.components.instructions as instr

class TaskMasterProtocol(NodeProtocol):
	def __init__(self, node, memory_size, cport_name0, qport_name0, cport_name1, qport_name1):
		super().__init__(node)
		self.node = node
		self._qport_name0 = qport_name0
		self._cport_name0 = cport_name0
		self._qport_name1 = qport_name1
		self._cport_name1 = cport_name1	

		self.size = memory_size
		self.memory = self.node.qmemory

		self.memory.reset()
		qubit = ns.qubits.create_qubits(self.size)

		self.memory.put(qubit)
		logging.debug('tm: put qubits in memory')

		self.index = random.randint(0, self.size)

		logging.debug('tm: init complete')

	def run(self):
		while True:

			qport0 = self.node.ports[self._qport_name0]
			cport0 = self.node.ports[self._cport_name0]
			qport1 = self.node.ports[self._qport_name1]
			cport1 = self.node.ports[self._cport_name1]
			
			instr.INSTR_INIT(self.memory, num_positions = self.size)

			#Port forwarding for Player Zero
			port_num = "qin" + str(self.index)
			self.node.qmemory.ports["qout"].forward_output(qport0)
			qport0.forward_input(self.node.qmemory.ports[str(port_num)])

			self.memory.pop(positions=self.index)
			logging.debug('tm: pop qubit index')

			print("Beforep0: ")
			for i in range(self.size):
				try:
					print(instr.INSTR_MEASURE_X(self.memory, positions=[i]))
				except:
					print('None')


			#Wait for return qubit
			logging.debug('tm: waiting for return qubit from p0')
			yield self.await_port_input(qport0)
			logging.debug('tm: recieved return qubit from p0')

			print("Afterp0: ")
			for i in range(self.size):
				try:
					print(instr.INSTR_MEASURE_X(self.memory, positions=[i]))
				except:
					print('None')


			#Send acknowledgement
			cport0.tx_output("Recieved qubit")
			logging.debug('tm: sent the ack signal to p0')
			
			#Wait for next index
			logging.debug('tm: waiting for the next index from p0')
			yield self.await_port_input(cport0)
			logging.debug('tm: recieved the next index from p0')

			self.index = cport0.rx_input().items[0]

			#-------------------------------------------------------
			#Port forwarding for Player One
			port_num = "qin" + str(self.index)
			self.node.qmemory.ports["qout"].forward_output(qport1)
			qport1.forward_input(self.node.qmemory.ports[str(port_num)])

			self.memory.pop(positions=self.index)
			logging.debug('tm: pop qubit index')

			print("Beforep1: ")
			for i in range(self.size):
				try:
					print(instr.INSTR_MEASURE_X(self.memory, positions=[i]))
				except:
					print('None')


			#Wait for return qubit
			logging.debug('tm: waiting for return qubit from p1')
			yield self.await_port_input(qport1)
			logging.debug('tm: recieved return qubit from p1')

			print("Afterp1: ")
			for i in range(self.size):
				try:
					print(instr.INSTR_MEASURE_X(self.memory, positions=[i]))
				except:
					print('None')


			#Send acknowledgement
			cport1.tx_output("Recieved qubit")
			logging.debug('tm: sent the ack signal to p1')
			
			#Wait for next index
			logging.debug('tm: waiting for the next index from p1')
			yield self.await_port_input(cport1)
			logging.debug('tm: recieved the next index from p1')

			self.index = cport1.rx_input().items[0]


class PlayerProtocol(NodeProtocol):
	def __init__(self, player_index, qport_name, cport_name, node=None, name=None):
		super().__init__(node=node, name=name)
		self._qport_name = qport_name
		self._cport_name = cport_name
		self.memory = self.node.qmemory
		self.tag = "p" + str(player_index)
		logging.debug(self.tag + ': init complete')

	def run(self):
		while True:
			qport = self.node.ports[self._qport_name]
			cport = self.node.ports[self._cport_name]

			logging.debug(self.tag + ': waiting for input')
			yield self.await_port_input(qport)
			print(self.tag, ' received', self.memory.peek([0]))

			#Operate on qubit here--------------------------------------------------------------------------------
			operation = None
			ops = ['X','Y','Z','H','K','S','T','I']
			#Ask the player what they want to do with the qubit
			while operation not in ops:
				operation = input(self.tag + "Enter the operation you want to perform on qubit: ")
				if operation not in ops:
					print("Invalid operation. Choose from ", ops)
			
			instr.INSTR_INIT(self.memory, positions=[0])
			#ns.qubits.operate(qubit, getattr(ns, operation))
			str1 = "INSTR_" + operation
			#implement instr.INSTR_x(self.memory, positions=[0]) || x can be any operation on qubit 
			getattr(instr, str1)(self.memory, positions=[0])
			print(self.memory.measure(0))
			#----------------------------------------------------------------------------------------------------
			
			self.memory.pop(positions=0)
			logging.debug(self.tag + ': sent the qubit')			

			#Wait for acknowledgement signal
			logging.debug(self.tag + ': waiting for ack signal')
			yield self.await_port_input(cport)	
			logging.debug(self.tag + ': recieved the ack signal')	

			#Send the next index
			self.index = input("Enter the next index: ")		
			cport.tx_output(int(self.index))
			logging.debug(self.tag + ': sent the next index')
