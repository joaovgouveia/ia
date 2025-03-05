import time

class AStar:
    """
    A* pathfinding algortimh
    """
    def __init__(self, board: list[list[int]], start: tuple[int, int], end: tuple[int, int]):
        self.board = board
        self.end = end
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
        open_nodes = [Node(self.start, 0, 0, None)]
        closed = []
        while len(open_nodes) > 0:
            open_nodes = sorted(open_nodes, key = lambda n: n.f)
            current = open_nodes.pop(0)
            closed.append(current)
            if current.position == self.end:
                return current.get_path()

            for neighbour in [Node(position, self.heuristic(position, self.end), current.g + 1, current)\
                              for position in self.get_moves(current.position)]:
                
                if neighbour in closed:
                    continue

                if not neighbour in open_nodes:
                    open_nodes.append(neighbour)
                
                for i in range(len(open_nodes)):
                    if neighbour == open_nodes[i] and neighbour.g < open_nodes[i].g:
                        open_nodes.pop(i)
                        open_nodes.append(neighbour)

        return

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
    def __init__(self, position: tuple[int, int], h: int, g: int, parent = None):
        self.position = position
        self.h = h
        self.g = g
        self.parent = parent
        self.f = self.g + self.h

    def set_parent(self, new_parent):
        self.parent = new_parent

    def get_path(self) -> list[tuple[int, int]]:
        if self.parent:
            return self.parent.get_path() + [self.position]
        
        return [self.position]
    
    def __eq__(self, other):
        return self.position == other.position
    
    def __repr__(self):
        return f"({self.position} - {self.f})"