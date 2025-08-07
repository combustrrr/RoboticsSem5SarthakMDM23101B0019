# JCB CAD Integration Usage Examples

## Quick Start
```bash
# 1. Setup the system
python setup_cad_integration.py

# 2. Process CAD files (if ZIP available)
python cad_file_processor.py

# 3. Launch interactive simulation
python enhanced_cad_interactive_arm.py
```

## Interactive Controls
### Joint Control Sliders
- **Boom**: -0.5 to 1.2 radians (main arm lift)
- **Stick**: -1.8 to 0.5 radians (secondary arm extend)
- **Bucket**: -1.5 to 1.0 radians (bucket curl)
- **Rotation**: -π to π radians (base rotation)

### Camera Views
- **0 - Wide Shot**: Overview of entire operation
- **1 - Operator View**: From operator cab perspective
- **2 - Action Shot**: Close-up of digging action
- **3 - Dramatic Low**: Low-angle cinematic view

### Demo Mode
- Set **Demo Mode** slider to 1 to run automatic excavation sequence
- Demonstrates: Approach → Dig → Lift → Dump → Return

## Computer Graphics Project Integration
### Video Recording
```python
# Record demo sequence for presentations
arm_system = EnhancedCADIntegratedArm()
arm_system.record_demo_sequence('demo_video.mp4')
```

### Screenshot Capture
```python
# Capture high-resolution screenshots
arm_system.capture_screenshot('jcb_presentation.png', resolution=(1920, 1080))
```

### Custom Animations
```python
# Create custom movement sequences
positions = [
    [0.0, -0.3, 0.2, 0.0],  # Rest
    [0.8, -0.8, 0.8, 0.5],  # Dig position
    [1.0, 0.2, -0.5, 1.0], # Lift and dump
]
arm_system.animate_sequence(positions, duration=10.0)
```

## Technical Specifications
- **Degrees of Freedom**: 4 (Boom, Stick, Bucket, Base Rotation)
- **Max Reach**: 8.0 meters
- **Max Dig Depth**: 6.2 meters
- **Bucket Capacity**: 1.2 cubic meters
- **Operating Weight**: 14,500 kg
- **Simulation Rate**: 240 Hz physics, 60 Hz rendering
- **Rendering Quality**: VFX-grade with professional lighting

