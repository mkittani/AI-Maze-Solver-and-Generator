import tkinter as tk
from tkinter import ttk, filedialog
import random
import heapq
from collections import deque
import math

def generate_maze():
    maze = []
    for _ in range(20):
        row = []
        for _ in range(20):
            if random.random() < 0.2: 
                cell = -1
            else:
                cell = random.randint(1, 9)
            row.append(cell)
        maze.append(row)
    return maze


def display_maze(maze):
    for widget in maze_frame.winfo_children(): 
        widget.destroy()
    
    for i, row in enumerate(maze): 
        row_frame = tk.Frame(maze_frame)
        row_frame.pack()
        for j, cell in enumerate(row):
            color = 'white'
            if cell == -1:
                color = 'black'
            elif (i, j) == start_point:
                color = 'blue'
            elif (i, j) == goal_point:
                color = 'red'
            elif (i, j) == second_goal_point:
                color = 'purple'
                
            cell_label = tk.Label(row_frame, text=str(cell), width=2, borderwidth=1, relief="solid", bg=color)
            cell_label.pack(side="left")
            cell_label.bind("<Button-1>", lambda click, temp1=i, temp2=j: handle_click(temp1, temp2)) 

def handle_click(i, j):
    global maze, boxType, start_point, goal_point, second_goal_point
    if boxType == "wall":
        cell_label = maze_frame.winfo_children()[i].winfo_children()[j] 
        if maze[i][j] == -1:
            maze[i][j] = random.randint(1, 9)
            cell_label.config(bg='white', text=str(maze[i][j])) 
        else:
            maze[i][j] = -1
            cell_label.config(bg='black', text='-1') 
    elif boxType == "start":
        if start_point: 
            row = start_point[0]
            col = start_point[1]
            maze_frame.winfo_children()[row].winfo_children()[col].config(bg='white', text=random.randint(1, 9))
        start_point = (i, j)
        maze[i][j] = 0
        cell_label = maze_frame.winfo_children()[i].winfo_children()[j]
        cell_label.config(bg='blue', text='0')
        boxType = "wall" 
    elif boxType == "goal":
        if goal_point:
            row = goal_point[0]
            col = goal_point[1]
            maze_frame.winfo_children()[row].winfo_children()[col].config(bg='white', text=random.randint(1, 9))
        goal_point = (i, j)
        maze[i][j] = 0
        cell_label = maze_frame.winfo_children()[i].winfo_children()[j]
        cell_label.config(bg='red', text='0')
        boxType = "wall"
    elif boxType == "second_goal":
        if second_goal_point:
            row = second_goal_point[0]
            col = second_goal_point[1]
            maze_frame.winfo_children()[row].winfo_children()[col].config(bg='white', text=random.randint(1, 9))
        second_goal_point = (i, j)
        maze[i][j] = 0
        cell_label = maze_frame.winfo_children()[i].winfo_children()[j]
        cell_label.config(bg='purple', text='0')
        boxType = "wall"

def clear_path():
    for i in range(20):
        for j in range(20):
            cell_label = maze_frame.winfo_children()[i].winfo_children()[j]
            if cell_label.cget('bg') == 'green':
                cell_label.config(bg='white')

def generate_random():
    global maze, start_point, goal_point, second_goal_point
    maze = generate_maze()
    start_point = (0, 0)
    goal_point = (19, 19)
    second_goal_point = None
    maze[0][0] = 0
    maze[19][19] = 0
    display_maze(maze)

def set_start_point(): 
    global boxType
    boxType = "start"

def set_goal_point():
    global boxType
    boxType = "goal"

def set_second_goal_point():
    global boxType
    boxType = "second_goal"


def heuristic(a, b):
    if heuristic_var.get() == "Manhattan":
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    elif heuristic_var.get() == "Euclidean":
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

directions = [(0, 1), (1, 0), (0, -1), (-1, 0), 
              (1, 1), (1, -1), (-1, 1), (-1, -1)]


#heu + total cost
def a_star(maze, start, goal, second_goal=None):
    rows, cols = len(maze), len(maze[0]) 
    open_set = [(0 + heuristic(start, goal), 0, start)] 
    heapq.heapify(open_set) 
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    nodes_tested = 0 

    while open_set:
        fScore, current_g_score, current_coords = heapq.heappop(open_set) 
        nodes_tested += 1

        if current_coords == goal or (second_goal and current_coords == second_goal): #found so print the path
            path = [] #add the path to a list from the goal to start then reverse it
            while current_coords in came_from:
                path.append(current_coords)
                current_coords = came_from[current_coords]
            path.append(start)
            path.reverse()
            return path, nodes_tested

        for direction in directions:
            neighbor = (current_coords[0] + direction[0], current_coords[1] + direction[1]) 

            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols: #check if in boundaries 0,row-1, and col-1
                if maze[neighbor[0]][neighbor[1]] == -1: #if we hit a wall
                    continue
                cost = maze[neighbor[0]][neighbor[1]] #calculating cost
                if direction[0] != 0 and direction[1] != 0:
                    cost *= 1.4 
                tot_g_score = current_g_score + cost

                if neighbor not in g_score or tot_g_score < g_score[neighbor]: 
                    came_from[neighbor] = current_coords
                    g_score[neighbor] = tot_g_score #updating the cost to reach this neighbor
                    f_score[neighbor] = tot_g_score + heuristic(neighbor, goal) #to calculate how much left from the new neighbor to goal
                    heapq.heappush(open_set, (f_score[neighbor], tot_g_score, neighbor)) #add the new neighbor to the heap with its tot cost and heu
    return None, nodes_tested

