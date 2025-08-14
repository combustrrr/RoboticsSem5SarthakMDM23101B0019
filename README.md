# Robotics Semester 5 - Sarthak MDM23101B0019

A comprehensive robotics assignment suite featuring robotic arm kinematics, advanced rotation mathematics, workspace analysis, and simulation systems.

## 🎯 Quick Start

### Run the Complete Assignment Suite
```bash
python main.py
```

### Run Individual Assignments
```bash
# Assignment 1: Robotic Arm Simulation Suite
cd assignment1/partb && python main.py  # Part B: Basic simulation
cd assignment1/partc && python main.py  # Part C: Advanced features

# Assignment 2: Advanced Robotics Mathematics  
cd assignment2/partb && python main.py  # Part B: Rotation matrices
```

## 📁 Repository Structure

```
.
├── assignment1/                    # Assignment 1: Robotic Arm Simulation Suite
│   ├── partb/                     # Basic robotic arm simulation (2D)
│   ├── partc/                     # Advanced features (4-DOF, conveyor, 3D)
│   ├── assets/                    # Assignment assets
│   ├── docs/                      # Assignment documentation
│   └── README.md                  # Assignment 1 overview
├── assignment2/                    # Assignment 2: Advanced Robotics Mathematics
│   ├── partb/                     # Rotation matrices and transformations
│   └── README.md                  # Assignment 2 overview
├── requirements.txt               # Python dependencies
├── main.py                        # Assignment suite launcher
└── README.md                      # This file
```

## 📋 Assignment Components

### Assignment 1: Robotic Arm Simulation Suite

#### Part B - Basic Robotic Arm Simulation
- 2D robotic arm kinematics
- Pick and place operations
- Workspace analysis and visualization
- Basic trajectory planning

#### Part C - Advanced Features
- 4-DOF robotic arm control
- 3D PyBullet simulation
- Conveyor belt sorting system
- Performance analysis and optimization
- Real-time physics simulation

### Assignment 2: Advanced Robotics Mathematics

#### Part B - Rotation Matrices and End-Effector Position
- Individual rotation matrix calculations (X, Y, Z axes)
- Composite rotation transformations
- End-effector position analysis
- Generic rotation sequence system
- Mathematical verification and testing

## 🎬 Demonstrations

The repository includes comprehensive demonstrations:
- **Assignment 1**: Robotic arm simulation showcases and technical analysis
- **Assignment 2**: Rotation matrix calculations and mathematical verification
- Professional presentation materials and analysis reports

## 🔧 Dependencies

```bash
pip install -r requirements.txt
```

Core dependencies:
- `numpy` - Numerical computing and matrix operations
- `matplotlib` - Plotting and visualization
- `scipy` - Scientific computing
- `opencv-python` - Image processing (Assignment 1)
- `pybullet` - Physics simulation (Assignment 1)

## 🎯 Academic Context

**Course**: Robotics Semester 5  
**Student**: Sarthak MDM23101B0019  
**Institution**: [University Name]

### Assignment Objectives
- Demonstrate understanding of robotic arm kinematics
- Master rotation matrix mathematics and transformations
- Implement forward and inverse kinematics solutions
- Design and analyze robotic workspace
- Develop real-time control systems
- Create professional simulation demonstrations

## 📖 Documentation

Detailed documentation is available in:
- **Assignment 1**: `assignment1/README.md`
- **Assignment 2**: `assignment2/README.md`
- **Technical Guides**: Available in respective assignment directories

## 🏆 Features Highlights

### Assignment 1: Robotic Arm Simulation
✅ Complete 2D and 3D robotic arm implementations  
✅ Forward and inverse kinematics solutions  
✅ Workspace analysis and optimization  
✅ Performance comparison studies  
✅ Professional documentation and analysis  

### Assignment 2: Advanced Mathematics
✅ Complete rotation matrix implementation  
✅ Composite transformation system  
✅ Mathematical verification and testing  
✅ Generic rotation sequence calculator  
✅ Comprehensive documentation and examples  

## 🚀 Advanced Features

### Assignment 1
- **Robotic Kinematics**: Forward and inverse kinematic solutions
- **Motion Planning**: Path planning and trajectory generation
- **Computer Vision**: Real-time object detection and classification
- **Physics Simulation**: 3D physics with PyBullet integration
- **Software Engineering**: Modular design with comprehensive testing

### Assignment 2
- **Rotation Mathematics**: Fundamental 3D rotation theory
- **Matrix Operations**: Efficient numerical computation
- **Transformation Analysis**: End-effector position calculations
- **Mathematical Verification**: Property validation and testing
- **Generic Framework**: Flexible rotation sequence system

## 📖 Technical Reports

### Assignment 1
- **Part B**: `assignment1/partb/ANALYSIS_REPORT.md`
- **Part C**: `assignment1/partc/PART_C_ANALYSIS_REPORT.md`  
- **3D Animation**: `assignment1/partc/3D_ANIMATION_README.md`
- **Complete Guide**: `assignment1/README.md`

