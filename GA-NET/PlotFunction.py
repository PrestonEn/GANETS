from igraph import Graph, plot as Plot
import numpy as np
def plot(g, filename, membership=None):
    if membership is not None:
        gcopy = g.copy()
        edges = []
        edges_colors = []
        for edge in g.es():
            if membership[edge.tuple[0]] != membership[edge.tuple[1]]:
                edges.append(edge)
                edges_colors.append("gray")
            else:
                edges_colors.append("black")
        gcopy.delete_edges(edges)
        layout = gcopy.layout("kk")
        g.es["color"] = edges_colors
    else:
        layout = g.layout("kk")
        g.es["color"] = "gray"
    visual_style = {}
    visual_style["vertex_label_dist"] = 0
    visual_style["vertex_shape"] = "circle"
    visual_style["edge_color"] = g.es["color"]
    # visual_style["bbox"] = (4000, 2500)
    visual_style["vertex_size"] = 30
    visual_style["layout"] = layout
    visual_style["bbox"] = (1024, 768)
    visual_style["margin"] = 40

    for vertex in g.vs():
        if "label" not in vertex.attribute_names() or vertex["label"] == None or vertex["label"] == "":
            vertex["label"] = vertex.index + 1


    if membership is not None:
        colors = []
        for i in range(0, max(membership) + 1):
            colors.append('%06X' % np.random.randint(0, 0xFFFFFF))
        for vertex in g.vs():
            vertex["color"] = str('#') + colors[membership[vertex.index]]
        visual_style["vertex_color"] = g.vs["color"]

    p = Plot(g, filename ,title="adsd" ,**visual_style)


