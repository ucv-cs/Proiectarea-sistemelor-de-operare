""""
Experiments script for Memory Allocation Simulator
@author alin-c
@link https://github.com/ucv-cs/Proiectarea-sistemelor-de-operare
"""
import ma_sim as M
import random as R
# from colorama import init, Fore, Style

# init()

experiment_count = 1
process_count = 5
memory_size = 1000
process_proportion = 0.5
prints = True
separator = "\n=========================="


def runner():
	global process_count
	global memory_size
	global process_proportion
	global prints
	global separator

	# random sizes for processes
	initial_sizes = [
	    R.randrange(1, int(process_proportion * memory_size))
	    for s in range(process_count)
	]
	# pids to be removed
	pids = [
	    R.randrange(0, process_count)
	    for s in range(1, R.randrange(1, process_count))
	]
	# new random sizes for processes
	final_sizes = [
	    R.randrange(1, int(process_proportion * memory_size))
	    for s in range(process_count)
	]

	print("Sizes to be added:  ", initial_sizes)
	print("PIDs to be removed: ", pids)
	print("Sizes to be readded:", final_sizes, "\n")

	# running the first fit algorithm
	if prints:
		print("First fit allocation" + separator)
	m = M.Memory(memory_size, prints)
	m.algorithm = "ff"
	for i in initial_sizes:
		m + i
	for i in pids:
		m - i
	for i in final_sizes:
		m + i
	ff_sr = (m.counter - m.fail_counter) / m.counter
	del m

	# running the best fit algorithm
	if prints:
		print("Best fit allocation" + separator)
	m = M.Memory(memory_size, prints)
	m.algorithm = "bf"
	for i in initial_sizes:
		m + i
	for i in pids:
		m - i
	for i in final_sizes:
		m + i
	bf_sr = (m.counter - m.fail_counter) / m.counter
	del m

	# running the worst fit algorithm
	if prints:
		print("Worst fit allocation" + separator)
	m = M.Memory(memory_size, prints)
	m.algorithm = "wf"
	for i in initial_sizes:
		m + i
	for i in pids:
		m - i
	for i in final_sizes:
		m + i
	wf_sr = (m.counter - m.fail_counter) / m.counter

	print(f"Allocation success rates:")
	print(f"  first fit: {ff_sr:.4f}")
	print(f"  best fit:  {bf_sr:.4f}")
	print(f"  worst fit: {wf_sr:.4f}\n")
	return (ff_sr, bf_sr, wf_sr)


def print_stats(data):
	result = (0, 0, 0)
	for r in range(len(data)):
		result = (result[0] + data[r][0], result[1] + data[r][1],
		          result[2] + data[r][2])
	print("Cumulative success rates (higher is better):")
	print(f"  first fit: {result[0]:.4f}")
	print(f"  best fit:  {result[1]:.4f}")
	print(f"  worst fit: {result[2]:.4f}")


results = []
for i in range(1, experiment_count + 1):
	print("Experiment #", i, separator)
	results.append(runner())

print_stats(results)