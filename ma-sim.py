"""
Memory Allocation Simulator
@version 1.0
@author Alin Clincea
"""
#import math
from colorama import init, Fore
init()


class Memory:
	"""
	Represents the memory as a list of Blocks.
	"""
	class Block:
		"""
		Represents the memory block.
		"""
		def __init__(self, name, size, address, process=True):
			self.name = name
			self.size = size
			self.address = address  # starting address
			self.process = process  # False = free space

	def __init__(self, capacity=1000):
		self.capacity = capacity
		self.content = [Memory.Block("0", self.capacity, 0, False)]

		# used for printing the memory representation
		self.line = ""
		for i in range(101):
			if i % int(self.capacity / 100) == 0:
				self.line += "|"
			else:
				self.line += "_"

		self.print_memory()

	def add_block(self, name, size, algorithm="first_fit"):
		"""
		Adds a memory block with a given name and size.

		param: name:
		param: size:
		param: algorithm: valid options are: first_fit, best_fit, worst_fit, next_fit
		"""
		for i in self.content:
			if i.process is False and i.size >= size:
				if i.size > size:
					self.content.insert(
					    self.content.index(i) + 1,
					    Memory.Block("0", i.size - size, i.address + size,
					                 False))
				i.name = str(name)
				i.size = size
				i.process = True
				break

		self.print_memory()

	def remove_block(self, name):
		"""
		Removes a block given the name and then merges to a single block any
		neighbouring free block.
		"""
		i = 0
		for i in range(len(self.content)):
			if self.content[i].name == str(name):
				# mark as free the first block with the given name
				self.content[i].name = "0"
				self.content[i].process = False
				break

		# compact adjacent free space, starting from the next block, to preserve
		# the i index when checking for the previous block
		if i + 1 < len(self.content) and self.content[i + 1].process is False:
			self.content[i].size += self.content[i + 1].size
			del self.content[i + 1]

		if i - 1 >= 0 and self.content[i - 1].process is False:
			self.content[i - 1].size += self.content[i].size
			del self.content[i]

		self.print_memory()

	def print_memory(self):
		"""
		Prints the memory graphical representation and stats.
		"""
		# print(self.line)
		print(
		    "0         10        20        30        40        50        60        70        80        90        100\n"
		    "|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|".replace("|", chr(8866))
		)
		s = ""
		for i in self.content:
			size = round(i.size * 100 / self.capacity)
			if i.process is False:
				s += Fore.GREEN + size * chr(9611)
			else:
				s += Fore.RED + size * chr(9611)
		print(s + Fore.BLACK)

		print("\nMemory content:")
		print("-------------------------------------")
		print("block #    name      size     address")
		print("-------------------------------------")
		counter = 0
		for i in self.content:
			name = i.name if i.process is True else "free"
			print(f"{counter:7}    {name:9} {i.size:4}   {i.address:9}")
			counter += 1
		print()

	#aliases
	a = add_block
	r = remove_block
	p = print_memory


if __name__ == "__main__":
	m = Memory()
	m.add_block("p1", 120)
	m.add_block("p2", 325)
	m.add_block("p3", 451)
	m.remove_block("p2")
	m.add_block("p4", 120)