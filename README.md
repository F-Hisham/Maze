# MazeSolver
An amazing maze solving masterpiece.

Create a class base off BaseMazeSolver from solvers.base.
Feel free to use any other objects in the code base such
as Coords and Moves from maze.cells.

Competition Goal:
1) Develop a maze solver that will produce the best scores 
for solving three out of sample mazes.
2) Scoring for the tests can be done using the base class
and lower scores are better.
3) The solver will be tested using multiple runs of the solver.
4) A score of zero is a fail, and failing to produce a successful
path each time will lead to a score of zero.
5) You can see the scoring code yourself, but in general 
the less nodes in the path and quicker it solves the better
it will score.

Testing Randomness:
- The solver analyzer can deal with randomness but only if
you use the "random" python module.
- The solver analyzing code will specify random seeds to
test different potential solutions from your solver.

Rules to the competition:
1) Do not change any of the other code in the project.
2) 