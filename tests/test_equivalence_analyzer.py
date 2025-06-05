import unittest
from graph_operations.equivalence_analyzer import EquivalenceAnalyzer


class TestEquivalenceAnalyzer(unittest.TestCase):
    """Набор тестов для анализатора свойств бинарных отношений"""
    
    # Тестовые случаи
    TEST_CASES = [
        # 1 Единичная матрица (рефлексивная, симметричная, транзитивная)
        {
            "matrix": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            "reflexive": True,
            "symmetric": True,
            "transitive": True
        },
        # 2 Полный граф (рефлексивная, симметричная, транзитивная)
        {
            "matrix": [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
            "reflexive": True,
            "symmetric": True,
            "transitive": True
        },
        # 3 Классический пример нетранзитивности
        {
            "matrix": [[1, 1, 0], [0, 1, 1], [0, 0, 1]],
            "reflexive": True,
            "symmetric": False,
            "transitive": False  # 0-1 и 1-2, но нет 0-2
        },
        # 4 Несимметричное отношение
        {
            "matrix": [[1, 1, 0], [0, 1, 0], [1, 0, 1]],
            "reflexive": True,
            "symmetric": False,  # 0-1 != 1-0
            "transitive": True
        },
        # 5 Пустое отношение
        {
            "matrix": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            "reflexive": False,  # Нет петель
            "symmetric": True,
            "transitive": True
        },
        # 6 Сложная транзитивная структура
        {
            "matrix": [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [1, 0, 0, 1]],
            "reflexive": True,
            "symmetric": False,
            "transitive": False  # Множество недостающих связей
        }
    ]
    
    def test_property_detection(self):
        """Тестирование определения свойств отношений"""
        for idx, case in enumerate(self.TEST_CASES, 1):
            with self.subTest(f"Test case #{idx}"):
                analyzer = EquivalenceAnalyzer(case["matrix"])
                self.assertEqual(analyzer.is_reflexive(), case["reflexive"])
                self.assertEqual(analyzer.is_symmetric(), case["symmetric"])
                self.assertEqual(analyzer.is_transitive(), case["transitive"])
    
    def test_error_handling(self):
        """Тестирование обработки невалидных матриц"""
        # Пустая матрица
        with self.assertRaises(ValueError):
            EquivalenceAnalyzer([])
            
        # Не квадратная матрица
        with self.assertRaises(ValueError):
            EquivalenceAnalyzer([[1, 0], [0, 1], [1, 0]])  # 3*2
            
        # Неправильные строки
        with self.assertRaises(ValueError):
            EquivalenceAnalyzer([[1, 0], [0]])  # Длина строк разная
    
    def test_closures(self):
        """Тестирование вычисления замыканий"""
        # Тестовая матрица
        matrix = [[0, 1], [0, 0]]
        analyzer = EquivalenceAnalyzer(matrix)
        
        # Рефлексивное замыкание
        self.assertEqual(
            analyzer.reflexive_closure(),
            [[1, 1], [0, 1]]  # Добавлены диагональные элементы
        )
        
        # Симметричное замыкание
        self.assertEqual(
            analyzer.symmetric_closure(),
            [[0, 1], [1, 0]]  # Добавлена обратная связь
        )
        
        # Транзитивное замыкание
        self.assertEqual(
            analyzer.transitive_closure(),
            [[0, 1], [0, 0]]  # Нет транзитивных связей
        )
        
        # Тест для транзитивного случая
        matrix = [[1, 1, 0], [0, 1, 1], [0, 0, 1]]
        analyzer = EquivalenceAnalyzer(matrix)
        self.assertEqual(
            analyzer.transitive_closure(),
            [[1, 1, 1], [0, 1, 1], [0, 0, 1]]  # Добавлена 0-2
        )

if __name__ == '__main__':
    unittest.main()
