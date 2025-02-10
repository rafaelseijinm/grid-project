import networkx as nx
import random

def grid_gen(size):
    grid = [[{"type": "empty"} for _ in range(size)] for _ in range(size)]
    
    # adding buildings with unique ids
    building_id = 1
    for _ in range(50):
        x, y = random.randint(0, size-10), random.randint(0, size-10)
        w, h = random.randint(3, 6), random.randint(3, 6)
        for i in range(w):
            for j in range(h):
                grid[y+j][x+i] = {"type": "building", "id": building_id}
        building_id += 1
    
    # adding roads with sizes 1 or 2
    for i in range(size):
        if i % 10 == 0:
            width = random.choice([1, 2])
            for j in range(size):
                grid[i][j] = {"type": "road", "width": width}  # Horizontal
                grid[j][i] = {"type": "road", "width": width}  # Vertical
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
    
    # Checks if its either intersection, terminal or width change
    if len(neighbors) != 2:
        return True
    for next_y, next_x in neighbors:
        if grid[next_y][next_x]["width"] != grid[y][x]["width"]:
            return True
    return False

def graph_create(grid):
    G = nx.Graph()
    size = len(grid)
    warehouse_ids = [1, 3, 5]  # warehouses
    
    # Identifying nodes: buildings, intersections and changes
    nodes = {}
    for y in range(size):
        for x in range(size):
            cell = grid[y][x]
            if cell["type"] == "building":
                node_id = f"BD_{cell['id']:02d}"
                # Defines if warehouse or normal building
                node_type = "warehouse" if cell["id"] in warehouse_ids else "building"
                G.add_node(node_id, type=node_type, pos=(y, x))
                nodes[(y, x)] = node_id
            elif cell["type"] == "road" and is_intersection_or_change(grid, y, x):
                node_id = f"R_{y}_{x}"
                G.add_node(node_id, type="road", width=cell["width"], pos=(y, x))
                nodes[(y, x)] = node_id
    
    # Connecting road nodes between themselves
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
    
    # Connecting buildings between roads
    for (y, x), node_id in nodes.items():
        if grid[y][x]["type"] == "building":
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                adj_y, adj_x = y + dy, x + dx
                if 0 <= adj_y < size and 0 <= adj_x < size:
                    adj_cell = grid[adj_y][adj_x]
                    if adj_cell["type"] == "road" and (adj_y, adj_x) in nodes:
                        adj_node = nodes[(adj_y, adj_x)]
                        G.add_edge(node_id, adj_node, weight=adj_cell["width"])
    return G

# Creating graphviz
def export_graphviz(G, filename="graph200x200.dot"):
    with open(filename, "w") as f:
        f.write("graph G {\n")
        for u, v, data in G.edges(data=True):
            f.write(f'  "{u}" -- "{v}" [label="{data["weight"]}"];\n')
        for node, data in G.nodes(data=True):
            if data["type"] == "warehouse":
                f.write(f'  "{node}" [shape=box, color=green, label="Warehouse {node}"];\n')
            elif data["type"] == "building":
                f.write(f'  "{node}" [shape=box, color=blue, label="Building {node}"];\n')
            else:
                f.write(f'  "{node}" [shape=circle, color=red, label="Width {data["width"]}"];\n')
        f.write("}\n")

def main():
    grid = grid_gen(200)
    G = graph_create(grid)
    export_graphviz(G)
    print("success!")

if __name__ == "__main__":
    main()