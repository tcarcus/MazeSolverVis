import math
from tkinter import Canvas


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(
            self.point1.x,
            self.point1.y,
            self.point2.x,
            self.point2.y,
            fill=fill_color,
            width=2,
        )


class Cell:
    def __init__(self, x1, y1, x2, y2, win=None):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._win = win

        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True

        self.visited = False

    compare = False

    @classmethod
    def set_compare(c, state: bool):
        c.compare = state

    def draw(self, canvas: Canvas):
        if canvas:
            # OS dependent
            bg_color = "#d9d9d9"

            if self.has_left_wall:
                canvas.create_line(
                    self._x1, self._y1, self._x1, self._y2, fill="black", width=2
                )
            else:
                canvas.create_line(
                    self._x1, self._y1, self._x1, self._y2, fill=bg_color, width=2
                )

            if self.has_right_wall:
                canvas.create_line(
                    self._x2, self._y1, self._x2, self._y2, fill="black", width=2
                )
            else:
                canvas.create_line(
                    self._x2, self._y1, self._x2, self._y2, fill=bg_color, width=2
                )

            if self.has_top_wall:
                canvas.create_line(
                    self._x1, self._y1, self._x2, self._y1, fill="black", width=2
                )
            else:
                canvas.create_line(
                    self._x1, self._y1, self._x2, self._y1, fill=bg_color, width=2
                )

            if self.has_bottom_wall:
                canvas.create_line(
                    self._x1, self._y2, self._x2, self._y2, fill="black", width=2
                )
            else:
                canvas.create_line(
                    self._x1, self._y2, self._x2, self._y2, fill=bg_color, width=2
                )

    # Undo: change color of backtracked path
    # path: change color of valid path if found
    # br: colorschema tracker for 2 different solve algos
    # compare: global class var, gets set by call to solve maze
    def draw_move(
        self, to_cell, canvas: Canvas = None, undo=False, path=False, br=False
    ):
        center_x1 = (self._x1 + self._x2) // 2
        center_y1 = (self._y1 + self._y2) // 2
        center_x2 = (to_cell._x1 + to_cell._x2) // 2
        center_y2 = (to_cell._y1 + to_cell._y2) // 2

        color = ""
        dx = center_x2 - center_x1
        dy = center_y2 - center_y1

        distance = math.sqrt(dx**2 + dy**2)
        unit_dx = dx / distance if distance != 0 else 0
        unit_dy = dy / distance if distance != 0 else 0

        offset = 6

        offset_x = -unit_dy * offset
        offset_y = unit_dx * offset

        if br and self.compare:
            center_x1 += offset_x
            center_y1 += offset_y
            center_x2 += offset_x
            center_y2 += offset_y
            color = "green" if path else "gray" if undo else "red"
        elif not br and self.compare:
            center_x1 -= offset_x
            center_y1 -= offset_y
            center_x2 -= offset_x
            center_y2 -= offset_y
            color = "green" if path else "blue" if undo else "yellow"
        else:
            color = "green" if path else "blue" if undo else "yellow"

        thic = 16 if path else 12
        canvas.create_line(
            center_x1, center_y1, center_x2, center_y2, fill=color, width=thic
        )
