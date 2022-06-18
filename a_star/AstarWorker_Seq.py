import numpy
import math

from a_star.Graph import Graph


#послідовна реалізація алгоритму
class  AstarWorker_Seq:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.hueristics = []
        self.num_nodes = self.graph.maze.num_nodes

    def init_hueristics(self):
        for i in range(self.num_nodes):
            self.hueristics.append(numpy.array([0 for x in range(self.num_nodes)]))
        for y in range(self.num_nodes):
            for x in range(self.num_nodes):
                self.hueristics[y][x] = math.sqrt(math.pow((self.set_nodes[x].x - self.set_nodes[y].x), 2) + math.pow((self.set_nodes[x].y - self.set_nodes[y].y), 2))
        return self.hueristics

