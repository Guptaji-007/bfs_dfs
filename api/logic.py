# Filename: 112301010.py

import sys
import json

class YantraCollector:
    def __init__(self, grid):
        self.grid = grid
        self.n = len(grid)
        self.start = self.find_position('P')
        self.exit = self.find_position('E')
        self.yantras = self.find_all_yantras()
        # If no yantras, set revealed_yantra to exit directly
        self.revealed_yantra = self.find_position('Y1') if self.yantras else self.exit
        self.collected_yantras = 0
        self.total_frontier_nodes = 0
        self.total_explored_nodes = 0
        
    def find_position(self, symbol):
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j] == symbol:
                    return (i, j)
        return None

    def find_all_yantras(self):
        positions = {}
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j].startswith('Y') and self.grid[i][j][1:].isdigit():
                    positions[int(self.grid[i][j][1:])] = (i, j)
                elif self.grid[i][j] == 'E':
                    self.exit = (i, j)
        return positions

    def reveal_next_yantra_or_exit(self):
        self.collected_yantras += 1
        if self.collected_yantras + 1 in self.yantras:
            self.revealed_yantra = self.yantras[self.collected_yantras + 1]
        elif self.collected_yantras == len(self.yantras):
            self.revealed_yantra = self.exit
        else:
            self.revealed_yantra = None

    def goal_test(self, position):
        if( position == self.revealed_yantra ):
            self.reveal_next_yantra_or_exit()
            return True
        return False
        
    def get_neighbours(self, position):
        
        # if the position is a list of tuples then take the first tuple
        if isinstance(position, list) and isinstance(position[0], tuple):
            position = position[0] 
        neighbours = []
        x,y = position

        # Move north
        x_coordinate, y_coordinate = x-1, y 
        if 0<=x_coordinate <= self.n - 1 and 0<=y_coordinate <= self.n - 1 and self.grid[x_coordinate][y_coordinate] != '#' and self.grid[x_coordinate][y_coordinate] != 'T':
            neighbours.append((x_coordinate, y_coordinate))

        # Move east
        x_coordinate, y_coordinate = x , y+1
        if 0<=x_coordinate <= self.n - 1 and 0<=y_coordinate <= self.n - 1 and self.grid[x_coordinate][y_coordinate] != '#' and self.grid[x_coordinate][y_coordinate] != 'T':
            neighbours.append((x_coordinate, y_coordinate))

        # Move south
        x_coordinate, y_coordinate = x+1, y 
        if 0<=x_coordinate <= self.n - 1 and 0<=y_coordinate <= self.n - 1 and self.grid[x_coordinate][y_coordinate] != '#' and self.grid[x_coordinate][y_coordinate] != 'T':
            neighbours.append((x_coordinate, y_coordinate))

        # Move west
        x_coordinate, y_coordinate = x , y - 1 
        if 0<=x_coordinate <= self.n - 1 and 0<=y_coordinate <= self.n - 1 and self.grid[x_coordinate][y_coordinate] != '#' and self.grid[x_coordinate][y_coordinate] != 'T':
            neighbours.append((x_coordinate, y_coordinate))

        return neighbours

    def bfs(self, start, goal):
        print(f"Starting BFS from {start} to {goal}", file=sys.stderr)
        path = []  # path to be returned  
        frontier_list = [start] # list of nodes to be explored
        explored_list = [] # list of nodes that have been explored 
        track_map = [(start, None)]  # it is a kind of map that stores the parent of the current node

        while frontier_list:
            current_node = frontier_list.pop(0)
            explored_list.append(current_node)
            if current_node == goal:
                print(f"Goal {goal} found using BFS", file=sys.stderr)
                self.total_frontier_nodes += len(frontier_list)
                self.total_explored_nodes += len(explored_list)
                # if the current node is the goal node then we will backtrack to get the path
                while current_node is not None:
                    path.append(current_node)
                    for pair in track_map:
                        if pair[0] == current_node:
                            current_node = pair[1]
                            break 
                path.reverse()
                return path
            
            # if the current node is not the goal node then we will add the neighbours of the current node to the frontier list
            for neighbour in self.get_neighbours(current_node):
                if (neighbour not in explored_list and neighbour not in frontier_list):
                    frontier_list.append(neighbour)
                    track_map.append((neighbour, current_node))

        print("No path found using BFS", file=sys.stderr)
        return None

    def dfs(self, start, goal):
        print(f"Starting DFS from {start} to {goal}", file=sys.stderr)
        path = []  # path to be returned  
        frontier_list = [start] # list of nodes to be explored
        explored_list = [] # list of nodes that have been explored 
        track_map = [(start, None)]  # it is a kind of map that stores the parent of the current node
        
        while frontier_list:
            current_node = frontier_list.pop(0)
            explored_list.append(current_node)
            # if the current node is the goal node then we will backtrack to get the path
            if current_node == goal:
                print(f"Goal {goal} found using DFS", file=sys.stderr)
                self.total_frontier_nodes += len(frontier_list)
                self.total_explored_nodes += len(explored_list)
                while current_node is not None:
                    path.append(current_node)
                    for pair in track_map:
                        if pair[0] == current_node:
                            current_node = pair[1]
                            break 
                path.reverse()
                return path
            # if the current node is not the goal node then we will add the neighbours of the current node to the frontier list
            for neighbour in reversed(self.get_neighbours(current_node)):
                if (neighbour not in explored_list and neighbour not in frontier_list):
                    frontier_list.insert(0,neighbour) # insert the neighbour at the beginning of the frontier list
                    track_map.append((neighbour, current_node))

        print("No path found using DFS", file=sys.stderr)
        return None

    def solve(self, strategy):
        print(f"Solving using {strategy}", file=sys.stderr)
        # check if the strategy is BFS or DFS
        if strategy == "BFS":
            search_method = self.bfs
        elif strategy == "DFS":
            search_method = self.dfs
        else:
            return None, 0, 0

        # If no yantras, find direct path to exit
        if not self.yantras:
            print("No yantras found, finding direct path to exit", file=sys.stderr)
            path = search_method(self.start, self.exit)
            if path:
                return path, self.total_frontier_nodes, self.total_explored_nodes
            return None, self.total_frontier_nodes, self.total_explored_nodes

        final_path = [] # final path to be returned 
        current_pos = self.start
        while True:
            print(f"Current position: {current_pos}, Revealed yantra: {self.revealed_yantra}", file=sys.stderr)
            # get the path from the current position to the revealed yantra
            path = search_method(current_pos, self.revealed_yantra)
            
            if not path: # if the path is None then return None
                print("No path found to the revealed yantra", file=sys.stderr)
                return None, self.total_frontier_nodes, self.total_explored_nodes
            
            if final_path: # if the final path is not empty then remove the first element of the path to avoid repetition
                path = path[1:] 
                
            final_path.extend(path) # extend the final path with the path from the current position to the revealed yantra
            current_pos = path[-1]  # update the current pos to the last element of the path
            
            if not self.goal_test(current_pos): 
                return None, self.total_frontier_nodes, self.total_explored_nodes
            
            if self.revealed_yantra is None: 
                break
                
        return final_path, self.total_frontier_nodes, self.total_explored_nodes  # return the final path, total frontier nodes and total explored nodes

    def get_path(self, strategy):
        solution, _, _ = self.solve(strategy)
        return solution

if __name__ == "__main__":
    grid = json.loads(sys.argv[1])
    strategy = sys.argv[2]
    
    print("Received grid:", grid, file=sys.stderr)
    
    game = YantraCollector(grid)
    path = game.get_path(strategy)
    
    print("Computed path:", path, file=sys.stderr)
    
    if path:
        print(json.dumps(path))
    else:
        print(json.dumps([]))
