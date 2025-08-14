"""
Assignment 2 Part B Main Demonstration Script

This script provides an interactive demonstration of the rotation matrices
and end-effector position calculation system.

Author: Sarthak MDM23101B0019
Course: Robotics Semester 5
"""

import sys
import os
import numpy as np

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))

from rotation_matrices import RotationMatrixCalculator, demonstrate_generic_rotation_system


def interactive_menu():
    """
    Display interactive menu for Assignment 2 Part B demonstrations.
    """
    calc = RotationMatrixCalculator()
    
    while True:
        print("\n" + "=" * 60)
        print("ASSIGNMENT 2 PART B - ROTATION MATRICES MENU")
        print("=" * 60)
        print("1. Solve Assignment 2 Part B Problem")
        print("2. Custom Rotation Sequence Calculator")
        print("3. Individual Rotation Matrix Calculator")
        print("4. Demonstrate Generic System Examples")
        print("5. Mathematical Verification Tests")
        print("6. Generate Visualization")
        print("7. Exit")
        print("-" * 60)
        
        try:
            choice = input("Enter your choice (1-7): ").strip()
            
            if choice == '1':
                solve_assignment_problem(calc)
            elif choice == '2':
                custom_rotation_calculator(calc)
            elif choice == '3':
                individual_matrix_calculator(calc)
            elif choice == '4':
                demonstrate_generic_rotation_system()
            elif choice == '5':
                mathematical_verification_tests(calc)
            elif choice == '6':
                generate_visualization(calc)
            elif choice == '7':
                print("\nExiting Assignment 2 Part B demonstration.")
                break
            else:
                print("Invalid choice. Please enter a number between 1-7.")
                
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")


def solve_assignment_problem(calc):
    """
    Solve the specific Assignment 2 Part B problem.
    """
    print("\n" + "=" * 50)
    print("SOLVING ASSIGNMENT 2 PART B PROBLEM")
    print("=" * 50)
    
    results = calc.solve_assignment_2_part_b()
    calc.print_summary_report(results)
    
    # Ask if user wants to save results
    save = input("\nSave results to file? (y/n): ").lower().strip()
    if save == 'y':
        save_results_to_file(results)


def custom_rotation_calculator(calc):
    """
    Allow user to input custom rotation sequences.
    """
    print("\n" + "=" * 50)
    print("CUSTOM ROTATION SEQUENCE CALCULATOR")
    print("=" * 50)
    
    try:
        # Get initial position
        print("Enter initial position (x, y, z):")
        x = float(input("X coordinate: "))
        y = float(input("Y coordinate: "))
        z = float(input("Z coordinate: "))
        initial_position = [x, y, z]
        
        # Get rotation sequence
        rotations = []
        print("\nEnter rotation sequence (press Enter with empty axis to finish):")
        
        while True:
            axis = input("Rotation axis (x/y/z) or Enter to finish: ").strip().lower()
            if not axis:
                break
            if axis not in ['x', 'y', 'z']:
                print("Invalid axis. Please enter 'x', 'y', or 'z'.")
                continue
                
            try:
                angle = float(input(f"Angle for {axis.upper()}-axis (degrees): "))
                rotations.append((axis, angle))
            except ValueError:
                print("Invalid angle. Please enter a number.")
                continue
        
        if not rotations:
            print("No rotations specified.")
            return
        
        # Calculate result
        print(f"\nInitial position: {initial_position}")
        print(f"Rotation sequence: {rotations}")
        
        final_position = calc.transform_position(initial_position, rotations)
        composite_matrix = calc.calculate_composite_rotation(rotations)
        
        print(f"\nFinal position: {final_position}")
        print(f"Position change: {final_position - np.array(initial_position)}")
        print(f"Distance moved: {np.linalg.norm(final_position - np.array(initial_position)):.4f}")
        
        print("\nComposite rotation matrix:")
        print(composite_matrix)
        
    except ValueError:
        print("Invalid input. Please enter numeric values for coordinates and angles.")
    except Exception as e:
        print(f"An error occurred: {e}")


def individual_matrix_calculator(calc):
    """
    Calculate and display individual rotation matrices.
    """
    print("\n" + "=" * 50)
    print("INDIVIDUAL ROTATION MATRIX CALCULATOR")
    print("=" * 50)
    
    try:
        axis = input("Enter rotation axis (x/y/z): ").strip().lower()
        if axis not in ['x', 'y', 'z']:
            print("Invalid axis. Please enter 'x', 'y', or 'z'.")
            return
            
        angle = float(input("Enter rotation angle (degrees): "))
        
        matrix = calc.get_rotation_matrix(axis, angle)
        
        print(f"\nRotation matrix for {angle}° about {axis.upper()}-axis:")
        print(matrix)
        
        # Show mathematical properties
        det = np.linalg.det(matrix)
        print(f"\nMatrix properties:")
        print(f"Determinant: {det:.6f} (should be 1.0)")
        
        # Check orthogonality
        identity_check = matrix @ matrix.T
        is_orthogonal = np.allclose(identity_check, np.eye(3))
        print(f"Orthogonal: {is_orthogonal}")
        
        if is_orthogonal:
            print("✓ Valid rotation matrix")
        else:
            print("✗ Invalid rotation matrix")
            
    except ValueError:
        print("Invalid input. Please enter a numeric value for the angle.")
    except Exception as e:
        print(f"An error occurred: {e}")


