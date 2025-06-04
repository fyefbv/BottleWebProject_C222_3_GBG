import unittest
from graph_operations.equivalence_analyzer import EquivalenceAnalyzer

print("Running tests...")
class TestEquivalenceAnalyzer(unittest.TestCase):
    """����� ������ ��� ����������� ������� �������� ���������"""
    
    # �������� ������ (5+ �������)
    TEST_CASES = [
        # 1 ��������� ������� (������������, ������������, ������������)
        {
            "matrix": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            "reflexive": True,
            "symmetric": True,
            "transitive": True
        },
        # 2 ������ ���� (������������, ������������, ������������)
        {
            "matrix": [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
            "reflexive": True,
            "symmetric": True,
            "transitive": True
        },
        # 3 ������������ ������ ����������������
        {
            "matrix": [[1, 1, 0], [0, 1, 1], [0, 0, 1]],
            "reflexive": True,
            "symmetric": False,
            "transitive": False  # 0-1 � 1-2, �� ��� 0-2
        },
        # 4 �������������� ���������
        {
            "matrix": [[1, 1, 0], [0, 1, 0], [1, 0, 1]],
            "reflexive": True,
            "symmetric": False,  # 0-1 != 1-0
            "transitive": True
        },
        # 5 ������ ���������
        {
            "matrix": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            "reflexive": False,  # ��� ������
            "symmetric": True,
            "transitive": True
        },
        # 6 ������� ������������ ���������
        {
            "matrix": [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [1, 0, 0, 1]],
            "reflexive": True,
            "symmetric": False,
            "transitive": False  # ��������� ����������� ������
        }
    ]
    
    def test_property_detection(self):
        """������������ ����������� ������� ���������"""
        for idx, case in enumerate(self.TEST_CASES, 1):
            with self.subTest(f"Test case #{idx}"):
                analyzer = EquivalenceAnalyzer(case["matrix"])
                self.assertEqual(analyzer.is_reflexive(), case["reflexive"])
                self.assertEqual(analyzer.is_symmetric(), case["symmetric"])
                self.assertEqual(analyzer.is_transitive(), case["transitive"])
    
    def test_error_handling(self):
        """������������ ��������� ���������� ������"""
        # ������ �������
        with self.assertRaises(ValueError):
            EquivalenceAnalyzer([])
            
        # �� ���������� �������
        with self.assertRaises(ValueError):
            EquivalenceAnalyzer([[1, 0], [0, 1], [1, 0]])  # 3 2
            
        # ������������ ������
        with self.assertRaises(ValueError):
            EquivalenceAnalyzer([[1, 0], [0]])  # ����� ����� ������
    
    def test_closures(self):
        """������������ ���������� ���������"""
        # �������� �������
        matrix = [[0, 1], [0, 0]]
        analyzer = EquivalenceAnalyzer(matrix)
        
        # ������������ ���������
        self.assertEqual(
            analyzer.reflexive_closure(),
            [[1, 1], [0, 1]]  # ��������� ������������ ��������
        )
        
        # ������������ ���������
        self.assertEqual(
            analyzer.symmetric_closure(),
            [[0, 1], [1, 0]]  # ��������� �������� �����
        )
        
        # ������������ ���������
        self.assertEqual(
            analyzer.transitive_closure(),
            [[0, 1], [0, 0]]  # ��� ������������ ������
        )
        
        # ���� ��� ������������� ������
        matrix = [[1, 1, 0], [0, 1, 1], [0, 0, 1]]
        analyzer = EquivalenceAnalyzer(matrix)
        self.assertEqual(
            analyzer.transitive_closure(),
            [[1, 1, 1], [0, 1, 1], [0, 0, 1]]  # ��������� 0-2
        )

if __name__ == '__main__':
    unittest.main()