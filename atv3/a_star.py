import heapq
import time

class AStar:
    """
    A* pathfinding algortimh
    """
    def __init__(self, board: list[list[int]], start: tuple[int, int], goal: tuple[int, int]):
        self.board = board
        self.goal = goal
        self.start = start
        self.path = None
        
    def run(self):
        """
        Runs the pathfinding algortitm
        """
        start_time = time.time()
        self.path = self.a_star()
        self.total_time = time.time() - start_time
            

    def a_star(self):
        hell = []
        nodes = []
        nodes.append((Node(self.start, 0, 0, None)))
        while len(nodes) > 0:
            node = nodes.pop(0)
            for child in [Node(position, node.distance + 1, self.heuristic(position, self.goal), node)\
                          for position in self.get_manhattan_moves(node.position)]:
                if child.position == self.goal:
                    return child.get_path()

                if not self.uelinton(child, nodes, hell):
                    nodes.append(child)

            hell.append(node)
            nodes = sorted(nodes, key = lambda node: node.f)

        return

    def uelinton(self, bode, a: list, b: list) -> bool:
        """
        Preguiça de dar nome, mas basicamente verifica se um node com uma mesma posição que o bode
        existe em uma das listas
        """
        for node in a + b:
            if node == bode and node.f <= bode.f: return True

        return False

    def heuristic(self, start: tuple[int, int], end:tuple[int, int]) -> int:
        """
        Return the aproximated distance from start to end
        """
        return abs(end[0] - start[0]) + abs(end[1] - start[1])
    
    def is_free(self, place: tuple[int, int]) -> bool:
        """
        Returns True if the place on the board is a free space.
        If it's a wall, or is out of the board, returns False.
        """
        board_size = (range(len(self.board)), range(len(self.board[-1])))
        return (place[0] in board_size[0] and place[1] in board_size[1] and\
            self.board[place[0]][place[1]] == 0)
            
    def get_moves(self, pos: tuple[int, int]) -> list[tuple[int,int]]:
        """
        Return a list of possible moves from the pos
        """
        moves = [(pos[0] + x, pos[1] + y) for x in [-1,0,1] for y in [-1,0,1]]
        return list(filter(lambda x: self.is_free(x) and x != pos, moves))

    def get_manhattan_moves(self, pos: tuple[int, int]) -> list[tuple[int,int]]:
        """
        Return a list of possible moves from the pos, but only the up, down, left, right
        """
        moves = [(pos[0] + x, pos[1]) for x in [-1,1]] + [(pos[0], pos[1] + y) for y in [-1,1]]
        return list(filter(self.is_free, moves))
            
    def get_path(self) -> list[tuple[int, int]]:
        """
        Return the path it found
        """
        return self.path
    
    def get_total_time(self) -> float:
        """
        Return the time it took to find the path, in seconds
        """
        return self.total_time

class Node:
    def __init__(self, position: tuple[int, int], heuristic: int, distance: int, parent = None):
        self.position = position
        self.heuristic = heuristic
        self.distance = distance
        self.parent = parent
        self.f = self.distance + self.heuristic

    def get_path(self) -> list[tuple[int, int]]:
        if self.parent:
            return self.parent.get_path() + [self.position]
        
        return [self.position]
    
    def __eq__(self, other):
        return self.position == other.position
    
    def __repr__(self):
        return f"({self.position} -> {self.f})"