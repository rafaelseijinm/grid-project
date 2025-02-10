### HOW TO RUN PROJECT

#Using VSCODE:
run `grade200x200.py` or `grade20x20.py` to generate the .dot file, then run `dot -Tpng <dot file name> -o <file-name>.png` on console to generate png image for easier visualization of the graph.

## What to expect

The grid is generated with buildings and roads. Buildings are contiguous blocks with unique IDs, and roads have varying widths (1 or 2). The create_graph function identifies nodes that are buildings, road intersections, width changes, or terminations. Roads are connected by edges in the graph, with weights corresponding to the road width.

Considering how nodes and edges are formed. Buildings are fixed nodes, and edges are roads connecting interest points, such as terminations, intersections and changes.

## Expected Output on Graphviz:

**Blue Nodes:** Regular buildings (e.g., Building BD_01).  
**Green Nodes:** Warehouses (e.g., Warehouse BD_03).  
**Red Nodes:** Road points (e.g., Width 2).  
**Edges:** Indicate the road width (e.g., `[label="2"]`).  

**Connectivity:**  
- Buildings are connected to adjacent roads.  
- Paths between buildings can be verified with `nx.has_path(G, "BD_01", "BD_02")`.
