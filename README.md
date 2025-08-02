# Robotics Simulation

This repository contains a comprehensive Python implementation of industrial robotic arm simulation with pick-and-place operations, workspace visualization, and **3D robotic arm animation**.

## Features

1. **Industrial Robot Simulation**: 
   - Multi-link robotic arm with configurable link lengths
   - Forward and inverse kinematics
   - Joint limits and constraints
   - Pick and place operations with smooth animation

2. **Workspace Visualization**:
   - Reachable point calculation and visualization
   - Workspace boundary analysis
   - Multiple arm configuration displays
   - Workspace metrics and statistics

3. **3D Robotic Arm Animation** (NEW):
   - PyBullet-based 3D physics simulation
   - JCB-style excavator arm visualization
   - Realistic 3D animation with smooth motion
   - Interactive 3D environment with camera controls

## Requirements

- Python 3.7+
- NumPy
- Matplotlib
- SciPy
- PyBullet (for 3D animation)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Robotics
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

Run the main demonstration:
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