# Project 2: MultiAgent Pacman

This project implements Pacman along with ghosts. It introduces evaluation function design.The aim of the project is to implement Pacman using both adversial and stochastic search problem.

1. **Reflex Agent**: The Reflex Agent uses an evaluation function (aka heuristic function) to estimate the value of an action using the current game state while considering both food and ghost locations. 

2. **Minimax Agent**: A minimax agent is an adversial search agent. It is implemented using a minimax tree with multiple min layers (one for each ghost) for every max layer. The agent uses an evaluation function that evaluates states, and chooses the best state which might in some scenario killing self early if death is inevitable as living incurs penalty.

3. **Alpha Beta Agent**: An alpha beta agent uses alpha-beta pruning to explore the minimax tree more efficiently.

4. **Expectimax**:  The expectimax pacman makes decisions using the expected value instead of working with assumption that Pacman is playing against an adversary who makes optimal decisions. Thus, in this case Expectimax is a good choice as it is useful for modeling probabilistic behavior of agents who may make suboptimal choices.

5. **Evaluation Function**: Designed evaluation function that considers states rather than actions.
