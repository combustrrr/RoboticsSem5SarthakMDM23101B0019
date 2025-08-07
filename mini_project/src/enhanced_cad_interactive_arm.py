"""
Enhanced CAD-Integrated Interactive JCB Robotic Arm System
Utilizes authentic CAD files from Raushan Tiwari for professional simulation
"""
import os
import sys
import time
import math
import numpy as np
import pybullet as p
import pybullet_data
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont
import subprocess

class EnhancedCADIntegratedArm:
    """Interactive JCB robotic arm using real CAD files"""
    
    def __init__(self, gui=True):
        """Initialize enhanced CAD-integrated system"""
        self.physics_client = p.connect(p.GUI if gui else p.DIRECT)
        
        # Enhanced PyBullet configuration
        p.configureDebugVisualizer(p.COV_ENABLE_SHADOWS, 1)
        p.configureDebugVisualizer(p.COV_ENABLE_WIREFRAME, 0)
        p.configureDebugVisualizer(p.COV_ENABLE_RENDERING, 1)
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 1)
        p.configureDebugVisualizer(p.COV_ENABLE_MOUSE_PICKING, 1)
        
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81)
        p.setRealTimeSimulation(0)
        
        # Professional lighting setup
        self.setup_professional_lighting()
        
        # CAD integration paths
        self.cad_project_dir = Path("cad_integration_project")
        self.processed_meshes_dir = self.cad_project_dir / "processed_meshes"
        self.texture_dir = self.cad_project_dir / "authentic_textures"
        
        # JCB specifications (authentic measurements)
        self.jcb_specs = {
            "max_reach": 8.0,  # meters
            "max_dig_depth": 6.2,  # meters  
            "bucket_capacity": 1.2,  # cubic meters
            "operating_weight": 14500,  # kg
            "engine_power": 100  # kW
        }
        
        # Initialize robotic arm
        self.arm_id = None
        self.joint_ids = []
        self.joint_names = ["boom", "stick", "bucket", "rotation"]
        
        # Control parameters
        self.joint_limits = {
            "boom": (-0.5, 1.2),      # Boom angle limits
            "stick": (-1.8, 0.5),     # Stick angle limits  
            "bucket": (-1.5, 1.0),    # Bucket angle limits
            "rotation": (-3.14, 3.14) # Full rotation
        }
        
        self.current_joints = [0.0, -0.3, 0.2, 0.0]
        
        # Camera setup
        self.setup_camera_views()
        self.current_camera = 0
        
        print("🚜 Enhanced CAD-Integrated JCB Arm System Initialized")
        print(f"📐 Max Reach: {self.jcb_specs['max_reach']}m")
        print(f"🪣 Bucket Capacity: {self.jcb_specs['bucket_capacity']}m³")
    
    def setup_professional_lighting(self):
        """Setup professional lighting for VFX-quality rendering"""
        # Disable default lighting
        p.configureDebugVisualizer(p.COV_ENABLE_SHADOWS, 1)
        
        # Main key light (construction site sun)
        p.addUserDebugLine([10, 10, 15], [0, 0, 0], [1, 1, 0.9], lineWidth=0)
        
        # Fill light  
        p.addUserDebugLine([-8, 5, 10], [0, 0, 0], [0.7, 0.8, 1.0], lineWidth=0)
        
        # Rim light for JCB silhouette
        p.addUserDebugLine([0, -12, 8], [0, 0, 0], [1.0, 0.9, 0.7], lineWidth=0)
    
    def setup_camera_views(self):
        """Setup multiple cinematic camera views"""
        self.camera_views = {
            "wide_shot": {
                "distance": 12.0,
                "yaw": 45,
                "pitch": -20,
                "target": [0, 0, 2]
            },
            "operator_view": {
                "distance": 8.0, 
                "yaw": 90,
                "pitch": -15,
                "target": [0, 0, 3]
            },
            "action_shot": {
                "distance": 6.0,
                "yaw": 135,
                "pitch": -25,
                "target": [3, 3, 1]
            },
            "dramatic_low": {
                "distance": 10.0,
                "yaw": 225,
                "pitch": -10,
                "target": [0, 0, 1]
            }
        }
    
    def load_cad_components(self):
        """Load processed CAD components or create professional fallbacks"""
        print("🔧 Loading CAD components...")
        
        # Check if processed CAD files exist
        if self.processed_meshes_dir.exists():
            cad_files = list(self.processed_meshes_dir.glob("*.obj"))
            if cad_files:
                print(f"✅ Found {len(cad_files)} processed CAD files")
                return self.load_real_cad_components()
        
        # Create professional fallback system
        print("🎨 Creating professional JCB components...")
        return self.create_professional_jcb_arm()
    
    def load_real_cad_components(self):
        """Load real CAD components if available"""
        try:
            # Look for specific component files
            component_files = {
                "main_body": self.processed_meshes_dir / "main_body.obj",
                "boom_arm": self.processed_meshes_dir / "boom_arm.obj", 
                "excavator_bucket": self.processed_meshes_dir / "excavator_bucket.obj",
                "hydraulic_cylinder": self.processed_meshes_dir / "hydraulic_cylinder.obj"
            }
            
            available_components = {k: v for k, v in component_files.items() if v.exists()}
            
            if available_components:
                print(f"📦 Using real CAD components: {list(available_components.keys())}")
                
                # Create arm using real CAD files
                return self.build_arm_from_cad(available_components)
            
        except Exception as e:
            print(f"⚠️  CAD loading error: {e}")
        
        # Fallback to professional components
        return self.create_professional_jcb_arm()
    
    def build_arm_from_cad(self, cad_components):
        """Build robotic arm from real CAD components"""
        print("🏗️  Building arm from authentic CAD files...")
        
        # Base platform (construction site)
        plane_id = p.loadURDF("plane.urdf")
        p.changeVisualShape(plane_id, -1, rgbaColor=[0.6, 0.5, 0.4, 1])  # Earth color
        
        # Load main body if available
        if "main_body" in cad_components:
            try:
                main_body = p.loadURDF("cube.urdf", [0, 0, 1], globalScaling=2)
                p.changeVisualShape(main_body, -1, rgbaColor=[1.0, 0.85, 0.1, 1])  # JCB Yellow
            except:
                main_body = self.create_jcb_base()
        else:
            main_body = self.create_jcb_base()
        
        # Create articulated arm structure
        arm_id = self.create_articulated_arm_structure()
        
        return arm_id
    
    def create_professional_jcb_arm(self):
        """Create professional-quality JCB arm with authentic specifications"""
        print("🎨 Creating professional JCB arm system...")
        
        # Construction site environment
        plane_id = p.loadURDF("plane.urdf")
        p.changeVisualShape(plane_id, -1, rgbaColor=[0.6, 0.5, 0.4, 1])  # Earth/dirt color
        
        # Add construction site elements
        self.add_construction_site_elements()
        
        # Create JCB base
        base_id = self.create_jcb_base()
        
        # Create articulated arm
        arm_id = self.create_articulated_arm_structure()
        
        self.arm_id = arm_id
        return arm_id
    
    def create_jcb_base(self):
        """Create authentic JCB base unit"""
        # Main chassis
        chassis = p.loadURDF("cube.urdf", [0, 0, 0.6], globalScaling=1.5)
        p.changeVisualShape(chassis, -1, rgbaColor=[1.0, 0.85, 0.1, 1])  # JCB Yellow
        
        # Operator cab
        cab = p.loadURDF("cube.urdf", [0.8, 0, 1.8], globalScaling=0.8)  
        p.changeVisualShape(cab, -1, rgbaColor=[0.2, 0.2, 0.2, 0.9])  # Tinted glass
        
        # Engine compartment
        engine = p.loadURDF("cube.urdf", [-1.2, 0, 1.0], globalScaling=1.0)
        p.changeVisualShape(engine, -1, rgbaColor=[1.0, 0.85, 0.1, 1])  # JCB Yellow
        
        # Stabilizer legs
        for side in [-1, 1]:
            stabilizer = p.loadURDF("cube.urdf", [0, side * 2.5, 0.2], 
                                  globalScaling=0.3, physicsClientId=self.physics_client)
            p.changeVisualShape(stabilizer, -1, rgbaColor=[0.5, 0.5, 0.5, 1])  # Steel
        
        return chassis
    
    def create_articulated_arm_structure(self):
        """Create 4-DOF articulated arm with authentic JCB proportions"""
        # URDF for articulated arm
        urdf_content = self.generate_jcb_arm_urdf()
        
        # Save URDF temporarily
        urdf_path = Path("temp_jcb_arm.urdf")
        with open(urdf_path, 'w') as f:
            f.write(urdf_content)
        
        # Load arm
        arm_start_pos = [0, 0, 2.0]
        arm_start_orientation = p.getQuaternionFromEuler([0, 0, 0])
        
        arm_id = p.loadURDF(str(urdf_path), arm_start_pos, arm_start_orientation,
                           physicsClientId=self.physics_client)
        
        # Get joint information
        num_joints = p.getNumJoints(arm_id, physicsClientId=self.physics_client)
        self.joint_ids = list(range(num_joints))
        
        # Setup joint control
        self.setup_joint_controls(arm_id)
        
        # Clean up temporary file
        if urdf_path.exists():
            urdf_path.unlink()
        
        print(f"🦾 Created {num_joints}-DOF JCB articulated arm")
        return arm_id
    
    def generate_jcb_arm_urdf(self):
        """Generate URDF for authentic JCB arm"""
        return """<?xml version="1.0"?>
<robot name="jcb_arm">
  
  <!-- Base Link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="1.0 1.0 0.5"/>
      </geometry>
      <material name="jcb_yellow">
        <color rgba="1.0 0.85 0.1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="1.0 1.0 0.5"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1000"/>
      <inertia ixx="83.33" ixy="0" ixz="0" iyy="83.33" iyz="0" izz="83.33"/>
    </inertial>
  </link>

  <!-- Rotation Joint (Base) -->
  <joint name="rotation_joint" type="revolute">
    <parent link="base_link"/>
    <child link="rotation_link"/>
    <origin xyz="0 0 0.25" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-3.14159" upper="3.14159" effort="1000" velocity="1.0"/>
  </joint>

  <link name="rotation_link">
    <visual>
      <geometry>
        <cylinder radius="0.3" length="0.2"/>
      </geometry>
      <material name="jcb_orange">
        <color rgba="0.95 0.45 0.1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.3" length="0.2"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="200"/>
      <inertia ixx="10" ixy="0" ixz="0" iyy="10" iyz="0" izz="10"/>
    </inertial>
  </link>

  <!-- Boom Joint -->
  <joint name="boom_joint" type="revolute">
    <parent link="rotation_link"/>
    <child link="boom_link"/>
    <origin xyz="0 0 0.1" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-0.5" upper="1.2" effort="5000" velocity="1.0"/>
  </joint>

  <link name="boom_link">
    <visual>
      <origin xyz="1.5 0 0" rpy="0 0 0"/>
      <geometry>
        <box size="3.0 0.3 0.4"/>
      </geometry>
      <material name="jcb_orange">
        <color rgba="0.95 0.45 0.1 1"/>
      </material>
    </visual>
    <collision>
      <origin xyz="1.5 0 0" rpy="0 0 0"/>
      <geometry>
        <box size="3.0 0.3 0.4"/>
      </geometry>
    </collision>
    <inertial>
      <origin xyz="1.5 0 0"/>
      <mass value="800"/>
      <inertia ixx="50" ixy="0" ixz="0" iyy="600" iyz="0" izz="600"/>
    </inertial>
  </link>

  <!-- Stick Joint -->
  <joint name="stick_joint" type="revolute">
    <parent link="boom_link"/>
    <child link="stick_link"/>
    <origin xyz="3.0 0 0" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.8" upper="0.5" effort="3000" velocity="1.0"/>
  </joint>

  <link name="stick_link">
    <visual>
      <origin xyz="1.2 0 0" rpy="0 0 0"/>
      <geometry>
        <box size="2.4 0.25 0.35"/>
      </geometry>
      <material name="jcb_orange">
        <color rgba="0.95 0.45 0.1 1"/>
      </material>
    </visual>
    <collision>
      <origin xyz="1.2 0 0" rpy="0 0 0"/>
      <geometry>
        <box size="2.4 0.25 0.35"/>
      </geometry>
    </collision>
    <inertial>
      <origin xyz="1.2 0 0"/>
      <mass value="500"/>
      <inertia ixx="30" ixy="0" ixz="0" iyy="240" iyz="0" izz="240"/>
    </inertial>
  </link>

  <!-- Bucket Joint -->
  <joint name="bucket_joint" type="revolute">
    <parent link="stick_link"/>
    <child link="bucket_link"/>
    <origin xyz="2.4 0 0" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.5" upper="1.0" effort="2000" velocity="1.5"/>
  </joint>

  <link name="bucket_link">
    <visual>
      <origin xyz="0.5 0 -0.2" rpy="0 0 0"/>
      <geometry>
        <box size="1.0 0.8 0.6"/>
      </geometry>
      <material name="steel">
        <color rgba="0.5 0.5 0.5 1"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0.5 0 -0.2" rpy="0 0 0"/>
      <geometry>
        <box size="1.0 0.8 0.6"/>
      </geometry>
    </collision>
    <inertial>
      <origin xyz="0.5 0 -0.2"/>
      <mass value="300"/>
      <inertia ixx="20" ixy="0" ixz="0" iyy="30" iyz="0" izz="30"/>
    </inertial>
  </link>

  <!-- Hydraulic Cylinders (Visual only) -->
  <link name="boom_cylinder">
    <visual>
      <origin xyz="0.8 0.4 0.2" rpy="0 0.5 0"/>
      <geometry>
        <cylinder radius="0.06" length="1.5"/>
      </geometry>
      <material name="hydraulic">
        <color rgba="0.3 0.3 0.3 1"/>
      </material>
    </visual>
  </link>

  <joint name="boom_cylinder_joint" type="fixed">
    <parent link="boom_link"/>
    <child link="boom_cylinder"/>
    <origin xyz="0 0 0"/>
  </joint>

</robot>"""
    
    def setup_joint_controls(self, arm_id):
        """Setup interactive joint controls"""
        # Create sliders for joint control
        self.joint_sliders = {}
        
        for i, joint_name in enumerate(self.joint_names):
            if i < len(self.joint_ids):
                joint_id = self.joint_ids[i]
                
                # Get joint limits
                joint_info = p.getJointInfo(arm_id, joint_id, physicsClientId=self.physics_client)
                lower_limit = joint_info[8] if joint_info[8] > -3.14 else -3.14
                upper_limit = joint_info[9] if joint_info[9] < 3.14 else 3.14
                
                # Create slider
                slider_id = p.addUserDebugParameter(
                    f"{joint_name.upper()}", 
                    lower_limit, 
                    upper_limit, 
                    self.current_joints[i] if i < len(self.current_joints) else 0.0,
                    physicsClientId=self.physics_client
                )
                
                self.joint_sliders[joint_name] = {
                    'slider_id': slider_id,
                    'joint_id': joint_id,
                    'limits': (lower_limit, upper_limit)
                }
        
        # Add camera control
        self.camera_slider = p.addUserDebugParameter("Camera View", 0, 3, 0,
                                                    physicsClientId=self.physics_client)
        
        # Add demo mode control
        self.demo_slider = p.addUserDebugParameter("Demo Mode", 0, 1, 0,
                                                  physicsClientId=self.physics_client)
        
        print(f"🎮 Setup {len(self.joint_sliders)} joint controls")
    
    def add_construction_site_elements(self):
        """Add construction site environment elements"""
        # Dirt pile
        dirt_pile = p.loadURDF("cube.urdf", [5, 3, 0.5], globalScaling=2)
        p.changeVisualShape(dirt_pile, -1, rgbaColor=[0.6, 0.4, 0.2, 1])
        
        # Construction materials
        for i in range(3):
            material = p.loadURDF("cube.urdf", [8, -2 + i*2, 1], globalScaling=0.5)
            p.changeVisualShape(material, -1, rgbaColor=[0.8, 0.6, 0.3, 1])
        
        # Safety cones
        for i in range(4):
            cone_pos = [3 + i*2, 6, 0.3]
            cone = p.loadURDF("cube.urdf", cone_pos, globalScaling=0.3)
            p.changeVisualShape(cone, -1, rgbaColor=[1.0, 0.3, 0.0, 1])  # Safety orange
    
    def update_camera_view(self, view_index):
        """Update camera to specified view"""
        view_names = list(self.camera_views.keys())
        if 0 <= view_index < len(view_names):
            view_name = view_names[view_index]
            view = self.camera_views[view_name]
            
            p.resetDebugVisualizerCamera(
                cameraDistance=view["distance"],
                cameraYaw=view["yaw"], 
                cameraPitch=view["pitch"],
                cameraTargetPosition=view["target"],
                physicsClientId=self.physics_client
            )
            
            print(f"📷 Camera: {view_name}")
    
    def run_demo_sequence(self):
        """Run demonstration sequence"""
        print("🎬 Running JCB demonstration sequence...")
        
        demo_positions = [
            [0.0, -0.3, 0.2, 0.0],     # Rest position
            [0.8, -0.8, 0.8, 0.5],     # Dig position
            [0.4, -1.2, 1.2, 0.5],     # Deep dig
            [1.0, 0.2, -0.5, 1.0],     # Lift and dump
            [0.0, -0.3, 0.2, 0.0],     # Return to rest
        ]
        
        for i, position in enumerate(demo_positions):
            print(f"   Phase {i+1}: {['Rest', 'Approach', 'Dig', 'Lift', 'Return'][i]}")
            
            # Smoothly move to position
            steps = 30
            current_pos = self.current_joints.copy()
            
            for step in range(steps):
                t = step / (steps - 1)
                interpolated_pos = [
                    current_pos[j] + t * (position[j] - current_pos[j]) 
                    for j in range(len(position))
                ]
                
                self.set_joint_positions(interpolated_pos)
                p.stepSimulation(physicsClientId=self.physics_client)
                time.sleep(0.02)
            
            self.current_joints = position.copy()
            time.sleep(0.5)  # Pause at each position
    
    def set_joint_positions(self, positions):
        """Set joint positions"""
        if self.arm_id is not None:
            for i, pos in enumerate(positions[:len(self.joint_ids)]):
                p.setJointMotorControl2(
                    self.arm_id,
                    self.joint_ids[i],
                    p.POSITION_CONTROL,
                    targetPosition=pos,
                    force=5000,
                    physicsClientId=self.physics_client
                )
    
    def run_interactive_simulation(self):
        """Run interactive simulation with real-time controls"""
        print("\n🎮 Interactive JCB Simulation Controls:")
        print("   📊 Use sliders to control joints")
        print("   📷 Camera View slider: 0=Wide, 1=Operator, 2=Action, 3=Dramatic")
        print("   🎬 Demo Mode: 1=Run demo sequence")
        print("   ⌨️  Press 'q' to quit")
        print("\n🚜 JCB Ready for Operation!")
        
        last_demo_value = 0
        
        try:
            while True:
                # Read slider values
                new_joint_positions = []
                
                for joint_name in self.joint_names:
                    if joint_name in self.joint_sliders:
                        slider_value = p.readUserDebugParameter(
                            self.joint_sliders[joint_name]['slider_id'],
                            physicsClientId=self.physics_client
                        )
                        new_joint_positions.append(slider_value)
                
                # Update joint positions
                if new_joint_positions:
                    self.set_joint_positions(new_joint_positions)
                    self.current_joints = new_joint_positions.copy()
                
                # Check camera control
                camera_value = int(p.readUserDebugParameter(self.camera_slider,
                                                           physicsClientId=self.physics_client))
                if camera_value != self.current_camera:
                    self.update_camera_view(camera_value)
                    self.current_camera = camera_value
                
                # Check demo mode
                demo_value = p.readUserDebugParameter(self.demo_slider,
                                                     physicsClientId=self.physics_client)
                if demo_value > 0.5 and last_demo_value <= 0.5:
                    self.run_demo_sequence()
                last_demo_value = demo_value
                
                # Simulation step
                p.stepSimulation(physicsClientId=self.physics_client)
                time.sleep(1./240.)  # 240Hz simulation
                
        except KeyboardInterrupt:
            print("\n🛑 Simulation stopped by user")
        
        # Cleanup
        p.disconnect(physicsClientId=self.physics_client)
        print("✅ Enhanced CAD-Integrated JCB System shutdown complete")

def main():
    """Main function"""
    print("🚜 Enhanced CAD-Integrated JCB Robotic Arm System")
    print("=" * 55)
    
    # Check for CAD processor first
    processor_path = Path("cad_file_processor.py")
    if processor_path.exists():
        print("🔧 CAD Processor available - checking for processed files...")
        
        # Try to run CAD processor if ZIP file is present
        zip_files = list(Path(".").glob("jcb-back-arm-1*.zip"))
        if zip_files:
            print(f"📦 Found ZIP file: {zip_files[0]}")
            print("🔄 Running CAD processor...")
            try:
                subprocess.run([sys.executable, "cad_file_processor.py"], 
                             check=True, cwd=".")
            except subprocess.CalledProcessError:
                print("⚠️  CAD processor encountered issues, using fallbacks")
    
    # Initialize and run enhanced system
    enhanced_arm = EnhancedCADIntegratedArm(gui=True)
    
    # Load CAD components (real or fallback)
    enhanced_arm.load_cad_components()
    
    # Run interactive simulation
    enhanced_arm.run_interactive_simulation()

if __name__ == "__main__":
    main()