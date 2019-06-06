import airplane_boarding
import statistics


trials = 50

data = {1: -1, 2: -1, 3: -1, 4: -1, 6: -1, 8: -1, 12: -1, 16: -1, 32: -1, 64: -1, 128: -1}
for g in data.keys():
    results = []
    for t in range(trials):
        queue = airplane_boarding.GroupQueue(128,  # hypothetical plane with 128 rows
                                             ['A', 'B', 'C', 'D', 'E', 'F'],
                                             3,
                                             g)
        results.append(airplane_boarding.simulate(queue, 4, 3))
    data[g] = statistics.mean(results)

random_data = []
inefficient_data = []
for t in range(trials):
    rqueue = airplane_boarding.RandomQueue(128,
                                           ['A', 'B', 'C', 'D', 'E', 'F'],
                                           3)
    iqueue = airplane_boarding.InefficientQueue(128,
                                                ['A', 'B', 'C', 'D', 'E', 'F'],
                                                3)
    random_data.append(airplane_boarding.simulate(rqueue, 4, 3))
    inefficient_data.append(airplane_boarding.simulate(iqueue, 4, 3))

print(f'for each, n = {trials}\n')
print('groups | time')
print('-------+-------')
for g, m in zip(data.keys(), data.values()):
    print(' ' + str(g).ljust(6) + '| ' + str(m))
print('-------+-------')
print(f'random | {statistics.mean(random_data)}')
print(f'infcnt | {statistics.mean(inefficient_data)}')
