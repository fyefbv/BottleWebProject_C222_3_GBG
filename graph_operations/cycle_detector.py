class CycleDetector:
    WHITE = 0  # Вершина не посещена
    GRAY = 1   # Вершина в процессе обработки
    BLACK = 2  # Вершина полностью обработана

    def __init__(self, adjacency_matrix):
        self.adj_matrix = adjacency_matrix
        self.n = len(adjacency_matrix)
        self.cycles = set()
        self.color = [self.WHITE] * self.n
        self.path = []

    # Находит все простые циклы в графе
    def find_cycles(self):
        self.cycles.clear()
        self.color = [self.WHITE] * self.n
        
        # Запускаем DFS для каждой непосещённой вершины
        for vertex in range(self.n):
            if self.color[vertex] == self.WHITE:
                self.path = []
                self.dfs(vertex)
                
        return sorted(self.cycles)

    # Выполняет рекурсивный обход в глубину для поиска циклов
    def dfs(self, u):
        self.color[u] = self.GRAY
        self.path.append(u)
        
        # Проверяем всех соседей вершины u
        for v in range(self.n):
            if self.adj_matrix[u][v] == 1:
                if self.color[v] == self.WHITE:
                    # Идём в непосещённую вершину
                    self.dfs(v)
                elif self.color[v] == self.GRAY:
                    # Найден цикл (обратное ребро к серой вершине)
                    cycle = self.extract_cycle(v)
                    canonical = self.canonical_form(cycle)
                    self.cycles.add(canonical)
        
        # Вершина обработана, возвращаемся назад
        self.color[u] = self.BLACK
        self.path.pop()

    # Извлекает цикл из текущего пути
    def extract_cycle(self, v):
        # Находим позицию v в пути и берём подсписок от v до u, замыкаем на v
        start_idx = self.path.index(v)
        cycle = self.path[start_idx:] + [v]
        return cycle

    # Преобразует цикл в каноническую форму
    def canonical_form(self, cycle):
        # Убираем последнее повторение вершины
        base = cycle[:-1]
        n = len(base)
        
        # Находим все возможные ротации
        rotations = [base[i:] + base[:i] for i in range(n)]
        # Находим минимальную ротацию
        min_rot = min(rotations)

        # Проверяем обратное направление
        rev_rot = min_rot[::-1]

        if rev_rot < min_rot:
            min_rot = rev_rot
        
        # Формируем строковое представление
        return "-".join(str(v) for v in min_rot + [min_rot[0]])