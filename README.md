# Virtual Robotic Arm

This repository contains a virtual robotic arm simulation project built with Python and web technologies.

## Running the Project

This project uses Python's built-in HTTP server to serve the web files. To run it:

```bash
python main.py
```

This will start the interactive robotic arm simulation with multiple options:
1. 2D robotic arm demonstrations
2. 3D PyBullet simulations  
3. Web-based interactive controls
4. Workspace analysis and visualization

For the web-based interface, you can also run:

```bash
cd mini_project/src
python web_interactive_arm.py
```

This will start a local HTTP server and open the web interface in your browser.
*Note: The web interface requires additional dependencies (open3d, trimesh) for full 3D visualization.*

## Features

- **2D Robotic Arm Simulation**: Forward and inverse kinematics, pick and place operations
- **3D Physics Simulation**: Real-time PyBullet integration with 4-DOF control
- **Web Interface**: Browser-based control panel with real-time updates
- **Workspace Analysis**: Comprehensive reachability and performance analysis
- **Interactive Controls**: Multiple interfaces including GUI, web, and command-line

## Dependencies

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Core requirements:
- numpy
- matplotlib  
- scipy
- opencv-python
- pybullet

Optional dependencies for advanced 3D web interface:
- open3d
- trimesh

## Project Structure

- `main.py` - Main entry point for demonstrations
- `assignment1/` - 2D robotic arm simulations and analysis
- `mini_project/` - 3D interactive robotic arm with web interface
- `requirements.txt` - Python dependencies

For detailed documentation, see the README files in each subdirectory.