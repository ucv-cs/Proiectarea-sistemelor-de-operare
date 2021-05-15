"""
Process Scheduler Simulator
@version 1.2
@author alin-c
@link https://github.com/ucv-cs/Proiectarea-sistemelor-de-operare

This program simulates a preemptive priority scheduler with 3 priority classes
and static priorities.
Assumptions: burst time is given, all processes are ready (arrival time = 0).
The output is a timeline showing the order of execution and stats.

Processes which run their entire burst time are terminated and removed from
the ready queue.

The CPU interrupts the current process execution on 2 events:
- the quantum is elapsed;
- the remaining time (or burst - executed) is 0.

At each interrupt a scheduling decision is made: basically, lookup the entire
ready queue for the next highest priority process and run it until an interrupt
(from the 2 mentioned above).

After all processes terminate, the output is displayed.

@usage
py -i ps_sim.py
"""

import random as R
from enum import Enum


class Priority(Enum):
	HIGH = 0
	NORMAL = 1
	LOW = 2


class Process:
	def __init__(self, pid=0, priority=Priority.NORMAL, burst_time=1):
		self.pid = pid
		self.priority = priority
		self.burst_time = burst_time
		self.executed_time = 0


class Scheduler:
	def __init__(self):
		# sublists / subqueues are priority class queues:
		# 0 -> HIGH,
		# 1 -> NORMAL,
		# 2 -> LOW
		self.ready_queue = [[], [], []]
		self.quantum = 10  # "ms"
		self.timer = 0  # "ms"
		self.counter = 0  # process counter used for pid
		self.execution_log = []  # will hold tuples gathered at each interrupt

	def schedule_process(self, process_priority, process_burst):
		"""
		Adds a new process to the correct priority queue.
		"""
		self.ready_queue[process_priority.value].append(
		    Process(self.counter, process_priority, process_burst))
		self.counter += 1

	def terminate_process(self, pid, process_priority):
		"""
		Removes from the ready queue a process which has exited (i.e. burst
		time completed).
		"""
		for i in range(len(self.ready_queue[process_priority])):
			if self.ready_queue[process_priority][i].pid == pid:
				self.ready_queue[process_priority].pop(i)
				return

	def execute(self):
		"""
		Executes the ready queue based on:
		- priorities among subqueues,
		- first-in-first-served and round-robin inside each priority subqueue.
		For each executed process, keeps track of the remaining time
		(= burst - executed).
		If a process terminates, it is removed from the ready queue.
		Builds the display string based on execution stats.
		"""
		while True:
			# get the first process with the highest priority
			running_process = self._get_next_process()

			# run as long as there are elements in the ready queue
			if running_process == None:
				self.print_execution()
				return

			# until an interrupt, simulate process execution (i.e. count a
			# quantum or the processes' remaining execution time)
			run_time = 0
			start = self.timer
			while run_time < self.quantum:
				if running_process.burst_time - running_process.executed_time == 0:
					break
				self.timer += 1
				running_process.executed_time += 1
				run_time += 1

			# append the info tuple (pid, priority, interrupt, burst, remaining)
			# to the execution log list
			self.execution_log.append(
			    (running_process.pid, running_process.priority.value,
			     self.timer, running_process.burst_time,
			     running_process.burst_time - running_process.executed_time,
			     start, run_time))

			# at interrupt check if process burst time elapsed and if so
			# terminate the process, else if there is more than 1 process in
			# the subqueue, do round robin
			if (running_process.burst_time -
			    running_process.executed_time) == 0:
				self.terminate_process(running_process.pid,
				                       running_process.priority.value)
			elif len(self.ready_queue[running_process.priority.value]) > 1:
				self._round_robin(
				    self.ready_queue[running_process.priority.value])

	def _get_next_process(self):
		"""
		Get the head process from the ready subqueues, searching from the highest
		priority subqueue.
		If nothing is found, return None (used to stop overall execution).
		"""
		if len(self.ready_queue[0]) > 0:
			return self.ready_queue[0][0]
		elif len(self.ready_queue[1]) > 0:
			return self.ready_queue[1][0]
		elif len(self.ready_queue[2]) > 0:
			return self.ready_queue[2][0]
		return None

	def _round_robin(self, queue):
		"""
		Given a list with more than 1 element, move its current first element
		after the current last element.
		"""
		if len(queue) > 1:
			queue.append(queue.pop(0))

	def print_execution(self):
		"""
		Displays the execution log in a friendly manner.
		"""
		# timelines chart
		timelines = {}
		for p in range(self.counter):
			timelines[p] = []

		for i in self.execution_log:
			timelines[i[0]].append((i[5], i[6]))

		for t in range(self.counter):
			line = f"{t}: "
			s_0 = 0
			s_1 = 0
			for s in timelines[t]:
				line += '.' * (s[0] - s_0 - s_1) + 'o' * s[1]
				s_0 = s[0]
				s_1 = s[1]
			print(line)

		# stats
		print("pid\tpriority\tinterrupt\tburst\tremaining")
		print("---------------------------------------------------------")
		for r in self.execution_log:
			print(f"{r[0]:>3}\t{r[1]:>8}\t{r[2]:>9}\t{r[3]:>5}\t{r[4]:>9}")


if __name__ == "__main__":
	s = Scheduler()
	s.schedule_process(Priority.NORMAL, 12)
	s.schedule_process(Priority.HIGH, 15)
	s.schedule_process(Priority.NORMAL, 22)
	s.schedule_process(Priority.LOW, 13)
	s.execute()
