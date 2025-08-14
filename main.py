"""
Robotics Semester 5 - Assignment Suite
Main entry point for all assignment demonstrations

Student: Sarthak MDM23101B0019
Course: Robotics Semester 5
"""
import sys
import os
import subprocess


def main():
    """Main demonstration function"""
    print("=" * 70)
    print("ROBOTICS SEMESTER 5 - ASSIGNMENT SUITE")
    print("Student: Sarthak MDM23101B0019")
    print("=" * 70)
    
    while True:
        print("\nSelect assignment:")
        print("1. Assignment 1: Robotic Arm Simulation Suite")
        print("2. Assignment 2: Advanced Robotics Mathematics")
        print("3. Exit")
        
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)
        
        if choice == "1":
            run_assignment_1()
        elif choice == "2":
            run_assignment_2()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def run_assignment_1():
    """Run Assignment 1 menu"""
    print("\n" + "=" * 60)
    print("ASSIGNMENT 1: ROBOTIC ARM SIMULATION SUITE")
    print("=" * 60)
    
    while True:
        print("\nSelect assignment 1 part:")
        print("1. Part B: Basic Robotic Arm Simulation (2D)")
        print("2. Part C: Advanced Features (4-DOF, Conveyor, 3D)")
        print("3. Back to main menu")
        
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
        except KeyboardInterrupt:
            print("\nReturning to main menu...")
            return
        
        if choice == "1":
            run_assignment_1_part_b()
        elif choice == "2":
            run_assignment_1_part_c()
        elif choice == "3":
            return
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def run_assignment_2():
    """Run Assignment 2 menu"""
    print("\n" + "=" * 60)
    print("ASSIGNMENT 2: ADVANCED ROBOTICS MATHEMATICS")
    print("=" * 60)
    
    while True:
        print("\nSelect assignment 2 part:")
        print("1. Part B: Rotation Matrices and End-Effector Position")
        print("2. Back to main menu")
        
        try:
            choice = input("\nEnter your choice (1-2): ").strip()
        except KeyboardInterrupt:
            print("\nReturning to main menu...")
            return
        
        if choice == "1":
            run_assignment_2_part_b()
        elif choice == "2":
            return
        else:
            print("Invalid choice. Please enter 1 or 2.")


def run_assignment_1_part_b():
    """Run Assignment 1 Part B demonstrations"""
    print("\n" + "=" * 50)
    print("LAUNCHING ASSIGNMENT 1 PART B: BASIC ROBOTIC ARM SIMULATION")
    print("=" * 50)
    
    partb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                              'assignment1', 'partb', 'main.py')
    
    if os.path.exists(partb_path):
        try:
            # Change to the partb directory and run
            partb_dir = os.path.dirname(partb_path)
            original_cwd = os.getcwd()
            os.chdir(partb_dir)
            
            # Import and run part B
            sys.path.insert(0, partb_dir)
            import main as partb_main
            partb_main.main()
            
            # Restore original directory
            os.chdir(original_cwd)
            sys.path.remove(partb_dir)
            
        except Exception as e:
            print(f"Error running Assignment 1 Part B: {e}")
            print("You can also run Part B directly with:")
            print(f"cd assignment1/partb && python main.py")
    else:
        print(f"Assignment 1 Part B main script not found at: {partb_path}")


def run_assignment_1_part_c():
    """Run Assignment 1 Part C demonstrations"""
    print("\n" + "=" * 50)
    print("LAUNCHING ASSIGNMENT 1 PART C: ADVANCED ROBOTIC ARM FEATURES")
    print("=" * 50)
    
    partc_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                              'assignment1', 'partc', 'main.py')
    
    if os.path.exists(partc_path):
        try:
            # Change to the partc directory and run
            partc_dir = os.path.dirname(partc_path)
            original_cwd = os.getcwd()
            os.chdir(partc_dir)
            
            # Import and run part C
            sys.path.insert(0, partc_dir)
            import main as partc_main
            partc_main.main()
            
            # Restore original directory
            os.chdir(original_cwd)
            sys.path.remove(partc_dir)
            
        except Exception as e:
            print(f"Error running Assignment 1 Part C: {e}")
            print("You can also run Part C directly with:")
            print(f"cd assignment1/partc && python main.py")
    else:
        print(f"Assignment 1 Part C main script not found at: {partc_path}")


def run_assignment_2_part_b():
    """Run Assignment 2 Part B demonstrations"""
    print("\n" + "=" * 50)
    print("LAUNCHING ASSIGNMENT 2 PART B: ROTATION MATRICES")
    print("=" * 50)
    
    partb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                              'assignment2', 'partb', 'rotation_matrices.py')
    
    if os.path.exists(partb_path):
        try:
            # Change to the assignment2/partb directory and run
            partb_dir = os.path.dirname(partb_path)
            original_cwd = os.getcwd()
            os.chdir(partb_dir)
            
            # Import and run the solution directly
            sys.path.insert(0, partb_dir)
            from rotation_matrices import RotationMatrixCalculator
            
            # Run the assignment solution
            calc = RotationMatrixCalculator()
            results = calc.solve_assignment_2_part_b()
            calc.print_summary_report(results)
            
            # Restore original directory
            os.chdir(original_cwd)
            sys.path.remove(partb_dir)
            
        except Exception as e:
            print(f"Error running Assignment 2 Part B: {e}")
            print("You can also run Assignment 2 Part B directly with:")
            print(f"cd assignment2/partb && python main.py")
    else:
        print(f"Assignment 2 Part B rotation_matrices.py not found at: {partb_path}")
        print("Trying main.py instead...")
        
        # Fallback to main.py
        main_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                 'assignment2', 'partb', 'main.py')
        if os.path.exists(main_path):
            print("Please run Assignment 2 Part B directly with:")
            print(f"cd assignment2/partb && python main.py")


def run_part_b():
    """Legacy function for backward compatibility"""
    run_assignment_1_part_b()


def run_part_c():
    """Legacy function for backward compatibility"""
    run_assignment_1_part_c()


def quick_demo():
    """Quick demonstration of all assignments"""
    print("Running quick demonstration of all assignment parts...")
    
    print("\n=== ASSIGNMENT 1 PART B QUICK DEMO ===")
    try:
        run_assignment_1_part_b()
    except Exception as e:
        print(f"Assignment 1 Part B demo error: {e}")
    
    print("\n=== ASSIGNMENT 1 PART C QUICK DEMO ===")
    try:
        run_assignment_1_part_c()
    except Exception as e:
        print(f"Assignment 1 Part C demo error: {e}")
    
    print("\n=== ASSIGNMENT 2 PART B QUICK DEMO ===")
    try:
        run_assignment_2_part_b()
    except Exception as e:
        print(f"Assignment 2 Part B demo error: {e}")
    
    print("\nComplete assignment suite demonstration finished!")


if __name__ == "__main__":
    try:
        # Try interactive demo first
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nRunning quick demo instead...")
        quick_demo()


