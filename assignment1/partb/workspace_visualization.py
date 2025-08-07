"""
Workspace Visualization for Robotic Arms
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from robot_arm import RoboticArm


class WorkspaceVisualizer:
    """Visualize the workspace and reachable points of a robotic arm"""
    
    def __init__(self, robot_arm):
        """
        Initialize workspace visualizer
        
        Args:
            robot_arm (RoboticArm): The robotic arm instance
        """
        self.robot = robot_arm
        self.reachable_points = None
        self.all_points = None
    
    def calculate_workspace(self, resolution=200):
        """
        Calculate the workspace with given resolution
        
        Args:
            resolution (int): Resolution for workspace calculation
        """
        print(f"Calculating workspace with resolution {resolution}x{resolution}...")
        self.reachable_points, self.all_points = self.robot.get_workspace(resolution)
        print(f"Found {len(self.reachable_points)} reachable points out of {len(self.all_points)} tested")
    
    def plot_workspace(self, show_unreachable=False, save_fig=False):
        """
        Plot the workspace visualization
        
        Args:
            show_unreachable (bool): Whether to show unreachable points
            save_fig (bool): Whether to save the figure
        """
        if self.reachable_points is None:
            self.calculate_workspace()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Plot 1: Reachable workspace
        self._plot_reachable_workspace(ax1, show_unreachable)
        
        # Plot 2: Workspace with arm configurations
        self._plot_workspace_with_arm(ax2)
        
        plt.tight_layout()
        
        if save_fig:
            plt.savefig('robot_workspace.png', dpi=300, bbox_inches='tight')
            print("Workspace visualization saved as 'robot_workspace.png'")
        
        plt.show()
    
    def _plot_reachable_workspace(self, ax, show_unreachable=False):
        """Plot the reachable workspace"""
        max_reach = np.sum(self.robot.link_lengths)
        
        # Plot reachable points
        if len(self.reachable_points) > 0:
            ax.scatter(self.reachable_points[:, 0], self.reachable_points[:, 1], 
                      c='green', s=1, alpha=0.6, label='Reachable')
        
        # Plot unreachable points if requested
        if show_unreachable and len(self.all_points) > 0:
            unreachable = []
            reachable_set = set(map(tuple, self.reachable_points))
            for point in self.all_points:
                if tuple(point) not in reachable_set:
                    unreachable.append(point)
            
            if unreachable:
                unreachable = np.array(unreachable)
                ax.scatter(unreachable[:, 0], unreachable[:, 1], 
                          c='red', s=1, alpha=0.3, label='Unreachable')
        
        # Add theoretical boundaries
        max_circle = Circle((0, 0), max_reach, fill=False, linestyle='--', 
                           color='blue', label='Max reach')
        ax.add_patch(max_circle)
        
        if len(self.robot.link_lengths) > 1:
            min_reach = abs(np.sum(self.robot.link_lengths[:-1]) - self.robot.link_lengths[-1])
            if min_reach > 0:
                min_circle = Circle((0, 0), min_reach, fill=False, linestyle='--', 
                                   color='orange', label='Min reach')
                ax.add_patch(min_circle)
        
        ax.set_xlim(-max_reach * 1.1, max_reach * 1.1)
        ax.set_ylim(-max_reach * 1.1, max_reach * 1.1)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_title('Robotic Arm Workspace')
        ax.set_xlabel('X (units)')
        ax.set_ylabel('Y (units)')
    
    def _plot_workspace_with_arm(self, ax):
        """Plot workspace with sample arm configurations"""
        max_reach = np.sum(self.robot.link_lengths)
        
        # Plot reachable points
        if len(self.reachable_points) > 0:
            ax.scatter(self.reachable_points[:, 0], self.reachable_points[:, 1], 
                      c='lightblue', s=1, alpha=0.4, label='Workspace')
        
        # Show several arm configurations
        sample_angles = [
            np.array([0, 0, 0]),
            np.array([np.pi/4, np.pi/6, -np.pi/3]),
            np.array([np.pi/2, -np.pi/4, np.pi/6]),
            np.array([-np.pi/3, np.pi/3, -np.pi/6]),
            np.array([np.pi, 0, 0])
        ]
        
        colors = ['red', 'blue', 'green', 'orange', 'purple']
        
        for i, angles in enumerate(sample_angles):
            if i < len(colors):
                # Ensure angles are within joint limits
                clipped_angles = np.clip(angles, 
                                       [limit[0] for limit in self.robot.joint_limits],
                                       [limit[1] for limit in self.robot.joint_limits])
                
                joint_positions = self.robot.forward_kinematics(clipped_angles)[1]
                
                ax.plot(joint_positions[:, 0], joint_positions[:, 1], 
                       color=colors[i], linewidth=2, alpha=0.8, 
                       label=f'Config {i+1}')
                ax.scatter(joint_positions[:-1, 0], joint_positions[:-1, 1], 
                          c=colors[i], s=50, zorder=5)
                ax.scatter(joint_positions[-1, 0], joint_positions[-1, 1], 
                          c=colors[i], s=100, marker='*', zorder=6)
        
        ax.scatter(0, 0, c='black', s=100, marker='o', zorder=7, label='Base')
        
        ax.set_xlim(-max_reach * 1.1, max_reach * 1.1)
        ax.set_ylim(-max_reach * 1.1, max_reach * 1.1)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_title('Sample Arm Configurations')
        ax.set_xlabel('X (units)')
        ax.set_ylabel('Y (units)')
    
    def analyze_workspace_metrics(self):
        """Analyze and print workspace metrics"""
        if self.reachable_points is None:
            self.calculate_workspace()
        
        max_reach_theoretical = np.sum(self.robot.link_lengths)
        min_reach_theoretical = abs(np.sum(self.robot.link_lengths[:-1]) - self.robot.link_lengths[-1])
        
        if len(self.reachable_points) > 0:
            distances = np.sqrt(self.reachable_points[:, 0]**2 + self.reachable_points[:, 1]**2)
            max_reach_actual = np.max(distances)
            min_reach_actual = np.min(distances)
            workspace_area = len(self.reachable_points) * (2 * max_reach_theoretical / np.sqrt(len(self.all_points)))**2
        else:
            max_reach_actual = 0
            min_reach_actual = 0
            workspace_area = 0
        
        print("\n=== WORKSPACE ANALYSIS ===")
        print(f"Robot Configuration:")
        print(f"  - Number of joints: {self.robot.num_joints}")
        print(f"  - Link lengths: {self.robot.link_lengths}")
        print(f"  - Joint limits: {self.robot.joint_limits}")
        
        print(f"\nReachability:")
        print(f"  - Theoretical max reach: {max_reach_theoretical:.2f}")
        print(f"  - Theoretical min reach: {min_reach_theoretical:.2f}")
        print(f"  - Actual max reach: {max_reach_actual:.2f}")
        print(f"  - Actual min reach: {min_reach_actual:.2f}")
        
        print(f"\nWorkspace Metrics:")
        print(f"  - Reachable points: {len(self.reachable_points)}")
        print(f"  - Total points tested: {len(self.all_points)}")
        print(f"  - Reachability ratio: {len(self.reachable_points)/len(self.all_points)*100:.1f}%")
        print(f"  - Approximate workspace area: {workspace_area:.2f} square units")


def demo_workspace_visualization():
    """Demonstration of workspace visualization"""
    # Create different robot configurations for comparison
    
    # 2-link robot
    print("=== 2-Link Robot ===")
    robot_2link = RoboticArm([3.0, 2.0])
    viz_2link = WorkspaceVisualizer(robot_2link)
    viz_2link.analyze_workspace_metrics()
    viz_2link.plot_workspace()
    
    # 3-link robot
    print("\n=== 3-Link Robot ===")
    robot_3link = RoboticArm([2.5, 2.0, 1.5])
    viz_3link = WorkspaceVisualizer(robot_3link)
    viz_3link.analyze_workspace_metrics()
    viz_3link.plot_workspace()
    
    # Robot with joint limits
    print("\n=== Robot with Joint Limits ===")
    joint_limits = [(-np.pi, np.pi), (-np.pi/2, np.pi/2), (-np.pi/3, np.pi/3)]
    robot_limited = RoboticArm([2.5, 2.0, 1.5], joint_limits)
    viz_limited = WorkspaceVisualizer(robot_limited)
    viz_limited.analyze_workspace_metrics()
    viz_limited.plot_workspace()


if __name__ == "__main__":
    demo_workspace_visualization()