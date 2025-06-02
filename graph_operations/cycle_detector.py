class CycleDetector:
    """
    Класс для поиска всех простых циклов в ориентированном графе,
    заданном матрицей смежности.
    """

    def __init__(self, adjacency_matrix):
        """
        :param adjacency_matrix: квадратная матрица смежности (список списков 0/1)
        """
        if not isinstance(adjacency_matrix, list) or not all(isinstance(row, list) for row in adjacency_matrix):
            raise ValueError("Матрица смежности должна быть списком списков")
        n = len(adjacency_matrix)
        for row in adjacency_matrix:
            if len(row) != n:
                raise ValueError("Матрица смежности должна быть квадратной (N x N)")
            for val in row:
                if val not in (0, 1):
                    raise ValueError("Элементы матрицы должны быть 0 или 1")

        self.adj_matrix = adjacency_matrix
        self.n = n
        self._cycles = set()

    def _dfs(self, start, current, visited, path):
        """
        Рекурсивный DFS для поиска циклов. 
        :param start: начальная вершина поиска (начало потенциального цикла)
        :param current: текущая вершина в обходе
        :param visited: множество уже посещённых вершин в этом пути
        :param path: список вершин, пройденных до текущей (включая current)
        """
        for neighbor in range(self.n):
            if self.adj_matrix[current][neighbor] == 1:
                if neighbor == start:
                    # найден цикл: path + [start]
                    cycle = path + [start]
                    canonical = self._canonical_form(cycle)
                    self._cycles.add(canonical)
                elif neighbor not in visited:
                    visited.add(neighbor)
                    self._dfs(start, neighbor, visited, path + [neighbor])
                    visited.remove(neighbor)

    def _canonical_form(self, cycle):
        """
        Приводит цикл к каноническому текстовому представлению,
        чтобы избежать дубликатов при совпадении циклов с разных стартовых точек.
        :param cycle: список вершин, замыкающийся на старт [v0, v1, ..., vk, v0]
        :return: строка вида "a-b-c-...-a", где (a,b,c,...) — лексикографически наименьшая ротация без последнего повторения
        """
        # Убираем последний элемент (повтор start) и работаем с базовой последовательностью
        base = cycle[:-1]
        rotations = []
        length = len(base)
        for i in range(length):
            # создаём ротацию: base[i:], base[:i]
            rotated = base[i:] + base[:i]
            rotations.append(tuple(rotated))

        # выбираем лексикографически минимальную ротацию
        minimal = min(rotations)
        # формируем строку и добавляем в конец первый элемент, чтобы замкнуть цикл
        minimal_str = "-".join(str(v) for v in minimal + (minimal[0],))
        return minimal_str

    def find_cycles(self):
        """
        Находит все простые циклы в ориентированном графе.
        :return: список строк вида "0-1-2-0"
        """
        self._cycles.clear()
        for v in range(self.n):
            self._dfs(v, v, {v}, [v])
        # возвращаем отсортированный список для детерминированного порядка
        return sorted(self._cycles)