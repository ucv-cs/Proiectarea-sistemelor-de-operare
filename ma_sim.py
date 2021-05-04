"""
Memory Allocation Simulator
@version 1.2
@author alin-c
@link https://github.com/ucv-cs/Proiectarea-sistemelor-de-operare

@usage
py -i ma_sim.py [-ff | -bf | -wf]

where:
	-ff = first_fit (default)
	-bf = best_fit
	-wf = worst_fit

interaction (if run with -i):
 - at the console prompt enter:
	m+123
		to add a process with the size 123
	m-2
		to remove the process with pid 2

 - to change the algorithm in interactive mode, type:
	m.algorithm = "bf"
		(or "wf" or back to "ff"...)
"""
import sys
from colorama import init, Fore, Style

init()
_algorithm = "ff"


class Memory:
	"""
	Represents the memory as a list of Blocks.
	"""
	class Block:
		"""
		Represents the memory block.
		"""
		def __init__(self, pid, size, address, process=True):
			self.pid = pid
			self.size = size
			self.address = address  # starting address
			self.process = process  # False = free space

	global _algorithm

	def __init__(self, capacity=1000):

		self.algorithm = _algorithm
		self.capacity = capacity
		self.content = [Memory.Block("0", self.capacity, 0, False)]
		self.counter = 0
		self.print_memory()

	def add_block(self, size, algorithm=_algorithm):
		"""
		Adds a memory block with a given size and allocation algorithm.
			algorithm valid options are:
				ff = first_fit
				bf = best_fit
				wf = worst_fit
		"""
		algorithm = self.algorithm
		if algorithm == "bf":
			self._bf(size)
		elif algorithm == "wf":
			self._wf(size)
		else:  # ff, default
			self._ff(size)
		self.counter += 1
		self.print_memory()

	def _ff(self, size):
		"""
		First fit allocation: finds the first block of free space with a size
		greater or equal than the input size and then allocates the new process.
		"""
		pid = self.counter
		for b in self.content:
			if b.process is False and b.size >= size:
				# split the block into a process and the rest of free space
				if b.size > size:
					self.content.insert(
					    self.content.index(b) + 1,
					    Memory.Block("0", b.size - size, b.address + size,
					                 False))
				(b.pid, b.size, b.process) = (pid, size, True)
				break

	def _bf(self, size):
		"""
		Best fit allocation: finds the smallest block of free space with a size
		greater or equal than the input size and then allocates the new process.
		"""
		candidates = dict()
		pid = self.counter
		# scan the memory and make a dictionary (index : size) of candidate blocks
		for b in self.content:
			if b.process is False and b.size >= size:
				candidates[self.content.index(b)] = b.size
		# no candidates means no best fit block
		if len(candidates) == 0:
			return
		# find the index of the minimal value in the dictionary
		# i.e. the best fit block
		i = min(candidates, key=candidates.get)
		# split the block into a process and the rest of free space
		if self.content[i].size > size:
			self.content.insert(
			    i + 1,
			    Memory.Block("0", self.content[i].size - size,
			                 self.content[i].address + size, False))
		(self.content[i].pid, self.content[i].size,
		 self.content[i].process) = (pid, size, True)

	def _wf(self, size):
		"""
		Worst fit allocation: finds the largest block of free space with a size
		greater or equal than the input size and then allocates the new process.
		"""
		candidates = dict()
		pid = self.counter
		# scan the memory and make a dictionary (index: size) of candidate blocks
		for b in self.content:
			if b.process is False and b.size >= size:
				candidates[self.content.index(b)] = b.size
		# no candidates means no best fit block
		if len(candidates) == 0:
			return
		# find the index of the maximal value in the dictionary
		# i.e. the worst fit block
		i = max(candidates, key=candidates.get)
		# split the block into a process and the rest of free space
		if self.content[i].size > size:
			self.content.insert(
			    i + 1,
			    Memory.Block("0", self.content[i].size - size,
			                 self.content[i].address + size, False))
		(self.content[i].pid, self.content[i].size,
		 self.content[i].process) = (pid, size, True)

	def remove_block(self, pid):
		"""
		Removes a block given the process id (pid) and then merges to a single block any
		neighbouring free block.
		"""
		i = 0
		for i in range(len(self.content)):
			if self.content[i].pid == pid:
				# mark as free the first block with the given pid
				self.content[i].pid = "0"
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

	# operator overloads for the lazy
	def __add__(self, other):
		self.add_block(other)

	def __sub__(self, other):
		self.remove_block(other)

	def print_memory(self):
		"""
		Prints the memory graphical representation and stats.
		"""
		red = Fore.RED + Style.BRIGHT
		green = Fore.GREEN + Style.BRIGHT
		reset = Style.RESET_ALL
		margin = "\t"
		# graph
		print(
		    f"{margin}0         10        20        30        40        50        60        70        80        90        100"
		    f"\n{margin}" + 10 * ("\u230a" + 9 * "_") + "\u230a")
		s = margin
		for i in self.content:
			# this size isn't precise because the character width is discrete
			size = round(i.size * 100 / self.capacity)
			if i.process is False:
				s += green + size * chr(9611)
			else:
				s += red + size * chr(9611)
		print(s + reset)
		# stats
		width = len(str(self.capacity))
		header = "block    pid" + ' ' * (width - 1) + "size" + ' ' * (
		    width - 1) + "address"
		separator = f"{margin}{'-' * len(header)}"
		print(f"\n{margin}Memory content:")
		print(separator)
		print(f"{margin}{header}")
		print(separator)
		counter = 1
		for i in self.content:
			pid = i.pid if i.process is True else "free"
			color = green if pid == "free" else red
			print(
			    f"{margin}{color}{counter:5}   {str(pid): >4}   {i.size: >{width}}{i.address: >{6 + width}}"
			)
			counter += 1
		print(reset)


if __name__ == "__main__":
	if "-ff" in str(sys.argv):
		_algorithm = "ff"
	elif "-bf" in str(sys.argv):
		_algorithm = "bf"
	elif "-wf" in str(sys.argv):
		_algorithm = "wf"

	m = Memory()

	#aliases for the lazy
	a = m.add_block
	r = m.remove_block
	p = m.print_memory

	# scripted operations
	m + 120  # add pid 0
	m + 130  # add pid 1
	m + 150  # add pid 2
	m + 190  # add pid 3
	m + 110  # add pid 4
	m + 140  # add pid 5
	m + 50  # add pid 6
	m - 1  # remove pid 1
	m - 3  # remove pid 3
	m - 5  # remove pid 5