from a_star.AstarWorker_Par import AstarWorker_Par
from a_star.config import(
    SIZE,
    START_X,
    START_Y,
    TARGET_X,
    TARGET_Y,
    PART_FREE_ROW_COL,
    PART_FREE_NODE
)

from a_star.Maze import Maze
from a_star.vec2 import Vec2
from a_star.Graph import Graph
from a_star.AstarWorker_Seq import AstarWorker_Seq
from a_star.Astar_Par import Astar_Par


import sys
from datetime import datetime



def parallel_worker(astar: Astar_Par):
        # потік, що виконує пошук від старту до цілі
        thread_1 = AstarWorker_Par( 
            1,
            astar,
            astar.openlist_1,
            astar.closedlist_1,
            astar.previous_1,
            Vec2(astar.target.x, astar.target.y),
            Vec2(astar.start.x, astar.start.y),
            astar.current_node_1,
            astar.min_cost_1,
            astar.best_node_1,
            astar.total_cost_1,
            astar.g_1,
            astar.g_2,
            astar.F_1,
            astar.F_2,
            astar.current_node_2,
            astar.new_open_node_1
        )
        # потік, що виконує пошук від цілі до старту
        thread_2 = AstarWorker_Par( 
            2,
            astar,
            astar.openlist_2,
            astar.closedlist_2,
            astar.previous_2,
            Vec2(astar.start.x, astar.start.y),
            Vec2(astar.target.x, astar.target.y),
            astar.current_node_2,
            astar.min_cost_2,
            astar.best_node_2,
            astar.total_cost_2,
            astar.g_2,
            astar.g_1,
            astar.F_2,
            astar.F_1,
            astar.current_node_1,
            astar.new_open_node_2
        )

        thread_1.start()
        thread_2.start()
        thread_1.join()
        thread_2.join()

        part1 = astar.build_path(astar.current_node_1.value, astar.graph.set_all_nodes.index(astar.start), astar.previous_1, astar.closedlist_1)
        part2 = astar.build_path(astar.current_node_2.value, astar.graph.set_all_nodes.index(astar.target), astar.previous_2, astar.closedlist_2)
        part2.reverse()
        print(part1, part2)
        print("Work parallel done!!!")


def main():
    
    sys.setrecursionlimit(1500) 
    maze = Maze(SIZE, PART_FREE_ROW_COL, PART_FREE_NODE)
    maze.generator_2()
    maze.reading_prototype()
    for i in range(SIZE):
        print(maze.matrix_prototype[i])
    graph = Graph(maze)

    #sequantial worker
    f = datetime.now()
    seq_worker = AstarWorker_Seq(graph,  Vec2(START_X, START_Y), Vec2(TARGET_X, TARGET_Y))
    path_seq = seq_worker.algorithm()
    final_f = datetime.now() - f
    print("Path by sequantial algorithm: ")
    print(path_seq)
    

    #parallel worker
    final_f_2 = datetime.now() 
    par_astar = Astar_Par(graph,  Vec2(START_X, START_Y), Vec2(TARGET_X, TARGET_Y))
    parallel_worker(par_astar)
    final_f_2 = datetime.now() - final_f_2
    print("First algorithm: " + str(final_f))
    print("Second algorithm: " + str(final_f_2))

if __name__ == '__main__':
    main()
