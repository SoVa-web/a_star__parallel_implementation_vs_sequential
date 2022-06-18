from a_star.Maze import Maze
from a_star.vec2 import Vec2

import numpy 

#представимо лабіринт через граф
class Graph:
    def __init__(self, maze: Maze):
        self.maze = maze
        self.set_all_nodes = []
        self.matrix_adjacency = []

        self.init_set_nodes()
        self.init_matrix_adjacency()


    def init_set_nodes(self):
        num_rows = self.maze.size
        while num_rows > 0:
            num_columns = self.maze.size
            num_rows -= 1
            while num_columns > 0:
                num_columns -= 1
                self.set_all_nodes.append(Vec2(num_columns, num_rows))
        self.set_all_nodes.reverse()

    def init_matrix_adjacency(self):
        num_rows = self.maze.num_nodes
        num_columns = self.maze.num_nodes
        for i in range(num_rows):
            self.matrix_adjacency.append(numpy.array([0 for x in range(num_columns)]))
        dir = [Vec2(+1, 0), Vec2(-1, 0), Vec2(0, +1), Vec2(0, -1)]
        for i in dir:
             for iter in range(self.maze.num_nodes):
                if self.can_draw_edge_graph(self.set_nodes[iter] + i):
                        index_adj = self.set_nodes.index((self.set_nodes[iter] + i))
                        if self.can_draw_edge_graph((self.set_nodes[iter])) and iter != index_adj:
                            self.matrix_adjacency[iter][index_adj] = self.matrix_adjacency[index_adj][iter] = 1

    def can_draw_edge_graph(self, pos: Vec2):
        if not (0 <= pos.x < self.maze.size and 0 <= pos.y < self.maze.size):
            return False
        for block_node in self.maze.blocked_nodes:
            if block_node.pos == pos:
                return False
        return True

    