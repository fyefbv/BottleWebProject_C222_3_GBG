import networkx as nx
class MaxFlowFinder:
    def __init__(self, adjacency_matrix):
        self.adjacency_matrix = adjacency_matrix
        self.source = self._find_source()
        self.sink = self._find_sink()
        
    def _find_source(self):
        """Находит исток (вершину без входящих ребер)"""
        n = len(self.adjacency_matrix)
        for j in range(n):
            is_source = True
            for i in range(n):
                if self.adjacency_matrix[i][j] > 0:
                    is_source = False
                    break
            if is_source:
                return j
        return 0  # По умолчанию, если не нашли

    def _find_sink(self):
        """Находит сток (вершину без исходящих ребер)"""
        n = len(self.adjacency_matrix)
        for i in range(n):
            is_sink = True
            for j in range(n):
                if self.adjacency_matrix[i][j] > 0:
                    is_sink = False
                    break
            if is_sink:
                return i
        return n-1  # По умолчанию, если не нашли

    def calculate_max_flow(self):
        """Вычисляет максимальный поток и возвращает результат"""
        G = nx.DiGraph()
        n = len(self.adjacency_matrix)
        
        # Добавляем вершины
        G.add_nodes_from(range(n))
        
        # Добавляем рёбра с пропускными способностями
        for i in range(n):
            for j in range(n):
                if self.adjacency_matrix[i][j] > 0:
                    G.add_edge(i, j, capacity=self.adjacency_matrix[i][j])
        
        # Вычисляем максимальный поток
        flow_value, flow_dict = nx.maximum_flow(G, self.source, self.sink)
        #            'edges': self._format_flow_edges(flow_dict)
        return {
            'value': flow_value,
            'source': self.source,
            'sink': self.sink,
        }
