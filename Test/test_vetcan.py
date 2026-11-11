import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../codePY')))
from vetcan import hull

class TestBruteForce(unittest.TestCase):
    
    def test_square(self):
        points = [(0, 0), (1, 0), (1, 1), (0, 1)]
        expected = [(0, 0), (1, 0), (1, 1), (0, 1)] # Bắt đầu từ (0,0) và đi CCW
        self.assertEqual(hull(points), expected)

    def test_collinear_points(self):
        points = [(0, 0), (1, 1), (2, 2), (3, 3)]
        expected = [(0, 0), (3, 3)] # Chỉ trả về 2 đầu mút
        self.assertEqual(hull(points), expected)

    def test_keep_collinear(self):
        points = [(0, 0), (1, 0), (2, 0), (2, 2), (0, 2)]
        # Có điểm (1,0) nằm giữa cạnh đáy
        expected_with_collinear = [(0, 0), (1, 0), (2, 0), (2, 2), (0, 2)]
        expected_without_collinear = [(0, 0), (2, 0), (2, 2), (0, 2)]
        
        self.assertEqual(hull(points, keep_collinear=True), expected_with_collinear)
        self.assertEqual(hull(points, keep_collinear=False), expected_without_collinear)

    def test_duplicates(self):
        points = [(0, 0), (1, 1), (0, 0), (1, 1), (0, 1), (1, 0)]
        expected = [(0, 0), (1, 0), (1, 1), (0, 1)]
        self.assertEqual(hull(points), expected)

if __name__ == '__main__':
    unittest.main()
