"""
Simple Robotic Arm Video Demonstration Generator
Creates animated demonstrations suitable for computer graphics projects
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os


class SimpleRoboticArm:
    """Simplified robotic arm for demonstration purposes"""
    
    def __init__(self, link_lengths):
        self.link_lengths = np.array(link_lengths)
        self.joint_angles = np.zeros(len(link_lengths))
    
    def forward_kinematics(self, angles=None):
        """Calculate forward kinematics"""
        if angles is None:
            angles = self.joint_angles
        
        # Calculate cumulative angles
        cumulative_angles = np.cumsum(angles)
        
        # Calculate joint positions
        positions = np.zeros((len(self.link_lengths) + 1, 2))
        
        for i in range(len(self.link_lengths)):
            positions[i+1, 0] = positions[i, 0] + self.link_lengths[i] * np.cos(cumulative_angles[i])
            positions[i+1, 1] = positions[i, 1] + self.link_lengths[i] * np.sin(cumulative_angles[i])
        
        return positions[-1], positions


def create_robotic_arm_demo():
    """Create a comprehensive robotic arm demonstration"""
    print("Creating Robotic Arm Demonstration Video...")
    
    # Initialize robotic arm
    arm = SimpleRoboticArm([2.5, 2.0, 1.5])
    
    # Set up the figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Left subplot: 2D Arm Animation
    ax1.set_xlim(-7, 7)
    ax1.set_ylim(-2, 7)
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.3)
    ax1.set_title('2D Robotic Arm - Pick & Place Operation', fontsize=14, fontweight='bold')
    ax1.set_xlabel('X Position (m)')
    ax1.set_ylabel('Y Position (m)')
    
    # Right subplot: Workspace Analysis
    ax2.set_xlim(-7, 7)
    ax2.set_ylim(-7, 7)
    ax2.set_aspect('equal')
    ax2.grid(True, alpha=0.3)
    ax2.set_title('Robotic Arm Workspace Analysis', fontsize=14, fontweight='bold')
    ax2.set_xlabel('X Position (m)')
    ax2.set_ylabel('Y Position (m)')
    
    # Plot workspace boundary
    theta = np.linspace(0, 2*np.pi, 100)
    max_reach = sum(arm.link_lengths)
    min_reach = abs(arm.link_lengths[0] - sum(arm.link_lengths[1:]))
    ax2.plot(max_reach * np.cos(theta), max_reach * np.sin(theta), 'r--', 
             alpha=0.7, linewidth=2, label='Maximum Reach')
    ax2.plot(min_reach * np.cos(theta), min_reach * np.sin(theta), 'b--', 
             alpha=0.7, linewidth=2, label='Minimum Reach')
    ax2.fill_between(max_reach * np.cos(theta), max_reach * np.sin(theta), 
                     alpha=0.1, color='green', label='Reachable Area')
    ax2.legend()
    
    # Initialize plot elements for left subplot
    arm_line, = ax1.plot([], [], 'b-', linewidth=4, label='Arm Links')
    joints_plot, = ax1.plot([], [], 'ro', markersize=10, label='Joints')
    end_effector, = ax1.plot([], [], 'gs', markersize=15, label='End Effector')
    trajectory, = ax1.plot([], [], 'r--', alpha=0.6, linewidth=2, label='Trajectory')
    
    # Initialize plot elements for right subplot
    current_arm, = ax2.plot([], [], 'b-', linewidth=3, alpha=0.8)
    current_end, = ax2.plot([], [], 'ro', markersize=8)
    workspace_trail, = ax2.plot([], [], 'g.', alpha=0.3, markersize=2)
    
    ax1.legend(loc='upper right')
    
    # Define animation sequence
    n_frames = 200
    trajectory_points = []
    workspace_points = []
    
    # Pre-calculate all joint angle sequences
    joint_sequences = []
    for frame in range(n_frames):
        t = frame / (n_frames - 1)
        
        # Create complex motion pattern
        angle1 = 0.3 * np.sin(4 * np.pi * t) + 0.2 * np.sin(6 * np.pi * t)
        angle2 = -0.5 * np.cos(3 * np.pi * t) + 0.3 * np.sin(5 * np.pi * t)
        angle3 = 0.4 * np.sin(2 * np.pi * t) + 0.2 * np.cos(7 * np.pi * t)
        
        angles = [angle1, angle2, angle3]
        joint_sequences.append(angles)
        
        # Calculate end effector position
        end_pos, _ = arm.forward_kinematics(angles)
        trajectory_points.append(end_pos.copy())
        workspace_points.append(end_pos.copy())
    
    def animate(frame):
        """Animation function"""
        if frame < len(joint_sequences):
            angles = joint_sequences[frame]
            arm.joint_angles = np.array(angles)
            
            # Get arm configuration
            end_pos, joint_positions = arm.forward_kinematics()
            
            # Update left subplot (arm animation)
            arm_line.set_data(joint_positions[:, 0], joint_positions[:, 1])
            joints_plot.set_data(joint_positions[:-1, 0], joint_positions[:-1, 1])
            end_effector.set_data([end_pos[0]], [end_pos[1]])
            
            # Update trajectory (last 50 points)
            if frame > 0:
                start_idx = max(0, frame - 50)
                traj_points = np.array(trajectory_points[start_idx:frame+1])
                trajectory.set_data(traj_points[:, 0], traj_points[:, 1])
            
            # Update right subplot (workspace analysis)
            current_arm.set_data(joint_positions[:, 0], joint_positions[:, 1])
            current_end.set_data([end_pos[0]], [end_pos[1]])
            
            # Update workspace trail
            if frame > 0:
                trail_points = np.array(workspace_points[:frame+1])
                workspace_trail.set_data(trail_points[:, 0], trail_points[:, 1])
            
            # Dynamic titles
            phase = (frame // 50) % 4
            phases = [
                "Scanning and Planning Path",
                "Picking Up Object", 
                "Transporting Object",
                "Placing Object"
            ]
            ax1.set_title(f'2D Robotic Arm - {phases[phase]}', fontsize=14, fontweight='bold')
        
        return arm_line, joints_plot, end_effector, trajectory, current_arm, current_end, workspace_trail
    
    # Create animation
    print("Generating animation frames...")
    anim = animation.FuncAnimation(fig, animate, frames=n_frames, 
                                 interval=100, blit=False, repeat=True)
    
    # Save animation
    output_path = 'assignment1'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    gif_filename = os.path.join(output_path, 'robotic_arm_demo.gif')
    print(f"Saving animation to: {gif_filename}")
    
    try:
        anim.save(gif_filename, writer='pillow', fps=8)
        print(f"✓ Successfully created robotic arm demo: {gif_filename}")
    except Exception as e:
        print(f"Error saving animation: {e}")
        
        # Create static images as fallback
        print("Creating static demonstration images...")
        for i, phase_name in enumerate(['initial', 'picking', 'transporting', 'placing']):
            frame_idx = i * 50
            if frame_idx < len(joint_sequences):
                angles = joint_sequences[frame_idx]
                end_pos, joint_positions = arm.forward_kinematics(angles)
                
                plt.figure(figsize=(10, 8))
                plt.plot(joint_positions[:, 0], joint_positions[:, 1], 'b-', linewidth=4)
                plt.plot(joint_positions[:-1, 0], joint_positions[:-1, 1], 'ro', markersize=10)
                plt.plot([end_pos[0]], [end_pos[1]], 'gs', markersize=15)
                plt.xlim(-7, 7)
                plt.ylim(-2, 7)
                plt.grid(True)
                plt.title(f'Robotic Arm - {phase_name.title()} Phase')
                plt.xlabel('X Position (m)')
                plt.ylabel('Y Position (m)')
                
                img_path = os.path.join(output_path, f'arm_demo_{phase_name}.png')
                plt.savefig(img_path, dpi=150, bbox_inches='tight')
                plt.close()
                print(f"  ✓ Saved: {img_path}")
    
    plt.close(fig)
    
    # Create additional demonstration images
    create_technical_diagrams(output_path)
    
    return gif_filename


def create_technical_diagrams(output_path):
    """Create technical diagrams for the demonstration"""
    print("Creating technical diagrams...")
    
    # 1. Joint Configuration Diagram
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    arm = SimpleRoboticArm([2.5, 2.0, 1.5])
    
    # Show different configurations
    configs = [
        ([0, 0, 0], 'Initial Position'),
        ([0.5, -0.3, 0.8], 'Extended Reach'),
        ([-0.4, 0.6, -0.5], 'Folded Position'),
        ([0.8, -0.8, 1.2], 'Maximum Reach')
    ]
    
    colors = ['blue', 'red', 'green', 'orange']
    
    for i, (angles, label) in enumerate(configs):
        end_pos, joint_positions = arm.forward_kinematics(angles)
        ax.plot(joint_positions[:, 0], joint_positions[:, 1], 
               color=colors[i], linewidth=3, alpha=0.7, label=label)
        ax.plot(joint_positions[:-1, 0], joint_positions[:-1, 1], 
               'o', color=colors[i], markersize=8)
        ax.plot([end_pos[0]], [end_pos[1]], 's', 
               color=colors[i], markersize=12)
    
    ax.set_xlim(-7, 7)
    ax.set_ylim(-2, 7)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_title('Robotic Arm - Joint Configurations', fontsize=16, fontweight='bold')
    ax.set_xlabel('X Position (m)', fontsize=12)
    ax.set_ylabel('Y Position (m)', fontsize=12)
    ax.legend()
    
    config_path = os.path.join(output_path, 'arm_configurations.png')
    plt.savefig(config_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  ✓ Saved: {config_path}")
    
    # 2. Workspace Analysis
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    
    # Generate workspace points
    workspace_points = []
    n_samples = 1000
    
    for _ in range(n_samples):
        # Random joint angles
        angles = np.random.uniform(-np.pi, np.pi, 3)
        end_pos, _ = arm.forward_kinematics(angles)
        workspace_points.append(end_pos)
    
    workspace_points = np.array(workspace_points)
    
    # Plot workspace
    ax.scatter(workspace_points[:, 0], workspace_points[:, 1], 
              c='lightblue', alpha=0.6, s=1, label='Reachable Points')
    
    # Add theoretical boundaries
    theta = np.linspace(0, 2*np.pi, 100)
    max_reach = sum(arm.link_lengths)
    min_reach = abs(arm.link_lengths[0] - sum(arm.link_lengths[1:]))
    
    ax.plot(max_reach * np.cos(theta), max_reach * np.sin(theta), 
           'r-', linewidth=2, label='Maximum Reach')
    ax.plot(min_reach * np.cos(theta), min_reach * np.sin(theta), 
           'b-', linewidth=2, label='Minimum Reach')
    
    ax.set_xlim(-7, 7)
    ax.set_ylim(-7, 7)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_title('Robotic Arm - Workspace Analysis', fontsize=16, fontweight='bold')
    ax.set_xlabel('X Position (m)', fontsize=12)
    ax.set_ylabel('Y Position (m)', fontsize=12)
    ax.legend()
    
    workspace_path = os.path.join(output_path, 'workspace_analysis.png')
    plt.savefig(workspace_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  ✓ Saved: {workspace_path}")


def main():
    """Main function to generate demonstration materials"""
    print("=== Robotic Arm Video Generator ===")
    print("Creating demonstration materials for computer graphics project...")
    
    try:
        # Generate main demonstration
        demo_file = create_robotic_arm_demo()
        
        print("\n=== Generation Complete ===")
        print("✓ Robotic arm demonstration materials created successfully!")
        print("📁 Files are saved in the 'assignment1' folder")
        print("\nGenerated files:")
        
        # List all files in assignment1 folder
        output_dir = 'assignment1'
        if os.path.exists(output_dir):
            files = os.listdir(output_dir)
            for file in sorted(files):
                if file.endswith(('.gif', '.png', '.mp4')):
                    print(f"  • {file}")
        
        print("\n🎬 These materials are ready for your computer graphics project demonstration!")
        print("💡 The GIF animation can be easily converted to video format if needed.")
        
    except Exception as e:
        print(f"\n❌ Error during generation: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()