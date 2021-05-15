""""
Experiments script for Memory Allocation Simulator
@author alin-c
@link https://github.com/ucv-cs/Proiectarea-sistemelor-de-operare
@usage
py -i experiments.py > output.txt
"""
import ma_sim as M
import random as R

separator = "\n=========================="


def runner(process_count=10,
           memory_size=1000,
           process_min_size=1,
           process_max_size=100,
           prints=False):
	"""
	1. Randomly generates 3 lists: initial process sizes, pids, final process sizes.
	2. Uses the lists for each algorithm to allocate memory.
	3. Displays the stats.
	"""
	global separator

	# random sizes for processes
	# generate a list of process_count items with random sizes between 1 and a bounded integer
	initial_sizes = [
	    R.randrange(process_min_size, process_max_size)
	    for s in range(process_count)
	]
	# pids to be removed
	# - the elements must not be duplicated
	# - the pids count must be 1/2 of the process_count
	pids = []
	while len(pids) != int(process_count / 2):
		p = R.randrange(0, process_count)
		if p not in pids:
			pids.append(p)
	# new random sizes for processes
	# try to replace the removed processes
	final_sizes = [
	    R.randrange(process_min_size, process_max_size)
	    for s in range(int(process_count / 2))
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
	return result


def do_experiments(experiment_count=100,
                   process_count=10,
                   memory_size=1000,
                   process_min_size=1,
                   process_max_size=100,
                   prints=False):
	"""
	Executes runner() for a given number of iterations with custom configuration.
	Displays the cumulative results.
	"""
	global separator

	results = []
	for i in range(1, experiment_count + 1):
		print("Experiment #", i, separator)
		results.append(
		    runner(process_count=process_count,
		           memory_size=memory_size,
		           process_min_size=process_min_size,
		           process_max_size=process_max_size,
		           prints=prints))

	return print_stats(results)


# tests
results = []

print("\nTest 1: using unbound but not 0 process sizes")
results.append(do_experiments(process_max_size=1000))

print(
    "\nTest 2: using bound process sizes (max size 100), but process count of 15"
)
results.append(do_experiments(process_max_size=100, process_count=15))

print("\nTest 3: using bound process sizes (min size 100, max size 300)")
results.append(do_experiments(process_min_size=100, process_max_size=300))

print("\nTest 4: using bound process sizes (min size 150, max size 500)")
results.append(do_experiments(process_min_size=150, process_max_size=500))

# print final stats
print("\nOverall success rates:")
print("\tff\tbf\twf")
for i in range(len(results)):
	print(
	    f"Test {i+1}\t{results[i][0]:>6.2f}\t{results[i][1]:>6.2f}\t{results[i][2]:>6.2f}"
	)