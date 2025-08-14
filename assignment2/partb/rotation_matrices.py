"""
Assignment 2 Part B: Rotation Matrices and End-Effector Position Calculation

This module implements rotation matrix calculations and composite transformations
for robotic arm end-effector position analysis.

Requirements:
- Initial position: (x,y,z) = (2,3,4)
- Successive rotations: 30° X-axis, 45° Y-axis, 60° Z-axis
- Calculate rotation matrices and final position
- Generic code for any rotation sequence

Author: Sarthak MDM23101B0019
Course: Robotics Semester 5
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Union


class RotationMatrixCalculator:
    """
    A comprehensive class for calculating rotation matrices and applying
    composite transformations to robotic arm end-effector positions.
    """
    
    def __init__(self):
        """Initialize the rotation matrix calculator."""
        self.transformation_history = []
        self.position_history = []
    
    @staticmethod
    def rotation_matrix_x(angle_degrees: float) -> np.ndarray:
        """
        Calculate rotation matrix for rotation about X-axis.
        
        Args:
            angle_degrees: Rotation angle in degrees
            
        Returns:
            3x3 rotation matrix for X-axis rotation
        """
        angle_rad = np.radians(angle_degrees)
        cos_a = np.cos(angle_rad)
        sin_a = np.sin(angle_rad)
        
        return np.array([
            [1, 0, 0],
            [0, cos_a, -sin_a],
            [0, sin_a, cos_a]
        ])
    
    @staticmethod
    def rotation_matrix_y(angle_degrees: float) -> np.ndarray:
        """
        Calculate rotation matrix for rotation about Y-axis.
        
        Args:
            angle_degrees: Rotation angle in degrees
            
        Returns:
            3x3 rotation matrix for Y-axis rotation
        """
        angle_rad = np.radians(angle_degrees)
        cos_a = np.cos(angle_rad)
        sin_a = np.sin(angle_rad)
        
        return np.array([
            [cos_a, 0, sin_a],
            [0, 1, 0],
            [-sin_a, 0, cos_a]
        ])
    
    @staticmethod
    def rotation_matrix_z(angle_degrees: float) -> np.ndarray:
        """
        Calculate rotation matrix for rotation about Z-axis.
        
        Args:
            angle_degrees: Rotation angle in degrees
            
        Returns:
            3x3 rotation matrix for Z-axis rotation
        """
        angle_rad = np.radians(angle_degrees)
        cos_a = np.cos(angle_rad)
        sin_a = np.sin(angle_rad)
        
        return np.array([
            [cos_a, -sin_a, 0],
            [sin_a, cos_a, 0],
            [0, 0, 1]
        ])
    
    def get_rotation_matrix(self, axis: str, angle_degrees: float) -> np.ndarray:
        """
        Get rotation matrix for specified axis and angle.
        
        Args:
            axis: Rotation axis ('x', 'y', or 'z')
            angle_degrees: Rotation angle in degrees
            
        Returns:
            3x3 rotation matrix
        """
        axis = axis.lower()
        if axis == 'x':
            return self.rotation_matrix_x(angle_degrees)
        elif axis == 'y':
            return self.rotation_matrix_y(angle_degrees)
        elif axis == 'z':
            return self.rotation_matrix_z(angle_degrees)
        else:
            raise ValueError(f"Invalid axis: {axis}. Must be 'x', 'y', or 'z'")
    
    def calculate_composite_rotation(self, rotations: List[Tuple[str, float]]) -> np.ndarray:
        """
        Calculate composite rotation matrix from sequence of rotations.
        
        Args:
            rotations: List of (axis, angle) tuples representing rotation sequence
            
        Returns:
            3x3 composite rotation matrix
        """
        composite_matrix = np.eye(3)
        
        for axis, angle in rotations:
            rotation_matrix = self.get_rotation_matrix(axis, angle)
            composite_matrix = rotation_matrix @ composite_matrix
            
        return composite_matrix
    
    def transform_position(self, initial_position: Union[List, np.ndarray], 
                          rotations: List[Tuple[str, float]]) -> np.ndarray:
        """
        Apply composite rotation to initial position.
        
        Args:
            initial_position: Initial 3D position [x, y, z]
            rotations: List of (axis, angle) tuples representing rotation sequence
            
        Returns:
            Final 3D position after all rotations
        """
        initial_pos = np.array(initial_position)
        composite_rotation = self.calculate_composite_rotation(rotations)
        final_position = composite_rotation @ initial_pos
        
        # Store transformation history
        self.transformation_history.append({
            'initial_position': initial_pos.copy(),
            'rotations': rotations.copy(),
            'composite_matrix': composite_rotation.copy(),
            'final_position': final_position.copy()
        })
        
        return final_position
    
    def solve_assignment_2_part_b(self) -> dict:
        """
        Solve the specific Assignment 2 Part B problem.
        
        Returns:
            Dictionary containing all results and matrices
        """
        # Problem parameters
        initial_position = np.array([2, 3, 4])
        rotations = [
            ('x', 30),  # 30° about X-axis
            ('y', 45),  # 45° about Y-axis
            ('z', 60)   # 60° about Z-axis
        ]
        
        print("=" * 60)
        print("ASSIGNMENT 2 PART B - ROTATION MATRICES SOLUTION")
        print("=" * 60)
        print(f"Initial end-effector position: {initial_position}")
        print(f"Rotation sequence: {rotations}")
        print()
        
        # Calculate individual rotation matrices
        print("INDIVIDUAL ROTATION MATRICES:")
        print("-" * 40)
        
        individual_matrices = {}
        for axis, angle in rotations:
            matrix = self.get_rotation_matrix(axis, angle)
            individual_matrices[f'{axis}_{angle}'] = matrix
            print(f"Rotation matrix for {angle}° about {axis.upper()}-axis:")
            print(matrix)
            print()
        
        # Calculate composite rotation matrix
        print("COMPOSITE ROTATION MATRIX:")
        print("-" * 40)
        composite_matrix = self.calculate_composite_rotation(rotations)
        print("R_composite = R_z(60°) * R_y(45°) * R_x(30°)")
        print(composite_matrix)
        print()
        
        # Calculate final position
        print("FINAL POSITION CALCULATION:")
        print("-" * 40)
        final_position = self.transform_position(initial_position, rotations)
        print(f"Final end-effector position: {final_position}")
        print()
        
        # Calculate step-by-step transformation
        print("STEP-BY-STEP TRANSFORMATION:")
        print("-" * 40)
        current_position = initial_position.copy()
        print(f"Initial position: {current_position}")
        
        for i, (axis, angle) in enumerate(rotations):
            rotation_matrix = self.get_rotation_matrix(axis, angle)
            current_position = rotation_matrix @ current_position
            print(f"After {angle}° rotation about {axis.upper()}-axis: {current_position}")
        
        print()
        
        return {
            'initial_position': initial_position,
            'rotations': rotations,
            'individual_matrices': individual_matrices,
            'composite_matrix': composite_matrix,
            'final_position': final_position,
            'position_change': final_position - initial_position,
            'distance_moved': np.linalg.norm(final_position - initial_position)
        }
    
    def visualize_transformation(self, results: dict):
        """
        Create visualization of the transformation process.
        
        Args:
            results: Results dictionary from solve_assignment_2_part_b
        """
        fig = plt.figure(figsize=(15, 10))
        
        # 3D visualization
        ax1 = fig.add_subplot(221, projection='3d')
        
        initial_pos = results['initial_position']
        final_pos = results['final_position']
        
        # Plot initial and final positions
        ax1.scatter(*initial_pos, color='blue', s=100, label='Initial Position')
        ax1.scatter(*final_pos, color='red', s=100, label='Final Position')
        
        # Plot transformation path
        positions = [initial_pos]
        current_pos = initial_pos.copy()
        
        for axis, angle in results['rotations']:
            rotation_matrix = self.get_rotation_matrix(axis, angle)
            current_pos = rotation_matrix @ current_pos
            positions.append(current_pos.copy())
        
        positions = np.array(positions)
        ax1.plot(positions[:, 0], positions[:, 1], positions[:, 2], 
                'g--', alpha=0.7, linewidth=2, label='Transformation Path')
        
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')
        ax1.set_title('3D Transformation Visualization')
        ax1.legend()
        ax1.grid(True)
        
        # Position components comparison
        ax2 = fig.add_subplot(222)
        components = ['X', 'Y', 'Z']
        initial_components = results['initial_position']
        final_components = results['final_position']
        
        x = np.arange(len(components))
        width = 0.35
        
        ax2.bar(x - width/2, initial_components, width, label='Initial', alpha=0.7)
        ax2.bar(x + width/2, final_components, width, label='Final', alpha=0.7)
        
        ax2.set_xlabel('Components')
        ax2.set_ylabel('Position')
        ax2.set_title('Position Components Comparison')
        ax2.set_xticks(x)
        ax2.set_xticklabels(components)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Rotation sequence visualization
        ax3 = fig.add_subplot(223)
        angles = [angle for _, angle in results['rotations']]
        axes = [axis.upper() for axis, _ in results['rotations']]
        
        bars = ax3.bar(axes, angles, color=['red', 'green', 'blue'], alpha=0.7)
        ax3.set_xlabel('Rotation Axis')
        ax3.set_ylabel('Angle (degrees)')
        ax3.set_title('Rotation Sequence')
        ax3.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, angle in zip(bars, angles):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{angle}°', ha='center', va='bottom')
        
        # Distance analysis
        ax4 = fig.add_subplot(224)
        
        # Calculate distances at each step
        distances = [0]  # Start at 0 distance
        current_pos = results['initial_position'].copy()
        
        for axis, angle in results['rotations']:
            rotation_matrix = self.get_rotation_matrix(axis, angle)
            new_pos = rotation_matrix @ current_pos
            distance = np.linalg.norm(new_pos - results['initial_position'])
            distances.append(distance)
            current_pos = new_pos
        
        steps = ['Initial'] + [f"{axis.upper()}({angle}°)" for axis, angle in results['rotations']]
        
        ax4.plot(range(len(distances)), distances, 'o-', linewidth=2, markersize=8)
        ax4.set_xlabel('Transformation Step')
        ax4.set_ylabel('Distance from Initial Position')
        ax4.set_title('Distance Change During Transformation')
        ax4.set_xticks(range(len(steps)))
        ax4.set_xticklabels(steps, rotation=45, ha='right')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        return fig
    
    def print_summary_report(self, results: dict):
        """
        Print a comprehensive summary report.
        
        Args:
            results: Results dictionary from solve_assignment_2_part_b
        """
        print("=" * 80)
        print("ASSIGNMENT 2 PART B - COMPREHENSIVE SUMMARY REPORT")
        print("=" * 80)
        
        print("\n1. PROBLEM STATEMENT:")
        print("-" * 50)
        print("• Initial end-effector position: (2, 3, 4)")
        print("• Rotation sequence: 30° about X-axis, 45° about Y-axis, 60° about Z-axis")
        print("• Find: Rotation matrices and final position")
        
        print("\n2. SOLUTION RESULTS:")
        print("-" * 50)
        print(f"• Final position: ({results['final_position'][0]:.4f}, "
              f"{results['final_position'][1]:.4f}, {results['final_position'][2]:.4f})")
        print(f"• Position change: ({results['position_change'][0]:.4f}, "
              f"{results['position_change'][1]:.4f}, {results['position_change'][2]:.4f})")
        print(f"• Total distance moved: {results['distance_moved']:.4f} units")
        
        print("\n3. ROTATION MATRICES:")
        print("-" * 50)
        print("R_x(30°) =")
        print(results['individual_matrices']['x_30'])
        print("\nR_y(45°) =")
        print(results['individual_matrices']['y_45'])
        print("\nR_z(60°) =")
        print(results['individual_matrices']['z_60'])
        
        print("\n4. COMPOSITE ROTATION MATRIX:")
        print("-" * 50)
        print("R_composite = R_z(60°) × R_y(45°) × R_x(30°) =")
        print(results['composite_matrix'])
        
        print("\n5. VERIFICATION:")
        print("-" * 50)
        verification_result = results['composite_matrix'] @ results['initial_position']
        print(f"R_composite × initial_position = {verification_result}")
        print(f"Direct calculation result:      = {results['final_position']}")
        print(f"Difference (should be ~0):      = {verification_result - results['final_position']}")
        
        print("\n6. MATHEMATICAL PROPERTIES:")
        print("-" * 50)
        det = np.linalg.det(results['composite_matrix'])
        print(f"• Determinant of composite matrix: {det:.6f} (should be 1.0 for rotation)")
        
        # Check if matrix is orthogonal
        identity_check = results['composite_matrix'] @ results['composite_matrix'].T
        is_orthogonal = np.allclose(identity_check, np.eye(3))
        print(f"• Matrix is orthogonal: {is_orthogonal}")
        
        print("\n" + "=" * 80)


def demonstrate_generic_rotation_system():
    """
    Demonstrate the generic rotation system with various examples.
    """
    calc = RotationMatrixCalculator()
    
    print("\n" + "=" * 60)
    print("GENERIC ROTATION SYSTEM DEMONSTRATION")
    print("=" * 60)
    
    # Example 1: Different position and rotations
    print("\nExample 1: Position (1, 0, 0) with 90° rotations")
    position1 = [1, 0, 0]
    rotations1 = [('z', 90), ('x', 90)]
    result1 = calc.transform_position(position1, rotations1)
    print(f"Initial: {position1} → Final: {result1}")
    
    # Example 2: Complex rotation sequence
    print("\nExample 2: Position (0, 1, 1) with complex sequence")
    position2 = [0, 1, 1]
    rotations2 = [('x', 15), ('y', 30), ('z', 45), ('x', -15)]
    result2 = calc.transform_position(position2, rotations2)
    print(f"Initial: {position2} → Final: {result2}")
    
    # Example 3: Identity transformation check
    print("\nExample 3: Identity transformation (360° rotation)")
    position3 = [2, 3, 4]
    rotations3 = [('x', 360)]
    result3 = calc.transform_position(position3, rotations3)
    print(f"Initial: {position3} → Final: {result3}")
    print(f"Difference: {np.array(result3) - np.array(position3)} (should be ~0)")


def main():
    """
    Main function to solve Assignment 2 Part B and demonstrate the system.
    """
    # Initialize calculator
    calc = RotationMatrixCalculator()
    
    # Solve the assignment problem
    results = calc.solve_assignment_2_part_b()
    
    # Print comprehensive report
    calc.print_summary_report(results)
    
    # Create visualization
    try:
        calc.visualize_transformation(results)
    except Exception as e:
        print(f"Visualization not available: {e}")
    
    # Demonstrate generic system
    demonstrate_generic_rotation_system()
    
    return results


if __name__ == "__main__":
    results = main()