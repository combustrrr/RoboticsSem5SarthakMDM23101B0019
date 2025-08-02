"""
Part C: Main Demo Script for Advanced 4-DOF Robotic Arm and 3D Animation
Demonstrates conveyor belt sorting, 4-DOF arm capabilities, and 3D PyBullet animation
"""
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main demonstration function for Part C"""
    print("=" * 60)
    print("PART C: ADVANCED ROBOTIC ARM FEATURES DEMO")
    print("=" * 60)
    
    while True:
        print("\nSelect demonstration:")
        print("1. 4-DOF Robotic Arm Capabilities")
        print("2. Conveyor Belt Sorting System")
        print("3. 3D Robotic Arm Animation (PyBullet)")
        print("4. Full Analysis and Testing")
        print("5. All demonstrations")
        print("6. Exit")
        
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)
        
        if choice == "1":
            demo_4dof_arm()
        elif choice == "2":
            demo_conveyor_sorting()
        elif choice == "3":
            demo_3d_animation()
        elif choice == "4":
            demo_full_analysis()
        elif choice == "5":
            demo_4dof_arm()
            demo_conveyor_sorting()
            demo_3d_animation()
            demo_full_analysis()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, or 6.")


def demo_4dof_arm():
    """Demonstrate 4-DOF robotic arm capabilities"""
    print("\n" + "=" * 40)
    print("4-DOF ROBOTIC ARM DEMONSTRATION")
    print("=" * 40)
    
    try:
        from robotic_arm_4dof import create_4dof_arm_configuration
        
        arm = create_4dof_arm_configuration()
        
        # Test multiple configurations
        test_configs = [
            np.array([0, 0, 0, 0]),           # Home position
            np.array([np.pi/4, np.pi/6, 1.0, -np.pi/3]),  # Extended configuration
            np.array([-np.pi/3, np.pi/4, 0.5, np.pi/2]),  # Different configuration
            np.array([np.pi/2, -np.pi/6, 1.5, -np.pi/4])  # Maximum extension
        ]
        
        print(f"\nJoint Configuration Types:")
        for i, joint in enumerate(arm.joints):
            print(f"  Joint {i+1}: {joint.joint_type} (limits: {joint.limits})")
        
        print(f"\nTesting {len(test_configs)} different configurations:")
        for i, config in enumerate(test_configs):
            print(f"\nConfiguration {i+1}: {config}")
            arm.set_joint_values(config)
            end_pos = arm.get_end_effector_position()
            print(f"  End effector position: ({end_pos[0]:.2f}, {end_pos[1]:.2f}, {end_pos[2]:.2f})")
            
    except ImportError as e:
        print(f"Import error: {e}")
        print("Required modules for 4-DOF arm not available.")


def demo_conveyor_sorting():
    """Demonstrate conveyor belt sorting system"""
    print("\n" + "=" * 40)
    print("CONVEYOR BELT SORTING DEMONSTRATION")
    print("=" * 40)
    
    try:
        from conveyor_sorting_system import SortingSystem, create_sorting_animation
        
        print("Initializing conveyor belt sorting system...")
        system = SortingSystem()
        
        # Add objects to the conveyor
        objects = [
            {"size": "small", "color": "red", "position": 1.0},
            {"size": "large", "color": "blue", "position": 2.0},
            {"size": "medium", "color": "green", "position": 3.0},
            {"size": "small", "color": "blue", "position": 4.0},
        ]
        
        print(f"\nAdding {len(objects)} objects to conveyor:")
        for i, obj in enumerate(objects):
            system.add_object(obj["size"], obj["color"], obj["position"])
            print(f"  Object {i+1}: {obj['size']} {obj['color']} at position {obj['position']}")
        
        print("\nStarting sorting animation...")
        print("Watch the robotic arm sort objects by size and color!")
        
        # Run sorting animation
        try:
            animation = create_sorting_animation(system)
            print("Sorting completed successfully!")
        except Exception as e:
            print(f"Animation error: {e}")
            print("This might be due to display limitations in the environment.")
            
    except ImportError as e:
        print(f"Import error: {e}")
        print("Required modules for conveyor sorting not available.")


def demo_3d_animation():
    """Demonstrate 3D robotic arm animation using PyBullet"""
    print("\n" + "=" * 40)
    print("3D ROBOTIC ARM ANIMATION DEMONSTRATION")
    print("=" * 40)
    
    try:
        # Import the 3D animation module
        from pybullet_arm_animation import PyBulletRoboticArm
        
        print("Initializing 3D PyBullet simulation...")
        print("This will open a new 3D visualization window.")
        print("Watch the JCB-style robotic arm perform digging motions!")
        
        # Create and run the 3D simulation
        arm_sim = PyBulletRoboticArm(gui=True)
        arm_sim.run_interactive_demo()
        arm_sim.cleanup()
        
    except ImportError as e:
        print(f"PyBullet import error: {e}")
        print("Please ensure PyBullet is installed: pip install pybullet")
    except Exception as e:
        print(f"3D Animation error: {e}")
        print("This might be due to display limitations in the environment.")


def demo_full_analysis():
    """Run full analysis and testing"""
    print("\n" + "=" * 40)
    print("FULL ANALYSIS AND TESTING")
    print("=" * 40)
    
    try:
        from part_c_demo import main as run_part_c_analysis
        print("Running comprehensive Part C analysis...")
        run_part_c_analysis()
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Part C analysis module not available.")
    except Exception as e:
        print(f"Analysis error: {e}")


def quick_demo():
    """Quick demonstration without user interaction"""
    print("Running quick demonstration of advanced features...")
    
    # Test 4-DOF arm
    print("\n1. Testing 4-DOF Arm:")
    demo_4dof_arm()
    
    # Test 3D animation (headless)
    print("\n2. Testing 3D Animation (headless):")
    try:
        from test_3d_animation import TestPyBulletArm
        test = TestPyBulletArm()
        test.test_arm_creation()
        test.test_joint_control()
        print("3D animation system verified successfully!")
    except Exception as e:
        print(f"3D animation test error: {e}")
    
    print("\nPart C demonstration complete!")


if __name__ == "__main__":
    try:
        # Try interactive demo first
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nRunning quick demo instead...")
        quick_demo()