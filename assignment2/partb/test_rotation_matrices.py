"""
Test Suite for Assignment 2 Part B - Rotation Matrices

This module provides comprehensive testing for the rotation matrix
calculations and end-effector position transformations.

Author: Sarthak MDM23101B0019
Course: Robotics Semester 5
"""

import unittest
import numpy as np
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))

from rotation_matrices import RotationMatrixCalculator


class TestRotationMatrices(unittest.TestCase):
    """Test cases for rotation matrix calculations."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.calc = RotationMatrixCalculator()
        self.tolerance = 1e-10
    
    def test_identity_rotations(self):
        """Test that 0-degree rotations produce identity matrices."""
        for axis in ['x', 'y', 'z']:
            with self.subTest(axis=axis):
                matrix = self.calc.get_rotation_matrix(axis, 0)
                np.testing.assert_allclose(matrix, np.eye(3), atol=self.tolerance)
    
    def test_full_rotations(self):
        """Test that 360-degree rotations produce identity matrices."""
        for axis in ['x', 'y', 'z']:
            with self.subTest(axis=axis):
                matrix = self.calc.get_rotation_matrix(axis, 360)
                np.testing.assert_allclose(matrix, np.eye(3), atol=self.tolerance)
    
    def test_matrix_orthogonality(self):
        """Test that rotation matrices are orthogonal (R * R^T = I)."""
        test_angles = [30, 45, 60, 90, 120, 180, 270]
        
        for axis in ['x', 'y', 'z']:
            for angle in test_angles:
                with self.subTest(axis=axis, angle=angle):
                    matrix = self.calc.get_rotation_matrix(axis, angle)
                    identity_check = matrix @ matrix.T
                    np.testing.assert_allclose(identity_check, np.eye(3), atol=self.tolerance)
    
    def test_matrix_determinant(self):
        """Test that rotation matrices have determinant of 1."""
        test_angles = [30, 45, 60, 90, 120, 180, 270]
        
        for axis in ['x', 'y', 'z']:
            for angle in test_angles:
                with self.subTest(axis=axis, angle=angle):
                    matrix = self.calc.get_rotation_matrix(axis, angle)
                    det = np.linalg.det(matrix)
                    self.assertAlmostEqual(det, 1.0, places=10)
    
    def test_inverse_equals_transpose(self):
        """Test that for rotation matrices, inverse equals transpose."""
        test_angles = [30, 45, 60, 90]
        
        for axis in ['x', 'y', 'z']:
            for angle in test_angles:
                with self.subTest(axis=axis, angle=angle):
                    matrix = self.calc.get_rotation_matrix(axis, angle)
                    matrix_inv = np.linalg.inv(matrix)
                    matrix_T = matrix.T
                    np.testing.assert_allclose(matrix_inv, matrix_T, atol=self.tolerance)
    
    def test_x_axis_rotation(self):
        """Test specific X-axis rotation properties."""
        # 90-degree rotation about X-axis should map (0,1,0) to (0,0,1)
        matrix = self.calc.rotation_matrix_x(90)
        original = np.array([0, 1, 0])
        expected = np.array([0, 0, 1])
        result = matrix @ original
        np.testing.assert_allclose(result, expected, atol=self.tolerance)
    
    def test_y_axis_rotation(self):
        """Test specific Y-axis rotation properties."""
        # 90-degree rotation about Y-axis should map (1,0,0) to (0,0,-1)
        matrix = self.calc.rotation_matrix_y(90)
        original = np.array([1, 0, 0])
        expected = np.array([0, 0, -1])
        result = matrix @ original
        np.testing.assert_allclose(result, expected, atol=self.tolerance)
    
    def test_z_axis_rotation(self):
        """Test specific Z-axis rotation properties."""
        # 90-degree rotation about Z-axis should map (1,0,0) to (0,1,0)
        matrix = self.calc.rotation_matrix_z(90)
        original = np.array([1, 0, 0])
        expected = np.array([0, 1, 0])
        result = matrix @ original
        np.testing.assert_allclose(result, expected, atol=self.tolerance)
    
    def test_composite_rotation_associativity(self):
        """Test that composite rotations are applied in correct order."""
        position = np.array([1, 0, 0])
        
        # Apply rotations individually
        r1 = self.calc.get_rotation_matrix('z', 90)
        r2 = self.calc.get_rotation_matrix('y', 90)
        
        # Method 1: Sequential application
        step1 = r1 @ position  # First rotation
        step2 = r2 @ step1     # Second rotation
        
        # Method 2: Composite matrix
        composite = r2 @ r1    # Note: order matters (right to left application)
        result2 = composite @ position
        
        np.testing.assert_allclose(step2, result2, atol=self.tolerance)
    
    def test_assignment_2_part_b_specific(self):
        """Test the specific Assignment 2 Part B problem."""
        initial_position = np.array([2, 3, 4])
        rotations = [('x', 30), ('y', 45), ('z', 60)]
        
        # Calculate using the class method
        result = self.calc.transform_position(initial_position, rotations)
        
        # Calculate manually for verification
        rx = self.calc.rotation_matrix_x(30)
        ry = self.calc.rotation_matrix_y(45)
        rz = self.calc.rotation_matrix_z(60)
        
        composite_manual = rz @ ry @ rx
        result_manual = composite_manual @ initial_position
        
        np.testing.assert_allclose(result, result_manual, atol=self.tolerance)
    
    def test_negative_angles(self):
        """Test that negative angles work correctly."""
        # Rotation by +angle followed by -angle should return to original position
        position = np.array([1, 2, 3])
        
        for axis in ['x', 'y', 'z']:
            for angle in [30, 45, 90]:
                with self.subTest(axis=axis, angle=angle):
                    rotations = [(axis, angle), (axis, -angle)]
                    result = self.calc.transform_position(position, rotations)
                    np.testing.assert_allclose(result, position, atol=self.tolerance)
    
    def test_invalid_axis(self):
        """Test that invalid axis raises appropriate error."""
        with self.assertRaises(ValueError):
            self.calc.get_rotation_matrix('invalid', 30)
    
    def test_large_angles(self):
        """Test that angles larger than 360 degrees work correctly."""
        # 450 degrees should be equivalent to 90 degrees
        matrix_450 = self.calc.get_rotation_matrix('x', 450)
        matrix_90 = self.calc.get_rotation_matrix('x', 90)
        np.testing.assert_allclose(matrix_450, matrix_90, atol=self.tolerance)
    
    def test_position_preservation(self):
        """Test that identity transformations preserve positions."""
        positions = [
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 1],
            [2, 3, 4],
            [-1, -2, -3]
        ]
        
        identity_rotations = [('x', 0), ('y', 0), ('z', 0)]
        
        for pos in positions:
            with self.subTest(position=pos):
                result = self.calc.transform_position(pos, identity_rotations)
                np.testing.assert_allclose(result, pos, atol=self.tolerance)


class TestAssignment2PartBResults(unittest.TestCase):
    """Test cases specifically for Assignment 2 Part B results."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.calc = RotationMatrixCalculator()
    
    def test_assignment_solution_format(self):
        """Test that the assignment solution returns proper format."""
        results = self.calc.solve_assignment_2_part_b()
        
        # Check that all required keys are present
        required_keys = [
            'initial_position',
            'rotations',
            'individual_matrices',
            'composite_matrix',
            'final_position',
            'position_change',
            'distance_moved'
        ]
        
        for key in required_keys:
            self.assertIn(key, results)
    
    def test_final_position_calculation(self):
        """Test the final position calculation for Assignment 2 Part B."""
        results = self.calc.solve_assignment_2_part_b()
        
        # Verify the calculation is correct
        initial = results['initial_position']
        composite = results['composite_matrix']
        final_expected = composite @ initial
        
        np.testing.assert_allclose(
            results['final_position'], 
            final_expected, 
            atol=1e-10
        )
    
    def test_position_change_calculation(self):
        """Test that position change is calculated correctly."""
        results = self.calc.solve_assignment_2_part_b()
        
        expected_change = results['final_position'] - results['initial_position']
        
        np.testing.assert_allclose(
            results['position_change'],
            expected_change,
            atol=1e-10
        )
    
    def test_distance_moved_calculation(self):
        """Test that distance moved is calculated correctly."""
        results = self.calc.solve_assignment_2_part_b()
        
        expected_distance = np.linalg.norm(results['position_change'])
        
        self.assertAlmostEqual(
            results['distance_moved'],
            expected_distance,
            places=10
        )