### Assignment 2
- **Part B**: `assignment2/partb/README.md`
- **Mathematical Analysis**: Comprehensive rotation matrix documentation
- **Testing Reports**: Validation and verification results

### Generated Assets
- Workspace visualization plots
- Performance analysis charts  
- 3D animation screenshots
- Rotation transformation visualizations
- Comparative analysis results

## 🔧 Usage Examples

### Assignment 1: Basic Robotic Arm (Part B)
```python
from robot_arm import RoboticArm
from workspace_visualization import WorkspaceVisualizer

# Create and analyze 3-link arm
robot = RoboticArm([3.0, 2.5, 1.5])
visualizer = WorkspaceVisualizer(robot)
visualizer.calculate_workspace()
visualizer.plot_workspace()
```

### Assignment 1: Advanced Features (Part C)
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

### Assignment 2: Rotation Matrices (Part B)
```python
from assignment2.partb.rotation_matrices import RotationMatrixCalculator

# Initialize calculator
calc = RotationMatrixCalculator()

# Solve Assignment 2 Part B problem
results = calc.solve_assignment_2_part_b()

# Custom rotation sequence
rotations = [('x', 30), ('y', 45), ('z', 60)]
final_pos = calc.transform_position([2, 3, 4], rotations)

# Individual rotation matrices
matrix_x = calc.rotation_matrix_x(30)
matrix_y = calc.rotation_matrix_y(45)
matrix_z = calc.rotation_matrix_z(60)
```

## 📝 License

This project is developed for educational purposes as part of robotics coursework.

---

**Note**: This comprehensive robotics assignment suite provides educational value and professional-quality demonstrations for advanced robotics coursework, covering both practical simulation and theoretical mathematical foundations.

## 🚀 Quick Start

```bash
python main.py
```

This will present an interactive menu with options to:
1. Assignment 1: Robotic Arm Simulation Suite
   - Part B: Basic Robotic Arm Simulation (2D)
   - Part C: Advanced Features (4-DOF, Conveyor, 3D)
2. Assignment 2: Advanced Robotics Mathematics  
   - Part B: Rotation Matrices and End-Effector Position
3. Exit

### Individual Modules

#### Assignment 1: 3D Robotic Arm Animation
```python
from pybullet_arm_animation import PyBulletRoboticArm

# Create 3D robotic arm with enhanced design
arm = PyBulletRoboticArm(gui=True)

# Set joint positions
arm.set_joint_positions([0.5, -0.8, 1.2, 0.3])

# Run animation sequence
arm.animate_digging_sequence(duration=10.0)

# Get end effector position
position = arm.get_end_effector_position()
print(f"End effector at: {position}")

# Cleanup
arm.cleanup()
```

#### Assignment 1: Pick and Place Simulation
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

#### Assignment 2: Rotation Matrix Analysis
```python
from assignment2.partb.rotation_matrices import RotationMatrixCalculator

# Create calculator
calc = RotationMatrixCalculator()

# Solve the specific assignment problem
results = calc.solve_assignment_2_part_b()

# Create custom rotation sequence
rotations = [('x', 30), ('y', 45), ('z', 60)]
final_position = calc.transform_position([2, 3, 4], rotations)

# Get individual matrices
rx = calc.rotation_matrix_x(30)
ry = calc.rotation_matrix_y(45)  
rz = calc.rotation_matrix_z(60)
```

## Files Structure

### Assignment 1
- `robot_arm.py`: Core robotic arm class with kinematics
- `robotic_arm_4dof.py`: 4-DOF robotic arm implementation
- `pybullet_arm_animation.py`: 3D robotic arm animation with PyBullet
- `pick_and_place.py`: Pick and place simulation with animation
- `workspace_visualization.py`: Workspace analysis and visualization
- `main.py`: Main demonstration script with menu
- `test_3d_animation.py`: Testing for 3D animation functionality

### Assignment 2
- `rotation_matrices.py`: Core rotation matrix implementation
- `main.py`: Interactive demonstration interface
- `test_rotation_matrices.py`: Comprehensive test suite

### Common
- `requirements.txt`: Python dependencies
- `main.py`: Master assignment launcher

## Technical Details

### Assignment 1: Robotic Arm Model
- 2D planar arm with configurable number of joints
- Forward kinematics using transformation matrices
- Inverse kinematics using numerical optimization
- Joint limit enforcement

### Assignment 1: Pick and Place Algorithm
1. Path planning between configurations
2. Smooth interpolation for animation
3. Object manipulation simulation
4. Real-time visualization

### Assignment 1: Workspace Analysis
- Brute force reachability testing
- Theoretical vs. actual reach comparison
- Workspace boundary visualization
- Performance metrics calculation

### Assignment 2: Rotation Mathematics
- Individual X, Y, Z axis rotation matrices
- Composite rotation calculations
- End-effector position transformations
- Mathematical property verification

## Examples

The simulation suite includes several pre-configured examples:
- 2-link arm workspace analysis
- 3-link arm pick and place operations
- Joint-limited robot configurations
- Multiple object manipulation scenarios
- Rotation matrix verification tests
- Composite transformation demonstrations