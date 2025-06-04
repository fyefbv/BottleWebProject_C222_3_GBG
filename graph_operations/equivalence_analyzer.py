class EquivalenceAnalyzer:
    """Анализатор свойств бинарных отношений без зависимостей"""
    
    def __init__(self, matrix):
        if not matrix:
            raise ValueError("Матрица не может быть пустой")
        
        # Проверяем, что матрица квадратная
        n = len(matrix)
        if any(len(row) != n for row in matrix):
            raise ValueError("Матрица должна быть квадратной")
            
        self.matrix = matrix
        self.n = n
        
    def is_reflexive(self):
        """Проверка рефлексивности: диагональ = 1"""
        for i in range(self.n):
            if self.matrix[i][i] != 1:
                return False
        return True
    
    def is_symmetric(self):
        """Проверка симметричности: matrix[i][j] == matrix[j][i]"""
        for i in range(self.n):
            for j in range(i + 1, self.n):  # Оптимизация: проверяем только половину
                if self.matrix[i][j] != self.matrix[j][i]:
                    return False
        return True
    
    def is_transitive(self):
        """Проверка транзитивности через алгоритм Уоршалла"""
        # Создаем копию матрицы
        closure = [row[:] for row in self.matrix]
        
        # Алгоритм Уоршалла (исправленная версия)
        for k in range(self.n):
            for i in range(self.n):
                if closure[i][k]:  # Оптимизация: проверяем только если есть связь
                    for j in range(self.n):
                        closure[i][j] = closure[i][j] or closure[k][j]
        
        # Сравниваем с оригиналом
        for i in range(self.n):
            for j in range(self.n):
                if closure[i][j] != self.matrix[i][j]:
                    return False
        return True
    
    def reflexive_closure(self):
        """Рефлексивное замыкание: добавляем 1 на диагональ"""
        closure = []
        for i in range(self.n):
            new_row = []
            for j in range(self.n):
                # Добавляем 1 на диагональ, остальное оставляем как есть
                if i == j:
                    new_row.append(1)
                else:
                    new_row.append(self.matrix[i][j])
            closure.append(new_row)
        return closure
    
    def symmetric_closure(self):
        """Симметричное замыкание: делаем матрицу симметричной"""
        closure = [row[:] for row in self.matrix]
        for i in range(self.n):
            for j in range(self.n):
                if closure[i][j] == 1:
                    closure[j][i] = 1
        return closure
    
    def transitive_closure(self):
        """Транзитивное замыкание (Уоршалл) - исправленная версия"""
        closure = [row[:] for row in self.matrix]
        for k in range(self.n):
            for i in range(self.n):
                if closure[i][k]:
                    for j in range(self.n):
                        if closure[k][j]:
                            closure[i][j] = 1
        return closure
    
    def format_matrix(self, matrix):
        """Форматирование матрицы для вывода"""
        return "\n".join(" ".join(str(x) for x in row) for row in matrix)
    
    def analyze(self):
        """Основной анализ отношений"""
        return {
            'vertex_count': self.n,
            'adjacency_matrix': self.format_matrix(self.matrix),
            'is_reflexive': self.is_reflexive(),
            'is_symmetric': self.is_symmetric(),
            'is_transitive': self.is_transitive(),
            'reflexive_closure': self.format_matrix(self.reflexive_closure()),
            'symmetric_closure': self.format_matrix(self.symmetric_closure()),
            'transitive_closure': self.format_matrix(self.transitive_closure()),
        }