# Robotics Semester 5 - Sarthak MDM23101B0019

A comprehensive robotics simulation system featuring assignment work and an interactive 3D robotic arm mini project.

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
.
├── assignment1/                    # Assignment 1 (Part B & C)
│   ├── partb/                     # Basic robotic arm simulation (2D)
│   ├── partc/                     # Advanced features (4-DOF, conveyor, 3D)
│   ├── assets/                    # Assignment assets
│   │   ├── images/               # Analysis plots and diagrams  
│   │   └── videos/               # Demonstration GIFs
│   ├── docs/                     # Assignment documentation
│   ├── showcase_materials/       # Presentation materials
│   └── README.md                 # Assignment overview
├── mini_project/                  # Interactive 3D Robotic Arm
│   ├── src/                      # Core source code
│   ├── assets/                   # Textures, models, CAD files
│   ├── demos/                    # Video demonstrations
│   ├── docs/                     # Technical documentation
│   ├── main.py                   # Main entry point
│   └── README.md                 # Project documentation
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🚀 Quick Start

### Assignment 1
```bash
cd assignment1
python main.py
```

### Mini Project - Interactive 3D Robotic Arm
```bash
cd mini_project
python main.py
## 📋 Assignment 1 Components

### Part B - Basic Robotic Arm Simulation
- 2D robotic arm kinematics
- Pick and place operations
- Workspace analysis and visualization
- Basic trajectory planning

### Part C - Advanced Features
- 4-DOF robotic arm control
- 3D PyBullet simulation
- Conveyor belt sorting system
- Performance analysis and optimization
- Real-time physics simulation

## 🎮 Mini Project Features

### Interactive 3D JCB Robotic Arm
- **4-DOF Control**: Boom, Stick, Bucket, Base Rotation
- **Multiple Interfaces**: PyBullet GUI, web-based, matplotlib
- **VFX-Quality Rendering**: Professional lighting and materials
- **CAD Integration**: Support for IGS, STEP, SLDPRT formats
- **Realistic Textures**: Photographic material enhancement
- **Automated Sequences**: Complete excavation demonstrations

### Technical Specifications
- **Max Reach**: 8.0 meters
- **Max Dig Depth**: 6.2 meters
- **Bucket Capacity**: 1.2 cubic meters
- **Real-Time Physics**: 240Hz simulation, 60Hz rendering

## 🎬 Demonstrations

The repository includes comprehensive video demonstrations:
- Assignment completion showcases
- Interactive robotic arm control demos
- Technical analysis visualizations
- Professional presentation materials

## 🔧 Dependencies

```bash
pip install -r requirements.txt
```

Core dependencies:
- `pybullet` - Physics simulation
- `numpy` - Numerical computing
- `matplotlib` - Plotting and visualization
- `opencv-python` - Image processing
- `pillow` - Image manipulation

## 🎯 Academic Context

**Course**: Robotics Semester 5  
**Student**: Sarthak MDM23101B0019  
**Institution**: [University Name]

### Assignment Objectives
- Demonstrate understanding of robotic arm kinematics
- Implement forward and inverse kinematics solutions
- Design and analyze robotic workspace
- Develop real-time control systems
- Create professional simulation demonstrations

### Mini Project Goals
- Build interactive 3D robotic arm simulation
- Integrate professional CAD files
- Implement VFX-quality rendering
- Create computer graphics project demonstrations
- Showcase virtual robot prototyping capabilities

## 📖 Documentation

Detailed documentation is available in each component:
- **Assignment 1**: `assignment1/README.md`
- **Mini Project**: `mini_project/README.md`
- **Technical Guides**: Available in respective `docs/` directories

## 🏆 Features Highlights

### Assignment Work
✅ Complete 2D and 3D robotic arm implementations  
✅ Forward and inverse kinematics solutions  
✅ Workspace analysis and optimization  
✅ Performance comparison studies  
✅ Professional documentation and analysis  

### Mini Project
✅ Interactive 4-DOF JCB robotic arm  
✅ Multiple control interfaces (GUI, web, CLI)  
✅ Professional CAD file integration  
✅ VFX-quality rendering and materials  
✅ Comprehensive demonstration package  

---

This repository represents a complete robotics simulation ecosystem, combining academic assignment requirements with professional-quality interactive demonstrations suitable for computer graphics projects and virtual robot prototyping.
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