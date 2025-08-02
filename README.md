# Assignment 1: Robotic Arm Simulation Suite

This repository contains a comprehensive Python implementation of robotic arm simulation and analysis, organized into **Part B** and **Part C** as required for Assignment 1.

## 🎯 Quick Start

### Run the Complete Assignment Suite
```bash
python main.py
```

### Run Individual Parts
```bash
# Part B: Basic Robotic Arm Simulation
cd assignment1/partb && python main.py

# Part C: Advanced Features (4-DOF, Conveyor, 3D Animation)
cd assignment1/partc && python main.py
```

## 📁 Repository Structure

```
assignment1/
├── README.md              # Comprehensive assignment documentation
├── partb/                 # Part B: Basic Robotic Arm Simulation
│   ├── main.py           # Part B main demo script
│   ├── robot_arm.py      # Core robotic arm implementation
│   ├── pick_and_place.py # Pick-and-place simulation
│   ├── workspace_visualization.py # Workspace analysis
│   └── ANALYSIS_REPORT.md # Part B technical analysis
└── partc/                 # Part C: Advanced Features
    ├── main.py           # Part C main demo script
    ├── robotic_arm_4dof.py # 4-DOF robotic arm system
    ├── conveyor_sorting_system.py # Computer vision sorting
    ├── pybullet_arm_animation.py # 3D PyBullet animation
    ├── part_c_demo.py    # Comprehensive demonstration
    ├── test_3d_animation.py # 3D animation testing
    ├── PART_C_ANALYSIS_REPORT.md # Part C technical analysis
    ├── 3D_ANIMATION_README.md # 3D animation documentation
    └── *.png             # Generated analysis visualizations
```

## 🤖 Part B: Basic Robotic Arm Simulation

### Features
- **Multi-link Robotic Arm**: Configurable link lengths with joint constraints
- **Forward & Inverse Kinematics**: Mathematical modeling and solution algorithms  
- **Pick-and-Place Operations**: Animated object manipulation scenarios
- **Workspace Visualization**: Reachable area analysis and visualization
- **Performance Analysis**: Comprehensive workspace metrics

### Key Demonstrations
1. **Pick and Place Animation**: Smooth trajectory planning and execution
2. **Workspace Visualization**: Reachable area mapping and analysis
3. **Inverse Kinematics Testing**: Solution validation for target positions

## 🚀 Part C: Advanced Features

### Features
- **4-DOF Robotic Arm**: Mixed revolute and prismatic joints
- **Conveyor Belt Sorting**: Computer vision-based object classification
- **3D PyBullet Animation**: Physics-based JCB-style excavator simulation
- **Advanced Analysis**: Performance metrics and comparative studies

### Key Demonstrations
1. **4-DOF Arm Capabilities**: Extended degrees of freedom control
2. **Conveyor Belt Sorting**: Real-time object detection and manipulation
3. **3D Physics Simulation**: Realistic JCB-style excavator with PyBullet
4. **Comprehensive Analysis**: Performance benchmarking and validation

## 🎥 3D Animation & Video Demonstration

The **3D PyBullet animation** provides professional-quality visualization perfect for:
- **Computer Graphics Projects**: High-quality 3D rendering with realistic physics
- **Video Demonstrations**: Smooth animation sequences suitable for recording
- **Interactive Prototyping**: Real-time 3D visualization with camera controls
- **Educational Presentations**: Professional-grade robotic arm demonstrations

### Video-Ready Features
- **JCB-Style Design**: Realistic construction equipment styling
- **Physics Simulation**: Gravity, collision detection, and material properties
- **Smooth Animation**: Pre-programmed digging, lifting, and dumping sequences
- **Professional Rendering**: Shadows, lighting, and multiple camera angles

To create video demonstrations:
```bash
cd assignment1/partc
python pybullet_arm_animation.py  # Interactive 3D demo
python demo_3d_screenshots.py    # Capture screenshots/frames
```

## ⚙️ Requirements & Installation

### Core Dependencies
```bash
pip install numpy matplotlib scipy
```

### Advanced Features (Part C)
```bash
pip install pybullet opencv-python  # For 3D animation and computer vision
```

### Complete Installation
```bash
pip install -r requirements.txt
```

## 🧪 Testing & Validation

### Run All Tests
```bash
# Test Part B
cd assignment1/partb && python main.py

# Test Part C with 3D animation
cd assignment1/partc && python test_3d_animation.py

# Full system validation
python main.py
```

### Headless Support
All features work without display for server environments and automated testing.

## 📊 Technical Analysis

### Part B Analysis
- **Workspace Coverage**: Complete reachable area mapping
- **Kinematic Accuracy**: Forward/inverse kinematics validation
- **Performance Metrics**: Computation time and accuracy analysis
- **Motion Planning**: Smooth trajectory generation algorithms

### Part C Analysis  
- **4-DOF Capabilities**: Mixed joint type performance evaluation
- **Computer Vision**: Object detection accuracy and classification
- **3D Physics**: Realistic simulation validation with collision detection
- **Comparative Studies**: Performance benchmarks across different configurations

