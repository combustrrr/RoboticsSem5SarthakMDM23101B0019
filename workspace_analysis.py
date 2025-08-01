"""
Advanced Workspace Analysis and Visualization
This script provides detailed analysis of the robot's workspace including
reachability maps, dexterity analysis, and configuration space visualization.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from robot_simulation import RobotArm


class WorkspaceAnalyzer:
    """Advanced workspace analysis for robot arms."""
    
    def __init__(self, robot):
        """
        Initialize workspace analyzer.
        
        Args:
            robot (RobotArm): Robot arm instance to analyze
        """
        self.robot = robot
        
    def generate_workspace_points(self, theta1_resolution=100, theta2_resolution=50):
        """
        Generate all reachable points in the workspace.
        
        Args:
            theta1_resolution (int): Number of samples for joint 1
            theta2_resolution (int): Number of samples for joint 2
            
        Returns:
            tuple: (x_points, y_points, theta1_grid, theta2_grid)
        """
        theta1_range = np.linspace(0, 2*np.pi, theta1_resolution)
        theta2_range = np.linspace(-np.pi, np.pi, theta2_resolution)
        
        x_points = []
        y_points = []
        theta1_vals = []
        theta2_vals = []
        
        for theta1 in theta1_range:
            for theta2 in theta2_range:
                x, y = self.robot.forward_kinematics(theta1, theta2)
                x_points.append(x)
                y_points.append(y)
                theta1_vals.append(theta1)
                theta2_vals.append(theta2)
        
        return np.array(x_points), np.array(y_points), np.array(theta1_vals), np.array(theta2_vals)
    
    def calculate_reachability_map(self, x_range=(-6, 6), y_range=(-6, 6), resolution=0.1):
        """
        Calculate reachability map showing which points can be reached.
        
        Args:
            x_range (tuple): (min_x, max_x) for analysis
            y_range (tuple): (min_y, max_y) for analysis
            resolution (float): Grid resolution
            
        Returns:
            tuple: (X, Y, reachability_map)
        """
        x_vals = np.arange(x_range[0], x_range[1] + resolution, resolution)
        y_vals = np.arange(y_range[0], y_range[1] + resolution, resolution)
        X, Y = np.meshgrid(x_vals, y_vals)
        
        reachability_map = np.zeros_like(X)
        
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                x, y = X[i, j], Y[i, j]
                theta1, theta2 = self.robot.inverse_kinematics(x, y)
                if theta1 is not None:
                    reachability_map[i, j] = 1
        
        return X, Y, reachability_map
    
    def calculate_manipulability(self, x_points, y_points, theta1_vals, theta2_vals):
        """
        Calculate manipulability index for workspace points.
        
        Args:
            x_points, y_points: Workspace points
            theta1_vals, theta2_vals: Corresponding joint angles
            
        Returns:
            numpy.ndarray: Manipulability indices
        """
        manipulability = []
        
        for i in range(len(x_points)):
            theta1, theta2 = theta1_vals[i], theta2_vals[i]
            
            # Calculate Jacobian matrix
            J = self.calculate_jacobian(theta1, theta2)
            
            # Manipulability index = sqrt(det(J * J^T))
            if J is not None:
                det_val = np.linalg.det(J @ J.T)
                if det_val >= 0:
                    manip = np.sqrt(det_val)
                else:
                    manip = 0.0
                manipulability.append(manip)
            else:
                manipulability.append(0)
        
        return np.array(manipulability)
    
    def calculate_jacobian(self, theta1, theta2):
        """
        Calculate the Jacobian matrix for given joint angles.
        
        Args:
            theta1, theta2: Joint angles
            
        Returns:
            numpy.ndarray: 2x2 Jacobian matrix
        """
        # Partial derivatives of end-effector position w.r.t. joint angles
        dx_dtheta1 = -self.robot.l1 * np.sin(theta1) - self.robot.l2 * np.sin(theta1 + theta2)
        dx_dtheta2 = -self.robot.l2 * np.sin(theta1 + theta2)
        dy_dtheta1 = self.robot.l1 * np.cos(theta1) + self.robot.l2 * np.cos(theta1 + theta2)
        dy_dtheta2 = self.robot.l2 * np.cos(theta1 + theta2)
        
        J = np.array([[dx_dtheta1, dx_dtheta2],
                     [dy_dtheta1, dy_dtheta2]])
        
        return J
    
    def plot_comprehensive_analysis(self):
        """Create comprehensive workspace analysis plots."""
        fig = plt.figure(figsize=(20, 12))
        
        # Generate workspace data
        x_points, y_points, theta1_vals, theta2_vals = self.generate_workspace_points()
        
        # Plot 1: Basic workspace with boundaries
        ax1 = fig.add_subplot(2, 3, 1)
        ax1.scatter(x_points, y_points, c='lightblue', s=1, alpha=0.6)
        ax1.set_xlim(-6, 6)
        ax1.set_ylim(-6, 6)
        ax1.set_aspect('equal')
        ax1.grid(True, alpha=0.3)
        ax1.set_title('Robot Workspace - All Reachable Points')
        ax1.set_xlabel('X Position')
        ax1.set_ylabel('Y Position')
        
        # Add workspace boundaries
        outer_circle = Circle((0, 0), self.robot.l1 + self.robot.l2, 
                            fill=False, color='blue', linewidth=2, linestyle='--')
        ax1.add_patch(outer_circle)
        
        if self.robot.l1 > self.robot.l2:
            inner_radius = abs(self.robot.l1 - self.robot.l2)
            inner_circle = Circle((0, 0), inner_radius, 
                                fill=False, color='red', linewidth=2, linestyle='--')
            ax1.add_patch(inner_circle)
        
        # Plot 2: Reachability map
        ax2 = fig.add_subplot(2, 3, 2)
        X, Y, reachability_map = self.calculate_reachability_map(resolution=0.2)
        im = ax2.imshow(reachability_map, extent=[-6, 6, -6, 6], origin='lower', 
                       cmap='RdYlBu', alpha=0.8)
        ax2.set_title('Reachability Map')
        ax2.set_xlabel('X Position')
        ax2.set_ylabel('Y Position')
        plt.colorbar(im, ax=ax2, label='Reachable (1) / Unreachable (0)')
        
        # Plot 3: Joint space visualization
        ax3 = fig.add_subplot(2, 3, 3)
        scatter = ax3.scatter(theta1_vals, theta2_vals, c=np.sqrt(x_points**2 + y_points**2), 
                            s=2, cmap='viridis', alpha=0.6)
        ax3.set_xlabel('Joint 1 Angle (rad)')
        ax3.set_ylabel('Joint 2 Angle (rad)')
        ax3.set_title('Joint Space Configuration')
        ax3.grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=ax3, label='Distance from Origin')
        
        # Plot 4: Manipulability analysis
        ax4 = fig.add_subplot(2, 3, 4)
        manipulability = self.calculate_manipulability(x_points, y_points, theta1_vals, theta2_vals)
        scatter2 = ax4.scatter(x_points, y_points, c=manipulability, s=3, cmap='plasma', alpha=0.7)
        ax4.set_xlim(-6, 6)
        ax4.set_ylim(-6, 6)
        ax4.set_aspect('equal')
        ax4.set_title('Manipulability Index')
        ax4.set_xlabel('X Position')
        ax4.set_ylabel('Y Position')
        ax4.grid(True, alpha=0.3)
        plt.colorbar(scatter2, ax=ax4, label='Manipulability')
        
        # Plot 5: Workspace sections analysis
        ax5 = fig.add_subplot(2, 3, 5)
        
        # Divide workspace into quadrants and analyze
        quadrant_colors = []
        for i in range(len(x_points)):
            x, y = x_points[i], y_points[i]
            if x >= 0 and y >= 0:
                quadrant_colors.append('red')      # Q1
            elif x < 0 and y >= 0:
                quadrant_colors.append('green')    # Q2
            elif x < 0 and y < 0:
                quadrant_colors.append('blue')     # Q3
            else:
                quadrant_colors.append('orange')   # Q4
        
        ax5.scatter(x_points, y_points, c=quadrant_colors, s=2, alpha=0.6)
        ax5.set_xlim(-6, 6)
        ax5.set_ylim(-6, 6)
        ax5.set_aspect('equal')
        ax5.set_title('Workspace Quadrants')
        ax5.set_xlabel('X Position')
        ax5.set_ylabel('Y Position')
        ax5.grid(True, alpha=0.3)
        ax5.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax5.axvline(x=0, color='k', linestyle='-', alpha=0.3)
        
        # Plot 6: Distance analysis
        ax6 = fig.add_subplot(2, 3, 6)
        distances = np.sqrt(x_points**2 + y_points**2)
        
        # Create histogram of reachable distances
        ax6.hist(distances, bins=50, alpha=0.7, color='skyblue', edgecolor='black')
        ax6.axvline(x=self.robot.l1 + self.robot.l2, color='red', linestyle='--', 
                   label=f'Max Reach ({self.robot.l1 + self.robot.l2:.1f})')
        if self.robot.l1 > self.robot.l2:
            ax6.axvline(x=abs(self.robot.l1 - self.robot.l2), color='blue', linestyle='--', 
                       label=f'Min Reach ({abs(self.robot.l1 - self.robot.l2):.1f})')
        ax6.set_xlabel('Distance from Origin')
        ax6.set_ylabel('Number of Reachable Points')
        ax6.set_title('Distance Distribution of Reachable Points')
        ax6.legend()
        ax6.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def print_workspace_statistics(self):
        """Print detailed workspace statistics."""
        print("Workspace Analysis Results")
        print("=" * 50)
        
        # Basic parameters
        print(f"Link 1 Length: {self.robot.l1:.2f}")
        print(f"Link 2 Length: {self.robot.l2:.2f}")
        print(f"Maximum Reach: {self.robot.l1 + self.robot.l2:.2f}")
        print(f"Minimum Reach: {abs(self.robot.l1 - self.robot.l2):.2f}")
        
        # Generate workspace points for analysis
        x_points, y_points, theta1_vals, theta2_vals = self.generate_workspace_points()
        
        print(f"\nGenerated {len(x_points)} workspace points")
        
        # Calculate workspace area (approximate)
        max_reach_area = np.pi * (self.robot.l1 + self.robot.l2)**2
        if self.robot.l1 > self.robot.l2:
            min_reach_area = np.pi * (abs(self.robot.l1 - self.robot.l2))**2
            workspace_area = max_reach_area - min_reach_area
        else:
            workspace_area = max_reach_area
        
        print(f"Theoretical Workspace Area: {workspace_area:.2f} square units")
        
        # Distance statistics
        distances = np.sqrt(x_points**2 + y_points**2)
        print(f"\nDistance Statistics:")
        print(f"  Mean distance: {np.mean(distances):.2f}")
        print(f"  Std deviation: {np.std(distances):.2f}")
        print(f"  Min distance: {np.min(distances):.2f}")
        print(f"  Max distance: {np.max(distances):.2f}")
        
        # Manipulability statistics
        manipulability = self.calculate_manipulability(x_points, y_points, theta1_vals, theta2_vals)
        print(f"\nManipulability Statistics:")
        print(f"  Mean manipulability: {np.mean(manipulability):.4f}")
        print(f"  Std deviation: {np.std(manipulability):.4f}")
        print(f"  Max manipulability: {np.max(manipulability):.4f}")


def main():
    """Main function for workspace analysis."""
    print("Advanced Robot Workspace Analysis")
    print("=" * 40)
    
    # Create robot and analyzer
    robot = RobotArm(link1_length=3.0, link2_length=2.0)
    analyzer = WorkspaceAnalyzer(robot)
    
    # Print statistics
    analyzer.print_workspace_statistics()
    
    # Create comprehensive plots
    print("\nGenerating comprehensive workspace analysis plots...")
    fig = analyzer.plot_comprehensive_analysis()
    
    # Show plots
    plt.show()
    
    print("\nAnalysis complete! Close the plot window to exit.")


if __name__ == "__main__":
    main()