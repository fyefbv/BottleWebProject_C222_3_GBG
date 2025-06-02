import networkx as nx

class GraphBuilder:
    def __init__(self, adjacency_matrix):
        n = len(adjacency_matrix)

        self.adj_matrix = adjacency_matrix
        self.vertex_count = n
        self.G = nx.DiGraph()
        self.G.add_nodes_from(range(self.vertex_count))

    def build_graph(self):
        self.G.remove_edges_from(list(self.G.edges()))
        for i in range(self.vertex_count):
            for j in range(self.vertex_count):
                if self.adj_matrix[i][j] == 1:
                    self.G.add_edge(i, j)
        return self.G

    def get_adjacency_list(self):
        if self.G.number_of_edges() == 0:
            self.build_graph()
        return {node: list(self.G.successors(node)) for node in self.G.nodes()}

    # Экспортирует граф в формат JSON, удобный для D3.js
    def to_d3_json(self):
        if self.G.number_of_edges() == 0:
            self.build_graph()

        nodes = [{"id": i} for i in range(self.vertex_count)]
        links = [
            {"source": u, "target": v}
            for u, v in self.G.edges()
        ]
        return {"nodes": nodes, "links": links}