## 🎓 Academic Applications

This implementation demonstrates:
- **Robotic Kinematics**: Forward and inverse kinematic solutions
- **Motion Planning**: Path planning and trajectory generation
- **Computer Vision**: Real-time object detection and classification
- **Physics Simulation**: 3D physics with PyBullet integration
- **Software Engineering**: Modular design with comprehensive testing

## 📖 Documentation

### Technical Reports
- **Part B**: `assignment1/partb/ANALYSIS_REPORT.md`
- **Part C**: `assignment1/partc/PART_C_ANALYSIS_REPORT.md`  
- **3D Animation**: `assignment1/partc/3D_ANIMATION_README.md`
- **Complete Guide**: `assignment1/README.md`

### Generated Assets
- Workspace visualization plots
- Performance analysis charts  
- 3D animation screenshots
- Comparative analysis results

## 🔧 Usage Examples

### Basic Robotic Arm (Part B)
```python
from robot_arm import RoboticArm
from workspace_visualization import WorkspaceVisualizer

# Create and analyze 3-link arm
robot = RoboticArm([3.0, 2.5, 1.5])
visualizer = WorkspaceVisualizer(robot)
visualizer.calculate_workspace()
visualizer.plot_workspace()
```

### Advanced Features (Part C)
```python
# 4-DOF Arm Control
from robotic_arm_4dof import create_4dof_arm_configuration
arm = create_4dof_arm_configuration()
arm.set_joint_values([0.5, 0.3, 1.2, -0.4])

# 3D Animation
from pybullet_arm_animation import PyBulletRoboticArm
arm_3d = PyBulletRoboticArm(gui=True)
arm_3d.animate_digging_sequence(duration=10.0)

# Conveyor Sorting
from conveyor_sorting_system import SortingSystem
system = SortingSystem()
system.add_object("large", "red", 1.0)
```

## 📝 License

This project is developed for educational purposes as part of Assignment 1.

---

**Note**: This comprehensive robotic arm simulation suite provides both educational value and professional-quality demonstrations suitable for computer graphics projects and video presentations.
```bash
python main.py
```

This will present an interactive menu with options to:
1. View pick and place animation (2D)
2. Analyze and visualize workspace (2D)
3. **3D Robotic Arm Animation (PyBullet)** - NEW!
4. Run all demonstrations
5. Exit

### Individual Modules

#### 3D Robotic Arm Animation
```python
from pybullet_arm_animation import PyBulletRoboticArm

# Create 3D robotic arm with JCB-style design
arm = PyBulletRoboticArm(gui=True)

# Set joint positions
arm.set_joint_positions([0.5, -0.8, 1.2, 0.3])

# Run digging animation sequence
arm.animate_digging_sequence(duration=10.0)

# Get end effector position
position = arm.get_end_effector_position()
print(f"End effector at: {position}")

# Cleanup
arm.cleanup()
```

#### Pick and Place Simulation
```python
from robot_arm import RoboticArm
from pick_and_place import PickAndPlaceSimulation

# Create a 3-link robot
robot = RoboticArm([3.0, 2.5, 1.5])

# Set up simulation
sim = PickAndPlaceSimulation(robot)
sim.add_object(4.0, 2.0)  # Object to pick
sim.add_target(-4.0, 1.0)  # Target location

# Run animation
sim.run_simulation()
```

#### Workspace Visualization
```python
from robot_arm import RoboticArm
from workspace_visualization import WorkspaceVisualizer

# Create robot
robot = RoboticArm([3.0, 2.5, 1.5])

# Visualize workspace
viz = WorkspaceVisualizer(robot)
viz.plot_workspace()
viz.analyze_workspace_metrics()
```

## Files Structure

- `robot_arm.py`: Core robotic arm class with kinematics
- `robotic_arm_4dof.py`: 4-DOF robotic arm implementation
- `pybullet_arm_animation.py`: 3D robotic arm animation with PyBullet (NEW)
- `pick_and_place.py`: Pick and place simulation with animation
- `workspace_visualization.py`: Workspace analysis and visualization
- `main.py`: Main demonstration script with menu
- `test_3d_animation.py`: Testing for 3D animation functionality
- `requirements.txt`: Python dependencies

## Technical Details

### Robotic Arm Model
- 2D planar arm with configurable number of joints
- Forward kinematics using transformation matrices
- Inverse kinematics using numerical optimization
- Joint limit enforcement

### Pick and Place Algorithm
1. Path planning between configurations
2. Smooth interpolation for animation
3. Object manipulation simulation
4. Real-time visualization

### Workspace Analysis
- Brute force reachability testing
- Theoretical vs. actual reach comparison
- Workspace boundary visualization
- Performance metrics calculation

## Examples

The simulation includes several pre-configured examples:
- 2-link arm workspace analysis
- 3-link arm pick and place operations
- Joint-limited robot configurations
- Multiple object manipulation scenarios