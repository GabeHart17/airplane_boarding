import airplane_boarding


rq = airplane_boarding.RandomQueue(30, ['A', 'B', 'C', 'D', 'E', 'F'], 3)
print('Random:', airplane_boarding.simulate(rq, 4, 3))
eq = airplane_boarding.EfficientQueue(30, ['A', 'B', 'C', 'D', 'E', 'F'], 3)
print('Efficient:', airplane_boarding.simulate(eq, 4, 3))
iq = airplane_boarding.InefficientQueue(30, ['A', 'B', 'C', 'D', 'E', 'F'], 3)
print('Inefficient:', airplane_boarding.simulate(iq, 4, 3))
bq = airplane_boarding.BackToFrontQueue(30, ['A', 'B', 'C', 'D', 'E', 'F'], 3)
print('Back to front:', airplane_boarding.simulate(bq, 4, 3))
gq = airplane_boarding.GroupQueue(30, ['A', 'B', 'C', 'D', 'E', 'F'], 3, 5)
print('Groups (5):', airplane_boarding.simulate(gq, 4, 3))
sq = airplane_boarding.SouthwestQueue()
print('Southwest:', airplane_boarding.simulate(sq, 4, 3))
