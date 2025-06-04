import unittest
from graph_operations.cycle_detector import CycleDetector

class TestCycleDetector(unittest.TestCase):
    def test_acyclic_graphs(self):
        cases = [
            # 1. ������ ����
            (
                [], 
                []
            ),
            
            # 2. ���� ������� ��� �����
            (
                [[0]], 
                []
            ),
            
            # 3. ��� �������, ���������������� �����
            (
                [
                    [0, 1],
                    [0, 0]
                ],
                []
            ),
            
            # 4. ��� �������, ������� ��� ������
            (
                [
                    [0, 1, 0],
                    [0, 0, 1],
                    [0, 0, 0]
                ], 
                []
            ),
            
            # 5. ���� � ����� ������
            (
                [
                    [0, 1, 1, 1], 
                    [0, 0, 0, 0], 
                    [0, 0, 0, 0], 
                    [0, 0, 0, 0]
                ], 
                []
            )
        ]

        for i, (matrix, expected) in enumerate(cases, start=1):
            with self.subTest(f"acyclic_case_{i}"):
                detector = CycleDetector(matrix)
                cycles = detector.find_cycles()
                self.assertEqual(cycles, expected)

    def test_simple_cycles(self):
        cases = [
            # 1. ��������������� ���� �� ���� ������
            (
                [
                    [0, 1],
                    [1, 0]
                ],
                ['0-1-0']
            ),
            
            # 2. �����������
            (
                [
                    [0, 1, 0], 
                    [0, 0, 1], 
                    [1, 0, 0]
                ], 
                ['0-1-2-0']
            ),
            
            # 3. ������� (4 �������)
            (
                [
                    [0, 1, 0, 0], 
                    [0, 0, 1, 0], 
                    [0, 0, 0, 1], 
                    [1, 0, 0, 0]
                ], 
                ['0-1-2-3-0']
            ),
            
            # 4. ������������� ����
            (
                [
                    [0, 1, 0, 0, 0], 
                    [0, 0, 1, 0, 0], 
                    [0, 0, 0, 1, 0], 
                    [0, 0, 0, 0, 1], 
                    [1, 0, 0, 0, 0]
                ], 
                ['0-1-2-3-4-0']
            ),
            
            # 5. ��� ����������� �����
            (
                [
                    [0, 1, 0, 0], 
                    [1, 0, 0, 0], 
                    [0, 0, 0, 1], 
                    [0, 0, 1, 0]
                ], 
                ['0-1-0', '2-3-2']
            )
        ]

        for i, (matrix, expected) in enumerate(cases, start=1):
            with self.subTest(f"simple_cycle_case_{i}"):
                detector = CycleDetector(matrix)
                cycles = detector.find_cycles()
                self.assertEqual(sorted(cycles), sorted(expected))

    def test_complex_cycles(self):
        cases = [
            # 1. ��� ����� � ����� ��������
            (
                [
                    [0, 1, 0, 0, 0],
                    [0, 0, 1, 1, 0],
                    [1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1],
                    [0, 0, 0, 1, 0]
                ], 
                ['0-1-2-0', '3-4-3']
            ),
            
            # 2. ������ ���� �� 3 �������� � �������������� ��������
            (
                [
                    [0, 1, 1, 1],
                    [1, 0, 1, 0],
                    [1, 1, 0, 0],
                    [1, 0, 0, 0]
                ], 
                ['0-1-0', '0-3-0', '0-1-2-0', '1-2-1']
            ),

            # 3. ����������� � ��������� ����
            (
                [
                    [0, 1, 0, 0, 0],
                    [0, 0, 1, 0, 0],
                    [1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1],
                    [0, 0, 0, 1, 0]
                ], 
                ['0-1-2-0', '3-4-3']
            ),

            # 4. ���� � ��������������� ������� � ����� ��������
            (
                [
                    [0, 1, 1, 0, 0],
                    [0, 0, 1, 1, 0],
                    [1, 0, 0, 1, 0],
                    [0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0]
                ], 
                ['0-1-2-0', '0-1-2-3-4-0']
            ),

            # 5. ���� � ���������� �������
            (
                [
                    [0, 1, 0, 0, 0, 0],
                    [0, 0, 1, 1, 0, 0],
                    [1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 1],
                    [0, 0, 0, 1, 0, 1],
                    [0, 0, 0, 1, 1, 0]
                ], 
                ['0-1-2-0', '3-4-5-3', '3-4-3', '4-5-4']
            )
        ]

        for i, (matrix, expected) in enumerate(cases, start=1):
            with self.subTest(f"complex_case_{i}"):
                detector = CycleDetector(matrix)
                cycles = detector.find_cycles()
                self.assertEqual(sorted(cycles), sorted(expected))

if __name__ == '__main__':
    unittest.main()