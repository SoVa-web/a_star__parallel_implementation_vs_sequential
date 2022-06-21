import string
from xml.etree.ElementTree import tostring
from a_star.Graph import Graph
from a_star.vec2 import Vec2
from a_star.ReferenceType import ReferenceType

import sys
import numpy
import math

import threading



class Astar_Par:
    def __init__(self, graph: Graph, start: Vec2, target: Vec2):
        self.threadLock = threading.Lock()

        # спільні дані для всіх потоків
        # {{
        self.graph = graph
        self.hueristics = []
        self.num_nodes = self.graph.maze.num_nodes

        # спільні дані, котрі змінюють потоки
        self.middle = [] # всі вершини, що знаходяться між двох пошуків, спочатку там знаходяться всі вершини
        self.L = sys.maxsize # зберігається найкраще рішення знайдене на даних момент, що дорівнює сумі g_1 i g_2
        # }}

        self.start = start
        self.target = target

        self.openlist_1 = [self.graph.set_all_nodes.index(self.start)]
        self.openlist_2 = [self.graph.set_all_nodes.index(self.target)]

        self.closedlist_1 = []
        self.closedlist_2 = []

        self.current_node_1: ReferenceType = ReferenceType()
        self.current_node_1.value = self.graph.set_all_nodes.index(self.start)
        self.current_node_2: ReferenceType = ReferenceType()
        self.current_node_2.value = self.graph.set_all_nodes.index(self.target)

        self.min_cost_1: ReferenceType = ReferenceType()
        self.min_cost_2: ReferenceType = ReferenceType()

        self.best_node_1: ReferenceType = ReferenceType()
        self.best_node_2: ReferenceType = ReferenceType()

        self.total_cost_1: ReferenceType = ReferenceType()
        self.total_cost_2: ReferenceType = ReferenceType()

        self.g_1 = [0 for i in range(self.num_nodes)]
        self.g_2 = [0 for i in range(self.num_nodes)]
        self.g_1[self.graph.set_all_nodes.index(self.start)] = 0
        self.g_2[self.graph.set_all_nodes.index(self.target)] = 0

        self.F_1: ReferenceType = ReferenceType()
        self.F_2: ReferenceType = ReferenceType()

        self.previous_1 = [None for i in range(self.num_nodes)]
        self.previous_2 = [None for i in range(self.num_nodes)]

        self.new_open_node_1 = []
        self.new_open_node_2 = []

        self.init_middle()
        self.hueristics = self.init_hueristics()

        

    def base_algorithm(
        self,
        num_thread,
        open,
        closed,
        previous,
        target,
        start,
        current: ReferenceType,
        min_cost: ReferenceType,
        best_node: ReferenceType,
        total_cost: ReferenceType,
        g,
        g_2,
        F: ReferenceType,
        F_neibor: ReferenceType,
        neibor_current: ReferenceType,
        new_open_node,
    ):
        while open and self.middle:
            current.value = self.choose_node(min_cost, best_node, open, total_cost, g, target)
            print("We in line 92 in thread number  " + str(num_thread) + "\n" + str(current.value) + "\n")
            if self.in_middle(current.value):
                func = (g[current.value] + self.hueristics[current.value][self.graph.set_all_nodes.index(target)])
                potential = F_neibor.value - self.hueristics[neibor_current.value][self.graph.set_all_nodes.index(start)]
                potential += g[current.value]
                print("We in ine 94 in thread number  " + str(num_thread) + "\n" + str(func) + "\n" + str(potential) + "\n" + str(self.L) + "\n")
                if func >= self.L or potential >= self.L:
                    # видаляємо current із middle і не розширюємо вузол
                    self.middle.remove(self.graph.set_all_nodes[current.value])
                else:
                    # алгоритм працює далі з поточною вершиною
                    new_open_node = self.get_adjacent_nodes(new_open_node, current, closed)
                    print("We in ine 103 in thread number  " + str(num_thread) + "\n" + str(new_open_node) + "\n")
                    for adjacent in new_open_node:
                        if self.in_middle(adjacent):
                            self.threadLock.acquire
                            F.value = min(F.value, g[current.value] + self.graph.matrix_adjacency[current.value][adjacent] + g_2[neibor_current.value] + self.hueristics[current.value][neibor_current.value])
                            self.L = min(F.value, F_neibor.value)
                            self.threadLock.release
                            if adjacent not in open:
                                open.append(adjacent)
                                previous[adjacent] = current.value
                                g[adjacent] = (g[current.value] + self.graph.matrix_adjacency[current.value][adjacent])
                            if g[current.value] + 1 < g[adjacent]:
                                previous[adjacent] = current.value
                                g[adjacent] = (g[current.value] + self.graph.matrix_adjacency[current.value][adjacent])
                    self.middle.remove(self.graph.set_all_nodes[current.value])
            open.remove(current.value)
            print("We in line 116 in thread number  " + str(num_thread) + "\n" + str(open) + "\n")
            closed.append(current.value)

    def in_middle(self, current):
        for i in self.middle:
            if i == self.graph.set_all_nodes[current]:
                return True
        return False



    def get_adjacent_nodes(self, new_open_node, current: ReferenceType, closed):
        new_open_node = []
        for adjacent in range(self.num_nodes):
            # на відміну від послідовного перевіряємо чи сусідні вершини є між двох пошуків
            if self.graph.matrix_adjacency[current.value][adjacent] == 1:
                new_open_node.append(adjacent)
        for closed_node in closed:
            if closed_node in new_open_node:
                new_open_node.remove(closed_node)
        return new_open_node



    def choose_node(self, min_cost: ReferenceType, best_node: ReferenceType, open, total_cost: ReferenceType, g, target):
        min_cost.value = sys.maxsize
        best_node.value = None
        for node in open:
            total_cost.value = (
                g[node] + self.hueristics[node][self.graph.set_all_nodes.index(target)]
            )
            if min_cost.value > total_cost.value:
                min_cost.value = total_cost.value
                best_node.value = node
        return best_node.value

    def init_middle(self):
        self.middle = self.graph.set_all_nodes.copy()



    # Евклідівська відстань/Euclidean distance
    def init_hueristics(self):
        for i in range(self.num_nodes):
            self.hueristics.append(numpy.array([0 for x in range(self.num_nodes)]))
        for y in range(self.num_nodes):
            for x in range(self.num_nodes):
                self.hueristics[y][x] = math.sqrt(
                    math.pow(
                        (self.graph.set_all_nodes[x].x - self.graph.set_all_nodes[y].x),
                        2,
                    )
                    + math.pow(
                        (self.graph.set_all_nodes[x].y - self.graph.set_all_nodes[y].y),
                        2,
                    )
                )
        return self.hueristics
