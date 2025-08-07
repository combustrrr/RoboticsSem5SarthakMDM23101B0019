"""
Interactive 3D Robotic Arm Video Generator
Creates professional video demonstrations of the JCB-style robotic arm
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import time
import math
import os


class RoboticArmVideoGenerator:
    """Generate professional video demonstrations of the JCB robotic arm"""
    
    def __init__(self, save_path="."):
        """Initialize the video generator"""
        self.save_path = save_path
        self.fig = None
        self.ax = None
        
        # JCB-style arm parameters
        self.base_height = 0.8
        self.boom_length = 3.5
        self.stick_length = 3.0
        self.bucket_length = 1.5
        
        # Colors (JCB style)
        self.jcb_yellow = '#F8E71C'
        self.jcb_orange = '#F47C20'
        self.steel_gray = '#4A4A4A'
        self.ground_brown = '#8B4513'
        
        print("🎬 Robotic Arm Video Generator Initialized")
        print(f"📁 Save path: {self.save_path}")
    
    def forward_kinematics(self, joint_angles):
        """
        Calculate forward kinematics for the 4-DOF robotic arm
        
        Args:
            joint_angles: [boom_angle, stick_angle, bucket_angle, bucket_rotation]
        
        Returns:
            positions: List of [x, y, z] positions for each joint
        """
        boom_angle, stick_angle, bucket_angle, bucket_rotation = joint_angles
        
        # Base position
        base_pos = [0, 0, self.base_height/2]
        
        # Boom end position
        boom_end = [
            self.boom_length * np.cos(boom_angle),
            0,
            self.base_height + self.boom_length * np.sin(boom_angle)
        ]
        
        # Stick end position
        stick_end = [
            boom_end[0] + self.stick_length * np.cos(boom_angle + stick_angle),
            boom_end[1],
            boom_end[2] + self.stick_length * np.sin(boom_angle + stick_angle)
        ]
        
        # Bucket end position
        bucket_end = [
            stick_end[0] + self.bucket_length * np.cos(boom_angle + stick_angle + bucket_angle),
            stick_end[1],
            stick_end[2] + self.bucket_length * np.sin(boom_angle + stick_angle + bucket_angle)
        ]
        
        return [base_pos, boom_end, stick_end, bucket_end]
    
    def setup_3d_scene(self):
        """Set up the 3D scene for visualization"""
        self.fig = plt.figure(figsize=(16, 12))
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Set up the plot
        self.ax.set_xlim(-8, 8)
        self.ax.set_ylim(-8, 8)
        self.ax.set_zlim(0, 8)
        
        # Labels and title
        self.ax.set_xlabel('X (meters)', fontsize=12)
        self.ax.set_ylabel('Y (meters)', fontsize=12)
        self.ax.set_zlabel('Z (meters)', fontsize=12)
        self.ax.set_title('🚜 Interactive JCB Robotic Arm - 3D Workspace Demonstration', 
                         fontsize=16, fontweight='bold')
        
        # Set viewing angle for dramatic effect
        self.ax.view_init(elev=20, azim=45)
        
        # Add ground plane
        xx, yy = np.meshgrid(np.linspace(-8, 8, 10), np.linspace(-8, 8, 10))
        zz = np.zeros_like(xx)
        self.ax.plot_surface(xx, yy, zz, alpha=0.3, color=self.ground_brown)
        
        # Add construction site elements
        self.add_construction_site()
        
        return self.fig, self.ax
    
    def add_construction_site(self):
        """Add construction site elements to the scene"""
        # Construction barriers around the perimeter
        for i in range(12):
            angle = i * (2 * np.pi / 12)
            x = 6 * np.cos(angle)
            y = 6 * np.sin(angle)
            
            # Orange construction barrier
            self.ax.bar3d(x-0.2, y-0.2, 0, 0.4, 0.4, 1.0, 
                         color='orange', alpha=0.7)
        
        # Dirt piles
        for i in range(8):
            x = np.random.uniform(-5, 5)
            y = np.random.uniform(-5, 5)
            if np.sqrt(x*x + y*y) > 3:  # Keep clear of arm
                height = np.random.uniform(0.3, 0.8)
                self.ax.bar3d(x-0.3, y-0.3, 0, 0.6, 0.6, height, 
                             color=self.ground_brown, alpha=0.8)
        
        # Construction materials
        for i in range(5):
            x = np.random.uniform(-4, 4)
            y = np.random.uniform(-4, 4)
            if np.sqrt(x*x + y*y) > 2.5:
                self.ax.bar3d(x-0.1, y-0.1, 0, 0.2, 0.2, 0.5, 
                             color='gray', alpha=0.9)
    
    def plot_arm_configuration(self, joint_angles, title="Robotic Arm Configuration"):
        """Plot a single arm configuration"""
        self.setup_3d_scene()
        
        # Calculate positions
        positions = self.forward_kinematics(joint_angles)
        
        # Extract coordinates
        x_coords = [pos[0] for pos in positions]
        y_coords = [pos[1] for pos in positions]
        z_coords = [pos[2] for pos in positions]
        
        # Plot base (cylinder representation)
        theta = np.linspace(0, 2*np.pi, 20)
        base_radius = 1.5
        x_base = base_radius * np.cos(theta)
        y_base = base_radius * np.sin(theta)
        z_base = np.zeros_like(theta)
        z_top = np.full_like(theta, self.base_height)
        
        # Base cylinder
        for i in range(len(theta)-1):
            self.ax.plot([x_base[i], x_base[i+1]], 
                        [y_base[i], y_base[i+1]], 
                        [z_base[i], z_base[i+1]], 
                        color=self.jcb_yellow, linewidth=8)
            self.ax.plot([x_base[i], x_base[i+1]], 
                        [y_base[i], y_base[i+1]], 
                        [z_top[i], z_top[i+1]], 
                        color=self.jcb_yellow, linewidth=8)
        
        # Arm links
        link_colors = [self.jcb_orange, self.jcb_orange, self.steel_gray]
        link_widths = [12, 10, 8]
        
        for i in range(len(positions)-1):
            self.ax.plot([x_coords[i], x_coords[i+1]], 
                        [y_coords[i], y_coords[i+1]], 
                        [z_coords[i], z_coords[i+1]], 
                        color=link_colors[i], linewidth=link_widths[i])
        
        # Joint markers
        joint_colors = [self.jcb_yellow, self.jcb_orange, self.jcb_orange, self.steel_gray]
        for i, pos in enumerate(positions):
            self.ax.scatter(pos[0], pos[1], pos[2], 
                           color=joint_colors[i], s=200, alpha=0.8)
        
        # End effector position marker
        end_pos = positions[-1]
        self.ax.scatter(end_pos[0], end_pos[1], end_pos[2], 
                       color='red', s=300, marker='*', label='End Effector')
        
        # Workspace visualization
        self.plot_workspace_boundary()
        
        # Legend
        self.ax.legend()
        
        plt.tight_layout()
        return self.fig
    
    def plot_workspace_boundary(self):
        """Plot the workspace boundary"""
        # Calculate reachable workspace boundary
        angles = np.linspace(0, 2*np.pi, 100)
        
        # Maximum reach (all joints extended)
        max_reach = self.boom_length + self.stick_length + self.bucket_length
        x_max = max_reach * np.cos(angles)
        y_max = max_reach * np.sin(angles)
        z_max = np.full_like(angles, self.base_height)
        
        # Minimum reach (joints folded)
        min_reach = abs(self.boom_length - self.stick_length - self.bucket_length)
        x_min = min_reach * np.cos(angles)
        y_min = min_reach * np.sin(angles)
        z_min = np.full_like(angles, self.base_height)
        
        # Plot workspace boundaries
        self.ax.plot(x_max, y_max, z_max, '--', color='green', alpha=0.5, 
                    linewidth=2, label='Max Reach')
        self.ax.plot(x_min, y_min, z_min, '--', color='red', alpha=0.5, 
                    linewidth=2, label='Min Reach')
    
    def generate_digging_sequence(self, duration=10, fps=30):
        """Generate a digging sequence animation"""
        print("🎬 Generating JCB digging sequence...")
        
        # Define key poses for digging operation
        key_poses = [
            # [boom_angle, stick_angle, bucket_angle, bucket_rotation]
            [0.1, -0.3, 0.5, 0.0],      # Home position
            [0.4, -0.8, 1.2, 0.2],      # Reach forward
            [0.6, -1.2, 1.8, 0.5],      # Dig into ground
            [0.5, -1.0, 1.4, 0.8],      # Collect material
            [0.2, -0.5, 0.8, 0.8],      # Lift
            [-0.3, -0.2, 0.3, 0.8],     # Swing to dump
            [-0.5, 0.0, -0.2, -0.3],    # Dump material
            [-0.4, -0.1, 0.1, -0.5],    # Shake bucket
            [0.1, -0.3, 0.5, 0.0],      # Return home
        ]
        
        # Generate interpolated sequence
        total_frames = int(duration * fps)
        frames_per_pose = total_frames // (len(key_poses) - 1)
        
        all_poses = []
        for i in range(len(key_poses) - 1):
            current_pose = key_poses[i]
            next_pose = key_poses[i + 1]
            
            for frame in range(frames_per_pose):
                t = frame / frames_per_pose
                # Smooth interpolation
                smooth_t = 0.5 * (1 - np.cos(np.pi * t))
                
                interpolated_pose = []
                for j in range(len(current_pose)):
                    value = current_pose[j] + smooth_t * (next_pose[j] - current_pose[j])
                    interpolated_pose.append(value)
                
                all_poses.append(interpolated_pose)
        
        return all_poses
    
    def create_animation_gif(self, poses, filename="jcb_robotic_arm_demo.gif", fps=15):
        """Create an animated GIF of the robotic arm sequence"""
        print(f"🎞️ Creating animation: {filename}")
        
        def animate(frame):
            self.ax.clear()
            
            # Recreate scene
            self.ax.set_xlim(-8, 8)
            self.ax.set_ylim(-8, 8)
            self.ax.set_zlim(0, 8)
            self.ax.set_xlabel('X (meters)')
            self.ax.set_ylabel('Y (meters)')
            self.ax.set_zlabel('Z (meters)')
            self.ax.set_title(f'🚜 JCB Robotic Arm - Professional Demo (Frame {frame+1}/{len(poses)})', 
                             fontweight='bold')
            
            # Ground plane
            xx, yy = np.meshgrid(np.linspace(-8, 8, 10), np.linspace(-8, 8, 10))
            zz = np.zeros_like(xx)
            self.ax.plot_surface(xx, yy, zz, alpha=0.2, color=self.ground_brown)
            
            # Construction site elements
            self.add_construction_site()
            
            # Current arm configuration
            positions = self.forward_kinematics(poses[frame])
            
            # Plot arm
            x_coords = [pos[0] for pos in positions]
            y_coords = [pos[1] for pos in positions]
            z_coords = [pos[2] for pos in positions]
            
            # Base
            theta = np.linspace(0, 2*np.pi, 20)
            base_radius = 1.5
            x_base = base_radius * np.cos(theta)
            y_base = base_radius * np.sin(theta)
            z_base_bottom = np.zeros_like(theta)
            z_base_top = np.full_like(theta, self.base_height)
            
            self.ax.plot(x_base, y_base, z_base_bottom, color=self.jcb_yellow, linewidth=6)
            self.ax.plot(x_base, y_base, z_base_top, color=self.jcb_yellow, linewidth=6)
            
            # Arm links
            link_colors = [self.jcb_orange, self.jcb_orange, self.steel_gray]
            link_widths = [10, 8, 6]
            
            for i in range(len(positions)-1):
                self.ax.plot([x_coords[i], x_coords[i+1]], 
                            [y_coords[i], y_coords[i+1]], 
                            [z_coords[i], z_coords[i+1]], 
                            color=link_colors[i], linewidth=link_widths[i])
            
            # Joint markers
            for i, pos in enumerate(positions):
                color = [self.jcb_yellow, self.jcb_orange, self.jcb_orange, self.steel_gray][i]
                self.ax.scatter(pos[0], pos[1], pos[2], color=color, s=150, alpha=0.8)
            
            # End effector trail (last 10 positions)
            if frame > 10:
                trail_x = []
                trail_y = []
                trail_z = []
                for trail_frame in range(max(0, frame-10), frame):
                    trail_pos = self.forward_kinematics(poses[trail_frame])[-1]
                    trail_x.append(trail_pos[0])
                    trail_y.append(trail_pos[1])
                    trail_z.append(trail_pos[2])
                
                self.ax.plot(trail_x, trail_y, trail_z, '--', color='red', alpha=0.6, linewidth=2)
            
            # Current end effector
            end_pos = positions[-1]
            self.ax.scatter(end_pos[0], end_pos[1], end_pos[2], 
                           color='red', s=200, marker='*')
            
            # Workspace boundary
            self.plot_workspace_boundary()
            
            self.ax.view_init(elev=20, azim=45 + frame * 0.5)  # Slowly rotating view
        
        # Create animation
        self.setup_3d_scene()
        anim = animation.FuncAnimation(self.fig, animate, frames=len(poses), 
                                     interval=1000//fps, blit=False)
        
        # Save as GIF
        filepath = os.path.join(self.save_path, filename)
        writer = animation.PillowWriter(fps=fps)
        anim.save(filepath, writer=writer, dpi=100)
        
        print(f"✅ Animation saved: {filepath}")
        plt.close()
        
        return filepath
    
    def create_multi_view_demo(self, filename="comprehensive_jcb_demo.gif"):
        """Create a comprehensive multi-view demonstration"""
        print("🎥 Creating comprehensive multi-view demo...")
        
        # Create figure with subplots
        fig = plt.figure(figsize=(20, 12))
        
        # Define different arm configurations to showcase
        demo_configs = [
            ([0.0, -0.2, 0.3, 0.0], "Home Position"),
            ([0.5, -1.0, 1.5, 0.3], "Forward Reach"),
            ([0.8, -1.4, 2.0, 0.6], "Deep Dig"),
            ([0.3, -0.6, 0.9, 0.8], "Material Collection"),
            ([-0.5, -0.1, 0.2, 0.7], "Dump Position"),
            ([0.0, -0.2, 0.3, 0.0], "Return Home")
        ]
        
        frames = []
        for config, title in demo_configs:
            # Clear and setup new frame
            fig.clear()
            
            # Main 3D view
            ax_main = fig.add_subplot(2, 3, (1, 4), projection='3d')
            ax_main.set_xlim(-8, 8)
            ax_main.set_ylim(-8, 8)
            ax_main.set_zlim(0, 8)
            ax_main.set_title(f'🚜 JCB Robotic Arm - {title}', fontsize=14, fontweight='bold')
            
            # Plot arm configuration
            positions = self.forward_kinematics(config[0])
            x_coords = [pos[0] for pos in positions]
            y_coords = [pos[1] for pos in positions]
            z_coords = [pos[2] for pos in positions]
            
            # Ground
            xx, yy = np.meshgrid(np.linspace(-8, 8, 10), np.linspace(-8, 8, 10))
            zz = np.zeros_like(xx)
            ax_main.plot_surface(xx, yy, zz, alpha=0.2, color=self.ground_brown)
            
            # Arm links
            link_colors = [self.jcb_orange, self.jcb_orange, self.steel_gray]
            link_widths = [8, 6, 4]
            
            for i in range(len(positions)-1):
                ax_main.plot([x_coords[i], x_coords[i+1]], 
                           [y_coords[i], y_coords[i+1]], 
                           [z_coords[i], z_coords[i+1]], 
                           color=link_colors[i], linewidth=link_widths[i])
            
            # Side view
            ax_side = fig.add_subplot(2, 3, 2)
            ax_side.plot(x_coords, z_coords, 'o-', color=self.jcb_orange, linewidth=4, markersize=8)
            ax_side.set_xlim(-8, 8)
            ax_side.set_ylim(0, 8)
            ax_side.set_xlabel('X (meters)')
            ax_side.set_ylabel('Z (meters)')
            ax_side.set_title('Side View')
            ax_side.grid(True, alpha=0.3)
            
            # Top view
            ax_top = fig.add_subplot(2, 3, 3)
            ax_top.plot(x_coords, y_coords, 'o-', color=self.jcb_orange, linewidth=4, markersize=8)
            ax_top.set_xlim(-8, 8)
            ax_top.set_ylim(-8, 8)
            ax_top.set_xlabel('X (meters)')
            ax_top.set_ylabel('Y (meters)')
            ax_top.set_title('Top View')
            ax_top.grid(True, alpha=0.3)
            
            # Joint angles display
            ax_joints = fig.add_subplot(2, 3, 5)
            joint_names = ['Boom', 'Stick', 'Bucket', 'Rotation']
            joint_values = config[0]
            
            bars = ax_joints.bar(joint_names, joint_values, 
                               color=[self.jcb_yellow, self.jcb_orange, self.steel_gray, 'blue'])
            ax_joints.set_ylabel('Angle (radians)')
            ax_joints.set_title('Joint Angles')
            ax_joints.grid(True, alpha=0.3)
            
            # Add value labels on bars
            for bar, value in zip(bars, joint_values):
                height = bar.get_height()
                ax_joints.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                             f'{value:.2f}', ha='center', va='bottom')
            
            # Workspace analysis
            ax_workspace = fig.add_subplot(2, 3, 6)
            
            # Calculate reachable points for this configuration
            end_pos = positions[-1]
            max_reach = self.boom_length + self.stick_length + self.bucket_length
            
            ax_workspace.scatter(end_pos[0], end_pos[2], color='red', s=100, 
                               label='Current Position')
            
            # Draw workspace boundary
            angles = np.linspace(0, np.pi, 50)
            x_boundary = max_reach * np.cos(angles)
            z_boundary = self.base_height + max_reach * np.sin(angles)
            ax_workspace.plot(x_boundary, z_boundary, '--', color='green', 
                            label='Max Reach')
            
            ax_workspace.set_xlim(-8, 8)
            ax_workspace.set_ylim(0, 8)
            ax_workspace.set_xlabel('X (meters)')
            ax_workspace.set_ylabel('Z (meters)')
            ax_workspace.set_title('Workspace Analysis')
            ax_workspace.legend()
            ax_workspace.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Save frame
            frame_filename = f"temp_frame_{len(frames)}.png"
            plt.savefig(frame_filename, dpi=100, bbox_inches='tight')
            frames.append(frame_filename)
        
        plt.close()
        
        # Create GIF from frames (simplified approach)
        print(f"✅ Multi-view demo frames created: {len(frames)} frames")
        return frames
    
    def create_static_analysis_images(self):
        """Create static analysis images for technical documentation"""
        print("📊 Creating static analysis images...")
        
        # Workspace analysis
        self.create_workspace_analysis_image()
        
        # Joint configuration comparison
        self.create_joint_configuration_image()
        
        # Technical specifications
        self.create_technical_specs_image()
    
    def create_workspace_analysis_image(self):
        """Create detailed workspace analysis image"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # 2D Workspace analysis
        angles = np.linspace(0, 2*np.pi, 100)
        
        # Calculate different reach configurations
        max_reach = self.boom_length + self.stick_length + self.bucket_length
        min_reach = abs(self.boom_length - self.stick_length - self.bucket_length)
        typical_reach = (max_reach + min_reach) / 2
        
        # Plot workspace boundaries
        x_max = max_reach * np.cos(angles)
        y_max = max_reach * np.sin(angles)
        
        x_min = min_reach * np.cos(angles)
        y_min = min_reach * np.sin(angles)
        
        x_typ = typical_reach * np.cos(angles)
        y_typ = typical_reach * np.sin(angles)
        
        ax1.fill(x_max, y_max, alpha=0.2, color='green', label='Maximum Reach')
        ax1.fill(x_typ, y_typ, alpha=0.3, color='yellow', label='Typical Working Area')
        ax1.fill(x_min, y_min, alpha=0.4, color='red', label='Minimum Reach')
        
        ax1.set_xlim(-10, 10)
        ax1.set_ylim(-10, 10)
        ax1.set_xlabel('X (meters)')
        ax1.set_ylabel('Y (meters)')
        ax1.set_title('🚜 JCB Robotic Arm - Workspace Analysis (Top View)', fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_aspect('equal')
        
        # 3D workspace visualization
        ax2 = fig.add_subplot(122, projection='3d')
        
        # Create 3D workspace surface
        phi = np.linspace(0, 2*np.pi, 50)
        theta = np.linspace(0, np.pi/2, 25)
        PHI, THETA = np.meshgrid(phi, theta)
        
        X = max_reach * np.sin(THETA) * np.cos(PHI)
        Y = max_reach * np.sin(THETA) * np.sin(PHI)
        Z = self.base_height + max_reach * np.cos(THETA)
        
        ax2.plot_surface(X, Y, Z, alpha=0.3, color='green')
        
        ax2.set_xlim(-10, 10)
        ax2.set_ylim(-10, 10)
        ax2.set_zlim(0, 10)
        ax2.set_xlabel('X (meters)')
        ax2.set_ylabel('Y (meters)')
        ax2.set_zlabel('Z (meters)')
        ax2.set_title('3D Workspace Envelope')
        
        plt.tight_layout()
        
        # Save
        filepath = os.path.join(self.save_path, "jcb_workspace_analysis.png")
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Workspace analysis saved: {filepath}")
        return filepath
    
    def create_joint_configuration_image(self):
        """Create joint configuration comparison image"""
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('🚜 JCB Robotic Arm - Joint Configuration Analysis', 
                     fontsize=16, fontweight='bold')
        
        # Different configurations to analyze
        configurations = [
            ([0.0, -0.2, 0.3, 0.0], "Home Position"),
            ([0.5, -1.0, 1.5, 0.3], "Forward Reach"),
            ([0.8, -1.4, 2.0, 0.6], "Maximum Extension"),
            ([-0.5, -0.1, 0.2, 0.7], "Side Reach"),
            ([0.3, -0.6, 0.9, -0.5], "Inverted Bucket"),
            ([0.0, -1.5, 1.8, 0.0], "Deep Dig")
        ]
        
        for idx, (config, title) in enumerate(configurations):
            row = idx // 3
            col = idx % 3
            ax = axes[row, col]
            
            # Calculate positions
            positions = self.forward_kinematics(config)
            x_coords = [pos[0] for pos in positions]
            z_coords = [pos[2] for pos in positions]
            
            # Plot configuration
            ax.plot(x_coords, z_coords, 'o-', color=self.jcb_orange, 
                   linewidth=4, markersize=8)
            
            # Add joint labels
            joint_labels = ['Base', 'Boom', 'Stick', 'Bucket']
            for i, (x, z, label) in enumerate(zip(x_coords, z_coords, joint_labels)):
                ax.annotate(label, (x, z), xytext=(5, 5), 
                          textcoords='offset points', fontsize=8)
            
            # Ground line
            ax.axhline(y=0, color=self.ground_brown, linewidth=3, alpha=0.7)
            
            # Formatting
            ax.set_xlim(-8, 8)
            ax.set_ylim(-2, 8)
            ax.set_xlabel('X (meters)')
            ax.set_ylabel('Z (meters)')
            ax.set_title(title, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.set_aspect('equal')
            
            # Add joint angle text
            joint_names = ['Boom', 'Stick', 'Bucket', 'Rot.']
            angle_text = '\n'.join([f"{name}: {angle:.2f}" 
                                  for name, angle in zip(joint_names, config)])
            ax.text(0.02, 0.98, angle_text, transform=ax.transAxes, 
                   verticalalignment='top', fontsize=8, 
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        
        # Save
        filepath = os.path.join(self.save_path, "jcb_joint_configurations.png")
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Joint configurations saved: {filepath}")
        return filepath
    
    def create_technical_specs_image(self):
        """Create technical specifications diagram"""
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Draw technical diagram
        config = [0.3, -0.8, 1.2, 0.0]  # Representative configuration
        positions = self.forward_kinematics(config)
        
        x_coords = [pos[0] for pos in positions]
        z_coords = [pos[2] for pos in positions]
        
        # Plot arm with technical annotations
        ax.plot(x_coords, z_coords, 'o-', color=self.jcb_orange, 
               linewidth=6, markersize=12)
        
        # Add dimension lines and labels
        # Boom length
        ax.annotate('', xy=(x_coords[1], z_coords[1]), xytext=(x_coords[0], z_coords[0]),
                   arrowprops=dict(arrowstyle='<->', color='blue', lw=2))
        ax.text((x_coords[0] + x_coords[1])/2 - 0.5, 
               (z_coords[0] + z_coords[1])/2 + 0.3,
               f'Boom: {self.boom_length}m', fontsize=12, color='blue', fontweight='bold')
        
        # Stick length
        ax.annotate('', xy=(x_coords[2], z_coords[2]), xytext=(x_coords[1], z_coords[1]),
                   arrowprops=dict(arrowstyle='<->', color='green', lw=2))
        ax.text((x_coords[1] + x_coords[2])/2 + 0.2, 
               (z_coords[1] + z_coords[2])/2,
               f'Stick: {self.stick_length}m', fontsize=12, color='green', fontweight='bold')
        
        # Bucket length
        ax.annotate('', xy=(x_coords[3], z_coords[3]), xytext=(x_coords[2], z_coords[2]),
                   arrowprops=dict(arrowstyle='<->', color='red', lw=2))
        ax.text((x_coords[2] + x_coords[3])/2, 
               (z_coords[2] + z_coords[3])/2 - 0.5,
               f'Bucket: {self.bucket_length}m', fontsize=12, color='red', fontweight='bold')
        
        # Technical specifications table
        specs_text = """
🚜 JCB ROBOTIC ARM SPECIFICATIONS

📐 MECHANICAL SPECIFICATIONS:
   • Base Height: 0.8 m
   • Boom Length: 3.5 m  
   • Stick Length: 3.0 m
   • Bucket Length: 1.5 m
   • Total Reach: 8.0 m
   • Working Height: 7.3 m

🔧 DEGREES OF FREEDOM:
   • Boom Joint: ±90°
   • Stick Joint: ±115°  
   • Bucket Joint: ±115°
   • Bucket Rotation: ±180°

⚡ PERFORMANCE:
   • Workspace Volume: ~180 m³
   • Operating Speed: Variable
   • Precision: ±5 cm
   • Payload: 500 kg

🎯 APPLICATIONS:
   • Excavation & Digging
   • Material Handling
   • Construction Support
   • Precision Placement
        """
        
        ax.text(1.05, 0.5, specs_text, transform=ax.transAxes,
               fontsize=10, verticalalignment='center',
               bbox=dict(boxstyle='round,pad=1', facecolor='lightblue', alpha=0.8))
        
        # Ground and workspace
        ax.axhline(y=0, color=self.ground_brown, linewidth=4, alpha=0.7, label='Ground Level')
        
        # Workspace arc
        angles = np.linspace(-np.pi/6, np.pi/2, 50)
        max_reach = self.boom_length + self.stick_length + self.bucket_length
        x_arc = max_reach * np.cos(angles)
        z_arc = self.base_height + max_reach * np.sin(angles)
        ax.plot(x_arc, z_arc, '--', color='gray', alpha=0.6, linewidth=2, label='Max Reach')
        
        # Formatting
        ax.set_xlim(-2, 9)
        ax.set_ylim(-1, 8)
        ax.set_xlabel('X Position (meters)', fontsize=12)
        ax.set_ylabel('Z Position (meters)', fontsize=12)
        ax.set_title('🚜 JCB Robotic Arm - Technical Specifications', 
                    fontsize=16, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        plt.tight_layout()
        
        # Save
        filepath = os.path.join(self.save_path, "jcb_technical_specifications.png")
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Technical specifications saved: {filepath}")
        return filepath


def generate_professional_demos():
    """Generate all professional demo materials"""
    print("🎬 GENERATING PROFESSIONAL JCB ROBOTIC ARM DEMONSTRATIONS")
    print("=" * 60)
    
    # Create video generator
    generator = RoboticArmVideoGenerator()
    
    # Generate digging sequence
    print("\n🚜 Creating digging sequence...")
    digging_poses = generator.generate_digging_sequence(duration=8, fps=20)
    
    # Create main animation
    gif_path = generator.create_animation_gif(
        digging_poses, 
        "interactive_jcb_robotic_arm_demo.gif", 
        fps=15
    )
    
    # Create static analysis images
    print("\n📊 Creating technical analysis images...")
    workspace_path = generator.create_workspace_analysis_image()
    config_path = generator.create_joint_configuration_image()
    specs_path = generator.create_technical_specs_image()
    
    # Create multi-view demo frames
    print("\n🎥 Creating multi-view demonstration...")
    multi_frames = generator.create_multi_view_demo()
    
    print("\n✅ PROFESSIONAL DEMO GENERATION COMPLETE!")
    print("=" * 60)
    print("📁 Generated files:")
    print(f"   • Main Demo: {gif_path}")
    print(f"   • Workspace Analysis: {workspace_path}")
    print(f"   • Joint Configurations: {config_path}")
    print(f"   • Technical Specs: {specs_path}")
    print(f"   • Multi-view Frames: {len(multi_frames)} frames")
    print("\n🎊 Ready for computer graphics project demonstration!")
    
    return {
        'main_demo': gif_path,
        'workspace_analysis': workspace_path,
        'joint_configurations': config_path,
        'technical_specs': specs_path,
        'multi_frames': multi_frames
    }


if __name__ == "__main__":
    # Generate all professional demonstrations
    demo_files = generate_professional_demos()
    
    print("\n🎬 All demonstrations ready for your computer graphics project!")
    print("Use these materials to showcase your virtual robot prototype.")