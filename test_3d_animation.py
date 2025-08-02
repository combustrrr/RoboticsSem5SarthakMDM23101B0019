"""
Test script for 3D Robotic Arm Animation
Tests functionality without GUI for CI/server environments
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pybullet_arm_animation import PyBulletRoboticArm
import numpy as np


def test_3d_arm_headless():
    """Test 3D arm functionality in headless mode"""
    print("Testing 3D Robotic Arm in headless mode...")
    
    try:
        # Create arm simulation without GUI
        arm_sim = PyBulletRoboticArm(gui=False)
        
        # Test joint control
        print("Testing joint control...")
        test_positions = [0.5, -0.8, 1.2, 0.3]
        arm_sim.set_joint_positions(test_positions)
        
        # Get joint positions
        current_positions = arm_sim.get_joint_positions()
        print(f"Set positions: {test_positions}")
        print(f"Current positions: {[f'{p:.3f}' for p in current_positions]}")
        
        # Test end effector position
        end_pos = arm_sim.get_end_effector_position()
        print(f"End effector position: ({end_pos[0]:.3f}, {end_pos[1]:.3f}, {end_pos[2]:.3f})")
        
        # Cleanup
        arm_sim.cleanup()
        
        print("✓ 3D Robotic Arm test completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def test_animation_sequence():
    """Test the animation sequence in fast mode"""
    print("\nTesting animation sequence (fast mode)...")
    
    try:
        arm_sim = PyBulletRoboticArm(gui=False)
        
        # Test a short animation sequence
        poses = [
            [0.2, -0.5, 0.8, 0.0],
            [0.4, -1.0, 1.5, 0.3],
            [0.2, -0.5, 0.8, 0.0]
        ]
        
        for i, pose in enumerate(poses):
            print(f"Setting pose {i+1}: {pose}")
            arm_sim.set_joint_positions(pose)
            
            # Simulate a few steps
            import pybullet as p
            for _ in range(10):
                p.stepSimulation()
            
            end_pos = arm_sim.get_end_effector_position()
            print(f"  End effector at: ({end_pos[0]:.3f}, {end_pos[1]:.3f}, {end_pos[2]:.3f})")
        
        arm_sim.cleanup()
        print("✓ Animation sequence test completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Animation test failed: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("3D ROBOTIC ARM ANIMATION TEST")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Run tests
    all_tests_passed &= test_3d_arm_headless()
    all_tests_passed &= test_animation_sequence()
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED! 3D Animation is ready to use.")
        print("\nTo run the interactive 3D animation:")
        print("python pybullet_arm_animation.py")
        print("\nOr use the main menu:")
        print("python main.py  # Select option 3")
    else:
        print("❌ Some tests failed. Check the error messages above.")
    print("=" * 50)