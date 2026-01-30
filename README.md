# Sudoku-ML
Sudoku-ML is a personal machine learning project focused on teaching an agent how to solve Sudoku puzzles and how to recommend the next best move for a given grid. The project is designed both as a learning exercise and as a portfolio piece that demonstrates end to end machine learning system design, from data generation to model training, evaluation, and planning.
The project intentionally explores approaches that are more complex than strictly necessary in order to showcase architectural decision making, hybrid learning strategies, and clear tradeoffs.

## Goals
1. Train a model capable of accurately solving incomplete Sudoku grids across varying difficulty levels.
2. Train the same system to recommend the next best move, defined as the move that maximizes the likelihood of completing the puzzle efficiently and legally.
3. Explore hybrid learning approaches combining supervised learning, reinforcement learning, and planning.
4. Produce a well documented, reproducible project suitable for a technical portfolio.

## Current Status
This project is under active development with an initial focus on:
- Dataset generation
- Supervised solver training
- Establishing strong evaluation baselines

## High-Level Approach
This project is built around a shared neural network backbone with multiple task specific outputs.
The system is trained in stages:
1. Supervised learning is used to teach the model Sudoku structure and solution patterns.
2. Reinforcement learning is used to refine performance on harder puzzles and improve long term decision making.
3. Planning techniques are layered on top to improve move selection and interpretability.

## Dataset Generation
Rather than relying solely on external datasets, this project generates its own Sudoku data.
The data pipeline includes:
- Generation of fully solved Sudoku grids
- Creation of incomplete puzzles by removing values from solved grids
- Assignment of difficulty labels using proxy metrics such as solve depth and backtracking complexity
- Storage of puzzle grids, solution grids, and metadata
This approach allows full control over puzzle distribution, difficulty balance, and curriculum learning.

## Input Representation
Each Sudoku puzzle is encoded using:
- One hot encoding for cell values, producing a 9 × 9 × 9 tensor
- Binary masks indicating which cells are pre-filled and immutable
The solution grid is used only for supervision, reward calculation, and evaluation.

## Model Architecture
The model consists of three main components.

### Shared Encoder
- Convolutional neural network
- Two dimensional convolutions
- Residual blocks to stabilize deep training
- Learns a shared representation of the Sudoku board

### Solver Head
- Outputs a probability distribution over digits for each cell
- Used to predict a full solved grid
- Trained using supervised learning

### Policy Head
- Outputs a probability distribution over possible moves (row, column, digit)
- Used to recommend the next best move
- Trained first with expert demonstrations, then refined with reinforcement learning

## Learning Strategy
### Supervised Learning
- Trains the encoder and solver head on easy and nearly solved puzzles
- Uses softmax activation with cross entropy loss
- Masks filled cells during loss computation
- Uses curriculum learning to progressively increase difficulty

### Reinforcement Learning
- Fine tunes the policy head and the encoder
- Uses a custom Sudoku environment
- Illegal moves are allowed but penalized rather than blocked
- Rewards encourage legal placements, progress toward completion, and efficient solving

This staged approach stabilizes learning and improves performance on medium and hard puzzles.

## Planning and Search
For enhanced move selection, the project integrates a lightweight planning layer inspired by AlphaZero style systems.
- Policy guided Monte Carlo Tree Search
- Limited rollout depth for computational efficiency
- Used only at inference time
This allows the model to evaluate future board states before committing to a move.

## Evaluation Metrics
Model performance is evaluated using:
- Full puzzle solve rate by difficulty
- Per cell accuracy
- Next move top k accuracy
- Average steps to completion
- Illegal move frequency
- Comparison between policy only and policy plus planning
Supervised components use standard validation techniques, while reinforcement learning performance is measured through repeated environment rollouts.

## Future Work
Planned extensions include:
- Improved difficulty estimation using human style solving heuristics
- Better interpretability of recommended moves
- Visualization tools for model decisions
- Performance comparisons with classical Sudoku solvers
