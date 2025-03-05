import os
import cv2
import time
from a_star import AStar

class Main:
    def __init__(self, board_path: str = "", start: tuple[int, int] = (0, 0), goal: tuple[int, int] = (0, 0)):
        if os.path.exists(board_path):
            if board_path.endswith(".txt"):
                self.read_board(board_path)
            else:
                self.read_board_from_image(board_path)
        else:
            self.board = [[0] * 8] * 8
        
        if not (self.is_free(start) and self.is_free(goal)):
            #raise Exception("Start or goal not valid")
            pass
        
        self.tiles = [
            " ", # 0 - Free spot 
            "■", # 1 - Wall
            "☻", # 2 - Player
            "X", # 3 - Goal
            "•"  # 4 - Path
            ]
        self.anim_fps = 5
        self.start = start
        self.goal = goal
        self.create_canvas([(0,0)])
        self.print_canvas()
        
    # Algorithms
    def run_a_star(self):
        """
        Runs the A* algorithm and set the route to the path that was found
        """
        alg = AStar(self.board,self.start,self.goal)
        try:
            alg.run()
            self.set_route(alg.get_path())
        except:
            print("Couldn't find a path!")
            exit()

        
    # Board
    def read_board(self, path: str) -> list[list[int]]:
        """
        ### Reads a board from a txt file, each number represents a place in the grid.
        Obs: separate each number with spaces.
        ##
        0 - For free spaces\n
        1 - For walls
        
        """
        board = []
        with open(path, 'r') as file:
            for line in file:
                board.append([x for x in list(map(int, line.split()))])

        self.board = board

    def read_board_from_image(self, path: str) -> list[list[int]]:
        """
        Does magic and create the board fom a image
        """
        board = []
        img = cv2.imread(path)
        for line in img:
            board.append([x for x in list(map(lambda x: 0 if sum(x) > 0 else 1, line))])

        self.board = board
            
    def is_free(self, place: tuple[int, int]) -> bool:
        """
        Returns true if the place on the board is a free space.
        If it's a wall, or is out of the board returns false.
        """
        board_size = (range(len(self.board)), range(len(self.board[-1])))
        return self.board[place[0]][place[1]] == 0 and\
            place[0] in board_size[0] and\
            place[1] in board_size[1]

    # Route    
    def set_route(self, route: list[tuple[int, int]]):
        self.route = route
        print(route)    

    # Canvas
    def print_canvas(self):
        """
        Displays the canvas in the terminal
        """
        if not self.canvas: raise Exception("There's no canvas")
        print(f"╔{"══" * len(self.canvas[0])}╗")
        for line in self.canvas:
            line_print = "║"
            for x in line:
                line_print += f"{self.get_tile(x)} "
            
            print(f"{line_print}║")
            
        print(f"╚{"══" * len(self.canvas[0])}╝")

    def create_canvas(self, route: list[tuple[int, int]]):
        """
        Generate the canvas to display
        """
        canvas = [[x for x in line] for line in self.board]
        canvas[self.goal[0]][self.goal[1]] = 3
        for coord in route:
            canvas[coord[0]][coord[1]] = 4
        
        player = route[-1]
        canvas[player[0]][player[1]] = 2

        self.canvas = canvas
    
    def set_tiles(self, tiles):
        self.tiles = tiles

    # Animation 
    def animate(self):
        """
        Animate the route step by step
        """
        delay = 1/self.anim_fps
        
        if not self.route: raise Exception("There's not a route to animate")
        for fase in [self.route[:i + 1] for i in range(len(self.route))]:
            os.system('clear')
            self.create_canvas(fase)
            self.print_canvas()
            time.sleep(delay)

    def get_tile(self, id: int) -> chr:
        """
        Return the tile by it's id
        """
        return self.tiles[id] if id in range(len(self.tiles)) else "🛇"

# Main
def main():
    game = Main(board_path="boards/a.png", start=(0, 30), goal=(31, 0))
    game.run_a_star()
    if game.route == None:
        print("Couldn't find a path to the end")
        return
    game.animate()

if __name__ == "__main__":
    main()