#total cost only
def ucs(maze, start, goal, second_goal=None):
    rows, cols = len(maze), len(maze[0])
    open_set = [(0, start)]
    heapq.heapify(open_set)
    came_from = {}
    g_score = {start: 0}
    nodes_tested = 0

    while open_set:
        current_g_score, current_coords = heapq.heappop(open_set)
        nodes_tested += 1

        if current_coords == goal or (second_goal and current_coords == second_goal): #found so print the path
            path = [] #add the path to a list from the goal to start then reverse it
            while current_coords in came_from:
                path.append(current_coords)
                current_coords = came_from[current_coords]
            path.append(start)
            path.reverse()
            return path, nodes_tested

        for direction in directions:
            neighbor = (current_coords[0] + direction[0], current_coords[1] + direction[1])

            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols: #check if in boundaries 0,row-1, and col-1
                if maze[neighbor[0]][neighbor[1]] == -1: #if we hit a wall
                    continue
                cost = maze[neighbor[0]][neighbor[1]] #calculating cost
                if direction[0] != 0 and direction[1] != 0:
                    cost *= 1.4
                tot_g_score = current_g_score + cost

                if neighbor not in g_score or tot_g_score < g_score[neighbor]:
                    g_score[neighbor] = tot_g_score #updating the cost to reach this neighbor
                    heapq.heappush(open_set, (tot_g_score, neighbor)) #add the new neighbor to the heap with its tot cost
                    came_from[neighbor] = current_coords

    return None, nodes_tested

#heu only
def bfs(maze, start, goal, second_goal=None):
    rows, cols = len(maze), len(maze[0])
    open_set = [(0, start)]
    heapq.heapify(open_set)
    came_from = {}
    visited = set() #a set to track visited nodes and not visit them again
    nodes_tested = 0 

    while open_set:
        current_h, current_coords = heapq.heappop(open_set)
        nodes_tested += 1
        
        if current_coords == goal or (second_goal and current_coords == second_goal): #found so print the path
            path = [] #add the path to a list from the goal to start then reverse it
            while current_coords in came_from:
                path.append(current_coords)
                current_coords = came_from[current_coords]
            path.append(start)
            path.reverse()
            return path, nodes_tested

        if current_coords in visited: #already visited so leave it
            continue

        visited.add(current_coords)

        for direction in directions:
            neighbor = (current_coords[0] + direction[0], current_coords[1] + direction[1])

            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if maze[neighbor[0]][neighbor[1]] == -1 or neighbor in visited:
                    continue #skip if a wall
                heu = heuristic(neighbor, goal) #compute the heu of the goal with the new neighbor we're in
                heapq.heappush(open_set, (heu, neighbor))
                came_from[neighbor] = current_coords

    return None, nodes_tested

def run_algorithm():
    clear_path()
    #call one of the 3 functions based on the selection of combobox and get the path and the tested nodes returned
    if algorithm_var.get() == "A*":
        path, nodes_tested = a_star(maze, start_point, goal_point, second_goal_point)
    elif algorithm_var.get() == "UCS":
        path, nodes_tested = ucs(maze, start_point, goal_point, second_goal_point)
    elif algorithm_var.get() == "BFS":
        path, nodes_tested = bfs(maze, start_point, goal_point, second_goal_point)

    if path:
        for (i, j) in path:
            cell_label = maze_frame.winfo_children()[i].winfo_children()[j]
            if (i, j) != start_point and (i, j) != goal_point and (i, j) != second_goal_point:
                cell_label.config(bg='green')

        steps = len(path) - 1  # Subtract one because start point is included
        result_label.config(text=f"Steps: {steps}, Nodes Tested: {nodes_tested}")
    else:
        result_label.config(text="No path found")

root = tk.Tk()
root.title("Maze Solver")

control_frame = ttk.Frame(root)
control_frame.grid(row=0, column=0, padx=10, pady=10)

ttk.Button(control_frame, text="Generate Random Maze", command=generate_random).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(control_frame, text="Set Start Point", command=set_start_point).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(control_frame, text="Set Goal Point", command=set_goal_point).grid(row=0, column=2, padx=5, pady=5)
ttk.Button(control_frame, text="Set Second Goal", command=set_second_goal_point).grid(row=0, column=3, padx=5, pady=5)
ttk.Button(control_frame, text="Run Algorithm", command=run_algorithm).grid(row=1, column=3, padx=5, pady=5)

ttk.Label(control_frame, text="Algorithm:").grid(row=2, column=0, padx=5, pady=5)
algorithm_var = tk.StringVar(value="A*")
ttk.Combobox(control_frame, textvariable=algorithm_var, values=["A*", "UCS", "BFS"]).grid(row=2, column=1, padx=5, pady=5)

ttk.Label(control_frame, text="Heuristic:").grid(row=2, column=2, padx=5, pady=5)
heuristic_var = tk.StringVar(value="Manhattan")
ttk.Combobox(control_frame, textvariable=heuristic_var, values=["Manhattan", "Euclidean"]).grid(row=2, column=3, padx=5, pady=5)


maze_frame = tk.Frame(root) 
maze_frame.grid(row=1, column=0, padx=10, pady=10)


result_label = ttk.Label(root, text="Steps: 0, Nodes Tested: 0")
result_label.grid(row=2, column=0, padx=10, pady=10)


maze = generate_maze()
start_point = (0, 0)
goal_point = (19, 19)
maze[0][0] = 0
maze[19][19] = 0
second_goal_point = None
display_maze(maze)

root.mainloop()
