"""
Generate example plots for demonstration
"""
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from robot_arm import RoboticArm
from workspace_visualization import WorkspaceVisualizer
from pick_and_place import PickAndPlaceSimulation


def generate_workspace_plot():
    """Generate and save workspace visualization"""
    print("Generating workspace visualization...")
    
    # Create a 3-link robot
    robot = RoboticArm([3.0, 2.5, 1.5])
    visualizer = WorkspaceVisualizer(robot)
    
    # Calculate workspace
    visualizer.calculate_workspace(resolution=150)
    
    # Create the plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot reachable workspace
    max_reach = np.sum(robot.link_lengths)
    
    if len(visualizer.reachable_points) > 0:
        ax1.scatter(visualizer.reachable_points[:, 0], visualizer.reachable_points[:, 1], 
                   c='green', s=1, alpha=0.6, label='Reachable')
    
    # Add theoretical boundaries
    from matplotlib.patches import Circle
    max_circle = Circle((0, 0), max_reach, fill=False, linestyle='--', 
                       color='blue', label='Max reach')
    ax1.add_patch(max_circle)
    
    min_reach = abs(np.sum(robot.link_lengths[:-1]) - robot.link_lengths[-1])
    if min_reach > 0:
        min_circle = Circle((0, 0), min_reach, fill=False, linestyle='--', 
                           color='orange', label='Min reach')
        ax1.add_patch(min_circle)
    
    ax1.set_xlim(-max_reach * 1.1, max_reach * 1.1)
    ax1.set_ylim(-max_reach * 1.1, max_reach * 1.1)
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.set_title('Robotic Arm Workspace')
    ax1.set_xlabel('X (units)')
    ax1.set_ylabel('Y (units)')
    
    # Plot workspace with sample arm configurations
    if len(visualizer.reachable_points) > 0:
        ax2.scatter(visualizer.reachable_points[:, 0], visualizer.reachable_points[:, 1], 
                   c='lightblue', s=1, alpha=0.4, label='Workspace')
    
    # Show several arm configurations
    sample_angles = [
        np.array([0, 0, 0]),
        np.array([np.pi/4, np.pi/6, -np.pi/3]),
        np.array([np.pi/2, -np.pi/4, np.pi/6]),
        np.array([-np.pi/3, np.pi/3, -np.pi/6]),
    ]
    
    colors = ['red', 'blue', 'green', 'orange']
    
    for i, angles in enumerate(sample_angles):
        if i < len(colors):
            joint_positions = robot.forward_kinematics(angles)[1]
            
            ax2.plot(joint_positions[:, 0], joint_positions[:, 1], 
                    color=colors[i], linewidth=2, alpha=0.8, 
                    label=f'Config {i+1}')
            ax2.scatter(joint_positions[:-1, 0], joint_positions[:-1, 1], 
                       c=colors[i], s=50, zorder=5)
            ax2.scatter(joint_positions[-1, 0], joint_positions[-1, 1], 
                       c=colors[i], s=100, marker='*', zorder=6)
    
    ax2.scatter(0, 0, c='black', s=100, marker='o', zorder=7, label='Base')
    
    ax2.set_xlim(-max_reach * 1.1, max_reach * 1.1)
    ax2.set_ylim(-max_reach * 1.1, max_reach * 1.1)
    ax2.set_aspect('equal')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_title('Sample Arm Configurations')
    ax2.set_xlabel('X (units)')
    ax2.set_ylabel('Y (units)')
    
    plt.tight_layout()
    plt.savefig('workspace_visualization.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Workspace visualization saved as 'workspace_visualization.png'")
    
    # Print analysis
    visualizer.analyze_workspace_metrics()


def generate_pick_place_snapshots():
    """Generate snapshots of pick and place operation"""
    print("\nGenerating pick and place snapshots...")
    
    # Create robot and simulation
    robot = RoboticArm([3.0, 2.5, 1.5])
    sim = PickAndPlaceSimulation(robot)
    
    # Add objects and targets
    sim.add_object(4.0, 2.0)
    sim.add_object(3.5, -1.5)
    sim.add_target(-4.0, 1.0)
    sim.add_target(-3.0, -2.0)
    
    # Plan the motion
    sequence = sim.plan_pick_and_place()
    
    # Create snapshots at key points
    key_frames = [0, len(sequence)//4, len(sequence)//2, 3*len(sequence)//4, len(sequence)-1]
    
    fig, axes = plt.subplots(1, len(key_frames), figsize=(20, 4))
    
    for i, frame_idx in enumerate(key_frames):
        ax = axes[i]
        
        # Set robot configuration
        if frame_idx < len(sequence):
            robot.set_joint_angles(sequence[frame_idx])
        
        # Get robot state
        joint_positions = robot.get_joint_positions()
        
        # Plot arm
        ax.plot(joint_positions[:, 0], joint_positions[:, 1], 'b-', linewidth=3, label='Robot Arm')
        ax.scatter(joint_positions[:-1, 0], joint_positions[:-1, 1], c='red', s=100, zorder=5)
        ax.scatter(joint_positions[-1, 0], joint_positions[-1, 1], c='green', s=150, marker='*', zorder=6)
        
        # Plot objects and targets (simplified)
        objects_pos = np.array([[4.0, 2.0], [3.5, -1.5]])
        targets_pos = np.array([[-4.0, 1.0], [-3.0, -2.0]])
        
        ax.scatter(objects_pos[:, 0], objects_pos[:, 1], c='orange', s=200, marker='s', label='Objects')
        ax.scatter(targets_pos[:, 0], targets_pos[:, 1], c='purple', s=200, marker='x', label='Targets')
        
        max_reach = np.sum(robot.link_lengths)
        ax.set_xlim(-max_reach * 1.1, max_reach * 1.1)
        ax.set_ylim(-max_reach * 1.1, max_reach * 1.1)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title(f'Step {frame_idx+1}/{len(sequence)}')
        
        if i == 0:
            ax.legend()
    
    plt.tight_layout()
    plt.savefig('pick_and_place_sequence.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Pick and place sequence saved as 'pick_and_place_sequence.png'")
    print(f"Motion sequence contains {len(sequence)} steps")


if __name__ == "__main__":
    print("Generating demonstration plots...")
    generate_workspace_plot()
    generate_pick_place_snapshots()
    print("\nAll demonstration plots generated successfully!")