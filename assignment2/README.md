# Assignment 2: Advanced Robotics Mathematics

**Student**: Sarthak MDM23101B0019  
**Course**: Robotics Semester 5

This directory contains the implementation of Assignment 2, focusing on advanced robotics mathematics including rotation matrices, transformations, and kinematic analysis.

## Assignment Structure

```
assignment2/
├── partb/                   # Part B: Rotation Matrices and End-Effector Position
│   ├── rotation_matrices.py    # Core rotation matrix implementation
│   ├── main.py                 # Interactive demonstration interface
│   ├── test_rotation_matrices.py   # Comprehensive test suite
│   └── README.md               # Part B documentation
└── README.md                   # This file
```

## Quick Start

### Run Assignment 2 Part B
```bash
cd assignment2/partb
python main.py
```

### Run from Repository Root
```bash
python main.py  # Select Assignment 2 from menu
```

## Part B: Rotation Matrices and End-Effector Position

### Problem Statement
- Initial end-effector position: (x,y,z) = (2,3,4)
- Apply successive rotations: 30° about X-axis, 45° about Y-axis, 60° about Z-axis
- Calculate rotation matrices and final position
- Create generic system for any rotation sequence

### Key Features
- **Individual Rotation Matrices**: X, Y, Z axis rotations with mathematical precision
- **Composite Rotations**: Sequential rotation handling with proper matrix multiplication
- **Generic Implementation**: Flexible system for any rotation sequence and initial position
- **Mathematical Verification**: Comprehensive property checking (orthogonality, determinant, etc.)
- **3D Visualization**: Interactive plots showing transformation process
- **Test Suite**: Extensive unit tests and performance benchmarks

### Solution Results
- **Final Position**: (0.3817, 4.9497, 2.0915)
- **Distance Moved**: 3.0237 units
- **Composite Matrix**: Full 3x3 rotation matrix calculated and verified

### Usage Examples

```python
from assignment2.partb.rotation_matrices import RotationMatrixCalculator

# Initialize calculator
calc = RotationMatrixCalculator()

# Solve the assignment problem
results = calc.solve_assignment_2_part_b()

# Custom rotation sequence
custom_rotations = [('x', 30), ('y', 45), ('z', 60)]
final_pos = calc.transform_position([2, 3, 4], custom_rotations)

# Individual rotation matrix
matrix_x = calc.rotation_matrix_x(30)
```

## Mathematical Foundation

### Rotation Matrices
The implementation uses standard 3D rotation matrices:

- **X-axis**: Rotates in YZ plane
- **Y-axis**: Rotates in XZ plane  
- **Z-axis**: Rotates in XY plane

### Properties Verified
- Orthogonality: R × R^T = I
- Unit determinant: det(R) = 1
- Inverse property: R^(-1) = R^T

### Composite Transformations
Sequential rotations applied as: R_final = R_3 × R_2 × R_1

## Testing and Validation

### Comprehensive Test Suite
- **Mathematical Properties**: Orthogonality, determinant, inverse checks
- **Specific Cases**: Identity rotations, full rotations, negative angles
- **Assignment Verification**: Specific problem solution validation
- **Performance Benchmarks**: Timing tests for optimization

### Run Tests
```bash
cd assignment2/partb
python test_rotation_matrices.py
```

## Dependencies

```
numpy>=1.19.0       # Core mathematical operations
matplotlib>=3.3.0   # Visualization (optional)
```

## Academic Objectives

This assignment demonstrates:
- **3D Rotation Mathematics**: Fundamental transformation theory
- **Matrix Operations**: Efficient numerical computation
- **Software Engineering**: Modular, testable code design
- **Mathematical Verification**: Property validation and testing
- **Visualization**: 3D transformation representation

## Integration with Repository

Assignment 2 integrates with the existing repository structure:
- Consistent coding style with Assignment 1
- Compatible dependency management
- Unified testing framework
- Documentation standards alignment

## Future Extensions

The generic rotation system supports:
- Additional rotation sequences
- Different coordinate systems
- Extended transformation types
- Real-time robotic control applications

---

**Note**: This assignment builds upon fundamental robotics concepts while introducing advanced mathematical frameworks for transformation analysis.