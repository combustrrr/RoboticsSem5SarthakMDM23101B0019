"""
Test the main robot simulation without interactive elements
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

from robot_simulation import PickPlaceSimulation, RobotArm
import matplotlib.pyplot as plt
import numpy as np


def test_robot_simulation():
    """Test the main robot simulation."""
    print("Testing Robot Pick and Place Simulation...")
    
    # Test basic robot arm functionality
    robot = RobotArm(link1_length=3.0, link2_length=2.0)
    
    # Test joint positions
    robot.joint1_angle = np.pi/4
    robot.joint2_angle = np.pi/6
    
    base, elbow, end_eff = robot.get_joint_positions()
    print(f"Base position: ({base[0]:.3f}, {base[1]:.3f})")
    print(f"Elbow position: ({elbow[0]:.3f}, {elbow[1]:.3f})")
    print(f"End-effector position: ({end_eff[0]:.3f}, {end_eff[1]:.3f})")
    
    # Test movement trajectory
    trajectory = robot.move_to_position(4.0, 1.0, steps=5)
    print(f"Generated trajectory with {len(trajectory)} steps")
    
    # Test simulation class
    simulation = PickPlaceSimulation()
    
    # Test workspace plotting (save to file)
    simulation.plot_workspace()
    plt.savefig('/tmp/simulation_workspace.png', dpi=150, bbox_inches='tight')
    print("Simulation workspace plot saved to /tmp/simulation_workspace.png")
    plt.close()
    
    # Test robot plotting
    simulation.update_robot_plot()
    plt.savefig('/tmp/robot_state.png', dpi=150, bbox_inches='tight')
    print("Robot state plot saved to /tmp/robot_state.png")
    plt.close()
    
    # Test trajectory animation (simplified - just run through positions)
    print("Testing trajectory execution...")
    
    # Move to pick location
    pick_trajectory = simulation.robot.move_to_position(4.0, 1.0, steps=3)
    for i, (theta1, theta2) in enumerate(pick_trajectory):
        simulation.robot.joint1_angle = theta1
        simulation.robot.joint2_angle = theta2
        print(f"  Step {i}: θ1={theta1:.3f}, θ2={theta2:.3f}")
    
    # Simulate pick
    simulation.robot.carrying_object = True
    print("  Object picked up")
    
    # Move to place location
    place_trajectory = simulation.robot.move_to_position(-3.0, 2.0, steps=3)
    for i, (theta1, theta2) in enumerate(place_trajectory):
        simulation.robot.joint1_angle = theta1
        simulation.robot.joint2_angle = theta2
        print(f"  Step {i}: θ1={theta1:.3f}, θ2={theta2:.3f}")
    
    # Simulate place
    simulation.robot.carrying_object = False
    print("  Object placed")
    
    # Test reachability of key locations
    locations = {
        "Home": (2.0, 3.0),
        "Pick": (4.0, 1.0),
        "Place": (-3.0, 2.0)
    }
    
    print("\nTesting location reachability:")
    for name, (x, y) in locations.items():
        theta1, theta2 = simulation.robot.inverse_kinematics(x, y)
        if theta1 is not None:
            print(f"  {name} location ({x}, {y}): REACHABLE")
        else:
            print(f"  {name} location ({x}, {y}): UNREACHABLE")


def test_visualization_components():
    """Test individual visualization components."""
    print("\nTesting visualization components...")
    
    # Test workspace generation
    robot = RobotArm()
    
    # Generate sample workspace points
    theta1_range = np.linspace(0, 2*np.pi, 50)
    theta2_range = np.linspace(-np.pi, np.pi, 25)
    
    x_points = []
    y_points = []
    
    for theta1 in theta1_range:
        for theta2 in theta2_range:
            x, y = robot.forward_kinematics(theta1, theta2)
            x_points.append(x)
            y_points.append(y)
    
    print(f"Generated {len(x_points)} workspace points for visualization")
    
    # Create a comprehensive visualization
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    # Plot 1: Workspace points
    ax1.scatter(x_points, y_points, c='lightblue', s=1, alpha=0.6)
    ax1.set_title('Robot Workspace')
    ax1.set_xlabel('X Position')
    ax1.set_ylabel('Y Position')
    ax1.grid(True, alpha=0.3)
    ax1.set_aspect('equal')
    
    # Plot 2: Robot in different configurations
    configs = [(0, 0), (np.pi/2, 0), (np.pi, np.pi/2), (3*np.pi/2, -np.pi/2)]
    colors = ['red', 'green', 'blue', 'orange']
    
    for i, (theta1, theta2) in enumerate(configs):
        robot.joint1_angle = theta1
        robot.joint2_angle = theta2
        base, elbow, end_eff = robot.get_joint_positions()
        
        # Draw robot configuration
        ax2.plot([base[0], elbow[0]], [base[1], elbow[1]], color=colors[i], 
                linewidth=3, alpha=0.7, label=f'Config {i+1}')
        ax2.plot([elbow[0], end_eff[0]], [elbow[1], end_eff[1]], color=colors[i], 
                linewidth=2, alpha=0.7)
        ax2.plot(end_eff[0], end_eff[1], 'o', color=colors[i], markersize=6)
    
    ax2.plot(0, 0, 'ko', markersize=8, label='Base')
    ax2.set_title('Robot Configurations')
    ax2.set_xlabel('X Position')
    ax2.set_ylabel('Y Position')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_aspect('equal')
    
    # Plot 3: Joint space representation
    theta1_vals = [config[0] for config in configs]
    theta2_vals = [config[1] for config in configs]
    
    ax3.scatter(theta1_vals, theta2_vals, c=colors, s=100)
    for i, (theta1, theta2) in enumerate(configs):
        ax3.annotate(f'Config {i+1}', (theta1, theta2), xytext=(5, 5), 
                    textcoords='offset points')
    
    ax3.set_title('Joint Space Configurations')
    ax3.set_xlabel('Joint 1 Angle (rad)')
    ax3.set_ylabel('Joint 2 Angle (rad)')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Distance from origin
    distances = np.sqrt(np.array(x_points)**2 + np.array(y_points)**2)
    ax4.hist(distances, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    ax4.axvline(x=robot.l1 + robot.l2, color='red', linestyle='--', 
               label=f'Max Reach ({robot.l1 + robot.l2:.1f})')
    ax4.axvline(x=abs(robot.l1 - robot.l2), color='blue', linestyle='--', 
               label=f'Min Reach ({abs(robot.l1 - robot.l2):.1f})')
    ax4.set_title('Distance Distribution')
    ax4.set_xlabel('Distance from Origin')
    ax4.set_ylabel('Count')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/tmp/comprehensive_test.png', dpi=150, bbox_inches='tight')
    print("Comprehensive test visualization saved to /tmp/comprehensive_test.png")
    plt.close()


if __name__ == "__main__":
    test_robot_simulation()
    test_visualization_components()
    print("\nAll simulation tests completed successfully!")