import math

def distance(c1, c2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1,c2)))

rgb_1 = (255,0,0)
rgb_2 = (250,0,0)

print(distance(rgb_1, rgb_2))