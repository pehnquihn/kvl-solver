
import string
import numpy as np


class Component:

	def __init__(self, index, name, comp_type, value, p_loop=-1, n_loop=-1):
		self.index = int(index)
		self.name = name
		self.comp_type = comp_type
		self.value = complex(value)
		self.p_loop = p_loop
		self.n_loop = n_loop
	
	def is_shared(self):
		return self.p_loop + self.n_loop > -1

	def __repr__(self):
		return 'Comp ' + self.name + '[' + str(self.index) + ']: ' + self.comp_type + str(self.value) + \
			' ' + str(self.p_loop) + ':' + str(self.n_loop)


class Loop:

	def __init__(self, index, components=None, equation=None):
		self.index = index
		self.fix = 0
		if components is None:
			self.components = list()
		if equation is None:
			self.equation = list()
	
	def build_equation(self):
		for comp in self.components:
			if comp.comp_type == 'r':
				if comp.p_loop > -1:
					self.equation[comp.p_loop] += comp.value
				if comp.n_loop > -1:
					self.equation[comp.n_loop] -= comp.value
			if comp.comp_type == 'v':
				if comp.p_loop == self.index:
					self.fix -= comp.value
				if comp.n_loop == self.index:
					self.fix += comp.value
			if comp.comp_type == 'c':
				if comp.is_shared():
					pass
				else:
					self.equation = [0] * len(self.equation)
					self.equation[self.index] = 1
					if comp.n_loop == self.index:
						self.fix = -1 *comp.value
					else:
						self.fix = comp.value
					break
	
	def __repr__(self):
		return 'Loop ' + str(self.index)


class Circuit:

	def __init__(self, loops=list()):
		self.loops = loops
	
	def build_equations(self):
		for loop in self.loops:
			loop.build_equation()
	

def define_circuit():
	print('Entering components...')
	circuit = Circuit()
	components = {}
	loops = []
	for i, c in enumerate(string.ascii_lowercase):
		line = input("Component " + c + ": ")
		if len(line) == 0:
			break
		components[c] = Component(i, c, line[0], line[1:])
	print('Entering loops...')
	for i in range(26):
		line = input("Loop " + str(i) + ": ")
		if len(line) == 0:
			break
		loops.append(line)
	for key, value in components.items():
		for i, loop in enumerate(loops):
			if str('-' + key) in loop:
				value.n_loop = i
			elif key in loop:
				value.p_loop = i
	for i, loop in enumerate(loops):
		add_loop = Loop(i)
		add_loop.equation = [0] * len(loops)
		for key in components:
			if key in loop:
				add_loop.components.append(components[key])
		circuit.loops.append(add_loop)
	return circuit


if __name__ == '__main__':
	c = define_circuit()

