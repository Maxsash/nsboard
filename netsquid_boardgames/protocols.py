import netsquid as ns
from netsquid.protocols import NodeProtocol
from netsquid.components import QuantumMemory

class TaskMasterProtocol(NodeProtocol):
	def __init__(self, node, memory_size):
		super().__init__(node)
		self.node = node
		self.memory_size = memory_size
		self.memory = QuantumMemory("TaskMasterMemory", num_positions=memory_size)
		mem = ns.qubits.create_qubits(memory_size)
		self.memory.put(mem)
		
		self.index = random.randint(0,24)

	def run(self):
		while True:
			print("current index is :", self.index)
			self.node.ports["IOp0"].tx_output(self.memory.pop(positions=self.index))

			yield self.await_port_input(self.node.ports["IOp0"])
			qbit_return = self.node.ports["IOp0"].rx_input()
			self.memory.put(qbit_return, positions=self.index)

			yield self.await_port_input(self.node.ports["cIO0"])
			move0 = self.node.ports["cIO0"].rx_input()
			self.index = int(move0)

			self.node.ports["IOp1"].tx_output(self.memory.pop(positions=self.index))

			yield self.await_port_input(self.node.ports["IOp1"])
			qbit_return = self.node.ports["IOp1"].rx_input()
			self.memory.put(qbit_return, positions=self.index)

			yield self.await_port_input(self.node.ports["cIO1"])
			move1 = self.node.ports["cIO1"].rx_input()
			self.index = int(move1)


class PlayerProtocol(NodeProtocol):
	def __init__(self, node, sign):
		super().__init__(node)
		self.node = node
		self.sign = sign
		print("You are player ", sign)

	def run(self):
		while True:
			yield self.await_port_input(self.node.ports["qubitIO"])
			message = self.node.ports["qubitIO"].rx_input()
			qubit = message.items[0]
			print(qubit)
			operation = None
			ops = ['X','Y','Z','H','K','S','T','I']
			#Ask the player what they want to do with the qubit
			while operation not in ops:
				operation = input("Enter the operation you want to perform on qubit: ")
				if operation not in ops:
					print("Invalid operation. Choose from ", ops)
			ns.qubits.operate(qubit, getattr(ns, operation))

			#send
			self.node.ports["cPtoTM"].tx_output(qubit)

			#ask the player the qubit to send to the opponent
			move = -1
			while not 0<= move <25:
				move = int(input("Enter the qubit index to send to opponent: "))
				if not 0<= move < 25:
					print("Invalid move. Choose a number from range [0,24]")
			
			#send the move
			self.node.ports["cPtoTM"].tx_output(move)
