# Assignment 2 Part B: Rotation Matrices and End-Effector Position

**Student**: Sarthak MDM23101B0019  
**Course**: Robotics Semester 5

## Problem Statement

Using any programming tool (MATLAB, Python, etc.), implement the following operations:

1. **Initial Position**: The initial position of the robotic arm's end-effector in the global frame is (x,y,z) = (2,3,4).

2. **Successive Rotations**: The arm is subjected to three successive rotations:
   - A rotation of 30° about the X-axis
   - A rotation of 45° about the Y-axis  
   - A rotation of 60° about the Z-axis

3. **Requirements**:
   - Find the corresponding rotation matrices
   - Find the final position of the end-effector
   - Make a generic code for calculating rotation matrices and to find position of end-effector after composite rotations

## Solution Overview

This implementation provides a comprehensive solution using Python with numpy for mathematical calculations and matplotlib for visualization.

### Key Features

- **Individual Rotation Matrices**: Calculate rotation matrices for X, Y, and Z axes
- **Composite Rotation System**: Handle sequences of rotations in any order
- **Generic Implementation**: Flexible system for any rotation sequence and initial position
- **Mathematical Verification**: Comprehensive testing for rotation matrix properties
- **Visualization**: 3D plots showing transformation process
- **Interactive Interface**: Menu-driven system for easy use

## File Structure

```
assignment2/partb/
├── rotation_matrices.py      # Core implementation
├── main.py                   # Interactive demonstration
├── test_rotation_matrices.py # Comprehensive test suite
└── README.md                 # This documentation
```

## Quick Start

### Run the Assignment Solution
```bash
cd assignment2/partb
python main.py
```

### Run Tests
```bash
python test_rotation_matrices.py
```

### Direct Problem Solution
```python
from rotation_matrices import RotationMatrixCalculator

calc = RotationMatrixCalculator()
results = calc.solve_assignment_2_part_b()
```

## Solution Results

For the specific assignment problem:

- **Initial Position**: (2, 3, 4)
- **Final Position**: (0.3817, 4.9497, 2.0915)
- **Distance Moved**: 3.0237 units

### Rotation Matrices

**30° X-axis Rotation:**
```
[[ 1.0000,  0.0000,  0.0000],
 [ 0.0000,  0.8660, -0.5000],
 [ 0.0000,  0.5000,  0.8660]]
```

**45° Y-axis Rotation:**
```
[[ 0.7071,  0.0000,  0.7071],
 [ 0.0000,  1.0000,  0.0000],
 [-0.7071,  0.0000,  0.7071]]
```

**60° Z-axis Rotation:**
```
[[ 0.5000, -0.8660,  0.0000],
 [ 0.8660,  0.5000,  0.0000],
 [ 0.0000,  0.0000,  1.0000]]
```

**Composite Rotation Matrix:**
```
R_composite = R_z(60°) × R_y(45°) × R_x(30°) =
[[ 0.3536, -0.6124,  0.7071],
 [ 0.9268,  0.2241,  0.3068],
 [-0.1268,  0.7588,  0.6385]]
```

## Mathematical Background

### Rotation Matrices

The fundamental rotation matrices for rotations about the coordinate axes are:

**X-axis rotation (angle θ):**
```
R_x(θ) = [1    0      0   ]
         [0  cos(θ) -sin(θ)]
         [0  sin(θ)  cos(θ)]
```

**Y-axis rotation (angle θ):**
```
R_y(θ) = [ cos(θ)  0  sin(θ)]
         [   0     1    0   ]
         [-sin(θ)  0  cos(θ)]
```

**Z-axis rotation (angle θ):**
```
R_z(θ) = [cos(θ) -sin(θ)  0]
         [sin(θ)  cos(θ)  0]
         [  0       0     1]
```

### Composite Rotations

For a sequence of rotations, the composite rotation matrix is calculated as:
```
R_composite = R_n × ... × R_2 × R_1
```

Where rotations are applied in order from right to left (R_1 first, then R_2, etc.).

### Properties of Rotation Matrices

Valid rotation matrices satisfy:
- **Orthogonal**: R × R^T = I
- **Determinant**: det(R) = 1
- **Inverse**: R^(-1) = R^T

## Usage Examples

### Basic Usage
```python
from rotation_matrices import RotationMatrixCalculator

calc = RotationMatrixCalculator()

# Get individual rotation matrix
matrix_x = calc.rotation_matrix_x(30)

# Calculate composite rotation
rotations = [('x', 30), ('y', 45), ('z', 60)]
composite = calc.calculate_composite_rotation(rotations)

# Transform position
initial_pos = [2, 3, 4]
final_pos = calc.transform_position(initial_pos, rotations)
```

### Custom Rotation Sequence
```python
# Example: Different sequence
custom_rotations = [('z', 90), ('x', 45), ('y', 30)]
custom_position = [1, 0, 0]

result = calc.transform_position(custom_position, custom_rotations)
print(f"Final position: {result}")
```

### Interactive Menu System

The main.py provides an interactive menu with options:
1. Solve Assignment 2 Part B Problem
2. Custom Rotation Sequence Calculator
3. Individual Rotation Matrix Calculator
4. Demonstrate Generic System Examples
5. Mathematical Verification Tests
6. Generate Visualization
7. Exit

## Testing and Verification

The test suite includes:

### Unit Tests
- Identity rotation tests (0° and 360°)
- Matrix orthogonality verification
- Determinant checks (should be 1.0)
- Inverse equals transpose verification
- Specific axis rotation tests

### Mathematical Verification
- Rotation matrix properties validation
- Composite rotation associativity
- Negative angle handling
- Large angle normalization

### Performance Tests
- Benchmark for single matrix calculations
- Composite rotation performance
- Full transformation timing

Run tests with:
```bash
python test_rotation_matrices.py
```

## Visualization

The system includes 3D visualization showing:
- Initial and final end-effector positions
- Transformation path through intermediate positions
- Position component comparisons
- Distance analysis during transformation

## Dependencies

```
numpy>=1.19.0       # Mathematical operations
matplotlib>=3.3.0   # Visualization (optional)
```

Install with:
```bash
pip install numpy matplotlib
```

## Academic Context

This implementation demonstrates:
- **Rotation Matrix Theory**: Fundamental 3D rotation mathematics
- **Composite Transformations**: Sequential rotation applications
- **Software Engineering**: Modular design with comprehensive testing
- **Numerical Methods**: Precision handling and verification
- **Visualization**: 3D transformation representation

## Technical Features

### Error Handling
- Input validation for axes and angles
- Numerical precision management
- Graceful fallback for visualization dependencies

### Code Quality
- Comprehensive documentation
- Type hints for clarity
- Modular design for reusability
- Extensive testing coverage

### Performance
- Efficient numpy operations
- Optimized matrix calculations
- Benchmark testing included

## License

This project is developed for educational purposes as part of Assignment 2.

---

**Note**: This comprehensive rotation matrix system provides both specific assignment solutions and a generic framework for robotic transformation calculations.