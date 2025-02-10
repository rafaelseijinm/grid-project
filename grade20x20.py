import networkx as nx
import random

def grid_gen(size):
    grid = [[{"type": "empty"} for _ in range(size)] for _ in range(size)]
    
    building_id = 1
    for _ in range(5):  # reduced range for testing
        x, y = random.randint(0, size-5), random.randint(0, size-5)
        w, h = random.randint(2, 3), random.randint(2, 3)
        for i in range(w):
            for j in range(h):
                grid[y+j][x+i] = {"type": "building", "id": building_id}
        building_id += 1
    
    for i in range(size):
        if i % 5 == 0:  # More frequent roads for a smaller grid
            width = random.choice([1, 2])
            for j in range(size):
                grid[i][j] = {"type": "road", "width": width}
                grid[j][i] = {"type": "road", "width": width}
    return grid

def is_intersection_or_change(grid, y, x):
    if grid[y][x]["type"] != "road":
        return False
    
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dy, dx in directions:
        next_y, next_x = y + dy, x + dx
        if 0 <= next_y < len(grid) and 0 <= next_x < len(grid):
            if grid[next_y][next_x]["type"] == "road":
                neighbors.append((next_y, next_x))
    
    if len(neighbors) != 2:
        return True
    for next_y, next_x in neighbors:
        if grid[next_y][next_x]["width"] != grid[y][x]["width"]:
            return True
    return False

def create_graph(grid):
    G = nx.Graph()
    size = len(grid)
    
    nodes = {}
    for y in range(size):
        for x in range(size):
            cell = grid[y][x]
            if cell["type"] == "building":
                node_id = f"B_{cell['id']}"
                G.add_node(node_id, type="building", pos=(y, x))
                nodes[(y, x)] = node_id
            elif cell["type"] == "road" and is_intersection_or_change(grid, y, x):
                node_id = f"R_{y}_{x}"
                G.add_node(node_id, type="road", width=cell["width"], pos=(y, x))
                nodes[(y, x)] = node_id
    
    for y in range(size):
        for x in range(size):
            if grid[y][x]["type"] == "road":
                current_node = nodes.get((y, x))
                if not current_node:
                    continue
                
                for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    next_y, next_x = y + dy, x + dx
                    while 0 <= next_y < size and 0 <= next_x < size:
                        if grid[next_y][next_x]["type"] != "road":
                            break
                        if (next_y, next_x) in nodes:
                            target_node = nodes[(next_y, next_x)]
                            weight = grid[y][x]["width"]
                            G.add_edge(current_node, target_node, weight=weight)
                            break
                        next_y += dy
                        next_x += dx
    return G

def export_graphviz(G, filename="graph20x20.dot"):
    with open(filename, "w") as f:
        f.write("graph G {\n")
        for u, v, data in G.edges(data=True):
            f.write(f'  "{u}" -- "{v}" [label="{data["weight"]}"];\n')
        for node, data in G.nodes(data=True):
            if data["type"] == "building":
                f.write(f'  "{node}" [shape=box, color=blue, label="Building {node}"];\n')
            else:
                f.write(f'  "{node}" [shape=circle, color=red, label="Width {data["width"]}"];\n')
        f.write("}\n")

def main():
    grid = grid_gen(20)  # reduced grid
    G = create_graph(grid)
    export_graphviz(G)
    print("test success!")

if __name__ == "__main__":
    main()
