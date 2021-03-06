from random import *
import numpy as np
from a_star.vec2 import Vec2
from a_star.Block import Block

#--Лабіринт імплементований у вигляді матриці--
class Maze:
    def __init__(self, size, part_free_row_col, part_free_node):
        self.size = size #розмірність матриці
        self.blocked_nodes = [] #заблоковані вершини
        self.num_nodes = size*size #кількість вершин всього
        self.matrix_prototype = [] #матриця прототип лабіринту: 0 - вільна вершина, 1- заблокована; використовується лише для генерації та демострації
        self.matrix_adjacency = [] #матриця суміжності вершин
        self.part_free_row_col = part_free_row_col
        self.part_free_node = part_free_node

    #алгоритм генерації випадкового завжди консистентного лабіринту за заданою розмірністю
    #з однаковою щільністю лабіринту, що важливо для досліджень ефективності роботи алгоритмів А* на лабіринтах різних розмірностей
    #застосовуваний для квадраних матриць
    def generator_2(self):
        #рядки і стовбці вільних вершин, ініціалізуються першими і останніми рядками/стовбцями
        #оскільки на них будуть знаходитись початкова і кінцеві вершини
        free_row_cols = [0, (self.size-1)]
        #кількість вільних рядків/стовбців без урахування перших і останніх
        num_free_row_cols = self.size // self.part_free_row_col
        #кількість окремо вільних вершин
        num_free_nodes = self.num_nodes // self.part_free_node

        #перевірка чи вільна вершина
        def is_free_nodes(x, y):
            for i in range(self.size):
                for j in range(self.size):
                    if (y == i and x == j): return False
            return True

        #генерація вільної вершини
        def gen_free_node():
            node_x = randint(0, (self.size - 1))
            node_y = randint(0, (self.size - 1))
            if( not is_free_nodes(node_x, node_y)): 
                self.matrix_prototype[node_x][node_y] = 0
                return
            else: return gen_free_node()

        #перевірка чи вільний рядок/стовбець
        def is_free_row_col(num):
            for i in free_row_cols:
                if i == num : return True
            return False

        #генерація вільних рядків/стовбців, без повторів (без першого і останнього рядка)
        def gen_free_row_col():
            num = randint(1, self.size-2)
            if is_free_row_col(num): return gen_free_row_col()
            else: return num

        #ініціюємо прототип блокованими вершинами
        self.matrix_prototype = []
        for i in range(self.size):
            self.matrix_prototype.append(np.array([1 for x in range(self.size)]))
        
        #генеруємо вільні рядки/стовбці вершин
        for i in range(num_free_row_cols):
            free_row_cols.append(gen_free_row_col())
        
        for num in free_row_cols:
            for i in range(self.size):
                self.matrix_prototype[num][i] = 0
                self.matrix_prototype[i][num] = 0
        
        #генеруємо вільні вершини
        for i in range(num_free_nodes):
            gen_free_node()


    #зчитуємо блоковані вершини у масив
    def reading_prototype(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.matrix_prototype[i][j] == 1:
                    self.blocked_nodes.append(Block(Vec2(j, i)))
                    print(Vec2(j, i))
        
