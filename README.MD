# Maze Solver

A fun and interactive maze solver implemented using Python's `tkinter` library for the graphical user interface. The application generates a random maze and visualizes the solving process using Depth-First Search (DFS) algorithms. You can compare two different solving strategies: a standard DFS and a modified DFS that prioritizes moving down and to the right.

## Features

- Random maze generation with customizable sizes.
- Visual representation of the maze and solving process.
- Two solving strategies:
  - Standard DFS.
  - Bottom/Right DFS, which emphasizes moving downwards and to the right.
- Ability to visualize the maze generation and solution paths in real-time.

## Installation

To run this project, ensure you have Python 3.x installed on your machine. Follow the steps below:

1. Clone the repository:

```bash
  git clone https://github.com/your-username/MazeSolverVis.git

  Navigate into the project directory:


  cd MazeSolverVis

  Run the application:


  python3 main.py
```

## Usage

### Upon running the application, a window will appear with the following components:

    Size Selection Buttons: Choose the size of the maze you want to generate (e.g., 4x4, 8x8, 12x17).
    Control Buttons:
        Shuffle: Generate maze and solve it using random shuffle DFS
        Bottom/Right DFS: Generate Maze and solve the maze using the bottom/right prioritization strategy.
        Compare: Solve the maze using both strategies simultaneously for visual comparison.


### Code Structure

    main.py: Entry point for the application.
    gui.py: Contains the GUI logic using tkinter.
    maze.py: Handles maze generation and solving algorithms.
    helper.py: Contains utility classes like Cell, Line, and Point used for drawing.

### Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to fork the repository and submit a pull request.
License

This project is licensed under the MIT License - see the LICENSE file for details.
