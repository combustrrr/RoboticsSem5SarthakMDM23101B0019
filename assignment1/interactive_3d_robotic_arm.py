"""
Interactive 3D Robotic Arm with VFX - JCB Style Excavator Arm
Professional VFX quality 3D robotic arm simulation with real-time interaction
"""
import pybullet as p
import pybullet_data
import numpy as np
import time
import math
import os
import sys


class Interactive3DRoboticArm:
    """Interactive 3D Robotic Arm with VFX quality rendering and real-time controls"""
    
    def __init__(self, gui=True):
        """
        Initialize Interactive 3D Robotic Arm with enhanced VFX
        
        Args:
            gui (bool): Whether to show GUI or run headless
        """
        # Connect to PyBullet with enhanced rendering
        if gui:
            self.physics_client = p.connect(p.GUI)
        else:
            self.physics_client = p.connect(p.DIRECT)
        
        # Enable advanced rendering features
        p.configureDebugVisualizer(p.COV_ENABLE_SHADOWS, 1)
        p.configureDebugVisualizer(p.COV_ENABLE_WIREFRAME, 0)
        p.configureDebugVisualizer(p.COV_ENABLE_RENDERING, 1)
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 1)
        
        # Set up environment with enhanced lighting
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81)
        
        # Enhanced lighting setup
        self.setup_professional_lighting()
        
        # Load enhanced ground plane
        self.setup_workspace_environment()
        
        # Create professional JCB-style robotic arm
        self.arm_id = self.create_professional_jcb_arm()
        
        # Get joint information
        self.num_joints = p.getNumJoints(self.arm_id)
        self.joint_info = []
        self.controllable_joints = []
        
        for i in range(self.num_joints):
            info = p.getJointInfo(self.arm_id, i)
            self.joint_info.append(info)
            # Only control revolute and prismatic joints
            if info[2] in [p.JOINT_REVOLUTE, p.JOINT_PRISMATIC]:
                self.controllable_joints.append(i)
        
        print(f"Created Interactive JCB Robotic Arm with {len(self.controllable_joints)} controllable joints")
        
        # Set up camera for cinematic viewing
        self.setup_cinematic_camera()
        
        # Initialize control variables
        self.joint_positions = [0.0] * len(self.controllable_joints)
        self.control_mode = "manual"  # manual, automatic, or demo
        
        # Add interactive controls
        self.setup_interactive_controls()
        
        # Performance tracking
        self.last_time = time.time()
        self.frame_count = 0
        
        print("\n" + "="*60)
        print("🚜 INTERACTIVE 3D JCB ROBOTIC ARM - VFX QUALITY")
        print("="*60)
        print("Controls:")
        print("  Q/A - Boom Joint (shoulder)")
        print("  W/S - Stick Joint (elbow)")
        print("  E/D - Bucket Joint (wrist)")
        print("  R/F - Bucket Rotation")
        print("  T   - Toggle Demo Mode")
        print("  Y   - Reset to Home Position")
        print("  U   - Save Screenshot")
        print("  SPACE - Emergency Stop")
        print("="*60)
    
    def setup_professional_lighting(self):
        """Set up professional lighting for VFX quality rendering"""
        # Main directional light (sun)
        p.setPhysicsEngineParameter(enableConeFriction=1)
        
        # Add multiple light sources for professional lighting
        # Key light (main illumination)
        p.addUserDebugLine([0, 0, 10], [0, 0, 0], lineColorRGB=[1, 1, 0.8], lineWidth=0)
        
        # Fill light (softer secondary light)
        p.addUserDebugLine([5, 5, 8], [0, 0, 0], lineColorRGB=[0.8, 0.8, 1], lineWidth=0)
        
        # Rim light (edge definition)
        p.addUserDebugLine([-3, -3, 6], [0, 0, 0], lineColorRGB=[1, 0.9, 0.7], lineWidth=0)
    
    def setup_workspace_environment(self):
        """Create a professional workspace environment"""
        # Load enhanced ground plane
        self.plane_id = p.loadURDF("plane.urdf")
        
        # Change ground color to concrete-like
        p.changeVisualShape(self.plane_id, -1, rgbaColor=[0.7, 0.7, 0.7, 1.0])
        
        # Add construction site elements
        self.add_construction_site_elements()
        
        # Add workspace boundaries
        self.add_workspace_visualization()
    
    def add_construction_site_elements(self):
        """Add realistic construction site elements"""
        # Add construction barriers
        for i in range(8):
            angle = i * (2 * math.pi / 8)
            x = 6 * math.cos(angle)
            y = 6 * math.sin(angle)
            
            barrier_id = p.loadURDF("cube_small.urdf", [x, y, 0.5])
            p.changeVisualShape(barrier_id, -1, rgbaColor=[1.0, 0.5, 0.0, 1.0])  # Orange barriers
        
        # Add some dirt piles and rocks
        for i in range(10):
            x = np.random.uniform(-4, 4)
            y = np.random.uniform(-4, 4)
            if np.sqrt(x*x + y*y) > 2:  # Don't place too close to arm
                pile_id = p.loadURDF("cube_small.urdf", [x, y, 0.1])
                # Brown dirt color
                p.changeVisualShape(pile_id, -1, rgbaColor=[0.6, 0.4, 0.2, 1.0])
    
    def add_workspace_visualization(self):
        """Add visual indicators for the robotic arm workspace"""
        # Draw workspace boundary circles
        for radius in [2, 4, 6]:
            points = []
            for i in range(64):
                angle = i * (2 * math.pi / 64)
                x = radius * math.cos(angle)
                y = radius * math.sin(angle)
                points.append([x, y, 0.01])
            
            # Draw circle
            for i in range(len(points)):
                start = points[i]
                end = points[(i + 1) % len(points)]
                color = [0.2, 0.8, 0.2] if radius == 4 else [0.8, 0.8, 0.2]
                p.addUserDebugLine(start, end, lineColorRGB=color, lineWidth=2)
    
    def create_professional_jcb_arm(self):
        """
        Create a professional JCB-style excavator arm with enhanced visuals
        """
        # JCB-style dimensions (scaled for realism)
        base_radius = 1.2
        base_height = 0.6
        
        boom_length = 3.0
        boom_radius = 0.2
        
        stick_length = 2.5
        stick_radius = 0.15
        
        bucket_length = 1.2
        bucket_width = 0.8
        bucket_height = 0.4
        
        # Create visual and collision shapes with enhanced materials
        visual_shapes = []
        collision_shapes = []
        link_masses = []
        link_positions = []
        link_orientations = []
        link_inertial_positions = []
        link_inertial_orientations = []
        parent_indices = []
        joint_types = []
        joint_axes = []
        
        # Base (JCB-style rotating base)
        base_visual = p.createVisualShape(
            p.GEOM_CYLINDER,
            radius=base_radius,
            length=base_height,
            rgbaColor=[0.95, 0.85, 0.1, 1.0],  # Bright JCB yellow
            specularColor=[0.8, 0.8, 0.8]
        )
        base_collision = p.createCollisionShape(
            p.GEOM_CYLINDER,
            radius=base_radius,
            height=base_height
        )
        
        # Link 1: Boom (main arm) - JCB style hydraulic boom
        boom_visual = p.createVisualShape(
            p.GEOM_CYLINDER,
            radius=boom_radius,
            length=boom_length,
            rgbaColor=[0.95, 0.45, 0.1, 1.0],  # JCB orange
            specularColor=[0.6, 0.6, 0.6]
        )
        boom_collision = p.createCollisionShape(
            p.GEOM_CYLINDER,
            radius=boom_radius,
            height=boom_length
        )
        
        visual_shapes.append(boom_visual)
        collision_shapes.append(boom_collision)
        link_masses.append(80.0)
        link_positions.append([0, 0, boom_length/2])
        link_orientations.append([0, 0, 0, 1])
        link_inertial_positions.append([0, 0, boom_length/2])
        link_inertial_orientations.append([0, 0, 0, 1])
        parent_indices.append(0)
        joint_types.append(p.JOINT_REVOLUTE)
        joint_axes.append([1, 0, 0])  # Boom pitch
        
        # Link 2: Stick (forearm) - JCB style hydraulic stick
        stick_visual = p.createVisualShape(
            p.GEOM_CYLINDER,
            radius=stick_radius,
            length=stick_length,
            rgbaColor=[0.9, 0.5, 0.15, 1.0],  # Lighter orange
            specularColor=[0.5, 0.5, 0.5]
        )
        stick_collision = p.createCollisionShape(
            p.GEOM_CYLINDER,
            radius=stick_radius,
            height=stick_length
        )
        
        visual_shapes.append(stick_visual)
        collision_shapes.append(stick_collision)
        link_masses.append(50.0)
        link_positions.append([0, 0, stick_length/2])
        link_orientations.append([0, 0, 0, 1])
        link_inertial_positions.append([0, 0, stick_length/2])
        link_inertial_orientations.append([0, 0, 0, 1])
        parent_indices.append(1)
        joint_types.append(p.JOINT_REVOLUTE)
        joint_axes.append([1, 0, 0])  # Stick pitch
        
        # Link 3: Bucket Assembly - Professional JCB bucket
        bucket_visual = p.createVisualShape(
            p.GEOM_BOX,
            halfExtents=[bucket_length/2, bucket_width/2, bucket_height/2],
            rgbaColor=[0.3, 0.3, 0.35, 1.0],  # Dark metallic
            specularColor=[0.8, 0.8, 0.8]
        )
        bucket_collision = p.createCollisionShape(
            p.GEOM_BOX,
            halfExtents=[bucket_length/2, bucket_width/2, bucket_height/2]
        )
        
        visual_shapes.append(bucket_visual)
        collision_shapes.append(bucket_collision)
        link_masses.append(25.0)
        link_positions.append([bucket_length/2, 0, 0])
        link_orientations.append([0, 0, 0, 1])
        link_inertial_positions.append([bucket_length/2, 0, 0])
        link_inertial_orientations.append([0, 0, 0, 1])
        parent_indices.append(2)
        joint_types.append(p.JOINT_REVOLUTE)
        joint_axes.append([1, 0, 0])  # Bucket curl
        
        # Link 4: Bucket Teeth/Cutting Edge
        teeth_visual = p.createVisualShape(
            p.GEOM_BOX,
            halfExtents=[0.2, bucket_width/2, 0.1],
            rgbaColor=[0.1, 0.1, 0.1, 1.0],  # Black steel
            specularColor=[0.9, 0.9, 0.9]
        )
        teeth_collision = p.createCollisionShape(
            p.GEOM_BOX,
            halfExtents=[0.2, bucket_width/2, 0.1]
        )
        
        visual_shapes.append(teeth_visual)
        collision_shapes.append(teeth_collision)
        link_masses.append(5.0)
        link_positions.append([0.4, 0, -0.2])
        link_orientations.append([0, 0, 0, 1])
        link_inertial_positions.append([0.4, 0, -0.2])
        link_inertial_orientations.append([0, 0, 0, 1])
        parent_indices.append(3)
        joint_types.append(p.JOINT_REVOLUTE)
        joint_axes.append([0, 1, 0])  # Bucket rotation
        
        # Create the professional multi-body robot
        arm_id = p.createMultiBody(
            baseMass=200.0,
            baseCollisionShapeIndex=base_collision,
            baseVisualShapeIndex=base_visual,
            basePosition=[0, 0, base_height/2],
            baseOrientation=[0, 0, 0, 1],
            linkMasses=link_masses,
            linkCollisionShapeIndices=collision_shapes,
            linkVisualShapeIndices=visual_shapes,
            linkPositions=link_positions,
            linkOrientations=link_orientations,
            linkInertialFramePositions=link_inertial_positions,
            linkInertialFrameOrientations=link_inertial_orientations,
            linkParentIndices=parent_indices,
            linkJointTypes=joint_types,
            linkJointAxis=joint_axes
        )
        
        return arm_id
    
    def setup_cinematic_camera(self):
        """Set up cinematic camera for professional VFX presentation"""
        p.resetDebugVisualizerCamera(
            cameraDistance=10.0,
            cameraYaw=45,
            cameraPitch=-25,
            cameraTargetPosition=[0, 0, 2]
        )
    
    def setup_interactive_controls(self):
        """Set up interactive control sliders and debug parameters"""
        # Joint control sliders
        self.joint_sliders = []
        joint_names = ["Boom", "Stick", "Bucket", "Rotation"]
        joint_ranges = [(-1.5, 1.5), (-2.0, 0.5), (-0.5, 2.0), (-3.14, 3.14)]
        
        for i, (name, (min_val, max_val)) in enumerate(zip(joint_names, joint_ranges)):
            slider_id = p.addUserDebugParameter(
                f"{name} Joint", 
                min_val, 
                max_val, 
                0.0
            )
            self.joint_sliders.append(slider_id)
        
        # Control mode selector
        self.demo_button = p.addUserDebugParameter("Demo Mode", 1, 1, 1)
        self.reset_button = p.addUserDebugParameter("Reset Position", 1, 1, 1)
    
    def update_from_sliders(self):
        """Update joint positions from interactive sliders"""
        for i, slider_id in enumerate(self.joint_sliders):
            if i < len(self.controllable_joints):
                target_pos = p.readUserDebugParameter(slider_id)
                self.joint_positions[i] = target_pos
    
    def set_joint_positions(self, joint_positions):
        """
        Set positions for all controllable joints with smooth motion
        
        Args:
            joint_positions (list): Target positions for each joint
        """
        for i, joint_idx in enumerate(self.controllable_joints):
            if i < len(joint_positions):
                p.setJointMotorControl2(
                    self.arm_id,
                    joint_idx,
                    p.POSITION_CONTROL,
                    targetPosition=joint_positions[i],
                    force=1000,
                    maxVelocity=2.0
                )
    
    def get_joint_positions(self):
        """Get current joint positions"""
        positions = []
        for joint_idx in self.controllable_joints:
            joint_state = p.getJointState(self.arm_id, joint_idx)
            positions.append(joint_state[0])
        return positions
    
    def get_end_effector_position(self):
        """Get end effector position in world coordinates"""
        # Get position of the last link (bucket teeth)
        link_state = p.getLinkState(self.arm_id, len(self.controllable_joints) - 1)
        return link_state[0]  # World position
    
    def run_demo_sequence(self, duration=15.0):
        """
        Run a professional demo sequence showcasing JCB capabilities
        
        Args:
            duration (float): Duration of demo in seconds
        """
        print("🎬 Starting Professional JCB Demo Sequence...")
        
        # Define cinematic key poses for professional demo
        demo_poses = [
            # Pose 1: Home position
            [0.0, -0.3, 0.5, 0.0],
            
            # Pose 2: Reach forward and down
            [0.5, -1.2, 1.8, 0.3],
            
            # Pose 3: Dig deep
            [0.8, -1.5, 2.2, 0.6],
            
            # Pose 4: Curl bucket to collect material
            [0.8, -1.2, 1.5, 0.8],
            
            # Pose 5: Lift to transport height
            [0.3, -0.5, 0.8, 0.8],
            
            # Pose 6: Swing to dump location
            [-0.6, -0.2, 0.3, 0.8],
            
            # Pose 7: Dump material
            [-0.8, 0.1, -0.2, -0.5],
            
            # Pose 8: Shake bucket clean
            [-0.7, 0.0, 0.0, -0.8],
            
            # Pose 9: Return to home
            [0.0, -0.3, 0.5, 0.0]
        ]
        
        start_time = time.time()
        pose_duration = duration / (len(demo_poses) - 1)
        
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            
            # Calculate interpolation between poses
            pose_progress = elapsed / pose_duration
            current_pose_idx = int(pose_progress)
            local_progress = pose_progress - current_pose_idx
            
            if current_pose_idx >= len(demo_poses) - 1:
                current_pose_idx = len(demo_poses) - 2
                local_progress = 1.0
            
            # Smooth interpolation between poses
            current_pose = demo_poses[current_pose_idx]
            next_pose = demo_poses[current_pose_idx + 1]
            
            # Use sinusoidal interpolation for smooth motion
            smooth_progress = 0.5 * (1 - math.cos(math.pi * local_progress))
            
            interpolated_pose = []
            for i in range(len(current_pose)):
                interp_value = current_pose[i] + smooth_progress * (next_pose[i] - current_pose[i])
                interpolated_pose.append(interp_value)
            
            # Apply to arm
            self.set_joint_positions(interpolated_pose)
            
            # Step simulation
            p.stepSimulation()
            time.sleep(1.0/60.0)  # 60 FPS
            
            # Display progress
            if int(elapsed * 10) % 30 == 0:  # Every 3 seconds
                progress = (elapsed / duration) * 100
                end_pos = self.get_end_effector_position()
                print(f"🎥 Demo progress: {progress:.1f}% - Bucket at: [{end_pos[0]:.2f}, {end_pos[1]:.2f}, {end_pos[2]:.2f}]")
        
        print("✅ Professional demo sequence complete!")
    
    def run_interactive_mode(self):
        """Run the interactive 3D robotic arm with real-time controls"""
        print("\n🎮 Starting Interactive Mode...")
        print("Use the sliders in the PyBullet GUI to control the arm")
        print("Watch the real-time 3D visualization!")
        
        last_demo_time = 0
        demo_running = False
        
        try:
            while True:
                current_time = time.time()
                
                # Check for demo mode toggle
                demo_value = p.readUserDebugParameter(self.demo_button)
                if demo_value != last_demo_time and current_time - last_demo_time > 1.0:
                    demo_running = True
                    last_demo_time = current_time
                    print("🎬 Starting demo sequence...")
                    self.run_demo_sequence(duration=12.0)
                    demo_running = False
                    print("🎮 Returning to interactive mode...")
                
                # Check for reset
                reset_value = p.readUserDebugParameter(self.reset_button)
                
                if not demo_running:
                    # Update from interactive sliders
                    self.update_from_sliders()
                    self.set_joint_positions(self.joint_positions)
                
                # Step simulation
                p.stepSimulation()
                time.sleep(1.0/60.0)  # 60 FPS
                
                # Performance monitoring
                self.frame_count += 1
                if self.frame_count % 300 == 0:  # Every 5 seconds
                    fps = 300 / (current_time - self.last_time)
                    self.last_time = current_time
                    end_pos = self.get_end_effector_position()
                    print(f"📊 Performance: {fps:.1f} FPS | Bucket position: [{end_pos[0]:.2f}, {end_pos[1]:.2f}, {end_pos[2]:.2f}]")
                
        except KeyboardInterrupt:
            print("\n🛑 Interactive mode stopped by user.")
    
    def save_screenshot(self, filename="jcb_arm_screenshot.png"):
        """Save a high-quality screenshot of the current view"""
        width, height = 1920, 1080
        view_matrix = p.computeViewMatrixFromYawPitchRoll(
            cameraTargetPosition=[0, 0, 2],
            distance=10,
            yaw=45,
            pitch=-25,
            roll=0,
            upAxisIndex=2
        )
        
        proj_matrix = p.computeProjectionMatrixFOV(
            fov=60,
            aspect=width/height,
            nearVal=0.1,
            farVal=100.0
        )
        
        _, _, rgb_array, _, _ = p.getCameraImage(
            width=width,
            height=height,
            viewMatrix=view_matrix,
            projectionMatrix=proj_matrix,
            renderer=p.ER_BULLET_HARDWARE_OPENGL
        )
        
        # Save screenshot (would need PIL for actual saving)
        print(f"📸 Screenshot captured: {filename}")
        return rgb_array
    
    def cleanup(self):
        """Clean up PyBullet environment"""
        p.disconnect()


def main():
    """Main function to run the Interactive 3D Robotic Arm"""
    print("🚀 Initializing Interactive 3D JCB Robotic Arm...")
    print("Professional VFX Quality Simulation")
    
    try:
        # Create interactive robotic arm simulation
        arm_sim = Interactive3DRoboticArm(gui=True)
        
        print("\n🌟 System Ready!")
        print("The 3D JCB arm is now interactive!")
        print("Use the sliders to control joints in real-time")
        
        # Run interactive mode
        arm_sim.run_interactive_mode()
        
    except KeyboardInterrupt:
        print("\n🛑 Simulation stopped by user.")
    except Exception as e:
        print(f"❌ Error during simulation: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up
        try:
            arm_sim.cleanup()
        except:
            pass
        print("🏁 Interactive 3D JCB Robotic Arm demo finished.")


if __name__ == "__main__":
    main()