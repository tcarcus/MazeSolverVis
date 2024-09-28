import asyncio
import random
import time
from helper import Cell


class Maze:
    def __init__(
        self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []

        if seed is not None:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)

    def _create_cells(self):
        for i in range(self._num_rows):
            row = []
            for j in range(self._num_cols):
                row.append(self._create_cell(i, j))
            self._cells.append(row)

    def _create_cell(self, i, j):
        x1 = self._x1 + j * self._cell_size_x
        y1 = self._y1 + i * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        cell = Cell(x1, y1, x2, y2, self._win)
        self._draw_cell(cell)
        return cell

    def _draw_cell(self, cell):
        if self._win:
            self._win.draw_cell(cell)
            self._animate()

    def _animate(self):
        if self._win:
            self._win.redraw()
            time.sleep(0.005)

    def _break_entrance_and_exit(self):
        entrance_cell = self._cells[0][0]
        entrance_cell.has_top_wall = False
        self._draw_cell(entrance_cell)

        exit_cell = self._cells[self._num_rows - 1][self._num_cols - 1]
        exit_cell.has_bottom_wall = False
        self._draw_cell(exit_cell)

    def _reset_cells_visited(self):
        for i in range(self._num_rows):
            for j in range(self._num_cols):
                self._cells[i][j].visited = False

    def _break_walls_r(self, i, j):
        current_cell = self._cells[i][j]
        current_cell.visited = True

        neighbors = [
            (0, -1, "left"),
            (0, 1, "right"),
            (-1, 0, "top"),
            (1, 0, "bottom"),
        ]

        random.shuffle(neighbors)

        for dx, dy, direction in neighbors:
            ni, nj = i + dx, j + dy

            if (
                0 <= ni < self._num_rows
                and 0 <= nj < self._num_cols
                and not self._cells[ni][nj].visited
            ):
                neighbor = self._cells[ni][nj]

                self._remove_wall(current_cell, neighbor, direction)

                self._break_walls_r(ni, nj)

    def _remove_wall(self, current_cell, neighbor, direction):
        if direction == "left":
            current_cell.has_left_wall = False
            neighbor.has_right_wall = False
        elif direction == "right":
            current_cell.has_right_wall = False
            neighbor.has_left_wall = False
        elif direction == "top":
            current_cell.has_top_wall = False
            neighbor.has_bottom_wall = False
        elif direction == "bottom":
            current_cell.has_bottom_wall = False
            neighbor.has_top_wall = False

        self._draw_cell(current_cell)
        self._draw_cell(neighbor)

    def generate_maze(self):
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    # creating a deep copy of _cells
    # because python deepcopy module
    # can not enumerate Tk objects
    def copy_cells(self):
        cells = self._cells
        new_cells = []
        for row in cells:
            new_row = []
            for cell in row:
                new_cell = Cell(
                    cell._x1,
                    cell._y1,
                    cell._x2,
                    cell._y2,
                    cell._win,
                )
                new_cell.has_top_wall = cell.has_top_wall
                new_cell.has_bottom_wall = cell.has_bottom_wall
                new_cell.has_left_wall = cell.has_left_wall
                new_cell.has_right_wall = cell.has_right_wall
                new_cell.visited = cell.visited
                new_row.append(new_cell)
            new_cells.append(new_row)
        return new_cells

    async def solve(self):
        self._reset_cells_visited()
        print("Starting to solve the maze...")
        cells_copy = self.copy_cells()
        success = await self._solve_r(0, 0, cells_copy)
        if success:
            print("Maze solved successfully!")
        else:
            print("No solution found.")

    async def _solve_r(self, i, j, mx):
        current_cell = mx[i][j]
        current_cell.visited = True

        if i == self._num_rows - 1 and j == self._num_cols - 1:
            return True

        neighbors = [
            (-1, 0, "top"),
            (1, 0, "bottom"),
            (0, 1, "right"),
            (0, -1, "left"),
        ]

        random.shuffle(neighbors)
        for dx, dy, direction in neighbors:
            ni, nj = i + dx, j + dy

            if 0 <= ni < self._num_rows and 0 <= nj < self._num_cols:
                neighbor = mx[ni][nj]

                if not neighbor.visited and self._can_move(
                    current_cell, neighbor, direction
                ):
                    self._win.draw_cell_move(current_cell, neighbor, br=True)
                    self._win.redraw()
                    await asyncio.sleep(0.1)

                    if await self._solve_r(ni, nj, mx):
                        self._win.draw_cell_move(
                            current_cell, neighbor, path=True, br=True
                        )
                        return True

                    self._win.draw_cell_move(current_cell, neighbor, undo=True, br=True)
                    self._win.redraw()
                    await asyncio.sleep(0.1)

        return False

    def _can_move(self, current_cell, neighbor, direction):
        if direction == "left":
            return not current_cell.has_left_wall and not neighbor.has_right_wall
        elif direction == "right":
            return not current_cell.has_right_wall and not neighbor.has_left_wall
        elif direction == "top":
            return not current_cell.has_top_wall and not neighbor.has_bottom_wall
        elif direction == "bottom":
            return not current_cell.has_bottom_wall and not neighbor.has_top_wall
        return False

    async def solve_dfs_bottom_right(self):
        self._reset_cells_visited()
        copy_cells = self.copy_cells()
        print("Starting to solve the maze with Bottom/Right DFS...")
        success = await self._dfs_bottom_right(0, 0, copy_cells)
        if success:
            print("Maze solved successfully!")
        else:
            print("No solution found.")

    async def _dfs_bottom_right(self, i, j, mx):
        current_cell = mx[i][j]
        current_cell.visited = True

        if i == self._num_rows - 1 and j == self._num_cols - 1:
            self._win.draw_cell_move(current_cell, mx[i][j], path=True)
            return True

        # down, right, left, up
        directions = [(1, 0), (0, 1), (0, -1), (-1, 0)]

        for direction in directions:
            ni, nj = i + direction[0], j + direction[1]
            if (
                0 <= ni < self._num_rows
                and 0 <= nj < self._num_cols
                and not mx[ni][nj].visited
            ):
                if direction == (1, 0) and not self._cells[i][j].has_bottom_wall:
                    self._win.draw_cell_move(current_cell, mx[ni][nj])
                    self._win.redraw()
                    await asyncio.sleep(0.1)

                    if await self._dfs_bottom_right(ni, nj, mx):
                        self._win.draw_cell_move(current_cell, mx[ni][nj], path=True)
                        return True

                    self._win.draw_cell_move(current_cell, mx[ni][nj], undo=True)
                    self._win.redraw()
                    await asyncio.sleep(0.3)

                elif direction == (0, 1) and not mx[i][j].has_right_wall:
                    self._win.draw_cell_move(current_cell, mx[ni][nj])
                    self._win.redraw()
                    await asyncio.sleep(0.1)

                    if await self._dfs_bottom_right(ni, nj, mx):
                        self._win.draw_cell_move(current_cell, mx[ni][nj], path=True)

                        return True

                    self._win.draw_cell_move(current_cell, mx[ni][nj], undo=True)
                    self._win.redraw()
                    await asyncio.sleep(0.3)

                elif direction == (0, -1) and not mx[ni][nj].has_right_wall:
                    self._win.draw_cell_move(current_cell, mx[ni][nj])
                    self._win.redraw()
                    await asyncio.sleep(0.1)

                    if await self._dfs_bottom_right(ni, nj, mx):
                        self._win.draw_cell_move(current_cell, mx[ni][nj], path=True)

                        return True

                    self._win.draw_cell_move(current_cell, mx[ni][nj], undo=True)
                    self._win.redraw()
                    await asyncio.sleep(0.3)

                elif direction == (-1, 0) and not mx[ni][nj].has_bottom_wall:
                    self._win.draw_cell_move(current_cell, mx[ni][nj])
                    self._win.redraw()
                    await asyncio.sleep(0.1)

                    if await self._dfs_bottom_right(ni, nj, mx):
                        self._win.draw_cell_move(current_cell, mx[ni][nj], path=True)
                        return True

                    self._win.draw_cell_move(current_cell, mx[ni][nj], undo=True)
                    self._win.redraw()
                    await asyncio.sleep(0.3)

        return False
