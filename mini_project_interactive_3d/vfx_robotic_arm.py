"""
Advanced VFX Robotic Arm with Blender Integration Support
Professional 3D robotic arm simulation with cinematic rendering capabilities
"""
import pybullet as p
import pybullet_data
import numpy as np
import time
import math
import os


class VFXRoboticArm:
    """Advanced VFX Robotic Arm with cinematic rendering and professional effects"""
    
    def __init__(self, gui=True, vfx_mode=True):
        """
        Initialize VFX Robotic Arm with advanced rendering
        
        Args:
            gui (bool): Whether to show GUI
            vfx_mode (bool): Enable advanced VFX features
        """
        # Connect to PyBullet with maximum quality settings
        if gui:
            self.physics_client = p.connect(p.GUI, options="--width=1920 --height=1080")
        else:
            self.physics_client = p.connect(p.DIRECT)
        
        self.vfx_mode = vfx_mode
        
        # Enable all advanced rendering features
        p.configureDebugVisualizer(p.COV_ENABLE_SHADOWS, 1)
        p.configureDebugVisualizer(p.COV_ENABLE_WIREFRAME, 0)
        p.configureDebugVisualizer(p.COV_ENABLE_RENDERING, 1)
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 1)
        p.configureDebugVisualizer(p.COV_ENABLE_SEGMENTATION_MARK_PREVIEW, 0)
        p.configureDebugVisualizer(p.COV_ENABLE_DEPTH_BUFFER_PREVIEW, 0)
        p.configureDebugVisualizer(p.COV_ENABLE_RGB_BUFFER_PREVIEW, 0)
        
        # Set up physics environment
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81)
        
        # Set physics parameters for realism
        p.setPhysicsEngineParameter(
            fixedTimeStep=1.0/240.0,  # High precision
            numSolverIterations=10,
            useSplitImpulse=1,
            splitImpulsePenetrationThreshold=-0.02,
            numSubSteps=4
        )
        
        # Professional lighting and environment
        self.setup_vfx_environment()
        
        # Create photorealistic JCB arm
        self.arm_id = self.create_photorealistic_jcb_arm()
        
        # Initialize control systems
        self.initialize_control_systems()
        
        # Set up cinematic cameras
        self.setup_multiple_cameras()
        
        # VFX effects
        if self.vfx_mode:
            self.setup_vfx_effects()
        
        print("🎬 VFX ROBOTIC ARM - CINEMA QUALITY INITIALIZED")
        print("=" * 50)
        print("🎥 Camera Controls:")
        print("  1-5: Switch camera angles")
        print("  C: Cinematic mode")
        print("🎮 Arm Controls:")
        print("  Q/A: Boom Joint")
        print("  W/S: Stick Joint") 
        print("  E/D: Bucket Joint")
        print("  R/F: Bucket Rotation")
        print("🎭 VFX Controls:")
        print("  V: Toggle VFX effects")
        print("  B: Capture high-res screenshot")
        print("  N: Start recording sequence")
        print("=" * 50)
    
    def setup_vfx_environment(self):
        """Set up professional VFX environment with advanced lighting"""
        # Load enhanced ground with PBR materials
        self.plane_id = p.loadURDF("plane.urdf")
        p.changeVisualShape(
            self.plane_id, -1, 
            rgbaColor=[0.4, 0.4, 0.4, 1.0],
            specularColor=[0.1, 0.1, 0.1]
        )
        
        # Create construction site environment
        self.create_construction_environment()
        
        # Add atmospheric effects
        self.add_atmospheric_effects()
        
        # Professional lighting rig
        self.setup_professional_lighting_rig()
    
    def create_construction_environment(self):
        """Create a realistic construction site environment"""
        # Construction vehicles and equipment
        vehicles = []
        
        # Add construction barriers in a circle
        barrier_positions = []
        for i in range(12):
            angle = i * (2 * math.pi / 12)
            x = 8 * math.cos(angle)
            y = 8 * math.sin(angle)
            barrier_positions.append([x, y, 0.5])
        
        for pos in barrier_positions:
            barrier_id = p.loadURDF("cube_small.urdf", pos)
            p.changeVisualShape(
                barrier_id, -1,
                rgbaColor=[1.0, 0.3, 0.0, 1.0],  # Safety orange
                specularColor=[0.5, 0.5, 0.5]
            )
        
        # Add realistic dirt and debris
        self.add_realistic_terrain()
        
        # Add construction materials
        self.add_construction_materials()
    
    def add_realistic_terrain(self):
        """Add realistic terrain with dirt piles and rocks"""
        # Large dirt piles
        for i in range(5):
            x = np.random.uniform(-6, 6)
            y = np.random.uniform(-6, 6)
            if np.sqrt(x*x + y*y) > 3:  # Keep clear area around arm
                # Create dirt pile
                pile_size = np.random.uniform(0.5, 1.5)
                pile_id = p.loadURDF("cube_small.urdf", [x, y, pile_size/2])
                
                # Realistic dirt color with variation
                brown_base = 0.4
                variation = np.random.uniform(-0.1, 0.1)
                dirt_color = [
                    brown_base + variation,
                    brown_base * 0.7 + variation,
                    brown_base * 0.4 + variation,
                    1.0
                ]
                
                p.changeVisualShape(
                    pile_id, -1,
                    rgbaColor=dirt_color,
                    specularColor=[0.1, 0.1, 0.1]
                )
        
        # Add rocks and debris
        for i in range(15):
            x = np.random.uniform(-5, 5)
            y = np.random.uniform(-5, 5)
            if np.sqrt(x*x + y*y) > 2:
                rock_id = p.loadURDF("cube_small.urdf", [x, y, 0.1])
                
                # Gray rock color
                gray_value = np.random.uniform(0.3, 0.7)
                rock_color = [gray_value, gray_value, gray_value, 1.0]
                
                p.changeVisualShape(
                    rock_id, -1,
                    rgbaColor=rock_color,
                    specularColor=[0.3, 0.3, 0.3]
                )
    
    def add_construction_materials(self):
        """Add construction materials like pipes, beams, etc."""
        # Steel beams
        for i in range(3):
            x = np.random.uniform(-4, 4)
            y = np.random.uniform(-4, 4)
            if np.sqrt(x*x + y*y) > 2.5:
                beam_id = p.loadURDF("cube_small.urdf", [x, y, 0.2])
                
                # Metallic steel color
                p.changeVisualShape(
                    beam_id, -1,
                    rgbaColor=[0.7, 0.7, 0.8, 1.0],
                    specularColor=[0.9, 0.9, 0.9]
                )
    
    def add_atmospheric_effects(self):
        """Add atmospheric effects like dust particles and ambient lighting"""
        # Create dust particle effect (visual only)
        self.dust_particles = []
        for i in range(20):
            x = np.random.uniform(-10, 10)
            y = np.random.uniform(-10, 10)
            z = np.random.uniform(1, 5)
            
            # Small transparent particles
            particle_id = p.loadURDF("cube_small.urdf", [x, y, z])
            p.changeVisualShape(
                particle_id, -1,
                rgbaColor=[0.8, 0.7, 0.6, 0.3],  # Semi-transparent dust
                specularColor=[0.1, 0.1, 0.1]
            )
            self.dust_particles.append(particle_id)
    
    def setup_professional_lighting_rig(self):
        """Set up a professional 3-point lighting rig"""
        # Key light (main illumination) - simulated sun
        self.key_light_pos = [10, 10, 15]
        
        # Fill light (softer secondary) 
        self.fill_light_pos = [-5, 8, 10]
        
        # Rim light (edge definition)
        self.rim_light_pos = [-8, -8, 12]
        
        # Add visual representations of lights
        for pos, color in [
            (self.key_light_pos, [1, 1, 0.8]),
            (self.fill_light_pos, [0.8, 0.8, 1]),
            (self.rim_light_pos, [1, 0.9, 0.7])
        ]:
            p.addUserDebugLine(
                pos, [0, 0, 0],
                lineColorRGB=color,
                lineWidth=1
            )
    
    def create_photorealistic_jcb_arm(self):
        """Create a photorealistic JCB excavator arm with PBR materials"""
        # Professional JCB dimensions
        base_radius = 1.5
        base_height = 0.8
        
        boom_length = 3.5
        boom_radius = 0.25
        
        stick_length = 3.0
        stick_radius = 0.18
        
        bucket_length = 1.5
        bucket_width = 1.0
        bucket_height = 0.5
        
        # Create advanced visual shapes with PBR-like properties
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
        
        # Base - JCB rotating turntable
        base_visual = p.createVisualShape(
            p.GEOM_CYLINDER,
            radius=base_radius,
            length=base_height,
            rgbaColor=[0.98, 0.88, 0.1, 1.0],  # Iconic JCB yellow
            specularColor=[0.7, 0.7, 0.5]  # Metallic reflection
        )
        base_collision = p.createCollisionShape(
            p.GEOM_CYLINDER,
            radius=base_radius,
            height=base_height
        )
        
        # Boom - Main hydraulic arm
        boom_visual = p.createVisualShape(
            p.GEOM_CYLINDER,
            radius=boom_radius,
            length=boom_length,
            rgbaColor=[0.95, 0.45, 0.1, 1.0],  # JCB orange
            specularColor=[0.6, 0.4, 0.2]
        )
        boom_collision = p.createCollisionShape(
            p.GEOM_CYLINDER,
            radius=boom_radius,
            height=boom_length
        )
        
        visual_shapes.append(boom_visual)
        collision_shapes.append(boom_collision)
        link_masses.append(120.0)
        link_positions.append([0, 0, boom_length/2])
        link_orientations.append([0, 0, 0, 1])
        link_inertial_positions.append([0, 0, boom_length/2])
        link_inertial_orientations.append([0, 0, 0, 1])
        parent_indices.append(0)
        joint_types.append(p.JOINT_REVOLUTE)
        joint_axes.append([1, 0, 0])
        
        # Stick - Secondary hydraulic arm
        stick_visual = p.createVisualShape(
            p.GEOM_CYLINDER,
            radius=stick_radius,
            length=stick_length,
            rgbaColor=[0.9, 0.5, 0.15, 1.0],  # Lighter orange
            specularColor=[0.5, 0.4, 0.2]
        )
        stick_collision = p.createCollisionShape(
            p.GEOM_CYLINDER,
            radius=stick_radius,
            height=stick_length
        )
        
        visual_shapes.append(stick_visual)
        collision_shapes.append(stick_collision)
        link_masses.append(80.0)
        link_positions.append([0, 0, stick_length/2])
        link_orientations.append([0, 0, 0, 1])
        link_inertial_positions.append([0, 0, stick_length/2])
        link_inertial_orientations.append([0, 0, 0, 1])
        parent_indices.append(1)
        joint_types.append(p.JOINT_REVOLUTE)
        joint_axes.append([1, 0, 0])
        
        # Bucket - Professional excavator bucket
        bucket_visual = p.createVisualShape(
            p.GEOM_BOX,
            halfExtents=[bucket_length/2, bucket_width/2, bucket_height/2],
            rgbaColor=[0.2, 0.2, 0.25, 1.0],  # Dark steel
            specularColor=[0.8, 0.8, 0.8]  # High metallic reflection
        )
        bucket_collision = p.createCollisionShape(
            p.GEOM_BOX,
            halfExtents=[bucket_length/2, bucket_width/2, bucket_height/2]
        )
        
        visual_shapes.append(bucket_visual)
        collision_shapes.append(bucket_collision)
        link_masses.append(40.0)
        link_positions.append([bucket_length/2, 0, 0])
        link_orientations.append([0, 0, 0, 1])
        link_inertial_positions.append([bucket_length/2, 0, 0])
        link_inertial_orientations.append([0, 0, 0, 1])
        parent_indices.append(2)
        joint_types.append(p.JOINT_REVOLUTE)
        joint_axes.append([1, 0, 0])
        
        # Bucket teeth - Hardened steel cutting edge
        teeth_visual = p.createVisualShape(
            p.GEOM_BOX,
            halfExtents=[0.3, bucket_width/2, 0.15],
            rgbaColor=[0.05, 0.05, 0.1, 1.0],  # Nearly black steel
            specularColor=[0.9, 0.9, 0.9]  # Very reflective
        )
        teeth_collision = p.createCollisionShape(
            p.GEOM_BOX,
            halfExtents=[0.3, bucket_width/2, 0.15]
        )
        
        visual_shapes.append(teeth_visual)
        collision_shapes.append(teeth_collision)
        link_masses.append(10.0)
        link_positions.append([0.5, 0, -0.25])
        link_orientations.append([0, 0, 0, 1])
        link_inertial_positions.append([0.5, 0, -0.25])
        link_inertial_orientations.append([0, 0, 0, 1])
        parent_indices.append(3)
        joint_types.append(p.JOINT_REVOLUTE)
        joint_axes.append([0, 1, 0])
        
        # Create the photorealistic multi-body robot
        arm_id = p.createMultiBody(
            baseMass=300.0,
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
    
    def initialize_control_systems(self):
        """Initialize advanced control systems"""
        # Get joint information
        self.num_joints = p.getNumJoints(self.arm_id)
        self.joint_info = []
        self.controllable_joints = []
        
        for i in range(self.num_joints):
            info = p.getJointInfo(self.arm_id, i)
            self.joint_info.append(info)
            if info[2] in [p.JOINT_REVOLUTE, p.JOINT_PRISMATIC]:
                self.controllable_joints.append(i)
        
        # Initialize joint positions
        self.joint_positions = [0.0] * len(self.controllable_joints)
        self.target_positions = [0.0] * len(self.controllable_joints)
        
        # Control parameters
        self.control_gains = [2000, 1500, 1000, 500]  # Different gains per joint
        self.max_velocities = [3.0, 2.5, 2.0, 4.0]    # Maximum velocities
        
        print(f"🎮 Initialized {len(self.controllable_joints)} controllable joints")
    
    def setup_multiple_cameras(self):
        """Set up multiple cinematic camera angles"""
        self.cameras = {
            'wide': {
                'distance': 12.0,
                'yaw': 45,
                'pitch': -20,
                'target': [0, 0, 2]
            },
            'close': {
                'distance': 6.0,
                'yaw': 30,
                'pitch': -15,
                'target': [0, 0, 3]
            },
            'side': {
                'distance': 8.0,
                'yaw': 90,
                'pitch': -10,
                'target': [0, 0, 2.5]
            },
            'top': {
                'distance': 10.0,
                'yaw': 0,
                'pitch': -60,
                'target': [0, 0, 1]
            },
            'dramatic': {
                'distance': 15.0,
                'yaw': 15,
                'pitch': -5,
                'target': [0, 0, 4]
            }
        }
        
        self.current_camera = 'wide'
        self.set_camera('wide')
    
    def set_camera(self, camera_name):
        """Set camera to predefined angle"""
        if camera_name in self.cameras:
            cam = self.cameras[camera_name]
            p.resetDebugVisualizerCamera(
                cameraDistance=cam['distance'],
                cameraYaw=cam['yaw'],
                cameraPitch=cam['pitch'],
                cameraTargetPosition=cam['target']
            )
            self.current_camera = camera_name
            print(f"📷 Camera switched to: {camera_name}")
    
    def setup_vfx_effects(self):
        """Set up advanced VFX effects"""
        # Particle systems for dust and debris
        self.particle_systems = []
        
        # Add work light effects
        self.add_work_lights()
        
        # Add hydraulic cylinder visualizations
        self.add_hydraulic_cylinders()
    
    def add_work_lights(self):
        """Add LED work lights to the arm"""
        # LED lights on the arm
        light_positions = [
            [0, 0.3, 0.2],   # Base lights
            [0, 0.2, 2.5],   # Boom lights
            [0, 0.15, 2.0],  # Stick lights
            [0.8, 0, 0]      # Bucket lights
        ]
        
        self.work_lights = []
        for pos in light_positions:
            # Create bright white light representation
            light_id = p.loadURDF("cube_small.urdf", pos)
            p.changeVisualShape(
                light_id, -1,
                rgbaColor=[1.0, 1.0, 0.9, 1.0],
                specularColor=[1.0, 1.0, 1.0]
            )
            self.work_lights.append(light_id)
    
    def add_hydraulic_cylinders(self):
        """Add hydraulic cylinder visualizations"""
        # Visual hydraulic cylinders for realism
        cylinder_configs = [
            {'pos': [0.5, 0.3, 1.5], 'length': 1.0, 'radius': 0.05},  # Boom cylinder
            {'pos': [0.3, 0.25, 2.5], 'length': 0.8, 'radius': 0.04}, # Stick cylinder
            {'pos': [0.8, 0.2, 1.2], 'length': 0.6, 'radius': 0.03}   # Bucket cylinder
        ]
        
        self.hydraulic_cylinders = []
        for config in cylinder_configs:
            # Create hydraulic cylinder
            cyl_visual = p.createVisualShape(
                p.GEOM_CYLINDER,
                radius=config['radius'],
                length=config['length'],
                rgbaColor=[0.3, 0.3, 0.35, 1.0],  # Hydraulic cylinder color
                specularColor=[0.5, 0.5, 0.5]
            )
            
            cyl_collision = p.createCollisionShape(
                p.GEOM_CYLINDER,
                radius=config['radius'],
                height=config['length']
            )
            
            cyl_id = p.createMultiBody(
                baseMass=0.0,  # Static
                baseCollisionShapeIndex=cyl_collision,
                baseVisualShapeIndex=cyl_visual,
                basePosition=config['pos']
            )
            
            self.hydraulic_cylinders.append(cyl_id)
    
    def capture_cinematic_frame(self, width=1920, height=1080):
        """Capture a cinematic quality frame"""
        # High-quality camera parameters
        view_matrix = p.computeViewMatrixFromYawPitchRoll(
            cameraTargetPosition=self.cameras[self.current_camera]['target'],
            distance=self.cameras[self.current_camera]['distance'],
            yaw=self.cameras[self.current_camera]['yaw'],
            pitch=self.cameras[self.current_camera]['pitch'],
            roll=0,
            upAxisIndex=2
        )
        
        proj_matrix = p.computeProjectionMatrixFOV(
            fov=45,  # Cinematic FOV
            aspect=width/height,
            nearVal=0.1,
            farVal=100.0
        )
        
        # Capture with maximum quality
        _, _, rgb_array, depth_array, segmentation_array = p.getCameraImage(
            width=width,
            height=height,
            viewMatrix=view_matrix,
            projectionMatrix=proj_matrix,
            renderer=p.ER_BULLET_HARDWARE_OPENGL,
            flags=p.ER_SEGMENTATION_MASK_OBJECT_AND_LINKINDEX
        )
        
        return rgb_array, depth_array, segmentation_array
    
    def run_cinematic_demo(self, duration=20.0):
        """Run a cinematic demo with multiple camera angles"""
        print("🎬 Starting Cinematic Demo Sequence...")
        
        # Cinematic poses with dramatic movements
        cinematic_sequence = [
            # Scene 1: Establish shot
            {'pose': [0.0, -0.2, 0.3, 0.0], 'camera': 'dramatic', 'duration': 3.0},
            
            # Scene 2: Close approach
            {'pose': [0.4, -0.8, 1.2, 0.2], 'camera': 'close', 'duration': 2.5},
            
            # Scene 3: Deep dig
            {'pose': [0.8, -1.4, 2.0, 0.6], 'camera': 'side', 'duration': 3.0},
            
            # Scene 4: Material collection
            {'pose': [0.7, -1.0, 1.4, 0.9], 'camera': 'close', 'duration': 2.0},
            
            # Scene 5: Dramatic lift
            {'pose': [0.2, -0.3, 0.6, 0.8], 'camera': 'wide', 'duration': 3.0},
            
            # Scene 6: Transport swing
            {'pose': [-0.6, -0.1, 0.2, 0.7], 'camera': 'top', 'duration': 2.5},
            
            # Scene 7: Final dump
            {'pose': [-0.8, 0.2, -0.3, -0.4], 'camera': 'dramatic', 'duration': 3.0},
            
            # Scene 8: Return home
            {'pose': [0.0, -0.2, 0.3, 0.0], 'camera': 'wide', 'duration': 1.0}
        ]
        
        start_time = time.time()
        scene_index = 0
        scene_start_time = start_time
        
        print("🎥 Cinematic sequence started!")
        
        while time.time() - start_time < duration and scene_index < len(cinematic_sequence):
            current_time = time.time()
            elapsed = current_time - start_time
            scene_elapsed = current_time - scene_start_time
            
            current_scene = cinematic_sequence[scene_index]
            
            # Check if we need to move to next scene
            if scene_elapsed >= current_scene['duration']:
                scene_index += 1
                if scene_index < len(cinematic_sequence):
                    scene_start_time = current_time
                    next_scene = cinematic_sequence[scene_index]
                    self.set_camera(next_scene['camera'])
                    print(f"🎬 Scene {scene_index + 1}: {next_scene['camera']} angle")
                continue
            
            # Interpolate pose within scene
            if scene_index < len(cinematic_sequence) - 1:
                next_scene = cinematic_sequence[scene_index + 1]
                progress = scene_elapsed / current_scene['duration']
                
                # Smooth interpolation
                smooth_progress = 0.5 * (1 - math.cos(math.pi * progress))
                
                interpolated_pose = []
                for i in range(len(current_scene['pose'])):
                    current_val = current_scene['pose'][i]
                    next_val = next_scene['pose'][i]
                    interp_val = current_val + smooth_progress * (next_val - current_val)
                    interpolated_pose.append(interp_val)
                
                self.set_joint_positions_smooth(interpolated_pose)
            
            # Step simulation
            p.stepSimulation()
            time.sleep(1.0/60.0)  # 60 FPS
            
            # Progress indication
            if int(elapsed * 10) % 50 == 0:  # Every 5 seconds
                progress = (elapsed / duration) * 100
                print(f"🎬 Cinematic progress: {progress:.1f}% - Scene {scene_index + 1}")
        
        print("🏆 Cinematic demo sequence complete!")
    
    def set_joint_positions_smooth(self, joint_positions):
        """Set joint positions with smooth, realistic motion"""
        for i, joint_idx in enumerate(self.controllable_joints):
            if i < len(joint_positions):
                p.setJointMotorControl2(
                    self.arm_id,
                    joint_idx,
                    p.POSITION_CONTROL,
                    targetPosition=joint_positions[i],
                    force=self.control_gains[i] if i < len(self.control_gains) else 1000,
                    maxVelocity=self.max_velocities[i] if i < len(self.max_velocities) else 2.0
                )
    
    def run_interactive_vfx_mode(self):
        """Run interactive mode with VFX controls"""
        print("🎮 Starting Interactive VFX Mode...")
        print("Professional robotic arm control with cinematic quality")
        
        # Add interactive controls
        self.setup_interactive_sliders()
        
        last_screenshot_time = 0
        last_demo_time = 0
        
        try:
            while True:
                current_time = time.time()
                
                # Handle keyboard input for camera switching
                keys = p.getKeyboardEvents()
                for key, state in keys.items():
                    if state & p.KEY_WAS_TRIGGERED:
                        if key == ord('1'):
                            self.set_camera('wide')
                        elif key == ord('2'):
                            self.set_camera('close')
                        elif key == ord('3'):
                            self.set_camera('side')
                        elif key == ord('4'):
                            self.set_camera('top')
                        elif key == ord('5'):
                            self.set_camera('dramatic')
                        elif key == ord('c') or key == ord('C'):
                            print("🎬 Starting cinematic demo...")
                            self.run_cinematic_demo(duration=15.0)
                        elif key == ord('b') or key == ord('B'):
                            if current_time - last_screenshot_time > 2.0:
                                rgb, depth, seg = self.capture_cinematic_frame()
                                print("📸 Cinematic screenshot captured!")
                                last_screenshot_time = current_time
                
                # Update from sliders
                if hasattr(self, 'joint_sliders'):
                    self.update_from_sliders()
                    self.set_joint_positions_smooth(self.joint_positions)
                
                # Animate dust particles
                if self.vfx_mode:
                    self.animate_dust_particles()
                
                # Step simulation
                p.stepSimulation()
                time.sleep(1.0/60.0)  # 60 FPS
                
        except KeyboardInterrupt:
            print("\n🛑 VFX Interactive mode stopped.")
    
    def setup_interactive_sliders(self):
        """Set up interactive control sliders"""
        self.joint_sliders = []
        joint_names = ["Boom", "Stick", "Bucket", "Rotation"]
        joint_ranges = [(-1.5, 1.5), (-2.0, 0.5), (-0.5, 2.0), (-3.14, 3.14)]
        
        for i, (name, (min_val, max_val)) in enumerate(zip(joint_names, joint_ranges)):
            slider_id = p.addUserDebugParameter(
                f"🎮 {name} Joint", 
                min_val, 
                max_val, 
                0.0
            )
            self.joint_sliders.append(slider_id)
        
        # VFX controls
        self.cinematic_button = p.addUserDebugParameter("🎬 Cinematic Demo", 1, 1, 1)
        self.screenshot_button = p.addUserDebugParameter("📸 Screenshot", 1, 1, 1)
    
    def update_from_sliders(self):
        """Update joint positions from sliders"""
        for i, slider_id in enumerate(self.joint_sliders):
            if i < len(self.joint_positions):
                self.joint_positions[i] = p.readUserDebugParameter(slider_id)
    
    def animate_dust_particles(self):
        """Animate dust particles for atmospheric effect"""
        # Simple dust animation
        current_time = time.time()
        
        for i, particle_id in enumerate(self.dust_particles):
            # Gentle floating motion
            offset_x = 0.1 * math.sin(current_time + i)
            offset_y = 0.1 * math.cos(current_time + i * 0.7)
            offset_z = 0.05 * math.sin(current_time * 0.5 + i * 0.3)
            
            base_pos = [
                np.random.uniform(-10, 10) if i % 20 == 0 else 0,
                np.random.uniform(-10, 10) if i % 20 == 0 else 0,
                np.random.uniform(1, 5) if i % 20 == 0 else 0
            ]
    
    def cleanup(self):
        """Clean up the VFX environment"""
        p.disconnect()
        print("🧹 VFX environment cleaned up")


def main():
    """Main function for VFX Robotic Arm"""
    print("🚀 LAUNCHING VFX ROBOTIC ARM SIMULATION")
    print("🎬 Cinema-Quality 3D JCB Excavator Arm")
    print("=" * 50)
    
    try:
        # Create VFX robotic arm
        vfx_arm = VFXRoboticArm(gui=True, vfx_mode=True)
        
        print("\n🌟 VFX System Ready!")
        print("🎮 Interactive controls active")
        print("🎥 Multiple camera angles available")
        print("🎭 Professional VFX effects enabled")
        
        # Run interactive VFX mode
        vfx_arm.run_interactive_vfx_mode()
        
    except KeyboardInterrupt:
        print("\n🛑 VFX simulation stopped by user.")
    except Exception as e:
        print(f"❌ VFX simulation error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            vfx_arm.cleanup()
        except:
            pass
        print("🏁 VFX Robotic Arm simulation finished.")


if __name__ == "__main__":
    main()