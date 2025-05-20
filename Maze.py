import tkinter as tk
import random
import time

# Maze settings
CELL_SIZE = 20
MAZE_WIDTH = 20
MAZE_HEIGHT = 15

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
        self.maze = {(x, y): [] for x in range(width) for y in range(height)}
        self.generate_maze()

    def generate_maze(self):
        def carve_passages(x, y):
            dirs = list(DIRS.keys())
            random.shuffle(dirs)
            for direction in dirs:
                dx, dy = DIRS[direction]
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height and not self.maze[(nx, ny)]:
                    self.maze[(x, y)].append(direction)
                    self.maze[(nx, ny)].append(OPPOSITE[direction])
                    carve_passages(nx, ny)
        carve_passages(0, 0)

        # Ensure exit is reachable
        if "W" not in self.maze[(self.width - 1, self.height - 1)]:
            self.maze[(self.width - 1, self.height - 1)].append("W")
            self.maze[(self.width - 2, self.height - 1)].append("E")

class MazeGame(tk.Frame):
    def __init__(self, master, maze):
        super().__init__(master)
        self.master = master
        self.maze = maze
        self.player_x = 0
        self.player_y = 0
        self.moves = 0
        self.start_time = time.time()
        self.editing = True  # Start in editor mode
        self.canvas = tk.Canvas(self, width=MAZE_WIDTH * CELL_SIZE, height=MAZE_HEIGHT * CELL_SIZE, bg='white')
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.toggle_wall)

        self.info = tk.Label(self, text="Editor Mode: Click to toggle walls. Press Enter to start.")
        self.info.pack()

        self.master.bind("<Key>", self.handle_key)
        self.pack()
        self.draw_maze()
        self.draw_player()

        self.update_timer()

    def draw_maze(self):
        self.canvas.delete("wall")
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cx = x * CELL_SIZE
                cy = y * CELL_SIZE
                walls = self.maze.maze.get((x, y), [])
                if "N" not in walls:
                    self.canvas.create_line(cx, cy, cx + CELL_SIZE, cy, tag="wall")
                if "S" not in walls:
                    self.canvas.create_line(cx, cy + CELL_SIZE, cx + CELL_SIZE, cy + CELL_SIZE, tag="wall")
                if "W" not in walls:
                    self.canvas.create_line(cx, cy, cx, cy + CELL_SIZE, tag="wall")
                if "E" not in walls:
                    self.canvas.create_line(cx + CELL_SIZE, cy, cx + CELL_SIZE, cy + CELL_SIZE, tag="wall")

    def draw_player(self):
        x1 = self.player_x * CELL_SIZE + 5
        y1 = self.player_y * CELL_SIZE + 5
        x2 = (self.player_x + 1) * CELL_SIZE - 5
        y2 = (self.player_y + 1) * CELL_SIZE - 5
        self.player = self.canvas.create_oval(x1, y1, x2, y2, fill='blue', tag="player")

    def handle_key(self, event):
        if self.editing:
            if event.keysym == "Return":
                self.editing = False
                self.info.config(text="Moves: 0 | Time: 0s")
            return

        dx, dy = 0, 0
        key = event.keysym
        directions = self.maze.maze.get((self.player_x, self.player_y), [])
        if key == "Up" and "N" in directions:
            dy = -1
        elif key == "Down" and "S" in directions:
            dy = 1
        elif key == "Left" and "W" in directions:
            dx = -1
        elif key == "Right" and "E" in directions:
            dx = 1

        new_x = self.player_x + dx
        new_y = self.player_y + dy
        if 0 <= new_x < self.maze.width and 0 <= new_y < self.maze.height:
            self.player_x = new_x
            self.player_y = new_y
            self.canvas.move(self.player, dx * CELL_SIZE, dy * CELL_SIZE)
            self.moves += 1
            self.update_info()
            self.check_win()

    def toggle_wall(self, event):
        if not self.editing:
            return

        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE
        if x >= MAZE_WIDTH or y >= MAZE_HEIGHT:
            return

        # Find nearest wall
        cx = x * CELL_SIZE
        cy = y * CELL_SIZE
        offset_x = event.x - cx
        offset_y = event.y - cy

        dir = None
        if offset_y < 5:
            dir = "N"
        elif offset_y > CELL_SIZE - 5:
            dir = "S"
        elif offset_x < 5:
            dir = "W"
        elif offset_x > CELL_SIZE - 5:
            dir = "E"

        if dir:
            dx, dy = DIRS[dir]
            nx, ny = x + dx, y + dy
            if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT:
                cell = self.maze.maze[(x, y)]
                neighbor = self.maze.maze[(nx, ny)]
                if dir in cell:
                    cell.remove(dir)
                    neighbor.remove(OPPOSITE[dir])
                else:
                    cell.append(dir)
                    neighbor.append(OPPOSITE[dir])
                self.draw_maze()

    def update_info(self):
        elapsed = int(time.time() - self.start_time)
        self.info.config(text=f"Moves: {self.moves} | Time: {elapsed}s")

    def update_timer(self):
        if not self.editing:
            self.update_info()
        self.master.after(1000, self.update_timer)

    def check_win(self):
        if self.player_x == self.maze.width - 1 and self.player_y == self.maze.height - 1:
            self.canvas.create_text(MAZE_WIDTH * CELL_SIZE // 2, MAZE_HEIGHT * CELL_SIZE // 2, text="You Win!", font=("Arial", 24), fill="green")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Maze Game with Editor, Timer & Moves")
    maze = Maze(MAZE_WIDTH, MAZE_HEIGHT)
    game = MazeGame(root, maze)
    root.mainloop()
