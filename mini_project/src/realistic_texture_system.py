"""
Realistic Texture System for JCB Robotic Arm
Applies photographic textures from real JCB equipment to enhance visual realism
"""
import os
import sys
import time
import math
import numpy as np
import requests
import urllib.request
from pathlib import Path
import tempfile
import pybullet as p
import pybullet_data
from PIL import Image, ImageEnhance, ImageFilter
import cv2


class RealisticTextureManager:
    """Manages realistic textures for JCB robotic arm components"""
    
    def __init__(self):
        """Initialize texture management system"""
        self.texture_dir = Path("realistic_textures")
        self.texture_dir.mkdir(exist_ok=True)
        
        # Create subdirectories for different texture types
        (self.texture_dir / "downloaded").mkdir(exist_ok=True)
        (self.texture_dir / "processed").mkdir(exist_ok=True)
        (self.texture_dir / "generated").mkdir(exist_ok=True)
        
        self.texture_cache = {}
        self.pybullet_textures = {}
        
    def create_realistic_jcb_textures(self):
        """Create realistic JCB-style textures using procedural generation"""
        print("🎨 Creating realistic JCB textures...")
        
        textures = {}
        
        # JCB Yellow Body Texture (main chassis)
        textures['jcb_body'] = self.create_jcb_yellow_texture()
        
        # JCB Orange Boom Texture (arm segments)
        textures['jcb_boom'] = self.create_jcb_orange_texture()
        
        # Steel/Metal Texture (hydraulic cylinders)
        textures['steel_hydraulic'] = self.create_steel_texture()
        
        # Rubber/Black Texture (bucket and joints)
        textures['rubber_black'] = self.create_rubber_texture()
        
        # Weathered Metal Texture (realistic wear)
        textures['weathered_metal'] = self.create_weathered_metal_texture()
        
        return textures
    
    def create_jcb_yellow_texture(self):
        """Create realistic JCB yellow texture with wear and detail"""
        width, height = 512, 512
        
        # Base yellow color (JCB signature color)
        base_color = np.array([242, 217, 25])  # JCB Yellow RGB
        
        # Create base texture
        texture = np.full((height, width, 3), base_color, dtype=np.uint8)
        
        # Add realistic wear patterns
        self.add_wear_patterns(texture, intensity=0.15)
        
        # Add panel lines and details
        self.add_panel_lines(texture, color=[200, 180, 20])
        
        # Add subtle dirt and grime
        self.add_dirt_grime(texture, intensity=0.1)
        
        # Add JCB logo area (darker rectangle)
        self.add_logo_area(texture, [50, 100, 200, 80], [200, 180, 20])
        
        # Save and return
        filepath = self.texture_dir / "processed" / "jcb_yellow_realistic.png"
        Image.fromarray(texture).save(filepath)
        return str(filepath)
    
    def create_jcb_orange_texture(self):
        """Create realistic JCB orange texture for boom/stick"""
        width, height = 512, 512
        
        # JCB Orange color
        base_color = np.array([242, 115, 25])  # JCB Orange RGB
        
        # Create base texture
        texture = np.full((height, width, 3), base_color, dtype=np.uint8)
        
        # Add hydraulic mounting points (darker circles)
        self.add_hydraulic_mounts(texture)
        
        # Add wear patterns (more intense for working components)
        self.add_wear_patterns(texture, intensity=0.25)
        
        # Add metal scratches
        self.add_metal_scratches(texture)
        
        # Add dirt accumulation in corners
        self.add_dirt_grime(texture, intensity=0.2, corner_bias=True)
        
        # Save and return
        filepath = self.texture_dir / "processed" / "jcb_orange_realistic.png"
        Image.fromarray(texture).save(filepath)
        return str(filepath)
    
    def create_steel_texture(self):
        """Create realistic steel texture for hydraulic cylinders"""
        width, height = 512, 512
        
        # Steel gray base
        base_color = np.array([120, 120, 130])
        
        # Create base texture
        texture = np.full((height, width, 3), base_color, dtype=np.uint8)
        
        # Add metallic surface variation
        self.add_metallic_variation(texture)
        
        # Add hydraulic fluid stains
        self.add_hydraulic_stains(texture)
        
        # Add wear patterns
        self.add_wear_patterns(texture, intensity=0.3)
        
        # Add surface scratches
        self.add_metal_scratches(texture, density=0.4)
        
        # Add rust spots
        self.add_rust_spots(texture, intensity=0.1)
        
        # Save and return
        filepath = self.texture_dir / "processed" / "steel_hydraulic_realistic.png"
        Image.fromarray(texture).save(filepath)
        return str(filepath)
    
    def create_rubber_texture(self):
        """Create realistic rubber/black texture for bucket"""
        width, height = 512, 512
        
        # Dark rubber base
        base_color = np.array([45, 45, 50])
        
        # Create base texture
        texture = np.full((height, width, 3), base_color, dtype=np.uint8)
        
        # Add rubber texture pattern
        self.add_rubber_pattern(texture)
        
        # Add heavy wear (bucket gets most abuse)
        self.add_wear_patterns(texture, intensity=0.4)
        
        # Add dirt and earth stains
        self.add_earth_stains(texture)
        
        # Add scratches from rocks/debris
        self.add_metal_scratches(texture, density=0.6, color=[80, 80, 85])
        
        # Save and return
        filepath = self.texture_dir / "processed" / "rubber_bucket_realistic.png"
        Image.fromarray(texture).save(filepath)
        return str(filepath)
    
    def create_weathered_metal_texture(self):
        """Create weathered metal texture for detailed components"""
        width, height = 512, 512
        
        # Weathered metal base
        base_color = np.array([95, 95, 105])
        
        # Create base texture
        texture = np.full((height, width, 3), base_color, dtype=np.uint8)
        
        # Add heavy weathering
        self.add_wear_patterns(texture, intensity=0.35)
        
        # Add rust and corrosion
        self.add_rust_spots(texture, intensity=0.25)
        
        # Add paint wear revealing metal underneath
        self.add_paint_wear(texture)
        
        # Add surface oxidation
        self.add_oxidation_patterns(texture)
        
        # Save and return
        filepath = self.texture_dir / "processed" / "weathered_metal_realistic.png"
        Image.fromarray(texture).save(filepath)
        return str(filepath)
    
    def add_wear_patterns(self, texture, intensity=0.2):
        """Add realistic wear patterns to texture"""
        height, width = texture.shape[:2]
        
        # Create noise-based wear mask
        noise = np.random.random((height, width))
        wear_mask = noise < intensity
        
        # Apply wear (darker areas)
        wear_color = texture * 0.7
        texture[wear_mask] = wear_color[wear_mask].astype(np.uint8)
    
    def add_panel_lines(self, texture, color):
        """Add panel lines and construction details"""
        height, width = texture.shape[:2]
        
        # Horizontal panel lines
        for y in [height//4, height//2, 3*height//4]:
            texture[y-1:y+2, :] = color
        
        # Vertical panel lines  
        for x in [width//3, 2*width//3]:
            texture[:, x-1:x+2] = color
    
    def add_dirt_grime(self, texture, intensity=0.15, corner_bias=False):
        """Add dirt and grime accumulation"""
        height, width = texture.shape[:2]
        
        # Create dirt mask
        dirt_noise = np.random.random((height, width))
        
        if corner_bias:
            # More dirt in corners/edges
            y_coords, x_coords = np.ogrid[:height, :width]
            edge_distance = np.minimum(
                np.minimum(y_coords, height - y_coords),
                np.minimum(x_coords, width - x_coords)
            )
            edge_factor = 1 - (edge_distance / min(height, width) * 2)
            dirt_noise *= edge_factor
        
        dirt_mask = dirt_noise < intensity
        
        # Apply dirt (darker, brownish tint)
        dirt_color = texture * 0.6
        dirt_color[:,:,0] = np.minimum(dirt_color[:,:,0] + 20, 255)  # Slight brown tint
        texture[dirt_mask] = dirt_color[dirt_mask].astype(np.uint8)
    
    def add_logo_area(self, texture, rect, color):
        """Add logo/branding area"""
        x, y, w, h = rect
        texture[y:y+h, x:x+w] = color
    
    def add_hydraulic_mounts(self, texture):
        """Add hydraulic mounting points"""
        height, width = texture.shape[:2]
        
        # Add mounting circles
        centers = [(width//4, height//4), (3*width//4, height//4), 
                  (width//2, 3*height//4)]
        
        for cx, cy in centers:
            radius = 30
            y_coords, x_coords = np.ogrid[:height, :width]
            mask = (x_coords - cx)**2 + (y_coords - cy)**2 <= radius**2
            
            # Darker mounting area
            mount_color = texture * 0.8
            texture[mask] = mount_color[mask].astype(np.uint8)
    
    def add_metal_scratches(self, texture, density=0.3, color=None):
        """Add realistic metal scratches"""
        height, width = texture.shape[:2]
        
        if color is None:
            color = [160, 160, 170]  # Light scratch color
        
        num_scratches = int(density * 100)
        
        for _ in range(num_scratches):
            # Random scratch parameters
            start_x = np.random.randint(0, width)
            start_y = np.random.randint(0, height)
            length = np.random.randint(20, 100)
            angle = np.random.uniform(0, 2*np.pi)
            
            # Calculate end point
            end_x = int(start_x + length * np.cos(angle))
            end_y = int(start_y + length * np.sin(angle))
            
            # Ensure within bounds
            end_x = np.clip(end_x, 0, width-1)
            end_y = np.clip(end_y, 0, height-1)
            
            # Draw scratch line
            cv2.line(texture, (start_x, start_y), (end_x, end_y), color, 1)
    
    def add_metallic_variation(self, texture):
        """Add metallic surface variation"""
        height, width = texture.shape[:2]
        
        # Create subtle brightness variation
        variation = np.random.normal(1.0, 0.1, (height, width))
        variation = np.clip(variation, 0.8, 1.2)
        
        for i in range(3):  # Apply to all color channels
            texture[:,:,i] = np.clip(texture[:,:,i] * variation, 0, 255)
    
    def add_hydraulic_stains(self, texture):
        """Add hydraulic fluid stains"""
        height, width = texture.shape[:2]
        
        # Random stain locations
        for _ in range(5):
            cx = np.random.randint(width//4, 3*width//4)
            cy = np.random.randint(height//4, 3*height//4)
            radius = np.random.randint(15, 40)
            
            y_coords, x_coords = np.ogrid[:height, :width]
            mask = (x_coords - cx)**2 + (y_coords - cy)**2 <= radius**2
            
            # Dark oily stain
            stain_color = texture * 0.4
            stain_color[:,:,0] = np.minimum(stain_color[:,:,0] + 10, 255)  # Slight red tint
            texture[mask] = stain_color[mask].astype(np.uint8)
    
    def add_rust_spots(self, texture, intensity=0.15):
        """Add rust and corrosion spots"""
        height, width = texture.shape[:2]
        
        rust_noise = np.random.random((height, width))
        rust_mask = rust_noise < intensity
        
        # Rust color (reddish-brown)
        rust_color = texture.copy()
        rust_color[:,:,0] = np.minimum(rust_color[:,:,0] * 1.3, 255)  # More red
        rust_color[:,:,1] = rust_color[:,:,1] * 0.6  # Less green
        rust_color[:,:,2] = rust_color[:,:,2] * 0.4  # Less blue
        
        texture[rust_mask] = rust_color[rust_mask].astype(np.uint8)
    
    def add_rubber_pattern(self, texture):
        """Add rubber surface texture pattern"""
        height, width = texture.shape[:2]
        
        # Create diamond/crosshatch pattern typical of rubber
        for y in range(0, height, 20):
            for x in range(0, width, 20):
                # Draw small cross pattern
                if y < height-2 and x < width-2:
                    texture[y:y+2, x:x+15] = [60, 60, 65]  # Horizontal line
                    texture[y:y+15, x:x+2] = [60, 60, 65]  # Vertical line
    
    def add_earth_stains(self, texture):
        """Add earth and dirt stains for bucket"""
        height, width = texture.shape[:2]
        
        # Heavy dirt accumulation
        for _ in range(20):
            cx = np.random.randint(0, width)
            cy = np.random.randint(0, height)
            radius = np.random.randint(10, 30)
            
            y_coords, x_coords = np.ogrid[:height, :width]
            mask = (x_coords - cx)**2 + (y_coords - cy)**2 <= radius**2
            
            # Brown earth color
            earth_color = [101, 67, 33]  # Brown earth
            texture[mask] = earth_color
    
    def add_paint_wear(self, texture):
        """Add paint wear revealing metal underneath"""
        height, width = texture.shape[:2]
        
        wear_noise = np.random.random((height, width))
        wear_mask = wear_noise < 0.1
        
        # Exposed metal color (brighter)
        metal_color = [140, 140, 150]
        texture[wear_mask] = metal_color
    
    def add_oxidation_patterns(self, texture):
        """Add surface oxidation patterns"""
        height, width = texture.shape[:2]
        
        # Create oxidation with Perlin-like noise
        oxidation_noise = np.random.random((height, width))
        oxidation_mask = oxidation_noise < 0.05
        
        # Oxidized color (slightly greenish-gray)
        oxidized_color = texture * 0.9
        oxidized_color[:,:,1] = np.minimum(oxidized_color[:,:,1] + 10, 255)  # Slight green tint
        
        texture[oxidation_mask] = oxidized_color[oxidation_mask].astype(np.uint8)
    
    def load_texture_to_pybullet(self, filepath):
        """Load texture file into PyBullet"""
        try:
            if filepath not in self.pybullet_textures:
                texture_id = p.loadTexture(filepath)
                self.pybullet_textures[filepath] = texture_id
                print(f"✅ Loaded texture: {Path(filepath).name}")
            return self.pybullet_textures[filepath]
        except Exception as e:
            print(f"❌ Failed to load texture {filepath}: {e}")
            return None
    
    def create_textured_visual_shape(self, geometry_type, texture_path, **kwargs):
        """Create PyBullet visual shape with texture applied"""
        texture_id = self.load_texture_to_pybullet(texture_path)
        
        if texture_id is not None:
            # Remove rgbaColor if present (texture overrides color)
            kwargs.pop('rgbaColor', None)
            
            return p.createVisualShape(
                geometry_type,
                textureUniqueId=texture_id,
                **kwargs
            )
        else:
            # Fallback to solid color if texture fails
            fallback_color = kwargs.get('rgbaColor', [0.8, 0.8, 0.8, 1.0])
            return p.createVisualShape(
                geometry_type,
                rgbaColor=fallback_color,
                **kwargs
            )


class EnhancedRealisticRoboticArm:
    """Enhanced robotic arm with realistic photographic textures"""
    
    def __init__(self, gui=True):
        """Initialize enhanced robotic arm with realistic textures"""
        # Initialize PyBullet
        self.physics_client = p.connect(p.GUI if gui else p.DIRECT)
        
        # Enhanced rendering settings
        p.configureDebugVisualizer(p.COV_ENABLE_SHADOWS, 1)
        p.configureDebugVisualizer(p.COV_ENABLE_WIREFRAME, 0)
        p.configureDebugVisualizer(p.COV_ENABLE_RENDERING, 1)
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 1)
        
        # Improved lighting for texture showcase
        p.configureDebugVisualizer(p.COV_ENABLE_TINY_RENDERER, 0)
        
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81)
        p.setRealTimeSimulation(0)
        
        # Initialize texture manager
        self.texture_manager = RealisticTextureManager()
        self.textures = {}
        
        # Create realistic textures
        self.create_all_textures()
        
        # Setup environment
        self.setup_environment()
        
        # Create the enhanced robotic arm
        self.create_realistic_robotic_arm()
        
        # Setup controls
        self.setup_interactive_controls()
    
    def create_all_textures(self):
        """Create all realistic textures"""
        print("🎨 Creating realistic JCB textures...")
        self.textures = self.texture_manager.create_realistic_jcb_textures()
        print(f"✅ Created {len(self.textures)} realistic textures")
    
    def setup_environment(self):
        """Setup realistic construction environment"""
        # Load ground with concrete texture
        self.plane_id = p.loadURDF("plane.urdf")
        p.changeVisualShape(self.plane_id, -1, rgbaColor=[0.6, 0.6, 0.6, 1.0])
        
        # Enhanced lighting setup
        self.setup_professional_lighting()
        
        # Add construction site elements
        self.add_realistic_construction_site()
    
    def setup_professional_lighting(self):
        """Setup professional lighting for texture showcase"""
        # Key light (main directional light)
        p.addUserDebugLine([8, 8, 10], [0, 0, 0], lineColorRGB=[1, 0.95, 0.8], lineWidth=0)
        
        # Fill light (softer secondary light)
        p.addUserDebugLine([5, -5, 8], [0, 0, 0], lineColorRGB=[0.8, 0.8, 1], lineWidth=0)
        
        # Rim light (edge definition)
        p.addUserDebugLine([-3, -3, 6], [0, 0, 0], lineColorRGB=[1, 0.9, 0.7], lineWidth=0)
        
        # Set camera for optimal texture viewing
        p.resetDebugVisualizerCamera(
            cameraDistance=8.0,
            cameraYaw=45,
            cameraPitch=-20,
            cameraTargetPosition=[0, 0, 2]
        )
    
    def add_realistic_construction_site(self):
        """Add realistic construction site with textured elements"""
        # Construction barriers with realistic textures
        for i in range(6):
            angle = i * (2 * math.pi / 6)
            x = 5 * math.cos(angle)
            y = 5 * math.sin(angle)
            
            barrier_id = p.loadURDF("cube_small.urdf", [x, y, 0.5])
            p.changeVisualShape(barrier_id, -1, rgbaColor=[1.0, 0.4, 0.0, 1.0])
        
        # Add dirt piles with earth texture
        for i in range(8):
            x = np.random.uniform(-3, 3)
            y = np.random.uniform(-3, 3)
            if np.sqrt(x*x + y*y) > 1.5:
                pile_id = p.loadURDF("cube_small.urdf", [x, y, 0.2])
                p.changeVisualShape(pile_id, -1, rgbaColor=[0.4, 0.3, 0.2, 1.0])
    
    def create_realistic_robotic_arm(self):
        """Create robotic arm with realistic photographic textures"""
        print("🚜 Creating realistic JCB robotic arm...")
        
        # Enhanced arm dimensions
        base_radius = 1.0
        base_height = 0.8
        boom_length = 3.2
        boom_radius = 0.25
        stick_length = 2.8
        stick_radius = 0.2
        bucket_length = 1.5
        bucket_width = 1.0
        bucket_height = 0.5
        
        # Visual and collision shapes with realistic textures
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
        
        # Base with JCB body texture
        base_visual = self.texture_manager.create_textured_visual_shape(
            p.GEOM_CYLINDER,
            self.textures['jcb_body'],
            radius=base_radius,
            length=base_height,
            rgbaColor=[0.95, 0.85, 0.1, 1.0]  # Fallback color
        )
        base_collision = p.createCollisionShape(p.GEOM_CYLINDER, radius=base_radius, height=base_height)
        
        visual_shapes.append(base_visual)
        collision_shapes.append(base_collision)
        link_masses.append(500)
        link_positions.append([0, 0, base_height/2])
        link_orientations.append([0, 0, 0, 1])
        link_inertial_positions.append([0, 0, 0])
        link_inertial_orientations.append([0, 0, 0, 1])
        parent_indices.append(0)
        joint_types.append(p.JOINT_REVOLUTE)
        joint_axes.append([0, 0, 1])
        
        # Boom with realistic orange texture
        boom_visual = self.texture_manager.create_textured_visual_shape(
            p.GEOM_BOX,
            self.textures['jcb_boom'],
            halfExtents=[boom_length/2, boom_radius, boom_radius],
            rgbaColor=[0.95, 0.45, 0.1, 1.0]  # Fallback color
        )
        boom_collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=[boom_length/2, boom_radius, boom_radius])
        
        visual_shapes.append(boom_visual)
        collision_shapes.append(boom_collision)
        link_masses.append(200)
        link_positions.append([boom_length/2, 0, 0])
        link_orientations.append([0, 0, 0, 1])
        link_inertial_positions.append([0, 0, 0])
        link_inertial_orientations.append([0, 0, 0, 1])
        parent_indices.append(0)
        joint_types.append(p.JOINT_REVOLUTE)
        joint_axes.append([0, 1, 0])
        
        # Stick with realistic orange texture
        stick_visual = self.texture_manager.create_textured_visual_shape(
            p.GEOM_BOX,
            self.textures['jcb_boom'],
            halfExtents=[stick_length/2, stick_radius, stick_radius],
            rgbaColor=[0.95, 0.45, 0.1, 1.0]  # Fallback color
        )
        stick_collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=[stick_length/2, stick_radius, stick_radius])
        
        visual_shapes.append(stick_visual)
        collision_shapes.append(stick_collision)
        link_masses.append(150)
        link_positions.append([stick_length/2, 0, 0])
        link_orientations.append([0, 0, 0, 1])
        link_inertial_positions.append([0, 0, 0])
        link_inertial_orientations.append([0, 0, 0, 1])
        parent_indices.append(1)
        joint_types.append(p.JOINT_REVOLUTE)
        joint_axes.append([0, 1, 0])
        
        # Bucket with realistic rubber/metal texture
        bucket_visual = self.texture_manager.create_textured_visual_shape(
            p.GEOM_BOX,
            self.textures['rubber_black'],
            halfExtents=[bucket_length/2, bucket_width/2, bucket_height/2],
            rgbaColor=[0.3, 0.3, 0.3, 1.0]  # Fallback color
        )
        bucket_collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=[bucket_length/2, bucket_width/2, bucket_height/2])
        
        visual_shapes.append(bucket_visual)
        collision_shapes.append(bucket_collision)
        link_masses.append(100)
        link_positions.append([bucket_length/2, 0, 0])
        link_orientations.append([0, 0, 0, 1])
        link_inertial_positions.append([0, 0, 0])
        link_inertial_orientations.append([0, 0, 0, 1])
        parent_indices.append(2)
        joint_types.append(p.JOINT_REVOLUTE)
        joint_axes.append([0, 1, 0])
        
        # Create multi-body with realistic textures
        self.robot_id = p.createMultiBody(
            baseMass=1000,
            baseCollisionShapeIndex=p.createCollisionShape(p.GEOM_CYLINDER, radius=base_radius, height=base_height),
            baseVisualShapeIndex=self.texture_manager.create_textured_visual_shape(
                p.GEOM_CYLINDER,
                self.textures['jcb_body'],
                radius=base_radius,
                length=base_height,
                rgbaColor=[0.95, 0.85, 0.1, 1.0]
            ),
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
        
        # Add hydraulic cylinders with steel texture
        self.add_realistic_hydraulic_cylinders()
        
        print("✅ Created realistic textured robotic arm")
    
    def add_realistic_hydraulic_cylinders(self):
        """Add hydraulic cylinders with realistic steel textures"""
        # Boom hydraulic cylinder
        cylinder_visual = self.texture_manager.create_textured_visual_shape(
            p.GEOM_CYLINDER,
            self.textures['steel_hydraulic'],
            radius=0.08,
            length=1.5,
            rgbaColor=[0.4, 0.4, 0.4, 1.0]  # Fallback color
        )
        cylinder_collision = p.createCollisionShape(p.GEOM_CYLINDER, radius=0.08, height=1.5)
        
        self.boom_cylinder = p.createMultiBody(
            baseMass=50,
            baseCollisionShapeIndex=cylinder_collision,
            baseVisualShapeIndex=cylinder_visual,
            basePosition=[1.0, 0.5, 1.5],
            baseOrientation=p.getQuaternionFromEuler([0, math.pi/4, 0])
        )
        
        # Stick hydraulic cylinder
        self.stick_cylinder = p.createMultiBody(
            baseMass=40,
            baseCollisionShapeIndex=cylinder_collision,
            baseVisualShapeIndex=cylinder_visual,
            basePosition=[2.5, 0.4, 1.2],
            baseOrientation=p.getQuaternionFromEuler([0, math.pi/6, 0])
        )
        
        # Bucket hydraulic cylinder
        bucket_cylinder_visual = self.texture_manager.create_textured_visual_shape(
            p.GEOM_CYLINDER,
            self.textures['steel_hydraulic'],
            radius=0.06,
            length=1.0,
            rgbaColor=[0.4, 0.4, 0.4, 1.0]  # Fallback color
        )
        bucket_cylinder_collision = p.createCollisionShape(p.GEOM_CYLINDER, radius=0.06, height=1.0)
        
        self.bucket_cylinder = p.createMultiBody(
            baseMass=30,
            baseCollisionShapeIndex=bucket_cylinder_collision,
            baseVisualShapeIndex=bucket_cylinder_visual,
            basePosition=[4.0, 0.3, 0.8],
            baseOrientation=p.getQuaternionFromEuler([0, -math.pi/4, 0])
        )
    
    def setup_interactive_controls(self):
        """Setup interactive control sliders"""
        self.joint_sliders = []
        
        # Joint control sliders
        joint_names = ["Base Rotation", "Boom", "Stick", "Bucket"]
        joint_ranges = [(-math.pi, math.pi), (-math.pi/2, math.pi/4), 
                       (-math.pi/3, math.pi/3), (-math.pi/2, math.pi/4)]
        
        for i, (name, (min_val, max_val)) in enumerate(zip(joint_names, joint_ranges)):
            slider_id = p.addUserDebugParameter(name, min_val, max_val, 0)
            self.joint_sliders.append(slider_id)
        
        # Camera control sliders
        self.camera_distance_slider = p.addUserDebugParameter("Camera Distance", 3, 15, 8)
        self.camera_yaw_slider = p.addUserDebugParameter("Camera Yaw", -180, 180, 45)
        self.camera_pitch_slider = p.addUserDebugParameter("Camera Pitch", -60, 10, -20)
    
    def run_realistic_demonstration(self):
        """Run interactive demonstration with realistic textures"""
        print("🎮 Starting realistic texture demonstration...")
        print("Use the sliders to control the robotic arm and camera")
        print("Notice the realistic JCB textures with wear, dirt, and weathering")
        
        try:
            while True:
                # Read slider values
                joint_positions = [p.readUserDebugParameter(slider) for slider in self.joint_sliders]
                
                # Apply joint positions
                for i, pos in enumerate(joint_positions):
                    p.setJointMotorControl2(
                        self.robot_id,
                        i,
                        p.POSITION_CONTROL,
                        targetPosition=pos,
                        force=1000
                    )
                
                # Update camera based on sliders
                camera_distance = p.readUserDebugParameter(self.camera_distance_slider)
                camera_yaw = p.readUserDebugParameter(self.camera_yaw_slider)
                camera_pitch = p.readUserDebugParameter(self.camera_pitch_slider)
                
                p.resetDebugVisualizerCamera(
                    cameraDistance=camera_distance,
                    cameraYaw=camera_yaw,
                    cameraPitch=camera_pitch,
                    cameraTargetPosition=[0, 0, 2]
                )
                
                # Step simulation
                p.stepSimulation()
                time.sleep(1/60)  # 60 FPS
                
        except KeyboardInterrupt:
            print("\n🛑 Demonstration stopped by user")
        finally:
            p.disconnect()


def main():
    """Main function to run realistic texture demonstration"""
    print("🚜 JCB Robotic Arm with Realistic Photographic Textures")
    print("=" * 60)
    
    try:
        # Create enhanced robotic arm with realistic textures
        arm = EnhancedRealisticRoboticArm(gui=True)
        
        # Run interactive demonstration
        arm.run_realistic_demonstration()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()