def mathematical_verification_tests(calc):
    """
    Run mathematical verification tests for the rotation system.
    """
    print("\n" + "=" * 50)
    print("MATHEMATICAL VERIFICATION TESTS")
    print("=" * 50)
    
    test_results = []
    
    # Test 1: Identity rotation (0 degrees)
    print("Test 1: Identity rotation (0° about X-axis)")
    matrix_0 = calc.get_rotation_matrix('x', 0)
    identity_test = np.allclose(matrix_0, np.eye(3))
    print(f"Result: {'PASS' if identity_test else 'FAIL'}")
    test_results.append(identity_test)
    
    # Test 2: 360-degree rotation
    print("\nTest 2: Full rotation (360° about Y-axis)")
    matrix_360 = calc.get_rotation_matrix('y', 360)
    full_rotation_test = np.allclose(matrix_360, np.eye(3))
    print(f"Result: {'PASS' if full_rotation_test else 'FAIL'}")
    test_results.append(full_rotation_test)
    
    # Test 3: Orthogonality check for all axes
    print("\nTest 3: Orthogonality check for all rotation matrices")
    angles_to_test = [30, 45, 60, 90, 120, 180]
    orthogonal_tests = []
    
    for axis in ['x', 'y', 'z']:
        for angle in angles_to_test:
            matrix = calc.get_rotation_matrix(axis, angle)
            identity_check = matrix @ matrix.T
            is_orthogonal = np.allclose(identity_check, np.eye(3))
            orthogonal_tests.append(is_orthogonal)
    
    all_orthogonal = all(orthogonal_tests)
    print(f"Result: {'PASS' if all_orthogonal else 'FAIL'}")
    test_results.append(all_orthogonal)
    
    # Test 4: Determinant check
    print("\nTest 4: Determinant check (should be 1.0 for all rotation matrices)")
    det_tests = []
    
    for axis in ['x', 'y', 'z']:
        for angle in angles_to_test:
            matrix = calc.get_rotation_matrix(axis, angle)
            det = np.linalg.det(matrix)
            det_ok = np.isclose(det, 1.0, atol=1e-10)
            det_tests.append(det_ok)
    
    all_det_ok = all(det_tests)
    print(f"Result: {'PASS' if all_det_ok else 'FAIL'}")
    test_results.append(all_det_ok)
    
    # Test 5: Inverse equals transpose
    print("\nTest 5: Inverse equals transpose for rotation matrices")
    inverse_tests = []
    
    for axis in ['x', 'y', 'z']:
        matrix = calc.get_rotation_matrix(axis, 45)  # Test with 45 degrees
        matrix_inv = np.linalg.inv(matrix)
        matrix_T = matrix.T
        inverse_equals_transpose = np.allclose(matrix_inv, matrix_T)
        inverse_tests.append(inverse_equals_transpose)
    
    all_inverse_ok = all(inverse_tests)
    print(f"Result: {'PASS' if all_inverse_ok else 'FAIL'}")
    test_results.append(all_inverse_ok)
    
    # Summary
    print("\n" + "=" * 50)
    print("VERIFICATION SUMMARY")
    print("=" * 50)
    passed_tests = sum(test_results)
    total_tests = len(test_results)
    print(f"Tests passed: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("✓ All tests PASSED - Rotation matrix implementation is correct!")
    else:
        print("✗ Some tests FAILED - Please check implementation.")


def generate_visualization(calc):
    """
    Generate visualization for the assignment problem.
    """
    print("\n" + "=" * 50)
    print("GENERATING VISUALIZATION")
    print("=" * 50)
    
    try:
        results = calc.solve_assignment_2_part_b()
        print("Generating 3D visualization...")
        calc.visualize_transformation(results)
        print("Visualization complete!")
        
    except ImportError:
        print("Matplotlib not available for visualization.")
        print("Install matplotlib with: pip install matplotlib")
    except Exception as e:
        print(f"Visualization error: {e}")


def save_results_to_file(results):
    """
    Save calculation results to a file.
    """
    try:
        filename = f"assignment2_partb_results.txt"
        with open(filename, 'w') as f:
            f.write("ASSIGNMENT 2 PART B - ROTATION MATRICES RESULTS\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Initial Position: {results['initial_position']}\n")
            f.write(f"Final Position: {results['final_position']}\n")
            f.write(f"Position Change: {results['position_change']}\n")
            f.write(f"Distance Moved: {results['distance_moved']:.6f}\n\n")
            
            f.write("Rotation Sequence:\n")
            for axis, angle in results['rotations']:
                f.write(f"  {angle}° about {axis.upper()}-axis\n")
            f.write("\n")
            
            f.write("Composite Rotation Matrix:\n")
            np.savetxt(f, results['composite_matrix'], fmt='%12.6f')
            f.write("\n")
            
            f.write("Individual Rotation Matrices:\n")
            for key, matrix in results['individual_matrices'].items():
                f.write(f"\n{key}:\n")
                np.savetxt(f, matrix, fmt='%12.6f')
        
        print(f"Results saved to {filename}")
        
    except Exception as e:
        print(f"Error saving results: {e}")


def main():
    """
    Main function for Assignment 2 Part B demonstration.
    """
    print("Assignment 2 Part B - Rotation Matrices and End-Effector Position")
    print("Student: Sarthak MDM23101B0019")
    print("Course: Robotics Semester 5")
    
    interactive_menu()


if __name__ == "__main__":
    main()