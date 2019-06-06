import airplane_boarding
import matplotlib.pyplot as plt


trials = 10000
letters = ['A', 'B', 'C', 'D', 'E', 'F']
aisle = 3
rows = 30
stow_time = 4
swap_time = 3


data = []
for i in range(trials):
    queue = airplane_boarding.RandomQueue(rows, letters, aisle)
    t = airplane_boarding.simulate(queue, stow_time, swap_time)
    data.append(t)
plt.hist(data, bins=30)
plt.show()
