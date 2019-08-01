Task:
There is a grid with S rows and S columns. Blocked cells are marked as ‘1’ and free cells are marked as ‘0’. You need to get from initial cell with coordinates (inX; inY) to target cell with coordinates (tgX; tgY). It is possible to move only by X and Y axes.
One move means any number of steps without changing of direction. 
Write a program to determine the minimum number of moves to get to the target cell.
Example:
0 0 0
1 1 0
0 0 0
Minimum number of moves from (0;0) (upper left corner) to (2;0) (bottom left corner) requires three moves: (0;0) -> (0;2) -> (2;2) -> (2;0)
Output: minimum number of moves or -1 if there is no way

Solution:
Two classes were implemented: “Map” and “Wayfinder”. “Map” contains everything necessary to manage labyrinth, and “Wayfinder” finds minimal number of moves. The idea of this program is simple: we create labyrinth by hand or generate it randomly, place start and finish, and push start position to the stack. After that, we pop it’s coordinates and determine where we can get from the that place by “projecting beams” in all four directions. Every non visited cell, that is reachable in one step from the current one, is pushed in stack. Then, we assign each of them number of steps, that is required to reach it. If we already know number of moves required to reach node, we compare it and new info to find a shortest way. We repeat this process until the stack is empty. But there is a drawback: this algorithm essentially maps whole grid. It finds required steps to reach all possible places, which hurts performance time.