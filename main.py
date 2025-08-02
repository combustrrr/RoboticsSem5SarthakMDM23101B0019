"""
Main Demo Script for Robotic Arm Simulation
Demonstrates both pick-and-place operations and workspace visualization
"""
import numpy as np
import matplotlib.pyplot as plt
from robot_arm import RoboticArm
from pick_and_place import PickAndPlaceSimulation
from workspace_visualization import WorkspaceVisualizer
import sys


def main():
    """Main demonstration function"""
    print("=" * 60)
    print("ROBOTIC ARM SIMULATION DEMO")
    print("=" * 60)
    
    # Create a 3-link robotic arm
    link_lengths = [3.0, 2.5, 1.5]
    print(f"Creating 3-link robotic arm with lengths: {link_lengths}")
    robot = RoboticArm(link_lengths)
    
    while True:
        print("\nSelect demonstration:")
        print("1. Pick and Place Animation (2D)")
        print("2. Workspace Visualization (2D)")
        print("3. 3D Robotic Arm Animation (PyBullet)")
        print("4. All demonstrations")
        print("5. Exit")
        
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)
        
        if choice == "1":
            demo_pick_and_place(robot)
        elif choice == "2":
            demo_workspace_visualization(robot)
        elif choice == "3":
            demo_3d_animation()
        elif choice == "4":
            demo_pick_and_place(robot)
            demo_workspace_visualization(robot)
            demo_3d_animation()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")


def demo_pick_and_place(robot):
    """Demonstrate pick and place functionality"""
    print("\n" + "=" * 40)
    print("PICK AND PLACE DEMONSTRATION")
    print("=" * 40)
    
    # Create simulation
    sim = PickAndPlaceSimulation(robot)
    
    # Add objects to pick up at various locations
    objects = [
        (4.0, 2.0),
        (3.5, -1.5),
        (-2.0, 3.0)
    ]
    
    # Add target locations
    targets = [
        (-4.0, 1.0),
        (-3.0, -2.0),
        (1.0, -4.0)
    ]
    
    print(f"Adding {len(objects)} objects to pick up:")
    for i, obj in enumerate(objects):
        sim.add_object(obj[0], obj[1])
        print(f"  Object {i+1}: ({obj[0]}, {obj[1]})")
    
    print(f"\nAdding {len(targets)} target locations:")
    for i, target in enumerate(targets):
        sim.add_target(target[0], target[1])
        print(f"  Target {i+1}: ({target[0]}, {target[1]})")
    
    print("\nStarting pick and place animation...")
    print("Close the animation window to continue.")
    
    # Run simulation
    try:
        animation = sim.run_simulation()
    except Exception as e:
        print(f"Animation error: {e}")
        print("This might be due to display limitations in the environment.")


def demo_workspace_visualization(robot):
    """Demonstrate workspace visualization"""
    print("\n" + "=" * 40)
    print("WORKSPACE VISUALIZATION DEMONSTRATION")
    print("=" * 40)
    
    # Create workspace visualizer
    visualizer = WorkspaceVisualizer(robot)
    
    # Calculate and analyze workspace
    print("Calculating workspace (this may take a moment)...")
    visualizer.calculate_workspace(resolution=150)
    
    # Print analysis
    visualizer.analyze_workspace_metrics()
    
    print("\nGenerating workspace visualization...")
    print("Close the plot window to continue.")
    
    try:
        visualizer.plot_workspace(show_unreachable=True, save_fig=True)
    except Exception as e:
        print(f"Visualization error: {e}")
        print("This might be due to display limitations in the environment.")


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


def quick_demo():
    """Quick demonstration without user interaction"""
    print("Running quick demonstration of both features...")
    
    # Create robot
    link_lengths = [3.0, 2.5, 1.5]
    robot = RoboticArm(link_lengths)
    
    # Workspace visualization
    print("\n1. Workspace Analysis:")
    visualizer = WorkspaceVisualizer(robot)
    visualizer.calculate_workspace(resolution=100)
    visualizer.analyze_workspace_metrics()
    
    # Test inverse kinematics
    print("\n2. Inverse Kinematics Test:")
    test_points = [(4.0, 2.0), (-3.0, 3.0), (0.0, 6.0), (2.0, -2.0)]
    
    for point in test_points:
        x, y = point
        print(f"\nTesting point ({x}, {y}):")
        print(f"  Reachable: {robot.is_reachable(x, y)}")
        
        angles = robot.inverse_kinematics(x, y)
        if angles is not None:
            robot.set_joint_angles(angles)
            end_pos, _ = robot.forward_kinematics()
            error = np.sqrt((end_pos[0] - x)**2 + (end_pos[1] - y)**2)
            print(f"  IK Solution: {np.degrees(angles):.1f}° (error: {error:.4f})")
        else:
            print(f"  No IK solution found")
    
    print("\nDemonstration complete!")


if __name__ == "__main__":
    try:
        # Try interactive demo first
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nRunning quick demo instead...")
        quick_demo()