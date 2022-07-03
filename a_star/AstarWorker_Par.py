from typing import TYPE_CHECKING

import threading

from a_star.ReferenceType import ReferenceType
from a_star.vec2 import Vec2
from a_star.Astar_Par import Astar_Par

class AstarWorker_Par (threading.Thread):
    def __init__(self, 
    num_thread,
    astar_par: Astar_Par, open, closed, previous, target: Vec2, start_node: Vec2, 
    current: ReferenceType, 
    min_cost: ReferenceType,
    best_node: ReferenceType,
    total_cost: ReferenceType,
    g,
    F: ReferenceType,
    F_neibor: ReferenceType,
    neibor_current: ReferenceType,
    new_open_node):
        threading.Thread.__init__(self)
        self.num_thread = num_thread
        self.algorithm: Astar_Par = astar_par
        self.open = open
        self.closed = closed
        self.previous = previous
        self.target: Vec2 = target
        self.start_node: Vec2 = start_node
        self.current: ReferenceType = current
        self.min_cost: ReferenceType = min_cost
        self.best_node: ReferenceType = best_node
        self.total_cost: ReferenceType = total_cost
        self.g = g
        self.F: ReferenceType = F
        self.F_neibor: ReferenceType = F_neibor
        self.neibor_current: ReferenceType = neibor_current
        self.new_open_node = new_open_node


    def run(self):
        self.algorithm.base_algorithm(
            self.num_thread,
            self.open, 
            self.closed, 
            self.previous, 
            Vec2(self.target.x, self.target.y),
            Vec2(self.start_node.x, self.start_node.y), 
            self.current, 
            self.min_cost,
            self.best_node, 
            self.total_cost, 
            self.g,  
            self.F, 
            self.F_neibor, 
            self.neibor_current, 
            self.new_open_node
        )