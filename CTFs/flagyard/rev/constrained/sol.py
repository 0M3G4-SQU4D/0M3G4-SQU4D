from z3 import *
import random

magic = [6596, 29872, 62287, 15227, 36671, 60341, 63931, 1709, 41434, 63916, 60583, 25325, 38705, 55592, 60787, 38714, 17528, 44216, 27185, 8035, 15695, 26256, 40808, 56784, 29555, 46895, 34850, 64576, 18532, 144, 31896, 4615, 17391, 26277, 32664, 8643, 13327, 16877, 43771, 54171, 59881, 62544, 54976, 10049, 30360, 9514, 26232, 21331, 17184, 2651, 63297, 1680, 54032, 43896, 6491, 56666, 48037]

random.seed(1337)

solver = Solver()


flag = [BitVec(f'flag{i}',16) for i in range(52)]

l = []

for i in range(56):
    a = random.randint(0, 51)
    b = random.randint(0, 51)
    c = random.randint(0, 51)
    d = random.randint(0, 51)
    l.append((a,b,c,d))
    eq = ((flag[a] << 8) + flag[b]) * ((flag[c] << 8) + flag[d]) & 65535
    print(eq)
    solver.add(eq == magic[i])

for i in range(52):
    solver.add(flag[i] <= 125)
    solver.add(flag[i] >= 48)

#solver.add(flag[i] == ord('g'))

for i in l:
    #print(i)
    if 3 in i:
        print(i)




if solver.check() == sat:
    model = solver.model()
    f = ""
    solution = {str(var): model[var] for var in flag}
    for k in flag:
        f += chr(model.eval(k).as_long())
    print(f)
    print("Solution:", solution)
else:
    print("No solution found")