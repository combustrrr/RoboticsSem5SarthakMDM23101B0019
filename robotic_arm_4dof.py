"""
Part C: Advanced 4-DOF Robotic Arm with Revolute and Prismatic Joints
for Conveyor Belt Sorting Application
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from scipy.optimize import minimize
import cv2
import time
from typing import List, Tuple, Dict, Optional


class Joint:
    """Base class for robotic arm joints"""
    def __init__(self, joint_type: str, limits: Tuple[float, float], initial_value: float = 0.0):
        """
        Initialize a joint
        
        Args:
            joint_type: 'revolute' or 'prismatic'
            limits: (min_value, max_value) for the joint
            initial_value: Initial position/angle of the joint
        """
        self.joint_type = joint_type
        self.limits = limits
        self.value = initial_value
        self.min_limit, self.max_limit = limits
    
    def set_value(self, value: float) -> bool:
        """Set joint value within limits"""
        if self.min_limit <= value <= self.max_limit:
            self.value = value
            return True
        return False


class RoboticArm4DOF:
    """4-DOF robotic arm with revolute and prismatic joints for industrial sorting"""
    
    def __init__(self, base_links: List[float], joint_types: List[str], joint_limits: List[Tuple[float, float]]):
        """
        Initialize 4-DOF robotic arm
        
        Args:
            base_links: Base link lengths (for revolute joints)
            joint_types: List of joint types ['revolute', 'prismatic', ...]
            joint_limits: List of (min, max) limits for each joint
        """
        self.base_links = np.array(base_links)
        self.num_joints = 4  # Fixed for 4-DOF
        
        # Initialize joints
        self.joints = []
        for i in range(self.num_joints):
            self.joints.append(Joint(joint_types[i], joint_limits[i]))
        
        # Current joint configuration
        self.joint_values = np.array([joint.value for joint in self.joints])
        
        # Base position
        self.base_position = np.array([0.0, 0.0])
        
        # Performance metrics
        self.fk_calculations = 0
        self.ik_calculations = 0
        self.calculation_times = []
    
    def forward_kinematics(self, joint_values: Optional[np.ndarray] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate forward kinematics for 4-DOF arm with mixed joint types
        
        Args:
            joint_values: Joint values [θ1, d2, θ3, θ4] or similar configuration
            
        Returns:
            end_effector_pos: (x, y) position of end effector
            joint_positions: All joint positions for visualization
        """
        start_time = time.time()
        
        if joint_values is None:
            joint_values = self.joint_values
        
        # Initialize transformation matrix (homogeneous coordinates)
        T = np.eye(3)  # 2D transformation matrix
        
        # Track all joint positions for visualization
        joint_positions = [self.base_position.copy()]
        current_pos = self.base_position.copy()
        current_angle = 0.0
        
        for i, (joint, value) in enumerate(zip(self.joints, joint_values)):
            if joint.joint_type == 'revolute':
                # Revolute joint: rotation
                current_angle += value
                # Move along the link
                if i < len(self.base_links):
                    link_length = self.base_links[i]
                else:
                    link_length = 1.0  # Default link length
                
                current_pos = current_pos + np.array([
                    link_length * np.cos(current_angle),
                    link_length * np.sin(current_angle)
                ])
                
            elif joint.joint_type == 'prismatic':
                # Prismatic joint: linear extension
                extension = value
                current_pos = current_pos + np.array([
                    extension * np.cos(current_angle),
                    extension * np.sin(current_angle)
                ])
            
            joint_positions.append(current_pos.copy())
        
        end_effector_pos = current_pos
        joint_positions = np.array(joint_positions)
        
        # Update performance metrics
        self.fk_calculations += 1
        self.calculation_times.append(time.time() - start_time)
        
        return end_effector_pos, joint_positions
    
    def inverse_kinematics(self, target_pos: np.ndarray, initial_guess: Optional[np.ndarray] = None) -> Tuple[bool, np.ndarray]:
        """
        Solve inverse kinematics using optimization for 4-DOF arm
        
        Args:
            target_pos: Target (x, y) position for end effector
            initial_guess: Initial joint configuration guess
            
        Returns:
            success: Whether IK solution was found
            joint_solution: Joint values that reach the target
        """
        start_time = time.time()
        
        if initial_guess is None:
            initial_guess = self.joint_values.copy()
        
        def objective_function(joint_vals):
            """Objective function: distance to target"""
            end_pos, _ = self.forward_kinematics(joint_vals)
            return np.linalg.norm(end_pos - target_pos)
        
        def constraint_function(joint_vals):
            """Joint limit constraints"""
            constraints = []
            for i, (joint, val) in enumerate(zip(self.joints, joint_vals)):
                constraints.append(val - joint.min_limit)  # val >= min_limit
                constraints.append(joint.max_limit - val)  # val <= max_limit
            return np.array(constraints)
        
        # Set up optimization constraints
        constraints = {'type': 'ineq', 'fun': constraint_function}
        
        # Solve inverse kinematics
        result = minimize(
            objective_function,
            initial_guess,
            method='SLSQP',
            constraints=constraints,
            options={'maxiter': 100, 'ftol': 1e-6}
        )
        
        # Update performance metrics
        self.ik_calculations += 1
        self.calculation_times.append(time.time() - start_time)
        
        success = result.success and result.fun < 0.01  # 1cm tolerance
        return success, result.x if success else initial_guess
    
    def set_joint_configuration(self, joint_values: np.ndarray) -> bool:
        """Set joint configuration if within limits"""
        valid = True
        for i, (joint, value) in enumerate(zip(self.joints, joint_values)):
            if not joint.set_value(value):
                valid = False
        
        if valid:
            self.joint_values = joint_values.copy()
        
        return valid
    
    def get_workspace_analysis(self, resolution: int = 50) -> Dict:
        """
        Analyze the workspace of the 4-DOF arm
        
        Args:
            resolution: Grid resolution for workspace analysis
            
        Returns:
            workspace_data: Dictionary with workspace analysis results
        """
        print("Analyzing 4-DOF workspace...")
        
        # Create grid for workspace analysis
        max_reach = np.sum(self.base_links) + max([joint.max_limit for joint in self.joints if joint.joint_type == 'prismatic'])
        x_range = np.linspace(-max_reach, max_reach, resolution)
        y_range = np.linspace(-max_reach, max_reach, resolution)
        
        reachable_points = []
        total_points = resolution * resolution
        
        for i, x in enumerate(x_range):
            for j, y in enumerate(y_range):
                target = np.array([x, y])
                success, _ = self.inverse_kinematics(target)
                if success:
                    reachable_points.append([x, y])
                
                # Progress indicator
                if (i * resolution + j) % (total_points // 10) == 0:
                    progress = ((i * resolution + j) / total_points) * 100
                    print(f"Workspace analysis progress: {progress:.1f}%")
        
        reachable_points = np.array(reachable_points)
        reachability_ratio = len(reachable_points) / total_points
        
        workspace_data = {
            'reachable_points': reachable_points,
            'reachability_ratio': reachability_ratio,
            'total_points_tested': total_points,
            'workspace_area': len(reachable_points) * (2 * max_reach / resolution) ** 2,
            'max_reach': max_reach
        }
        
        print(f"4-DOF Workspace Analysis Complete:")
        print(f"  Reachability Ratio: {reachability_ratio:.3f}")
        print(f"  Workspace Area: {workspace_data['workspace_area']:.2f} units²")
        
        return workspace_data
    
    def visualize_arm(self, ax, joint_positions: np.ndarray, title: str = "4-DOF Robotic Arm"):
        """Visualize the robotic arm configuration"""
        ax.clear()
        
        # Draw base
        base_circle = plt.Circle(self.base_position, 0.1, color='black', zorder=5)
        ax.add_patch(base_circle)
        
        # Draw links
        for i in range(len(joint_positions) - 1):
            ax.plot([joint_positions[i, 0], joint_positions[i+1, 0]],
                   [joint_positions[i, 1], joint_positions[i+1, 1]], 
                   'b-', linewidth=3, alpha=0.7)
        
        # Draw joints
        for i, pos in enumerate(joint_positions[1:]):
            joint_type = self.joints[i].joint_type
            color = 'red' if joint_type == 'revolute' else 'green'
            marker = 'o' if joint_type == 'revolute' else 's'
            ax.plot(pos[0], pos[1], marker, markersize=8, color=color, zorder=4)
        
        # Draw end effector
        end_pos = joint_positions[-1]
        ax.plot(end_pos[0], end_pos[1], 'ko', markersize=10, zorder=5)
        
        # Configure plot
        ax.set_xlim(-6, 6)
        ax.set_ylim(-6, 6)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title(title)
        ax.set_xlabel('X Position')
        ax.set_ylabel('Y Position')
        
        # Add legend
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=8, label='Revolute Joint'),
            Line2D([0], [0], marker='s', color='w', markerfacecolor='green', markersize=8, label='Prismatic Joint'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=8, label='End Effector')
        ]
        ax.legend(handles=legend_elements, loc='upper right')


