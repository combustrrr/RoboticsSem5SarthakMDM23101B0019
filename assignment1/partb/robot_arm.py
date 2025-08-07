"""
Robotic Arm Simulation with Forward and Inverse Kinematics
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.optimize import minimize
import time


class RoboticArm:
    """A 2D robotic arm with multiple joints for pick and place operations"""
    
    def __init__(self, link_lengths, joint_limits=None):
        """
        Initialize the robotic arm
        
        Args:
            link_lengths (list): Length of each link in the arm
            joint_limits (list): [(min_angle, max_angle)] for each joint in radians
        """
        self.link_lengths = np.array(link_lengths)
        self.num_joints = len(link_lengths)
        self.joint_angles = np.zeros(self.num_joints)
        
        if joint_limits is None:
            # Default joint limits: -180 to 180 degrees
            self.joint_limits = [(-np.pi, np.pi) for _ in range(self.num_joints)]
        else:
            self.joint_limits = joint_limits
    
    def forward_kinematics(self, joint_angles=None):
        """
        Calculate forward kinematics to get end effector position
        
        Args:
            joint_angles (array): Joint angles in radians
            
        Returns:
            tuple: (x, y) position of end effector, joint positions
        """
        if joint_angles is None:
            joint_angles = self.joint_angles
        
        # Calculate cumulative angles
        cumulative_angles = np.cumsum(joint_angles)
        
        # Calculate joint positions
        joint_positions = np.zeros((self.num_joints + 1, 2))
        
        for i in range(self.num_joints):
            joint_positions[i + 1, 0] = joint_positions[i, 0] + self.link_lengths[i] * np.cos(cumulative_angles[i])
            joint_positions[i + 1, 1] = joint_positions[i, 1] + self.link_lengths[i] * np.sin(cumulative_angles[i])
        
        end_effector_pos = joint_positions[-1]
        return end_effector_pos, joint_positions
    
    def inverse_kinematics(self, target_x, target_y, initial_guess=None):
        """
        Calculate inverse kinematics to reach target position
        
        Args:
            target_x (float): Target x coordinate
            target_y (float): Target y coordinate
            initial_guess (array): Initial guess for joint angles
            
        Returns:
            array: Joint angles to reach target
        """
        if initial_guess is None:
            initial_guess = self.joint_angles.copy()
        
        def objective(angles):
            pos, _ = self.forward_kinematics(angles)
            return (pos[0] - target_x)**2 + (pos[1] - target_y)**2
        
        def constraint(angles):
            # Joint limit constraints
            constraints = []
            for i, (min_angle, max_angle) in enumerate(self.joint_limits):
                constraints.append(angles[i] - min_angle)
                constraints.append(max_angle - angles[i])
            return np.array(constraints)
        
        # Optimize
        result = minimize(objective, initial_guess, method='SLSQP',
                         constraints={'type': 'ineq', 'fun': constraint})
        
        if result.success:
            return result.x
        else:
            return None
    
    def is_reachable(self, x, y):
        """
        Check if a point is reachable by the arm
        
        Args:
            x (float): x coordinate
            y (float): y coordinate
            
        Returns:
            bool: True if reachable
        """
        distance = np.sqrt(x**2 + y**2)
        max_reach = np.sum(self.link_lengths)
        min_reach = abs(np.sum(self.link_lengths[:-1]) - self.link_lengths[-1])
        
        return min_reach <= distance <= max_reach
    
    def get_workspace(self, resolution=100):
        """
        Calculate the workspace (reachable points) of the robot
        
        Args:
            resolution (int): Number of points to sample in each dimension
            
        Returns:
            tuple: (reachable_points, all_points_tested)
        """
        max_reach = np.sum(self.link_lengths)
        x_range = np.linspace(-max_reach, max_reach, resolution)
        y_range = np.linspace(-max_reach, max_reach, resolution)
        
        reachable_points = []
        all_points = []
        
        for x in x_range:
            for y in y_range:
                all_points.append((x, y))
                if self.is_reachable(x, y):
                    # Additional check with inverse kinematics
                    angles = self.inverse_kinematics(x, y)
                    if angles is not None:
                        reachable_points.append((x, y))
        
        return np.array(reachable_points), np.array(all_points)
    
    def set_joint_angles(self, angles):
        """Set the joint angles"""
        self.joint_angles = np.array(angles)
    
    def get_joint_positions(self):
        """Get current joint positions"""
        _, joint_positions = self.forward_kinematics()
        return joint_positions