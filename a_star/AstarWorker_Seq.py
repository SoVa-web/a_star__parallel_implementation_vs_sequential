import numpy
import math
import sys

from a_star.Graph import Graph
from a_star.vec2 import Vec2


#послідовна реалізація алгоритму
class  AstarWorker_Seq:
    def __init__(self, graph: Graph, start: Vec2, target: Vec2):
        self.graph = graph
        self.start = start
        self.target = target
        self.hueristics = []
        self.num_nodes = self.graph.maze.num_nodes
        self.g = [0 for i in range(self.num_nodes)]
        self.previous = [None for i in range(self.num_nodes)]
        self.openlist = [self.graph.set_all_nodes.index(self.start)]
        self.closedlist = []
        self.new_open_node = []
        self.current_node = None

        #ініціалізація змінних для методу choose_node
        self.mincost = sys.maxsize
        self.best_node = None
        self.cost_start_to_node = None
        self.cost_node_to_goal = None
        self.total_cost = None

        self.hueristics = self.init_hueristics()
    
    def algorithm(self): 
        while self.openlist:
            self.current_node = self.choose_node()
            if self.current_node == self.graph.set_all_nodes.index(self.target):
                return self.build_path(self.current_node)
            self.openlist.remove(self.current_node)
            self.closedlist.append(self.current_node)
            self.get_adjacent_nodes()
            for adjacent in self.new_open_node:
                if adjacent not in self.openlist:
                    self.openlist.append(adjacent)
                    self.previous[adjacent] = self.current_node
                    self.g[adjacent] = self.g[self.current_node] + self.graph.matrix_adjacency[self.current_node][adjacent]
                if self.g[self.current_node] + 1  < self.g[adjacent]: 
                    self.previous[adjacent] = self.current_node
                    self.g[adjacent] = self.g[self.current_node] + 1
        return []

    def choose_node(self):
        self.min_cost = sys.maxsize
        self.best_node = None
        for node in self.openlist:
            self.cost_start_to_node = self.g[node]
            self.cost_node_to_goal = self.hueristics[node][self.graph.set_all_nodes.index(self.target)]
            self.total_cost = self.cost_start_to_node + self.cost_node_to_goal
            if self.min_cost > self.total_cost:
                self.min_cost = self.total_cost
                self.best_node = node
        return self.best_node

    def build_path(self, to_node):
        path = []
        while self.previous[to_node] != None:
            path.append(self.graph.set_all_nodes[to_node])
            for node in self.closedlist:
                if self.previous[to_node] == node:
                    to_node = node
        path.append(self.start)
        path.reverse()
        return path

    def get_adjacent_nodes(self):
        self.new_open_node = []
        for adjacent in range(self.num_nodes):
            if self.graph.matrix_adjacency[self.current_node][adjacent] == 1:
                self.new_open_node.append(adjacent)
        for closed_node in self.closedlist:
            if closed_node in self.new_open_node:
                self.new_open_node.remove(closed_node)


    #Евклідівська відстань/Euclidean distance
    def init_hueristics(self):
        for i in range(self.num_nodes):
            self.hueristics.append(numpy.array([0 for x in range(self.num_nodes)]))
        for y in range(self.num_nodes):
            for x in range(self.num_nodes):
                self.hueristics[y][x] = math.sqrt(math.pow((self.graph.set_all_nodes[x].x - self.graph.set_all_nodes[y].x), 2) + math.pow((self.graph.set_all_nodes[x].y - self.graph.set_all_nodes[y].y), 2))
        return self.hueristics

