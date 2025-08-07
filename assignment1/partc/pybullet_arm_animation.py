"""
3D Robotic Arm Animation using PyBullet
Creates a realistic JCB-style robotic arm with 3D visualization and animation
"""
import pybullet as p
import pybullet_data
import numpy as np
import time
import math


class PyBulletRoboticArm:
    """3D Robotic Arm simulation using PyBullet physics engine"""
    
    def __init__(self, gui=True):
        """
        Initialize PyBullet environment and create robotic arm
        
        Args:
            gui (bool): Whether to show GUI or run headless
        """
        # Connect to PyBullet
        if gui:
            self.physics_client = p.connect(p.GUI)
        else:
            self.physics_client = p.connect(p.DIRECT)
        
        # Set up environment
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81)
        
        # Load ground plane
        self.plane_id = p.loadURDF("plane.urdf")
        
        # Create JCB-style robotic arm
        self.arm_id = self.create_jcb_style_arm()
        
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
        
        print(f"Created robotic arm with {len(self.controllable_joints)} controllable joints")
        
        # Set camera position for better viewing
        self.setup_camera()
        
    def create_jcb_style_arm(self):
        """
        Create a JCB-style excavator arm using primitive shapes
        """
        # Base dimensions (like JCB base)
        base_radius = 0.8
        base_height = 0.4
        
        # Arm segment dimensions (like JCB arm segments)
        boom_length = 2.5
        boom_radius = 0.15
        
        stick_length = 2.0
        stick_radius = 0.12
        
        bucket_length = 1.0
        bucket_radius = 0.1
        
        # Create visual and collision shapes
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
        
        # Base (fixed)
        base_visual = p.createVisualShape(
            p.GEOM_CYLINDER,
            radius=base_radius,
            length=base_height,
            rgbaColor=[0.7, 0.7, 0.1, 1.0]  # Yellow like JCB
        )
        base_collision = p.createCollisionShape(
            p.GEOM_CYLINDER,
            radius=base_radius,
            height=base_height
        )
        
        # Link 1: Boom (main arm)
        boom_visual = p.createVisualShape(
            p.GEOM_CYLINDER,
            radius=boom_radius,
            length=boom_length,
            rgbaColor=[0.8, 0.4, 0.1, 1.0]  # Orange
        )
        boom_collision = p.createCollisionShape(
            p.GEOM_CYLINDER,
            radius=boom_radius,
            height=boom_length
        )
        
        visual_shapes.append(boom_visual)
        collision_shapes.append(boom_collision)
        link_masses.append(50.0)
        link_positions.append([0, 0, boom_length/2])
        link_orientations.append([0, 0, 0, 1])
        link_inertial_positions.append([0, 0, boom_length/2])
        link_inertial_orientations.append([0, 0, 0, 1])
        parent_indices.append(0)
        joint_types.append(p.JOINT_REVOLUTE)
        joint_axes.append([1, 0, 0])  # Rotate around X-axis
        
        # Link 2: Stick (forearm)
        stick_visual = p.createVisualShape(
            p.GEOM_CYLINDER,
            radius=stick_radius,
            length=stick_length,
            rgbaColor=[0.9, 0.5, 0.1, 1.0]  # Lighter orange
        )
        stick_collision = p.createCollisionShape(
            p.GEOM_CYLINDER,
            radius=stick_radius,
            height=stick_length
        )
        
        visual_shapes.append(stick_visual)
        collision_shapes.append(stick_collision)
        link_masses.append(30.0)
        link_positions.append([0, 0, stick_length/2])
        link_orientations.append([0, 0, 0, 1])
        link_inertial_positions.append([0, 0, stick_length/2])
        link_inertial_orientations.append([0, 0, 0, 1])
        parent_indices.append(1)
        joint_types.append(p.JOINT_REVOLUTE)
        joint_axes.append([1, 0, 0])  # Rotate around X-axis
        
        # Link 3: Bucket/End Effector
        bucket_visual = p.createVisualShape(
            p.GEOM_BOX,
            halfExtents=[bucket_length/2, 0.3, 0.2],
            rgbaColor=[0.3, 0.3, 0.3, 1.0]  # Gray bucket
        )
        bucket_collision = p.createCollisionShape(
            p.GEOM_BOX,
            halfExtents=[bucket_length/2, 0.3, 0.2]
        )
        
        visual_shapes.append(bucket_visual)
        collision_shapes.append(bucket_collision)
        link_masses.append(15.0)
        link_positions.append([bucket_length/2, 0, 0])
        link_orientations.append([0, 0, 0, 1])
        link_inertial_positions.append([bucket_length/2, 0, 0])
        link_inertial_orientations.append([0, 0, 0, 1])
        parent_indices.append(2)
        joint_types.append(p.JOINT_REVOLUTE)
        joint_axes.append([1, 0, 0])  # Rotate around X-axis
        
        # Link 4: Bucket rotation
        bucket_tip_visual = p.createVisualShape(
            p.GEOM_BOX,
            halfExtents=[0.1, 0.2, 0.1],
            rgbaColor=[0.2, 0.2, 0.2, 1.0]  # Dark gray
        )
        bucket_tip_collision = p.createCollisionShape(
            p.GEOM_BOX,
            halfExtents=[0.1, 0.2, 0.1]
        )
        
        visual_shapes.append(bucket_tip_visual)
        collision_shapes.append(bucket_tip_collision)
        link_masses.append(5.0)
        link_positions.append([0.3, 0, 0])
        link_orientations.append([0, 0, 0, 1])
        link_inertial_positions.append([0.3, 0, 0])
        link_inertial_orientations.append([0, 0, 0, 1])
        parent_indices.append(3)
        joint_types.append(p.JOINT_REVOLUTE)
        joint_axes.append([0, 1, 0])  # Rotate around Y-axis
        
        # Create the multi-body robot
        arm_id = p.createMultiBody(
            baseMass=100.0,
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
    
    def setup_camera(self):
        """Set up camera for optimal viewing of the robotic arm"""
        p.resetDebugVisualizerCamera(
            cameraDistance=8.0,
            cameraYaw=45,
            cameraPitch=-30,
            cameraTargetPosition=[0, 0, 1]
        )
    
    def set_joint_positions(self, joint_positions):
        """
        Set positions for all controllable joints
        
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
                    force=500
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
        # Get position of the last link (bucket tip)
        link_state = p.getLinkState(self.arm_id, len(self.controllable_joints) - 1)
        return link_state[0]  # World position
    
    def animate_digging_sequence(self, duration=10.0):
        """
        Animate a digging sequence like a JCB excavator
        
        Args:
            duration (float): Duration of animation in seconds
        """
        print("Starting JCB-style digging animation...")
        
        # Define key poses for digging sequence
        poses = [
            # Pose 1: Initial position (arm extended forward)
            [0.2, -0.5, 0.8, 0.0],
            
            # Pose 2: Reach down to dig
            [0.4, -1.0, 1.5, 0.3],
            
            # Pose 3: Dig into ground
            [0.6, -1.2, 1.8, 0.5],
            
            # Pose 4: Lift with material
            [0.3, -0.8, 1.2, 0.2],
            
            # Pose 5: Swing to dump position
            [-0.5, -0.3, 0.5, -0.3],
            
            # Pose 6: Dump material
            [-0.7, -0.1, 0.2, -0.5],
            
            # Pose 7: Return to initial
            [0.2, -0.5, 0.8, 0.0]
        ]
        
        start_time = time.time()
        pose_duration = duration / (len(poses) - 1)
        
        current_pose_idx = 0
        
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            
            # Calculate which pose we're interpolating between
            pose_progress = elapsed / pose_duration
            current_pose_idx = int(pose_progress)
            local_progress = pose_progress - current_pose_idx
            
            if current_pose_idx >= len(poses) - 1:
                current_pose_idx = len(poses) - 2
                local_progress = 1.0
            
            # Interpolate between current and next pose
            current_pose = poses[current_pose_idx]
            next_pose = poses[current_pose_idx + 1]
            
            interpolated_pose = []
            for i in range(len(current_pose)):
                interp_value = current_pose[i] + local_progress * (next_pose[i] - current_pose[i])
                interpolated_pose.append(interp_value)
            
            # Apply smooth interpolation (ease in/out)
            smooth_progress = 0.5 * (1 - math.cos(math.pi * local_progress))
            final_pose = []
            for i in range(len(current_pose)):
                smooth_value = current_pose[i] + smooth_progress * (next_pose[i] - current_pose[i])
                final_pose.append(smooth_value)
            
            # Set joint positions
            self.set_joint_positions(final_pose)
            
            # Step simulation
            p.stepSimulation()
            time.sleep(1.0/60.0)  # 60 FPS
            
            # Print progress
            if int(elapsed * 10) % 20 == 0:  # Every 2 seconds
                progress = (elapsed / duration) * 100
                end_pos = self.get_end_effector_position()
                print(f"Animation progress: {progress:.1f}% - End effector at: {end_pos}")
    
    def run_interactive_demo(self):
        """Run an interactive demo with multiple animation sequences"""
        print("\n" + "="*50)
        print("3D ROBOTIC ARM ANIMATION DEMO")
        print("PyBullet JCB-Style Excavator Arm")
        print("="*50)
        
        # Add some objects to interact with
        self.add_demo_objects()
        
        print("\nRunning digging sequence animation...")
        print("Watch the 3D visualization window!")
        
        # Run multiple animation cycles
        for cycle in range(3):
            print(f"\nAnimation cycle {cycle + 1}/3")
            self.animate_digging_sequence(duration=8.0)
            
            # Pause between cycles
            time.sleep(1.0)
        
        print("\nAnimation complete! Close the PyBullet window when done.")
        
        # Keep simulation running for manual interaction
        try:
            while True:
                p.stepSimulation()
                time.sleep(1.0/60.0)
        except KeyboardInterrupt:
            print("Simulation stopped by user.")
    
    def add_demo_objects(self):
        """Add some objects to the scene for realism"""
        # Add some boxes to represent dirt/debris
        for i in range(5):
            x = np.random.uniform(-2, 2)
            y = np.random.uniform(-2, 2)
            z = 0.1
            
            box_id = p.loadURDF("cube_small.urdf", [x, y, z])
            # Change color to brown (dirt-like)
            p.changeVisualShape(box_id, -1, rgbaColor=[0.6, 0.4, 0.2, 1.0])
    
    def cleanup(self):
        """Clean up PyBullet environment"""
        p.disconnect()


def main():
    """Main function to run the 3D robotic arm animation"""
    print("Initializing 3D Robotic Arm Animation...")
    
    try:
        # Create robotic arm simulation
        arm_sim = PyBulletRoboticArm(gui=True)
        
        # Run interactive demo
        arm_sim.run_interactive_demo()
        
    except KeyboardInterrupt:
        print("\nAnimation stopped by user.")
    except Exception as e:
        print(f"Error during animation: {e}")
    finally:
        # Clean up
        try:
            arm_sim.cleanup()
        except:
            pass
        print("3D Animation demo finished.")


if __name__ == "__main__":
    main()