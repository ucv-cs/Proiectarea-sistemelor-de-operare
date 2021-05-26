"""
Process Scheduler Simulator
@version 1.3
@author alin-c
@link https://github.com/ucv-cs/Proiectarea-sistemelor-de-operare

This program simulates a preemptive priority scheduler with 3 priority classes
and static priorities.
Assumptions: burst time is given, all processes are ready (arrival time = 0).
The output is a timeline showing the order of execution and stats.

Processes which run their entire burst time are terminated and removed from
the ready queue.

Current process execution interrupts on 2 events:
- the quantum is elapsed;
- the remaining time (or burst - executed) is 0.

At each interrupt a scheduling decision is made: basically, lookup the entire
ready queue for the next highest priority process and run it until an interrupt
(from the 2 mentioned above).

After all processes terminate, the output is displayed. Also, the timelines are
output to a text file (to allow display of potentially long lines).

@usage
py -i ps_sim.py

outputs to file: timelines.txt
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
	def __init__(self, quantum=20):
		# sublists / subqueues are priority class queues:
		# [0] = HIGH,
		# [1] = NORMAL,
		# [2] = LOW
		self.ready_queue = [[], [], []]
		self.quantum = quantum  # "ms"
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

	# operator overload for the lazy
	def __add__(self, pd):
		self.schedule_process(pd[0], pd[1])

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
		print("Timelines and context switches:")
		timelines = {}  # dictionary: {pid: [(start, length, priority), ...]}
		for p in range(self.counter):
			timelines[p] = []

		# add the values: [(start, length, priority), ...]
		# FIXME: priority is currently redundant, but it may be used for color printing
		for i in self.execution_log:
			timelines[i[0]].append((i[5], i[6], i[1]))

		# hold process stats: [(pid, priority, burst, waiting, response)]
		stats = []

		# output timelines to file
		with open("timelines.txt", "w") as file:

			# build and print each timeline
			for t in range(self.counter):
				priority = timelines[t][0][2]
				line = f"{t} [{priority}]: "
				s_0 = 0
				s_1 = 0
				for s in timelines[t]:
					line += '.' * (s[0] - s_0 - s_1) + 'X' * s[1]
					s_0 = s[0]
					s_1 = s[1]
				# count . and X and fill the process stats
				stats.append((t, priority, line.count('X'), line.count('.'),
				              timelines[t][0][0]))
				print(line)
				file.write(line + "\n")

		# stats
		print(
		    "\nExecution sequence:\npid\tpriority\tinterrupt\tburst\tremaining"
		)
		print("---------------------------------------------------------")
		for r in self.execution_log:
			print(f"{r[0]:>3}\t{r[1]:>8}\t{r[2]:>9}\t{r[3]:>5}\t{r[4]:>9}")
		print(
		    "\nProcess stats:\npid\tpriority\tburst\twaiting\t\tresponse\tturnaround"
		)
		print(
		    "--------------------------------------------------------------------------"
		)
		total_response = 0
		total_waiting = 0
		total_turnaround = 0
		count = len(stats)
		for s in stats:
			print(
			    f"{s[0]:>3}\t{s[1]:>8}\t{s[2]:>5}\t{s[3]:>7}\t\t{s[4]:>8}\t{s[2]+s[3]:>10}"
			)
			total_response += s[4]
			total_waiting += s[3]
			total_turnaround += s[2] + s[3]
		print(f"Average response time:   {total_response/count:.2f}")
		print(f"Average waiting time:    {total_waiting/count:.2f}")
		print(f"Average turnaround time: {total_turnaround/count:.2f}")


# aliases for the lazy
L = Priority.LOW
N = Priority.NORMAL
H = Priority.HIGH

if __name__ == "__main__":
	s = Scheduler(10)
	s + (H, 35)
	s + (H, 47)
	s + (N, 24)
	s + (N, 38)
	s + (L, 45)
	s + (L, 55)
	s.execute()