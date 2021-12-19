
from enum import Enum
import random
from threading import Timer

DEBUG = 1

TASKS = []


FOUR_SEC = 4
EIGHT_SEC = 8

MENU = "enter 0 to simulate no traffic condition, enter > 0 to simulate traffic condition"

class State(Enum):
	INACTIVE = 0
	ACTIVE = 1
	SLEEPING = 2



class Node():

	def __init__(self, name, state, in_pehra):
		self.id = name
		self.state = state
		self.in_pehra = in_pehra
		self.pehredar = False
		self.interval = EIGHT_SEC		
		self.t_self_chk = Timer(self.interval, self.self_chk)
		self.t_self_chk.start()

	def self_chk(self):
		if self.in_pehra and self.pehredar:
			self._stay_awake()

		self.t_self_chk = Timer(self.interval, self.self_chk)
		self.t_self_chk.start()
		if DEBUG: print("Node {} Self check done... State: {}, Pehredar: {}".format(self.id, self.state, self.pehredar))

	def _stay_awake(self):
		self.state = State.ACTIVE
		if DEBUG: print("Node {} Called Stay Awake, State: {}, Pehredar: {}".format(self.id, self.state, self.pehredar))

class Pehra():

	def __init__(self, nodes):
		self.nodes = nodes
		self.pehredar = None

	def start_pehra(self):
		
		while(self._all_nodes_active()):
			task = self._tasks()
			if DEBUG: print("Incoming task: ", task)			
			if(task == 0): # 0 indicates no traffic, > 0 indicates traffic				
				t_elect = Timer(FOUR_SEC, self._election)
				if not t_elect.is_alive():
					t_elect.start()
				if DEBUG: print("Nodes before allowed to sleep all: ", self._disp(self.nodes))			
			else:
				if DEBUG: print("New task: ", task)
				if(self.pehredar):
					self._wake_up_all()
					t_elect.cancel()

				if self._all_nodes_active():
					n = self.nodes[random.randint(0, len(self.nodes) - 1)]
				if DEBUG: print("Task Node {}, {}, with task {} ".format(n.id, n.state, task))
			
		if not self._all_nodes_active():
			if DEBUG: print("Alert :: Cluster Down ", self._disp(self.nodes))
			self._wake_up_all() # try to wake up all

	def _tasks(self):
		task = int(input()) # incoming traffic
		return task

	def _disp(self, nodes):
		li = []
		for node in nodes:
			li.append("Node: {}, State: {}, Pehredar: {}".format(node.id, node.state, node.pehredar))
		return li

	def _election(self):

		current_pehredar = self.pehredar
		if DEBUG: print("Current Pehredar: {}".format(current_pehredar.id if current_pehredar else "No Pehredar"))
		
		in_pehra_nodes = [ n for n in self.nodes if n.in_pehra ]
		index = random.randint(0, len(in_pehra_nodes) - 1 ) # select a random node from the nodes who are participating in PEHRA
		new_pehredar = in_pehra_nodes[index]
		
		new_pehredar.pehra_term = FOUR_SEC
		new_pehredar.state = State.ACTIVE
		new_pehredar.pehredar = True

		self.pehredar = new_pehredar	

		if DEBUG: print("New Pehredar: ", self.pehredar.id)

		if current_pehredar and new_pehredar.state == State.ACTIVE:
			current_pehredar.pehredar = False
			new_pehredar.pehredar = True

		if DEBUG: print("Nodes after election: ", self._disp(self.nodes))
		
		self._allow_to_sleep(pehredar=new_pehredar) # new pehredar is elected let others sleep

		return new_pehredar

	def _allow_to_sleep(self, pehredar):

		for node in self.nodes:
			if not node.pehredar and node.in_pehra:
				node.state = State.SLEEPING

		if DEBUG: print("Nodes after allowed to sleep all: ", self._disp(self.nodes))

	def _wake_up_all(self):
		for node in self.nodes:
			if node.in_pehra: # only wake up those nodes participating in PEHRA
				node.state = State.ACTIVE

		if DEBUG: print("Nodes after wake up all: ", self._disp(self.nodes))
		return True

	def _all_nodes_active(self):

		all_active = True

		for node in self.nodes:
			if node.state == State.INACTIVE:
				all_active = False
				break;

		return all_active

	def subscribe_to_pehra(self, node, sub=True): # subscribe/unsubscribe a node to PEHRA

		subscribed = False
		for n in self.nodes:
			if n.id == node.id:
				n.in_pehra = sub
				subscribed = sub
				break;
		return subscribed

	def subscribe_to_pehra(self, nodes, sub=True): # subscribe/unsubscribe list of nodes to PEHRA

		subscribed = []

		ids_to_sub = [ n.id for n in nodes ]

		for n in self.nodes:
			if n.id in ids_to_sub:
				n.in_pehra = sub
				subscribed.append([n.id])

		return subscribed



print("Usage: {}".format(MENU))

nodes = [Node('x', State.ACTIVE, True), Node('y', State.ACTIVE, True), Node('z', State.ACTIVE, False)]

p = Pehra(nodes)

p.start_pehra()


