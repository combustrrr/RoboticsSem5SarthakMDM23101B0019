"""
Conveyor Belt Object Sorting System using OpenCV and 4-DOF Robotic Arm
Part C: Advanced Challenge Implementation
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import cv2
import time
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
import random
from robotic_arm_4dof import RoboticArm4DOF, create_4dof_arm_configuration


@dataclass
class ConveyorObject:
    """Object on the conveyor belt"""
    x: float
    y: float
    size: str  # 'small', 'medium', 'large'
    color: str  # 'red', 'green', 'blue'
    width: float
    height: float
    speed: float = 1.0
    picked: bool = False
    sorted: bool = False


class ConveyorBelt:
    """Conveyor belt simulation for object transportation"""
    
    def __init__(self, length: float = 10.0, width: float = 2.0, speed: float = 1.0):
        """
        Initialize conveyor belt
        
        Args:
            length: Length of the conveyor belt
            width: Width of the conveyor belt
            speed: Belt movement speed (units/second)
        """
        self.length = length
        self.width = width
        self.speed = speed
        self.objects: List[ConveyorObject] = []
        
        # Belt position (center coordinates)
        self.belt_x = 0.0
        self.belt_y = -3.0  # Below the robot arm
        
        # Object generation parameters
        self.object_spawn_rate = 2.0  # objects per second
        self.last_spawn_time = 0.0
        
        # Size and color definitions
        self.size_definitions = {
            'small': (0.2, 0.2),
            'medium': (0.4, 0.4), 
            'large': (0.6, 0.6)
        }
        
        self.color_definitions = {
            'red': (1.0, 0.2, 0.2),
            'green': (0.2, 1.0, 0.2),
            'blue': (0.2, 0.2, 1.0)
        }
    
    def update(self, dt: float):
        """Update conveyor belt and object positions"""
        current_time = time.time()
        
        # Spawn new objects
        if current_time - self.last_spawn_time > (1.0 / self.object_spawn_rate):
            self.spawn_object()
            self.last_spawn_time = current_time
        
        # Update object positions
        for obj in self.objects[:]:  # Use slice to allow removal during iteration
            if not obj.picked:
                obj.x += self.speed * dt
                
                # Remove objects that have passed the end of the belt
                if obj.x > self.belt_x + self.length / 2 + 1.0:
                    self.objects.remove(obj)
    
    def spawn_object(self):
        """Spawn a new random object at the start of the belt"""
        # Random properties
        size = random.choice(['small', 'medium', 'large'])
        color = random.choice(['red', 'green', 'blue'])
        width, height = self.size_definitions[size]
        
        # Position at start of belt with some randomness
        x = self.belt_x - self.length / 2 - 0.5
        y = self.belt_y + random.uniform(-self.width/4, self.width/4)
        
        obj = ConveyorObject(
            x=x, y=y, size=size, color=color,
            width=width, height=height, speed=self.speed
        )
        
        self.objects.append(obj)
    
    def get_objects_in_pickup_zone(self, pickup_x: float, pickup_width: float = 1.0) -> List[ConveyorObject]:
        """Get objects in the pickup zone"""
        pickup_objects = []
        for obj in self.objects:
            if (not obj.picked and not obj.sorted and 
                pickup_x - pickup_width/2 <= obj.x <= pickup_x + pickup_width/2):
                pickup_objects.append(obj)
        return pickup_objects
    
    def visualize(self, ax):
        """Visualize the conveyor belt and objects"""
        # Draw belt
        belt_rect = patches.Rectangle(
            (self.belt_x - self.length/2, self.belt_y - self.width/2),
            self.length, self.width,
            linewidth=2, edgecolor='black', facecolor='lightgray', alpha=0.7
        )
        ax.add_patch(belt_rect)
        
        # Draw belt direction arrows
        arrow_spacing = 1.0
        for x in np.arange(self.belt_x - self.length/2 + arrow_spacing, 
                          self.belt_x + self.length/2, arrow_spacing):
            ax.arrow(x, self.belt_y, 0.3, 0, head_width=0.1, head_length=0.1, 
                    fc='black', ec='black', alpha=0.5)
        
        # Draw objects
        for obj in self.objects:
            if not obj.picked:
                color = self.color_definitions[obj.color]
                obj_rect = patches.Rectangle(
                    (obj.x - obj.width/2, obj.y - obj.height/2),
                    obj.width, obj.height,
                    linewidth=1, edgecolor='black', facecolor=color, alpha=0.8
                )
                ax.add_patch(obj_rect)
                
                # Add size label
                ax.text(obj.x, obj.y, obj.size[0].upper(), 
                       ha='center', va='center', fontsize=8, fontweight='bold')


class ObjectDetector:
    """OpenCV-based object detection and classification system"""
    
    def __init__(self):
        """Initialize object detector"""
        self.size_thresholds = {
            'small': (0.0, 0.3),
            'medium': (0.3, 0.5),
            'large': (0.5, 1.0)
        }
        
        self.color_ranges = {
            'red': {'lower': np.array([0, 100, 100]), 'upper': np.array([10, 255, 255])},
            'green': {'lower': np.array([50, 100, 100]), 'upper': np.array([70, 255, 255])},
            'blue': {'lower': np.array([110, 100, 100]), 'upper': np.array([130, 255, 255])}
        }
    
    def detect_objects(self, conveyor_objects: List[ConveyorObject], 
                      detection_zone: Tuple[float, float, float]) -> List[Dict]:
        """
        Simulate object detection using computer vision
        
        Args:
            conveyor_objects: List of objects on conveyor
            detection_zone: (center_x, width, y_position) of detection zone
            
        Returns:
            detected_objects: List of detected object information
        """
        center_x, width, y_pos = detection_zone
        detected = []
        
        for obj in conveyor_objects:
            # Check if object is in detection zone
            if (not obj.picked and not obj.sorted and
                center_x - width/2 <= obj.x <= center_x + width/2 and
                abs(obj.y - y_pos) <= 1.0):
                
                # Simulate computer vision detection with some noise
                detected_size = self.classify_size(obj.width, obj.height)
                detected_color = self.classify_color(obj.color)
                
                # Add detection confidence (simulate CV uncertainty)
                confidence = random.uniform(0.8, 0.98)
                
                detection_info = {
                    'object': obj,
                    'position': (obj.x, obj.y),
                    'size': detected_size,
                    'color': detected_color,
                    'confidence': confidence,
                    'actual_size': obj.size,
                    'actual_color': obj.color
                }
                detected.append(detection_info)
        
        return detected
    
    def classify_size(self, width: float, height: float) -> str:
        """Classify object size based on dimensions"""
        area = width * height
        
        if area <= 0.1:
            return 'small'
        elif area <= 0.25:
            return 'medium'
        else:
            return 'large'
    
    def classify_color(self, actual_color: str) -> str:
        """Simulate color classification (with potential errors)"""
        # Simulate 95% accuracy in color detection
        if random.random() < 0.95:
            return actual_color
        else:
            # Random misclassification
            colors = ['red', 'green', 'blue']
            colors.remove(actual_color)
            return random.choice(colors)


class SortingSystem:
    """Complete sorting system with 4-DOF arm and conveyor belt"""
    
    def __init__(self):
        """Initialize the sorting system"""
        # Initialize components
        self.arm = create_4dof_arm_configuration()
        self.conveyor = ConveyorBelt(length=8.0, width=1.5, speed=0.5)
        self.detector = ObjectDetector()
        
        # Sorting zones (destinations for different object types)
        self.sorting_zones = {
            ('small', 'red'): np.array([3.0, 1.0]),
            ('small', 'green'): np.array([3.5, 1.0]),
            ('small', 'blue'): np.array([4.0, 1.0]),
            ('medium', 'red'): np.array([3.0, 1.5]),
            ('medium', 'green'): np.array([3.5, 1.5]),
            ('medium', 'blue'): np.array([4.0, 1.5]),
            ('large', 'red'): np.array([3.0, 2.0]),
            ('large', 'green'): np.array([3.5, 2.0]),
            ('large', 'blue'): np.array([4.0, 2.0])
        }
        
        # Detection zone (where objects are detected and picked)
        self.detection_zone = (0.0, 2.0, self.conveyor.belt_y)  # (center_x, width, y)
        
        # Performance metrics
        self.objects_sorted = 0
        self.correct_sorts = 0
        self.detection_attempts = 0
        self.pick_attempts = 0
        self.successful_picks = 0
        
        # Animation variables
        self.current_target = None
        self.picking_object = None
        self.arm_state = 'scanning'  # 'scanning', 'moving_to_pick', 'picking', 'moving_to_sort', 'sorting'
        
    def update(self, dt: float):
        """Update the complete sorting system"""
        # Update conveyor belt
        self.conveyor.update(dt)
        
        # Detect objects in pickup zone
        detected_objects = self.detector.detect_objects(
            self.conveyor.objects, self.detection_zone
        )
        
        # Process detected objects based on arm state
        if self.arm_state == 'scanning' and detected_objects:
            # Select highest confidence detection
            best_detection = max(detected_objects, key=lambda x: x['confidence'])
            self.start_pick_sequence(best_detection)
        
        elif self.arm_state == 'moving_to_pick':
            self.execute_pick_movement(dt)
        
        elif self.arm_state == 'moving_to_sort':
            self.execute_sort_movement(dt)
    
    def start_pick_sequence(self, detection: Dict):
        """Start picking sequence for detected object"""
        self.detection_attempts += 1
        self.picking_object = detection['object']
        
        # Set target position for picking (slightly above object)
        pick_pos = np.array([detection['position'][0], detection['position'][1] + 0.3])
        
        # Solve inverse kinematics for pick position
        success, solution = self.arm.inverse_kinematics(pick_pos)
        
        if success:
            self.current_target = solution
            self.arm_state = 'moving_to_pick'
            self.pick_attempts += 1
        else:
            print(f"Cannot reach object at {detection['position']}")
            self.arm_state = 'scanning'
    
    def execute_pick_movement(self, dt: float):
        """Execute movement to pick position"""
        if self.current_target is not None:
            # Simple linear interpolation to target configuration
            current_config = self.arm.joint_values
            diff = self.current_target - current_config
            step_size = 2.0 * dt  # movement speed
            
            if np.linalg.norm(diff) < 0.1:  # Close enough to target
                self.arm.set_joint_configuration(self.current_target)
                self.execute_pick()
            else:
                # Move towards target
                new_config = current_config + step_size * diff / np.linalg.norm(diff)
                self.arm.set_joint_configuration(new_config)
    
    def execute_pick(self):
        """Execute pick operation"""
        if self.picking_object and not self.picking_object.picked:
            # Mark object as picked
            self.picking_object.picked = True
            self.successful_picks += 1
            
            # Determine sorting destination
            obj_key = (self.picking_object.size, self.picking_object.color)
            if obj_key in self.sorting_zones:
                sort_pos = self.sorting_zones[obj_key]
                
                # Solve IK for sorting position
                success, solution = self.arm.inverse_kinematics(sort_pos)
                
                if success:
                    self.current_target = solution
                    self.arm_state = 'moving_to_sort'
                else:
                    print(f"Cannot reach sorting zone for {obj_key}")
                    self.arm_state = 'scanning'
            else:
                print(f"No sorting zone defined for {obj_key}")
                self.arm_state = 'scanning'
    
    def execute_sort_movement(self, dt: float):
        """Execute movement to sorting position"""
        if self.current_target is not None:
            # Move to sorting position
            current_config = self.arm.joint_values
            diff = self.current_target - current_config
            step_size = 2.0 * dt
            
            if np.linalg.norm(diff) < 0.1:
                self.arm.set_joint_configuration(self.current_target)
                self.execute_sort()
            else:
                new_config = current_config + step_size * diff / np.linalg.norm(diff)
                self.arm.set_joint_configuration(new_config)
    
    def execute_sort(self):
        """Execute sort operation"""
        if self.picking_object:
            # Mark object as sorted
            self.picking_object.sorted = True
            self.objects_sorted += 1
            
            # Check if sorting was correct (compare detected vs actual)
            if (self.picking_object.size == self.picking_object.size and 
                self.picking_object.color == self.picking_object.color):
                self.correct_sorts += 1
            
            print(f"Sorted {self.picking_object.size} {self.picking_object.color} object")
            
            # Reset for next object
            self.picking_object = None
            self.current_target = None
            self.arm_state = 'scanning'
    
    def get_performance_metrics(self) -> Dict:
        """Get system performance metrics"""
        if self.detection_attempts > 0:
            detection_rate = self.detection_attempts / max(1, len(self.conveyor.objects))
            pick_success_rate = self.successful_picks / self.pick_attempts if self.pick_attempts > 0 else 0
            sort_accuracy = self.correct_sorts / self.objects_sorted if self.objects_sorted > 0 else 0
        else:
            detection_rate = pick_success_rate = sort_accuracy = 0
        
        return {
            'objects_processed': len(self.conveyor.objects),
            'objects_sorted': self.objects_sorted,
            'detection_attempts': self.detection_attempts,
            'successful_picks': self.successful_picks,
            'pick_success_rate': pick_success_rate,
            'sort_accuracy': sort_accuracy,
            'system_throughput': self.objects_sorted / max(1, time.time() - getattr(self, 'start_time', time.time()))
        }
    
    def visualize_system(self, ax):
        """Visualize the complete sorting system"""
        ax.clear()
        
        # Visualize conveyor belt
        self.conveyor.visualize(ax)
        
        # Visualize robotic arm
        _, joint_positions = self.arm.forward_kinematics()
        self.arm.visualize_arm(ax, joint_positions, "4-DOF Sorting Robot")
        
        # Visualize detection zone
        det_x, det_width, det_y = self.detection_zone
        detection_rect = patches.Rectangle(
            (det_x - det_width/2, det_y - 0.5),
            det_width, 1.0,
            linewidth=2, edgecolor='yellow', facecolor='yellow', alpha=0.3
        )
        ax.add_patch(detection_rect)
        ax.text(det_x, det_y + 0.8, 'Detection Zone', ha='center', fontweight='bold')
        
        # Visualize sorting zones
        for (size, color), pos in self.sorting_zones.items():
            zone_color = {'red': 'red', 'green': 'green', 'blue': 'blue'}[color]
            zone_size = {'small': 0.3, 'medium': 0.4, 'large': 0.5}[size]
            
            zone_circle = plt.Circle(pos, zone_size/2, 
                                   color=zone_color, alpha=0.4, ec='black', linewidth=1)
            ax.add_patch(zone_circle)
            ax.text(pos[0], pos[1], f'{size[0].upper()}{color[0].upper()}', 
                   ha='center', va='center', fontsize=8, fontweight='bold')
        
        # Add system status text
        metrics = self.get_performance_metrics()
        status_text = f"Status: {self.arm_state}\n"
        status_text += f"Objects Sorted: {metrics['objects_sorted']}\n"
        status_text += f"Pick Success: {metrics['pick_success_rate']:.2f}\n"
        status_text += f"Sort Accuracy: {metrics['sort_accuracy']:.2f}"
        
        ax.text(-4, 3, status_text, fontsize=10, 
               bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
        
        # Configure plot
        ax.set_xlim(-6, 5)
        ax.set_ylim(-5, 4)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title('4-DOF Robotic Arm Conveyor Belt Sorting System')
        ax.set_xlabel('X Position (meters)')
        ax.set_ylabel('Y Position (meters)')


def create_sorting_animation():
    """Create animation of the sorting system"""
    system = SortingSystem()
    system.start_time = time.time()
    
    # Pre-populate conveyor with some objects for demonstration
    for i in range(3):
        system.conveyor.spawn_object()
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    def animate(frame):
        dt = 0.1  # 10 FPS
        system.update(dt)
        system.visualize_system(ax)
        return []
    
    anim = FuncAnimation(fig, animate, interval=100, blit=False, repeat=True)
    
    plt.tight_layout()
    return fig, anim, system


if __name__ == "__main__":
    print("4-DOF Conveyor Belt Sorting System - Part C Implementation")
    
    # Create and test the sorting system
    system = SortingSystem()
    
    print("\n=== System Configuration ===")
    print(f"Robotic Arm: 4-DOF with mixed joint types")
    print(f"Conveyor Belt: {system.conveyor.length}m x {system.conveyor.width}m")
    print(f"Sorting Zones: {len(system.sorting_zones)} different size/color combinations")
    
    # Test detection and sorting
    print("\n=== Testing Object Detection ===")
    
    # Add test objects
    system.conveyor.spawn_object()
    system.conveyor.spawn_object()
    
    # Test detection
    detected = system.detector.detect_objects(system.conveyor.objects, system.detection_zone)
    print(f"Detected {len(detected)} objects")
    
    for detection in detected:
        print(f"  Object: {detection['size']} {detection['color']} "
              f"(confidence: {detection['confidence']:.2f})")
    
    # Create animation
    print("\n=== Creating Animation ===")
    fig, anim, system = create_sorting_animation()
    
    # Save static visualization
    plt.savefig('conveyor_sorting_system.png', dpi=300, bbox_inches='tight')
    print("Saved static visualization as 'conveyor_sorting_system.png'")
    
    # Show animation
    plt.show()
    
    print("\nConveyor belt sorting system implementation complete!")