def create_4dof_arm_configuration():
    """Create a sample 4-DOF arm configuration for testing"""
    # Configuration: 2 revolute + 1 prismatic + 1 revolute
    base_links = [2.0, 1.5, 0.0, 1.0]  # Link lengths (0 for prismatic joint base)
    joint_types = ['revolute', 'revolute', 'prismatic', 'revolute']
    joint_limits = [
        (-np.pi, np.pi),      # Joint 1: Revolute ±180°
        (-np.pi/2, np.pi/2),  # Joint 2: Revolute ±90°
        (0.0, 2.0),           # Joint 3: Prismatic 0-2 units extension
        (-np.pi, np.pi)       # Joint 4: Revolute ±180°
    ]
    
    return RoboticArm4DOF(base_links, joint_types, joint_limits)


if __name__ == "__main__":
    print("Testing 4-DOF Robotic Arm with Mixed Joint Types")
    
    # Create 4-DOF arm
    arm = create_4dof_arm_configuration()
    
    # Test forward kinematics
    print("\n=== Forward Kinematics Test ===")
    test_config = np.array([np.pi/4, np.pi/6, 1.0, -np.pi/3])
    end_pos, joint_pos = arm.forward_kinematics(test_config)
    print(f"Joint Configuration: {test_config}")
    print(f"End Effector Position: ({end_pos[0]:.3f}, {end_pos[1]:.3f})")
    
    # Test inverse kinematics
    print("\n=== Inverse Kinematics Test ===")
    target = np.array([3.0, 2.0])
    success, solution = arm.inverse_kinematics(target)
    print(f"Target Position: ({target[0]:.3f}, {target[1]:.3f})")
    print(f"IK Success: {success}")
    if success:
        print(f"IK Solution: {solution}")
        # Verify solution
        end_pos_verify, _ = arm.forward_kinematics(solution)
        error = np.linalg.norm(end_pos_verify - target)
        print(f"Verification Error: {error:.6f}")
    
    # Visualize the arm
    print("\n=== Visualization ===")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Test configuration
    arm.set_joint_configuration(test_config)
    _, joint_positions = arm.forward_kinematics()
    arm.visualize_arm(ax1, joint_positions, "4-DOF Arm - Test Configuration")
    
    # IK solution configuration
    if success:
        arm.set_joint_configuration(solution)
        _, joint_positions = arm.forward_kinematics()
        arm.visualize_arm(ax2, joint_positions, "4-DOF Arm - IK Solution")
        ax2.plot(target[0], target[1], 'r*', markersize=15, label='Target')
        ax2.legend()
    
    plt.tight_layout()
    plt.savefig('4dof_arm_test.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("\n4-DOF Robotic Arm implementation complete!")