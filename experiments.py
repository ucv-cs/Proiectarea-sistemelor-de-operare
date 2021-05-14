""""
Experiments script for Memory Allocation Simulator
@author alin-c
@link https://github.com/ucv-cs/Proiectarea-sistemelor-de-operare
"""
import ma_sim as M
import random as R

separator = "\n=========================="


def runner(process_count=10,
           memory_size=1000,
           process_proportion=0.2,
           prints=False):
	"""
	1. Randomly generates 3 lists: initial process sizes, pids, final process sizes.
	2. Uses the lists for each algorithm to allocate memory.
	3. Displays the stats.
	"""
	global separator

	# random sizes for processes
	initial_sizes = [
	    R.randrange(1, int(process_proportion * memory_size))
	    for s in range(process_count)
	]
	# pids to be removed
	# - the list must not be empty: i.e. avoid counts as range(1, 1)
	# - the elements must not be duplicated, hence the use of set()
	pids = list(
	    set([
	        R.randrange(0, process_count)
	        for s in range(1,
	                       R.randrange(1, process_count) + 1)
	    ]))
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
	return result


def do_experiments(experiment_count=100,
                   process_count=10,
                   memory_size=1000,
                   process_proportion=0.2,
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
		           process_proportion=process_proportion,
		           prints=prints))

	return print_stats(results)


# tests
results = []

print("Test 1: using unbound process sizes")
results.append(do_experiments(process_proportion=1))

print("Test 2: using bound process sizes (max size 10% of memory)")
results.append(do_experiments(process_proportion=0.1))

print("Test 3: using bound process sizes (max size 25% of memory)")
results.append(do_experiments(process_proportion=0.25))

print("Test 4: using bound process sizes (max size 50% of memory)")
results.append(do_experiments(process_proportion=0.5))

# print final stats
print("Overall success rates:")
print("\tff\tbf\twf")
for i in range(len(results)):
	print(
	    f"Test {i+1}\t{results[i][0]:.2f}\t{results[i][1]:.2f}\t{results[i][2]:.2f}"
	)

# append results to a file
with open("output.txt", "a") as output:
	output.write("Overall success rates:\n")
	output.write("\t\tff\t\tbf\t\twf\n")
	for i in range(len(results)):
		output.write(
		    f"Test {i+1}\t{results[i][0]:.2f}\t{results[i][1]:.2f}\t{results[i][2]:.2f}\n"
		)
	output.write(separator)
