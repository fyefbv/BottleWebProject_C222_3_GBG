import networkx as nx

class GraphBuilder:
    def __init__(self, adjacency_matrix):
        n = len(adjacency_matrix)

        self.adj_matrix = adjacency_matrix
        self.vertex_count = n
        self.G = nx.DiGraph()
        self.G.add_nodes_from(range(self.vertex_count))

        #Какой граф отрисовываем?
        self.flag = False
        for i in range(self.vertex_count):
           if self.flag == True:
               break
           for j in range(self.vertex_count):
               if self.adj_matrix[i][j] > 1:
                   self.flag = True
                   break

    # Строит граф на основе матрицы смежности (возвращает экземпляр nx.DiGraph с добавленными рёбрами)
    def build_graph(self):
        self.G.remove_edges_from(list(self.G.edges()))
        if self.flag == False:
            for i in range(self.vertex_count):
                for j in range(self.vertex_count):
                    if self.adj_matrix[i][j] == 1:
                        self.G.add_edge(i, j)
            return self.G
        if self.flag == True:
            for i in range(self.vertex_count):
                for j in range(self.vertex_count):
                    weight = self.adj_matrix[i][j]
                    if weight >= 1:
                        self.G.add_edge(i, j, weight=weight)  # сохраняем вес
            return self.G


    # Возвращает список смежности графа в виде словаря {вершина: [список соседей]}
    def get_adjacency_list(self):
        if self.G.number_of_edges() == 0:
            self.build_graph()
        return {node: list(self.G.successors(node)) for node in self.G.nodes()}

    # Экспортирует граф в формат JSON, удобный для D3.js
    def to_d3_json(self):
        if self.G.number_of_edges() == 0:
            self.build_graph()

        nodes = [{"id": i} for i in range(self.vertex_count)]
        if self.flag == False:
            links = [
                {"source": u, "target": v}
                for u, v in self.G.edges()
            ]
        if self.flag == True:
            links = [
            {
                "source": u,
                "target": v,
                "weight": self.G[u][v]["weight"]  # передаём вес
            }
            for u, v in self.G.edges()
        ]
        return {"nodes": nodes, "links": links}
