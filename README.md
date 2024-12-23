# Checkers AI Endgame Solver

## Introduction
This project is an AI-powered Checkers endgame solver built using Python. It leverages advanced techniques like alpha-beta pruning, node ordering, and state caching to solve Checkers puzzles efficiently and optimally. The solver is designed to find winning solutions for the red player, simulating intelligent gameplay and strategy.

## Problem Statement
Endgame scenarios in Checkers can be highly complex, with many possible moves to evaluate. Manually solving these puzzles requires significant time and expertise. This project addresses the challenge by automating the solution process, finding optimal strategies to win games or avoid losses in minimal time.

## Features
- **Alpha-Beta Pruning**: Optimizes the minimax algorithm by eliminating unnecessary branches, reducing computation time.
- **Evaluation Function**: Estimates utility values for non-terminal states, considering factors like piece counts, king advantages, and positional strengths.
- **Node Ordering**: Orders possible moves to maximize pruning efficiency.
- **State Caching**: Stores previously evaluated game states to avoid redundant calculations, improving performance.

## How It Works
The program takes an input file representing the initial game state and uses a combination of search algorithms and heuristics to compute the sequence of moves leading to a game-ending state. The output is a step-by-step solution, ensuring that the red player achieves victory optimally.

### Core Algorithm
1. **Game Simulation**: Simulates Checkers gameplay based on the rules of the game.
2. **Search Algorithm**: Implements alpha-beta pruning to explore possible moves efficiently within a set depth limit.
3. **Heuristics and Optimizations**: Uses an evaluation function and node ordering to prioritize advantageous moves and speed up calculations.

## Getting Started

### Prerequisites
- Python 3.7 or higher

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/checkers-ai-solver.git
   ```
2. Navigate to the project directory:
   ```bash
   cd checkers-ai-solver
   ```

### Running the Solver
To run the program, use the following command:
```bash
python3 checkers.py --inputfile <input file> --outputfile <output file>
```

#### Example
Input file: `puzzle1.txt`
Output file: `puzzle1_sol.txt`
```bash
python3 checkers.py --inputfile puzzle1.txt --outputfile puzzle1_sol.txt
```

### Input/Output Format
#### Input File
- The input file contains a single state represented as a grid of 64 characters:
  - `.`: Empty square
  - `r`: Red piece
  - `b`: Black piece
  - `R`: Red king
  - `B`: Black king

Example:
```
........
....b...
.......R
..b.b...
...b...r
........
...r....
....B...
```

#### Output File
- The output file contains the sequence of game states from the initial state to the terminal state. States are separated by an empty line.

Example:
```
........
....b...
.......R
..b.b...
...b...r
........
...r....
....B...

........
....b...
.......R
..b.b...
...b....
........
...r....
....B...
```

## Testing
To ensure correctness:
- Verify that the solution starts with the input state and ends with a terminal state.
- Confirm that all intermediate states follow valid Checkers rules.
- Check that the solution minimizes the moves to win or maximizes the moves to delay a loss.

## Performance
- The program is designed to solve puzzles within 4 minutes for a given depth limit.
- Depth limits can be adjusted based on the complexity of the puzzle and system performance. They are chosen to balance accuracy and execution time.

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests to improve this solver.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

