"""
Industrial Robot Pick and Place Simulation with Animation
This module implements a 2DOF robot arm simulation with pick and place operations
and workspace visualization.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, Rectangle
import time


class RobotArm:
    """
    2DOF Robot Arm class for industrial pick and place operations.
    """
    
    def __init__(self, link1_length=3.0, link2_length=2.0):
        """
        Initialize robot arm with given link lengths.
        
        Args:
            link1_length (float): Length of first link
            link2_length (float): Length of second link
        """
        self.l1 = link1_length  # Length of first link
        self.l2 = link2_length  # Length of second link
        self.joint1_angle = 0.0  # Joint 1 angle in radians
        self.joint2_angle = 0.0  # Joint 2 angle in radians
        
        # Pick and place state
        self.carrying_object = False
        self.object_pos = None
        
    def forward_kinematics(self, theta1, theta2):
        """
        Calculate end-effector position given joint angles.
        
        Args:
            theta1 (float): Joint 1 angle in radians
            theta2 (float): Joint 2 angle in radians
            
        Returns:
            tuple: (x, y) position of end-effector
        """
        # Position of joint 2 (elbow)
        x1 = self.l1 * np.cos(theta1)
        y1 = self.l1 * np.sin(theta1)
        
        # Position of end-effector
        x2 = x1 + self.l2 * np.cos(theta1 + theta2)
        y2 = y1 + self.l2 * np.sin(theta1 + theta2)
        
        return x2, y2
    
    def inverse_kinematics(self, x, y):
        """
        Calculate joint angles for desired end-effector position.
        
        Args:
            x (float): Desired x position
            y (float): Desired y position
            
        Returns:
            tuple: (theta1, theta2) joint angles in radians, or None if unreachable
        """
        # Distance from origin to target
        d = np.sqrt(x**2 + y**2)
        
        # Check if target is reachable
        if d > (self.l1 + self.l2) or d < abs(self.l1 - self.l2):
            return None, None
        
        # Calculate joint angles using cosine rule
        cos_theta2 = (x**2 + y**2 - self.l1**2 - self.l2**2) / (2 * self.l1 * self.l2)
        
        # Clamp to valid range to avoid numerical errors
        cos_theta2 = np.clip(cos_theta2, -1, 1)
        
        # Calculate theta2 (elbow up configuration)
        theta2 = np.arccos(cos_theta2)
        
        # Calculate theta1
        k1 = self.l1 + self.l2 * np.cos(theta2)
        k2 = self.l2 * np.sin(theta2)
        theta1 = np.arctan2(y, x) - np.arctan2(k2, k1)
        
        return theta1, theta2
    
    def get_joint_positions(self):
        """
        Get positions of all joints and end-effector.
        
        Returns:
            tuple: ((x0, y0), (x1, y1), (x2, y2)) for base, elbow, and end-effector
        """
        # Base position
        x0, y0 = 0, 0
        
        # Elbow position
        x1 = self.l1 * np.cos(self.joint1_angle)
        y1 = self.l1 * np.sin(self.joint1_angle)
        
        # End-effector position
        x2, y2 = self.forward_kinematics(self.joint1_angle, self.joint2_angle)
        
        return (x0, y0), (x1, y1), (x2, y2)
    
    def move_to_position(self, target_x, target_y, steps=50):
        """
        Generate smooth trajectory to target position.
        
        Args:
            target_x (float): Target x position
            target_y (float): Target y position
            steps (int): Number of interpolation steps
            
        Returns:
            list: List of (theta1, theta2) tuples for trajectory
        """
        # Calculate target joint angles
        target_theta1, target_theta2 = self.inverse_kinematics(target_x, target_y)
        
        if target_theta1 is None:
            print(f"Target position ({target_x:.2f}, {target_y:.2f}) is unreachable!")
            return []
        
        # Generate smooth trajectory
        theta1_traj = np.linspace(self.joint1_angle, target_theta1, steps)
        theta2_traj = np.linspace(self.joint2_angle, target_theta2, steps)
        
        trajectory = list(zip(theta1_traj, theta2_traj))
        
        # Update current angles
        self.joint1_angle = target_theta1
        self.joint2_angle = target_theta2
        
        return trajectory


class PickPlaceSimulation:
    """
    Pick and Place Simulation with Animation
    """
    
    def __init__(self):
        """Initialize the simulation."""
        self.robot = RobotArm(link1_length=3.0, link2_length=2.0)
        
        # Define pick and place locations
        self.pick_location = (4.0, 1.0)
        self.place_location = (-3.0, 2.0)
        self.home_position = (2.0, 3.0)
        
        # Object state
        self.object_at_pick = True
        
        # Animation setup
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(15, 6))
        self.setup_plots()
        
    def setup_plots(self):
        """Setup the plotting environment."""
        # Left plot: Robot animation
        self.ax1.set_xlim(-6, 6)
        self.ax1.set_ylim(-1, 6)
        self.ax1.set_aspect('equal')
        self.ax1.grid(True, alpha=0.3)
        self.ax1.set_title('Robot Pick and Place Simulation')
        self.ax1.set_xlabel('X Position')
        self.ax1.set_ylabel('Y Position')
        
        # Robot arm lines
        self.link1_line, = self.ax1.plot([], [], 'b-', linewidth=8, label='Link 1')
        self.link2_line, = self.ax1.plot([], [], 'r-', linewidth=6, label='Link 2')
        self.joint1_point, = self.ax1.plot([], [], 'ko', markersize=10, label='Joint 1')
        self.joint2_point, = self.ax1.plot([], [], 'ko', markersize=8, label='Joint 2')
        self.end_effector, = self.ax1.plot([], [], 'go', markersize=12, label='End Effector')
        
        # Pick and place locations
        self.ax1.plot(self.pick_location[0], self.pick_location[1], 'bs', markersize=15, label='Pick Location')
        self.ax1.plot(self.place_location[0], self.place_location[1], 'rs', markersize=15, label='Place Location')
        self.ax1.plot(self.home_position[0], self.home_position[1], 'ys', markersize=12, label='Home Position')
        
        # Object
        self.object_circle = Circle(self.pick_location, 0.2, color='orange', label='Object')
        self.ax1.add_patch(self.object_circle)
        
        self.ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Right plot: Workspace visualization
        self.ax2.set_xlim(-6, 6)
        self.ax2.set_ylim(-6, 6)
        self.ax2.set_aspect('equal')
        self.ax2.grid(True, alpha=0.3)
        self.ax2.set_title('Robot Workspace')
        self.ax2.set_xlabel('X Position')
        self.ax2.set_ylabel('Y Position')
        
        self.plot_workspace()
        
    def plot_workspace(self):
        """Plot the robot's reachable workspace."""
        # Generate workspace points
        theta1_range = np.linspace(0, 2*np.pi, 100)
        theta2_range = np.linspace(-np.pi, np.pi, 50)
        
        workspace_x = []
        workspace_y = []
        
        for theta1 in theta1_range:
            for theta2 in theta2_range:
                x, y = self.robot.forward_kinematics(theta1, theta2)
                workspace_x.append(x)
                workspace_y.append(y)
        
        # Plot workspace
        self.ax2.scatter(workspace_x, workspace_y, c='lightblue', s=1, alpha=0.5, label='Reachable Points')
        
        # Plot workspace boundaries
        # Outer circle (maximum reach)
        outer_circle = Circle((0, 0), self.robot.l1 + self.robot.l2, 
                            fill=False, color='blue', linewidth=2, linestyle='--', label='Max Reach')
        self.ax2.add_patch(outer_circle)
        
        # Inner circle (minimum reach) - only if l1 > l2
        if self.robot.l1 > self.robot.l2:
            inner_radius = abs(self.robot.l1 - self.robot.l2)
            inner_circle = Circle((0, 0), inner_radius, 
                                fill=False, color='red', linewidth=2, linestyle='--', label='Min Reach')
            self.ax2.add_patch(inner_circle)
        
        # Mark important points
        self.ax2.plot(0, 0, 'ko', markersize=10, label='Base')
        self.ax2.plot(self.pick_location[0], self.pick_location[1], 'bs', markersize=12, label='Pick Location')
        self.ax2.plot(self.place_location[0], self.place_location[1], 'rs', markersize=12, label='Place Location')
        self.ax2.plot(self.home_position[0], self.home_position[1], 'ys', markersize=10, label='Home Position')
        
        self.ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
    def update_robot_plot(self):
        """Update the robot visualization."""
        base, elbow, end_eff = self.robot.get_joint_positions()
        
        # Update robot arm
        self.link1_line.set_data([base[0], elbow[0]], [base[1], elbow[1]])
        self.link2_line.set_data([elbow[0], end_eff[0]], [elbow[1], end_eff[1]])
        
        # Update joint positions
        self.joint1_point.set_data([base[0]], [base[1]])
        self.joint2_point.set_data([elbow[0]], [elbow[1]])
        self.end_effector.set_data([end_eff[0]], [end_eff[1]])
        
        # Update object position if being carried
        if self.robot.carrying_object:
            self.object_circle.center = end_eff
        
    def execute_pick_place_sequence(self):
        """Execute a complete pick and place sequence with animation."""
        print("Starting pick and place sequence...")
        
        # Move to home position
        print("Moving to home position...")
        trajectory = self.robot.move_to_position(self.home_position[0], self.home_position[1])
        self.animate_trajectory(trajectory)
        
        # Move to pick location
        print("Moving to pick location...")
        trajectory = self.robot.move_to_position(self.pick_location[0], self.pick_location[1])
        self.animate_trajectory(trajectory)
        
        # Pick object
        print("Picking object...")
        self.robot.carrying_object = True
        self.object_at_pick = False
        plt.pause(1.0)
        
        # Move to place location
        print("Moving to place location...")
        trajectory = self.robot.move_to_position(self.place_location[0], self.place_location[1])
        self.animate_trajectory(trajectory)
        
        # Place object
        print("Placing object...")
        self.robot.carrying_object = False
        self.object_circle.center = self.place_location
        plt.pause(1.0)
        
        # Return to home
        print("Returning to home position...")
        trajectory = self.robot.move_to_position(self.home_position[0], self.home_position[1])
        self.animate_trajectory(trajectory)
        
        print("Pick and place sequence completed!")
        
    def animate_trajectory(self, trajectory, delay=0.05):
        """Animate the robot following a trajectory."""
        for theta1, theta2 in trajectory:
            self.robot.joint1_angle = theta1
            self.robot.joint2_angle = theta2
            self.update_robot_plot()
            plt.pause(delay)
            
    def run_simulation(self):
        """Run the complete simulation."""
        plt.ion()  # Turn on interactive mode
        plt.show()
        
        # Initial robot position
        self.robot.joint1_angle = np.pi/4
        self.robot.joint2_angle = np.pi/6
        self.update_robot_plot()
        
        print("Robot Simulation Started!")
        print("Press Enter to start pick and place sequence...")
        input()
        
        # Execute pick and place
        self.execute_pick_place_sequence()
        
        print("Press Enter to exit...")
        input()


def main():
    """Main function to run the robot simulation."""
    print("Industrial Robot Pick and Place Simulation")
    print("=========================================")
    
    # Create and run simulation
    simulation = PickPlaceSimulation()
    simulation.run_simulation()


if __name__ == "__main__":
    main()