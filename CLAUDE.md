# Claude Code instructions

Sudoku-ML is Judhy's personal learning and portfolio project. The README describes the full design.

## Collaboration: Judhy writes the code

- Don't write implementations. Explain concepts, give pseudocode, point out bugs and tradeoffs, and ask comprehension questions so Judhy can write it.
- Docstrings are the exception: writing or improving those is fine.
- Code review is welcome: point to the line and explain the problem, but let Judhy make the fix unless told otherwise.
- Work on a branch; don't commit or push unless asked.

## Current state

- Only the data side exists: `data/sudoku_generator.py` (optimized filled-grid generator) and `data/puzzle_creator.py` (difficulty configs, uniqueness check, chunked JSON output with metadata).
- `env/`, `models/`, `training/` and `evaluation/` files are empty stubs.
- Next step: finish the dataset pipeline (puzzle/solution pairs with difficulty labels), then the first supervised model.

## Planned design

- Input: one-hot 9×9×9 tensor plus a fixed-cell mask. The solution grid is only for supervision, rewards and evaluation.
- Shared CNN encoder with residual blocks → solver head (per-cell digit distribution) and policy head (row, column, digit move distribution).
- Training: supervised first (cross-entropy with filled cells masked, curriculum by difficulty), then RL fine-tuning in a custom environment (illegal moves penalized, not blocked), then policy-guided MCTS at inference only.
- Later: a computer vision component to read physical puzzles from photos.

Run modules from the repo root (e.g. `python -m data.puzzle_creator`) since imports use the `data.` package path.
