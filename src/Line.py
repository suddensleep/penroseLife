import matplotlib.pyplot as plt
import numpy

class Line(object):
    """
    Stores a line of the form ax + by + c = 0.
    """
    
    def __init__(self, a, b, c):
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)
        self.is_vert = self.b == 0
        self.is_horiz = self.a == 0

        if not self.is_vert:
            self.slope = -float(self.a) / self.b
        else:
            self.slope = None

    def __repr__(self):
        return "{0}*x + {1}*y + {2} = 0".format(self.a, self.b, self.c)

    def intersect(self, other):
        if self.slope == other.slope:
            return None
        elif self.is_horiz:
            return other.intersect(self)
        else:
            det1 = (other.b*self.a - self.b*other.a)
            det2 = (other.c*self.a - self.c*other.a)
            y = -det2 / det1
            return [(-self.c - self.b*y) / self.a, y]

    def get_y(self, x):
        if self.is_vert:
            return None
        return (-self.c - self.a*x) / self.b
        
    def plot(self, x_max, color):
        xs = range(-x_max, x_max + 1)
        if self.is_vert:
            plt.plot([-self.c / self.a for x in xs], xs, color)
        else:
            ys = [self.get_y(x) for x in xs]
            plt.plot(xs, ys, color)
            
if __name__ == "__main__":
    l1 = Line(1, 0, 2)
    print("l1: {}".format(l1))
    print("l1 is vertical? {}".format(l1.is_vert))
    print("l1 slope = {}".format(l1.slope))
    l2 = Line(0, 1, 2)
    print("l2: {}".format(l2))
    print("l2 is horizontal? {}".format(l2.is_horiz))
    print("l2 slope = {}".format(l2.slope))
    l3 = Line(1, 1, 2)
    print("l3: {}".format(l3))
    print("l3 is vertical? {0} l3 is horizontal? {1}".format(l3.is_vert, l3.is_horiz))
    print("l3 slope = {}".format(l3.slope))

    print("l1 and l2 intersect at: {}".format(l1.intersect(l2)))
    print("l2 and l3 intersect at: {}".format(l2.intersect(l3)))
    print("l1 and l3 intersect at: {}".format(l3.intersect(l1)))
    print("l1 intersects itself at: {}".format(l1.intersect(l1)))
