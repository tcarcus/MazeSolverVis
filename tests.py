import unittest
from maze import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._cells), num_rows)
        self.assertEqual(len(m1._cells[0]), num_cols)

    def test_maze_different_sizes(self):
        m2 = Maze(0, 0, 5, 5, 20, 20)
        self.assertEqual(len(m2._cells), 5)
        self.assertEqual(len(m2._cells[0]), 5)

        m3 = Maze(0, 0, 8, 3, 15, 15)
        self.assertEqual(len(m3._cells), 8)
        self.assertEqual(len(m3._cells[0]), 3)

        m4 = Maze(0, 0, 1, 1, 10, 10)
        self.assertEqual(len(m4._cells), 1)
        self.assertEqual(len(m4._cells[0]), 1)

    def test_maze_cells_position(self):
        m5 = Maze(0, 0, 2, 2, 10, 10)
        cell_00 = m5._cells[0][0]
        cell_11 = m5._cells[1][1]

        self.assertEqual(cell_00._x1, 0)
        self.assertEqual(cell_00._y1, 0)
        self.assertEqual(cell_00._x2, 10)
        self.assertEqual(cell_00._y2, 10)

        self.assertEqual(cell_11._x1, 10)
        self.assertEqual(cell_11._y1, 10)
        self.assertEqual(cell_11._x2, 20)
        self.assertEqual(cell_11._y2, 20)

    def test_maze_break_entrance_and_exit(self):
        num_cols = 5
        num_rows = 5
        m = Maze(0, 0, num_rows, num_cols, 10, 10)

        m._break_entrance_and_exit()

        entrance_cell = m._cells[0][0]
        self.assertFalse(entrance_cell.has_top_wall)

        exit_cell = m._cells[num_rows - 1][num_cols - 1]
        self.assertFalse(exit_cell.has_bottom_wall)


if __name__ == "__main__":
    unittest.main()
