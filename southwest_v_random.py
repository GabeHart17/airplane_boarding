import statistics
import airplane_boarding


trials = 1000
stow = 4
swap = 3

southwest_res = []
random_res = []
for t in range(trials):
    sq = airplane_boarding.SouthwestQueue()
    rq = airplane_boarding.RandomQueue(30, ['A', 'B', 'C', 'D', 'E', 'F'], 3)
    southwest_res.append(airplane_boarding.simulate(sq, stow, swap))
    random_res.append(airplane_boarding.simulate(rq, stow, swap))

print('Soutwest:')
print('n', len(southwest_res))
print('mean', statistics.mean(southwest_res))
print('stdev', statistics.stdev(southwest_res))
print('\nRandom:')
print('n', len(random_res))
print('mean', statistics.mean(random_res))
print('stdev', statistics.stdev(random_res))
