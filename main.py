"""
Assignment 1: Robotic Arm Simulation Suite
Main entry point for Part B and Part C demonstrations
"""
import sys
import os
import subprocess


def main():
    """Main demonstration function"""
    print("=" * 60)
    print("ASSIGNMENT 1: ROBOTIC ARM SIMULATION SUITE")
    print("=" * 60)
    
    while True:
        print("\nSelect assignment part:")
        print("1. Part B: Basic Robotic Arm Simulation (2D)")
        print("2. Part C: Advanced Features (4-DOF, Conveyor, 3D)")
        print("3. Exit")
        
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)
        
        if choice == "1":
            run_part_b()
        elif choice == "2":
            run_part_c()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def run_part_b():
    """Run Part B demonstrations"""
    print("\n" + "=" * 50)
    print("LAUNCHING PART B: BASIC ROBOTIC ARM SIMULATION")
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
            print(f"Error running Part B: {e}")
            print("You can also run Part B directly with:")
            print(f"cd assignment1/partb && python main.py")
    else:
        print(f"Part B main script not found at: {partb_path}")


def run_part_c():
    """Run Part C demonstrations"""
    print("\n" + "=" * 50)
    print("LAUNCHING PART C: ADVANCED ROBOTIC ARM FEATURES")
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
            print(f"Error running Part C: {e}")
            print("You can also run Part C directly with:")
            print(f"cd assignment1/partc && python main.py")
    else:
        print(f"Part C main script not found at: {partc_path}")


def quick_demo():
    """Quick demonstration of both parts"""
    print("Running quick demonstration of both assignment parts...")
    
    print("\n=== PART B QUICK DEMO ===")
    try:
        run_part_b()
    except Exception as e:
        print(f"Part B demo error: {e}")
    
    print("\n=== PART C QUICK DEMO ===")
    try:
        run_part_c()
    except Exception as e:
        print(f"Part C demo error: {e}")
    
    print("\nComplete assignment demonstration finished!")


if __name__ == "__main__":
    try:
        # Try interactive demo first
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nRunning quick demo instead...")
        quick_demo()


