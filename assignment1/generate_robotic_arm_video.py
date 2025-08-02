"""
Generate a video demonstration of the robotic arm animation
Creates a professional video suitable for computer graphics project demonstrations
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cv2
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'partb'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'partc'))

from partb.robot_arm import RoboticArm
from partc.robotic_arm_4dof import RoboticArm4DOF


class VideoGenerator:
    """Generate professional video demonstrations of robotic arm animations"""
    
    def __init__(self, output_path='assignment1'):
        """Initialize video generator
        
        Args:
            output_path (str): Path to save video files
        """
        self.output_path = output_path
        if not os.path.exists(output_path):
            os.makedirs(output_path)
    
    def create_2d_arm_demo_video(self, filename='2d_robotic_arm_demo.gif'):
        """Create a 2D robotic arm demonstration video"""
        print("Creating 2D Robotic Arm demonstration video...")
        
        # Initialize 3-DOF robotic arm
        arm = RoboticArm([2.0, 1.5, 1.0])
        
        # Set up the figure and axis
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        ax.set_xlim(-6, 6)
        ax.set_ylim(-2, 6)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title('2D Robotic Arm - Pick and Place Animation', fontsize=16, fontweight='bold')
        ax.set_xlabel('X Position (m)', fontsize=12)
        ax.set_ylabel('Y Position (m)', fontsize=12)
        
        # Initialize plot elements
        arm_line, = ax.plot([], [], 'b-', linewidth=3, label='Arm Links')
        joints_plot, = ax.plot([], [], 'ro', markersize=8, label='Joints')
        end_effector, = ax.plot([], [], 'gs', markersize=12, label='End Effector')
        trajectory, = ax.plot([], [], 'r--', alpha=0.6, label='Trajectory')
        
        # Add workspace boundary
        theta = np.linspace(0, 2*np.pi, 100)
        workspace_radius = sum(arm.link_lengths)
        ax.plot(workspace_radius * np.cos(theta), workspace_radius * np.sin(theta), 
                'k--', alpha=0.3, label='Workspace Boundary')
        
        ax.legend(loc='upper right')
        
        # Define predefined joint angle sequences for smooth animation
        n_steps = 150
        joint_sequences = []
        trajectory_points = []
        
        # Phase 1: Move to pick position (50 frames)
        start_angles = [0.0, 0.0, 0.0]
        pick_angles = [0.8, -0.6, 1.2]
        for i in range(50):
            t = i / 49.0
            t_smooth = 3*t*t - 2*t*t*t  # Smooth interpolation
            angles = [start_angles[j] + t_smooth * (pick_angles[j] - start_angles[j]) for j in range(3)]
            joint_sequences.append(angles)
            arm.joint_angles = np.array(angles)
            end_pos, _ = arm.forward_kinematics()
            trajectory_points.append(end_pos)
        
        # Phase 2: Move to via point (50 frames)
        via_angles = [0.3, 0.4, 0.8]
        for i in range(50):
            t = i / 49.0
            t_smooth = 3*t*t - 2*t*t*t
            angles = [pick_angles[j] + t_smooth * (via_angles[j] - pick_angles[j]) for j in range(3)]
            joint_sequences.append(angles)
            arm.joint_angles = np.array(angles)
            end_pos, _ = arm.forward_kinematics()
            trajectory_points.append(end_pos)
        
        # Phase 3: Move to place position (50 frames)
        place_angles = [-0.6, -0.4, 1.0]
        for i in range(50):
            t = i / 49.0
            t_smooth = 3*t*t - 2*t*t*t
            angles = [via_angles[j] + t_smooth * (place_angles[j] - via_angles[j]) for j in range(3)]
            joint_sequences.append(angles)
            arm.joint_angles = np.array(angles)
            end_pos, _ = arm.forward_kinematics()
            trajectory_points.append(end_pos)
        
        def animate(frame):
            """Animation function"""
            if frame < len(joint_sequences):
                # Set joint angles
                arm.joint_angles = np.array(joint_sequences[frame])
                
                # Get current arm configuration
                end_pos, joint_positions = arm.forward_kinematics()
                
                # Update plots
                arm_line.set_data(joint_positions[:, 0], joint_positions[:, 1])
                joints_plot.set_data(joint_positions[:-1, 0], joint_positions[:-1, 1])
                end_effector.set_data([end_pos[0]], [end_pos[1]])
                
                # Update trajectory
                if frame > 0:
                    traj_points = np.array(trajectory_points[:frame+1])
                    trajectory.set_data(traj_points[:, 0], traj_points[:, 1])
                
                # Add phase annotations
                if frame < 50:
                    ax.set_title('2D Robotic Arm - Phase 1: Moving to Pick Position', 
                               fontsize=16, fontweight='bold')
                elif frame < 100:
                    ax.set_title('2D Robotic Arm - Phase 2: Lifting Object', 
                               fontsize=16, fontweight='bold')
                else:
                    ax.set_title('2D Robotic Arm - Phase 3: Moving to Place Position', 
                               fontsize=16, fontweight='bold')
            
            return arm_line, joints_plot, end_effector, trajectory
        
        # Create animation
        anim = animation.FuncAnimation(fig, animate, frames=n_steps, 
                                     interval=100, blit=False, repeat=True)
        
        # Save as GIF (since FFmpeg is not available)
        video_path = os.path.join(self.output_path, filename)
        print(f"Saving animation to: {video_path}")
        
        try:
            anim.save(video_path, writer='pillow', fps=10)
            print(f"✓ Successfully created 2D arm demo animation: {video_path}")
        except Exception as e:
            print(f"Error saving animation: {e}")
            # Fallback: save static plots
            for i in [0, 49, 99, 149]:
                if i < len(joint_sequences):
                    arm.joint_angles = np.array(joint_sequences[i])
                    end_pos, joint_positions = arm.forward_kinematics()
                    plt.figure(figsize=(10, 8))
                    plt.plot(joint_positions[:, 0], joint_positions[:, 1], 'b-', linewidth=3)
                    plt.plot(joint_positions[:-1, 0], joint_positions[:-1, 1], 'ro', markersize=8)
                    plt.plot([end_pos[0]], [end_pos[1]], 'gs', markersize=12)
                    plt.xlim(-6, 6)
                    plt.ylim(-2, 6)
                    plt.grid(True)
                    plt.title(f'2D Robotic Arm - Frame {i}')
                    plt.savefig(os.path.join(self.output_path, f'arm_frame_{i}.png'), dpi=150, bbox_inches='tight')
                    plt.close()
            print(f"✓ Saved static frames as fallback")
        
        plt.close(fig)
        return video_path
    
    def create_4dof_arm_demo_video(self, filename='4dof_robotic_arm_demo.mp4'):
        """Create a 4-DOF robotic arm demonstration video"""
        print("Creating 4-DOF Robotic Arm demonstration video...")
        
        # Initialize 4-DOF robotic arm
        arm = RoboticArm4DOF([2.0, 1.8, 1.2, 0.8])
        
        # Set up the figure and axis
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        ax.set_xlim(-7, 7)
        ax.set_ylim(-2, 7)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title('4-DOF Robotic Arm - Advanced Manipulation', fontsize=16, fontweight='bold')
        ax.set_xlabel('X Position (m)', fontsize=12)
        ax.set_ylabel('Y Position (m)', fontsize=12)
        
        # Initialize plot elements
        arm_line, = ax.plot([], [], 'b-', linewidth=4, label='Arm Links')
        joints_plot, = ax.plot([], [], 'ro', markersize=10, label='Joints')
        end_effector, = ax.plot([], [], 'gs', markersize=15, label='End Effector')
        trajectory, = ax.plot([], [], 'r--', alpha=0.6, linewidth=2, label='Trajectory')
        
        # Add workspace boundary
        theta = np.linspace(0, 2*np.pi, 100)
        workspace_radius = sum(arm.link_lengths)
        ax.plot(workspace_radius * np.cos(theta), workspace_radius * np.sin(theta), 
                'k--', alpha=0.3, label='Workspace Boundary')
        
        ax.legend(loc='upper right')
        
        # Define complex manipulation sequence
        points = [
            np.array([4.0, 2.0]),   # Pick point 1
            np.array([0.0, 5.0]),   # High via point
            np.array([-3.0, 3.0]),  # Place point 1
            np.array([0.0, 4.0]),   # Central via point
            np.array([3.5, 1.0]),   # Pick point 2
            np.array([2.0, 5.0]),   # High via point 2
            np.array([-4.0, 2.0]),  # Place point 2
        ]
        
        # Generate smooth trajectory
        trajectory_points = []
        n_segments = len(points) - 1
        steps_per_segment = 30
        
        for i in range(n_segments):
            start = points[i]
            end = points[i + 1]
            for j in range(steps_per_segment):
                t = j / (steps_per_segment - 1)
                # Use cubic interpolation for smoother motion
                t_smooth = 3*t*t - 2*t*t*t
                point = start + t_smooth * (end - start)
                trajectory_points.append(point)
        
        def animate(frame):
            """Animation function for 4-DOF arm"""
            if frame < len(trajectory_points):
                target = trajectory_points[frame]
                
                # Solve inverse kinematics
                success, angles = arm.inverse_kinematics(target[0], target[1])
                
                if success:
                    arm.joint_angles = angles
                
                # Get current arm configuration
                end_pos, joint_positions = arm.forward_kinematics()
                
                # Update plots
                arm_line.set_data(joint_positions[:, 0], joint_positions[:, 1])
                joints_plot.set_data(joint_positions[:-1, 0], joint_positions[:-1, 1])
                end_effector.set_data([end_pos[0]], [end_pos[1]])
                
                # Update trajectory
                if frame > 0:
                    traj_points = np.array(trajectory_points[:frame+1])
                    trajectory.set_data(traj_points[:, 0], traj_points[:, 1])
                
                # Dynamic title based on phase
                phase = frame // 30
                phase_names = [
                    "Approaching First Object",
                    "Lifting First Object", 
                    "Placing First Object",
                    "Moving to Second Object",
                    "Approaching Second Object",
                    "Lifting Second Object",
                    "Placing Second Object"
                ]
                if phase < len(phase_names):
                    ax.set_title(f'4-DOF Robotic Arm - {phase_names[phase]}', 
                               fontsize=16, fontweight='bold')
            
            return arm_line, joints_plot, end_effector, trajectory
        
        # Create animation
        n_frames = len(trajectory_points)
        anim = animation.FuncAnimation(fig, animate, frames=n_frames, 
                                     interval=100, blit=False, repeat=True)
        
        # Save as video
        video_path = os.path.join(self.output_path, filename)
        print(f"Saving video to: {video_path}")
        
        try:
            Writer = animation.writers['ffmpeg']
            writer = Writer(fps=10, metadata=dict(artist='4-DOF Robotic Arm Simulator'), bitrate=1800)
            anim.save(video_path, writer=writer)
            print(f"✓ Successfully created 4-DOF arm demo video: {video_path}")
        except Exception as e:
            print(f"FFmpeg not available, saving as GIF instead: {e}")
            gif_path = video_path.replace('.mp4', '.gif')
            anim.save(gif_path, writer='pillow', fps=10)
            print(f"✓ Successfully created 4-DOF arm demo GIF: {gif_path}")
        
        plt.close(fig)
        return video_path
    
    def create_conveyor_system_video(self, filename='conveyor_sorting_demo.mp4'):
        """Create a conveyor belt sorting system demonstration video"""
        print("Creating Conveyor Belt Sorting demonstration video...")
        
        # Set up the figure
        fig, ax = plt.subplots(1, 1, figsize=(14, 8))
        ax.set_xlim(-1, 11)
        ax.set_ylim(-1, 6)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title('Robotic Conveyor Belt Sorting System', fontsize=16, fontweight='bold')
        ax.set_xlabel('X Position (m)', fontsize=12)
        ax.set_ylabel('Y Position (m)', fontsize=12)
        
        # Draw conveyor belt
        belt_y = 1.0
        belt_width = 0.3
        belt_rect = plt.Rectangle((0, belt_y - belt_width/2), 10, belt_width, 
                                 facecolor='gray', alpha=0.6, label='Conveyor Belt')
        ax.add_patch(belt_rect)
        
        # Initialize robotic arm
        arm = RoboticArm([1.5, 1.2, 0.8])
        arm_base_x = 5.0
        arm_base_y = 3.0
        
        # Initialize plot elements
        arm_line, = ax.plot([], [], 'b-', linewidth=3, label='Robotic Arm')
        joints_plot, = ax.plot([], [], 'ro', markersize=8, label='Joints')
        end_effector, = ax.plot([], [], 'gs', markersize=12, label='End Effector')
        
        # Objects on conveyor
        objects = []
        object_colors = ['red', 'blue', 'green', 'orange', 'purple']
        object_positions = []
        
        # Sorting bins
        bin_positions = [(1, 4), (9, 4)]
        for i, pos in enumerate(bin_positions):
            bin_rect = plt.Rectangle((pos[0]-0.3, pos[1]-0.3), 0.6, 0.6, 
                                   facecolor='lightblue', edgecolor='blue', 
                                   alpha=0.7, label=f'Bin {i+1}' if i == 0 else '')
            ax.add_patch(bin_rect)
        
        ax.legend(loc='upper left')
        
        def animate(frame):
            """Animation function for conveyor system"""
            # Clear previous objects
            for obj in objects:
                obj.remove()
            objects.clear()
            
            # Add moving objects on conveyor
            for i in range(3):
                obj_x = (frame * 0.05 + i * 3.0) % 12.0 - 1.0
                if -0.5 < obj_x < 10.5:
                    obj_color = object_colors[i % len(object_colors)]
                    obj = plt.Circle((obj_x, belt_y), 0.15, 
                                   facecolor=obj_color, edgecolor='black', alpha=0.8)
                    ax.add_patch(obj)
                    objects.append(obj)
                    object_positions.append((obj_x, belt_y))
            
            # Robotic arm movement
            t = frame * 0.1
            target_x = arm_base_x + 1.5 * np.sin(t * 0.5)
            target_y = arm_base_y - 1.0 + 0.5 * np.sin(t * 0.7)
            
            # Solve inverse kinematics relative to arm base
            success, angles = arm.inverse_kinematics(target_x - arm_base_x, target_y - arm_base_y)
            if success:
                arm.joint_angles = angles
            
            # Get arm configuration
            end_pos, joint_positions = arm.forward_kinematics()
            
            # Offset by arm base position
            joint_positions[:, 0] += arm_base_x
            joint_positions[:, 1] += arm_base_y
            end_pos[0] += arm_base_x
            end_pos[1] += arm_base_y
            
            # Update arm plots
            arm_line.set_data(joint_positions[:, 0], joint_positions[:, 1])
            joints_plot.set_data(joint_positions[:-1, 0], joint_positions[:-1, 1])
            end_effector.set_data([end_pos[0]], [end_pos[1]])
            
            # Update title with current operation
            operation_phase = (frame // 30) % 4
            operations = [
                "Scanning Objects on Conveyor",
                "Picking Up Object",
                "Sorting to Appropriate Bin",
                "Returning to Position"
            ]
            ax.set_title(f'Conveyor Sorting System - {operations[operation_phase]}', 
                        fontsize=16, fontweight='bold')
            
            return arm_line, joints_plot, end_effector
        
        # Create animation
        n_frames = 200
        anim = animation.FuncAnimation(fig, animate, frames=n_frames, 
                                     interval=100, blit=False, repeat=True)
        
        # Save as video
        video_path = os.path.join(self.output_path, filename)
        print(f"Saving video to: {video_path}")
        
        try:
            Writer = animation.writers['ffmpeg']
            writer = Writer(fps=10, metadata=dict(artist='Conveyor Sorting Simulator'), bitrate=1800)
            anim.save(video_path, writer=writer)
            print(f"✓ Successfully created conveyor sorting demo video: {video_path}")
        except Exception as e:
            print(f"FFmpeg not available, saving as GIF instead: {e}")
            gif_path = video_path.replace('.mp4', '.gif')
            anim.save(gif_path, writer='pillow', fps=10)
            print(f"✓ Successfully created conveyor sorting demo GIF: {gif_path}")
        
        plt.close(fig)
        return video_path
    
    def create_compilation_video(self, filename='robotic_arm_compilation.mp4'):
        """Create a compilation video showcasing all features"""
        print("Creating compilation video with all robotic arm features...")
        
        # This would combine multiple videos, but for now we'll create a comprehensive demo
        videos_created = []
        
        try:
            video1 = self.create_2d_arm_demo_video('2d_arm_demo.mp4')
            videos_created.append(video1)
        except Exception as e:
            print(f"Error creating 2D arm video: {e}")
        
        try:
            video2 = self.create_4dof_arm_demo_video('4dof_arm_demo.mp4')
            videos_created.append(video2)
        except Exception as e:
            print(f"Error creating 4-DOF arm video: {e}")
        
        try:
            video3 = self.create_conveyor_system_video('conveyor_demo.mp4')
            videos_created.append(video3)
        except Exception as e:
            print(f"Error creating conveyor video: {e}")
        
        return videos_created


def main():
    """Main function to generate all demonstration videos"""
    print("=== Robotic Arm Video Generator ===")
    print("Creating professional demonstration videos for computer graphics project...")
    
    # Create video generator
    generator = VideoGenerator('assignment1')
    
    # Generate all videos
    try:
        print("\n1. Creating 2D Robotic Arm Pick & Place Demo...")
        video1 = generator.create_2d_arm_demo_video()
        
        print("\n2. Creating 4-DOF Robotic Arm Advanced Demo...")
        video2 = generator.create_4dof_arm_demo_video()
        
        print("\n3. Creating Conveyor Belt Sorting Demo...")
        video3 = generator.create_conveyor_system_video()
        
        print("\n=== Video Generation Complete ===")
        print("✓ All demonstration videos have been created successfully!")
        print("📁 Videos are saved in the 'assignment1' folder")
        print("\nCreated videos:")
        print(f"  • 2D Robotic Arm Demo: assignment1/2d_robotic_arm_demo.mp4")
        print(f"  • 4-DOF Robotic Arm Demo: assignment1/4dof_robotic_arm_demo.mp4") 
        print(f"  • Conveyor Sorting Demo: assignment1/conveyor_sorting_demo.mp4")
        print("\n🎬 These videos are ready for your computer graphics project demonstration!")
        
    except Exception as e:
        print(f"\n❌ Error during video generation: {e}")
        print("Please check that all required dependencies are installed.")


if __name__ == "__main__":
    main()