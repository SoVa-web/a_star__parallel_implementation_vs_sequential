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
import sys
def main():
    
    sys.setrecursionlimit(1500) 
   
    maze = Maze(SIZE, Vec2(START_X, START_Y), Vec2(TARGET_X, TARGET_Y), PART_FREE_ROW_COL, PART_FREE_NODE)
    
    maze.generator_2()
    print("we in nain")
    print(SIZE)
    for i in range(SIZE):
        print(maze.matrix_prototype[i])

if __name__ == '__main__':
    main()
