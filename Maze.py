import tkinter as tk
import random

# Maze settings
CELL_SIZE = 20
MAZE_WIDTH = 20
MAZE_HEIGHT = 15

# Directions: (dx, dy)
DIRS = {
    "N": (0, -1),
    "S": (0, 1),
    "E": (1, 0),
    "W": (-1, 0)
}

OPPOSITE = {
    "N": "S",
    "S": "N",
    "E": "W",
    "W": "E"
}

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = {}
        self.generate_maze()

    def generate_maze(self):
        def carve_passages(x, y, maze):
            dirs = list(DIRS.keys())
            random.shuffle(dirs)
            for direction in dirs:
                dx, dy = DIRS[direction]
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.width) and (0 <= ny < self.height) and ((nx, ny) not in maze):
                    maze[(x, y)] = maze.get((x, y), []) + [direction]
                    maze[(nx, ny)] = maze.get((nx, ny), []) + [OPPOSITE[direction]]
                    carve_passages(nx, ny, maze)

        # Start carving from the top-left corner
        carve_passages(0, 0, self.maze)

        # Ensure the bottom-right corner is reachable
        if (self.width - 1, self.height - 1) not in self.maze:
            self.maze[(self.width - 2, self.height - 1)] = self.maze.get((self.width - 2, self.height - 1), []) + ["E"]
            self.maze[(self.width - 1, self.height - 1)] = ["W"]

class MazeGame(tk.Frame):
    def __init__(self, master, maze):
        super().__init__(master)
        self.master = master
        self.maze = maze
        self.player_x = 0
        self.player_y = 0
        self.canvas = tk.Canvas(self, width=MAZE_WIDTH * CELL_SIZE, height=MAZE_HEIGHT * CELL_SIZE, bg='white')
        self.canvas.pack()
        self.draw_maze()
        self.draw_player()
        self.master.bind("<Key>", self.move_player)
        self.pack()

    def draw_maze(self):
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cx = x * CELL_SIZE
                cy = y * CELL_SIZE
                walls = self.maze.maze.get((x, y), [])
                if "N" not in walls:
                    self.canvas.create_line(cx, cy, cx + CELL_SIZE, cy)
                if "S" not in walls:
                    self.canvas.create_line(cx, cy + CELL_SIZE, cx + CELL_SIZE, cy + CELL_SIZE)
                if "W" not in walls:
                    self.canvas.create_line(cx, cy, cx, cy + CELL_SIZE)
                if "E" not in walls:
                    self.canvas.create_line(cx + CELL_SIZE, cy, cx + CELL_SIZE, cy + CELL_SIZE)

    def draw_player(self):
        x1 = self.player_x * CELL_SIZE + 5
        y1 = self.player_y * CELL_SIZE + 5
        x2 = (self.player_x + 1) * CELL_SIZE - 5
        y2 = (self.player_y + 1) * CELL_SIZE - 5
        self.player = self.canvas.create_oval(x1, y1, x2, y2, fill='blue')

    def move_player(self, event):
        dx, dy = 0, 0
        key = event.keysym
        if key == "Up" and "N" in self.maze.maze.get((self.player_x, self.player_y), []):
            dy = -1
        elif key == "Down" and "S" in self.maze.maze.get((self.player_x, self.player_y), []):
            dy = 1
        elif key == "Left" and "W" in self.maze.maze.get((self.player_x, self.player_y), []):
            dx = -1
        elif key == "Right" and "E" in self.maze.maze.get((self.player_x, self.player_y), []):
            dx = 1

        new_x = self.player_x + dx
        new_y = self.player_y + dy
        if 0 <= new_x < self.maze.width and 0 <= new_y < self.maze.height:
            self.player_x = new_x
            self.player_y = new_y
            self.canvas.move(self.player, dx * CELL_SIZE, dy * CELL_SIZE)
            self.check_win()

    def check_win(self):
        if self.player_x == self.maze.width - 1 and self.player_y == self.maze.height - 1:
            self.canvas.create_text(MAZE_WIDTH * CELL_SIZE // 2, MAZE_HEIGHT * CELL_SIZE // 2, text="You Win!", font=("Arial", 24), fill="green")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Simple Maze Game")
    maze = Maze(MAZE_WIDTH, MAZE_HEIGHT)
    game = MazeGame(root, maze)
    root.mainloop()