def run_performance_tests():
    """Run performance and benchmark tests."""
    print("\n" + "=" * 50)
    print("PERFORMANCE TESTS")
    print("=" * 50)
    
    import time
    
    calc = RotationMatrixCalculator()
    
    # Test single matrix calculation performance
    start_time = time.time()
    for _ in range(1000):
        calc.get_rotation_matrix('x', 45)
    single_matrix_time = time.time() - start_time
    
    print(f"1000 single matrix calculations: {single_matrix_time:.4f} seconds")
    
    # Test composite rotation performance
    start_time = time.time()
    rotations = [('x', 30), ('y', 45), ('z', 60)]
    for _ in range(1000):
        calc.calculate_composite_rotation(rotations)
    composite_time = time.time() - start_time
    
    print(f"1000 composite rotation calculations: {composite_time:.4f} seconds")
    
    # Test full transformation performance
    start_time = time.time()
    position = [2, 3, 4]
    for _ in range(1000):
        calc.transform_position(position, rotations)
    transform_time = time.time() - start_time
    
    print(f"1000 full transformations: {transform_time:.4f} seconds")


def main():
    """Run all tests for Assignment 2 Part B."""
    print("Assignment 2 Part B - Rotation Matrices Test Suite")
    print("Student: Sarthak MDM23101B0019")
    print("Course: Robotics Semester 5")
    print("=" * 60)
    
    # Run unit tests
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run performance tests
    run_performance_tests()
    
    print("\n" + "=" * 60)
    print("TEST SUITE COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()