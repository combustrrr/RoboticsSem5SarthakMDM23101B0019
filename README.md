# Industrial Robot Pick and Place Simulation

This project implements a comprehensive industrial robot simulation with pick and place operations, including animation and workspace analysis.

## Features

1. **Robot Simulation (`robot_simulation.py`)**
   - 2-DOF robot arm with configurable link lengths
   - Forward and inverse kinematics
   - Smooth trajectory generation
   - Pick and place operation simulation
   - Real-time animation using matplotlib
   - Workspace visualization with reachable points

2. **Advanced Workspace Analysis (`workspace_analysis.py`)**
   - Comprehensive workspace visualization
   - Reachability mapping
   - Manipulability analysis
   - Joint space configuration visualization
   - Distance distribution analysis
   - Detailed workspace statistics

3. **Kinematics Testing (`test_kinematics.py`)**
   - Forward/inverse kinematics validation
   - Trajectory generation testing
   - Workspace boundary verification

## Requirements

- Python 3.7+
- numpy
- matplotlib
- scipy

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

### Run the Pick and Place Simulation
```bash
python robot_simulation.py
```

This will open a dual-plot window showing:
- Left: Real-time robot animation with pick and place operation
- Right: Robot workspace visualization with reachable points

### Run Advanced Workspace Analysis
```bash
python workspace_analysis.py
```

This generates comprehensive workspace analysis including:
- Reachability maps
- Manipulability index visualization
- Joint space configuration
- Distance distribution analysis

### Test Kinematics
```bash
python test_kinematics.py
```

This validates the robot kinematics implementation and tests various functionality.

## Robot Configuration

The default robot configuration uses:
- Link 1 length: 3.0 units
- Link 2 length: 2.0 units
- Maximum reach: 5.0 units
- Minimum reach: 1.0 units

You can modify these parameters in the `RobotArm` class constructor.

## Pick and Place Locations

The simulation uses predefined locations:
- **Home Position**: (2.0, 3.0)
- **Pick Location**: (4.0, 1.0) - marked with blue square
- **Place Location**: (-3.0, 2.0) - marked with red square

## Animation Controls

- The simulation starts with the robot in an initial position
- Press Enter to begin the pick and place sequence
- The robot will automatically:
  1. Move to home position
  2. Move to pick location and pick the object
  3. Move to place location and place the object
  4. Return to home position

## Technical Details

### Forward Kinematics
The end-effector position is calculated using:
```
x = l1*cos(θ1) + l2*cos(θ1 + θ2)
y = l1*sin(θ1) + l2*sin(θ1 + θ2)
```

### Inverse Kinematics
Joint angles are calculated using geometric approach with cosine rule:
```
θ2 = ±arccos((x² + y² - l1² - l2²) / (2*l1*l2))
θ1 = atan2(y, x) - atan2(l2*sin(θ2), l1 + l2*cos(θ2))
```

### Workspace Analysis
- **Reachability Map**: Grid-based analysis of reachable positions
- **Manipulability Index**: √(det(J*J^T)) where J is the Jacobian matrix
- **Workspace Boundaries**: Theoretical limits based on link lengths

## File Structure

```
Robotics/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── robot_simulation.py          # Main simulation with pick & place
├── workspace_analysis.py        # Advanced workspace analysis
└── test_kinematics.py          # Kinematics validation tests
```

## Educational Value

This simulation demonstrates key robotics concepts:
- Forward and inverse kinematics
- Trajectory planning and generation
- Workspace analysis and limitations
- Industrial automation (pick and place)
- Real-time visualization and animation

Perfect for learning robotics fundamentals and understanding how industrial robots operate in manufacturing environments.