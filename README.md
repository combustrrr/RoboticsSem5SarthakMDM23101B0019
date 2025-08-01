# Robotics Simulation

This repository contains a comprehensive Python implementation of industrial robotic arm simulation with pick-and-place operations and workspace visualization.

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

## Requirements

- Python 3.7+
- NumPy
- Matplotlib
- SciPy

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
1. View pick and place animation
2. Analyze and visualize workspace
3. Run both demonstrations
4. Exit

### Individual Modules

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
- `pick_and_place.py`: Pick and place simulation with animation
- `workspace_visualization.py`: Workspace analysis and visualization
- `main.py`: Main demonstration script
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