"""
Test script for robot kinematics validation
"""

import numpy as np
import matplotlib.pyplot as plt
from robot_simulation import RobotArm


def test_kinematics():
    """Test forward and inverse kinematics."""
    print("Testing Robot Kinematics...")
    
    robot = RobotArm(link1_length=3.0, link2_length=2.0)
    
    # Test forward kinematics
    theta1, theta2 = np.pi/4, np.pi/6
    x, y = robot.forward_kinematics(theta1, theta2)
    print(f"Forward Kinematics: θ1={theta1:.3f}, θ2={theta2:.3f} -> x={x:.3f}, y={y:.3f}")
    
    # Test inverse kinematics
    target_x, target_y = 3.0, 2.0
    calc_theta1, calc_theta2 = robot.inverse_kinematics(target_x, target_y)
    
    if calc_theta1 is not None:
        # Verify by forward kinematics
        verify_x, verify_y = robot.forward_kinematics(calc_theta1, calc_theta2)
        print(f"Inverse Kinematics: x={target_x}, y={target_y} -> θ1={calc_theta1:.3f}, θ2={calc_theta2:.3f}")
        print(f"Verification: θ1={calc_theta1:.3f}, θ2={calc_theta2:.3f} -> x={verify_x:.3f}, y={verify_y:.3f}")
        print(f"Error: dx={abs(target_x - verify_x):.6f}, dy={abs(target_y - verify_y):.6f}")
    else:
        print(f"Position ({target_x}, {target_y}) is unreachable!")
    
    # Test workspace boundaries
    print("\nTesting Workspace Boundaries:")
    max_reach = robot.l1 + robot.l2
    min_reach = abs(robot.l1 - robot.l2)
    print(f"Maximum reach: {max_reach}")
    print(f"Minimum reach: {min_reach}")
    
    # Test reachable positions
    test_positions = [
        (4.9, 0),     # Near max reach
        (0.5, 0),     # Near min reach (if exists)
        (0, 0),       # Origin
        (2, 3),       # Random point
        (6, 0),       # Beyond max reach
    ]
    
    for x, y in test_positions:
        theta1, theta2 = robot.inverse_kinematics(x, y)
        if theta1 is not None:
            print(f"  Position ({x}, {y}): REACHABLE")
        else:
            print(f"  Position ({x}, {y}): UNREACHABLE")


def test_trajectory_generation():
    """Test smooth trajectory generation."""
    print("\nTesting Trajectory Generation...")
    
    robot = RobotArm()
    robot.joint1_angle = 0
    robot.joint2_angle = 0
    
    # Generate trajectory to target
    target_x, target_y = 3.0, 2.0
    trajectory = robot.move_to_position(target_x, target_y, steps=10)
    
    print(f"Generated trajectory with {len(trajectory)} steps")
    if trajectory:
        print("First few trajectory points:")
        for i, (theta1, theta2) in enumerate(trajectory[:3]):
            x, y = robot.forward_kinematics(theta1, theta2)
            print(f"  Step {i}: θ1={theta1:.3f}, θ2={theta2:.3f} -> x={x:.3f}, y={y:.3f}")


if __name__ == "__main__":
    test_kinematics()
    test_trajectory_generation()
    print("\nAll tests completed!")