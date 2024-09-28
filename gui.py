import asyncio
from tkinter import Tk, BOTH, Canvas, Frame, Button
from maze import Maze
from helper import Cell, Line


class Window:
    def __init__(self, width: int, height: int):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.geometry(f"{width}x{height}")
        self.__canvas = Canvas(self.__root, bg="#f0f0f0")
        self.__canvas.pack(side="left", fill=BOTH, expand=True)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        self.__button_frame = Frame(self.__root, bg="#ffffff")
        self.__button_frame.pack(side="right", fill="y")

        self.__size_var = None
        self.__selected_button = None
        self.create_size_buttons()

        self.start_button = Button(
            self.__button_frame,
            text="shuffle",
            command=self.start_maze,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 14),
            padx=10,
            pady=5,
        )
        self.start_button.pack(pady=10)

        self.bottom_right_button = Button(
            self.__button_frame,
            text="bottom/right",
            command=self.start_dfs_bottom_right,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 14),
            padx=10,
            pady=5,
        )
        self.bottom_right_button.pack(pady=10)

        self.overlap_button = Button(
            self.__button_frame,
            text="compare",
            command=self.start_compare,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 14),
            padx=10,
            pady=5,
        )
        self.overlap_button.pack(pady=10)

    def create_size_buttons(self):
        sizes = [
            (4, 4),  # Small
            (8, 8),  # Medium
            (12, 17),  # Large
        ]
        self.__selected_button = None

        for rows, cols in sizes:
            button = Button(
                self.__button_frame,
                text=f"{rows}x{cols}",
                bg="#e7e7e7",
                fg="black",
                font=("Arial", 12),
                padx=10,
                pady=5,
            )

            button.config(
                command=lambda r=rows, c=cols, b=button: self.set_maze_size(r, c, b)
            )
            button.pack(pady=5)

            if self.__selected_button is None:
                self.__selected_button = button
                button.config(bg="#a5d6a7")

    def set_maze_size(self, rows, cols, button):
        if self.__selected_button:
            self.__selected_button.config(bg="#e7e7e7")

        self.__size_var = (rows, cols)
        self.__selected_button = button
        button.config(bg="#a5d6a7")

    def start_maze(self):
        if self.__size_var is None:
            print("Please select a maze size first.")
            return

        rows, cols = self.__size_var
        self.__canvas.delete("all")

        maze = Maze(50, 50, rows, cols, 50, 50, self, seed=None)
        maze.generate_maze()
        Cell.set_compare(False)
        asyncio.run(maze.solve())

    def start_dfs_bottom_right(self):
        if self.__size_var is None:
            print("Please select a maze size first.")
            return

        rows, cols = self.__size_var
        self.__canvas.delete("all")

        maze = Maze(50, 50, rows, cols, 50, 50, self, seed=None)
        Cell.set_compare(False)
        maze.generate_maze()
        asyncio.run(maze.solve_dfs_bottom_right())

    def start_compare(self):
        if self.__size_var is None:
            print("Please select a maze size first.")
            return

        rows, cols = self.__size_var
        self.__canvas.delete("all")
        maze = Maze(50, 50, rows, cols, 50, 50, self, seed=None)

        maze.generate_maze()
        Cell.set_compare(True)
        asyncio.run(self.fuckPythonAsync(maze))

    async def fuckPythonAsync(self, maze):
        rows, cols = self.__size_var
        t1 = asyncio.create_task(maze.solve())
        t2 = asyncio.create_task(maze.solve_dfs_bottom_right())
        await asyncio.gather(t1, t2)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def draw_line(self, line: Line, fill_color: str):
        line.draw(self.__canvas, fill_color)

    def draw_cell(self, cell):
        cell.draw(self.__canvas)

    def draw_cell_move(self, from_cell, to_cell, undo=False, path=False, br=False):
        from_cell.draw_move(to_cell, self.__canvas, undo, path, br)

    def wait_for_close(self):
        self.__running = True

        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False
        self.__root.destroy()
