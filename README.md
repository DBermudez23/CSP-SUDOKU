# CSP-SUDOKU

# Killer Sudoku Solver using Constraint Programming (Z3 Solver)

### Authors: 
- **Daniel Felipe Bermudez Florez**
- **Juan Sebastián Tamayo Cuadrado**

## Overview
This project implements a **Killer Sudoku Solver** using the powerful **Z3 Solver** library, which leverages constraint programming techniques. The program models each cell of the Sudoku board as a variable with specific constraints and applies rules of uniqueness and sum targets to solve the puzzle efficiently.

## Features
- **Flexible Board Dimensions**: Supports standard 9x9 Sudoku boards, but can easily be extended to other dimensions.
- **Constraint Validation**:
  - Each row and column contains unique values.
  - Each subgrid (e.g., 3x3 for 9x9 boards) contains unique values.
  - Groups of cells (cages) have a defined sum target with unique values.
- **Multiple Solutions**:
  - Finds all valid solutions to the given puzzle.
  - Avoids duplicates by dynamically adding constraints to the solver.
- **Optimized Using Z3 Solver**:
  - Uses advanced constraint programming to efficiently explore the solution space.

## How It Works
1. **Input**: 
   The program takes a set of constraints as input, where each constraint includes:
   - A **target sum**.
   - A list of **cells** (defined as row-column pairs) in the cage.

   Example:
   ```python
   sudoku_constraints = [
       (8, [(1, 1), (2, 1)]),
       (24, [(1, 2), (1, 3), (2, 3)]),
       (9, [(1, 4), (2, 4)])
   ]
