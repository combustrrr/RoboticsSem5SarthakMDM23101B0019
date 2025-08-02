"""
Pick and Place Simulation with Animation
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from robot_arm import RoboticArm
import time


class PickAndPlaceSimulation:
    """Simulation of pick and place operations with animation"""
    
    def __init__(self, robot_arm):
        """
        Initialize the simulation
        
        Args:
            robot_arm (RoboticArm): The robotic arm instance
        """
        self.robot = robot_arm
        self.objects = []
        self.target_locations = []
        self.animation_data = []
        
        # Set up the plot
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.ax.set_xlim(-np.sum(robot_arm.link_lengths) * 1.2, np.sum(robot_arm.link_lengths) * 1.2)
        self.ax.set_ylim(-np.sum(robot_arm.link_lengths) * 1.2, np.sum(robot_arm.link_lengths) * 1.2)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_title('Robotic Arm Pick and Place Simulation')
        
        # Initialize plot elements
        self.arm_line, = self.ax.plot([], [], 'b-', linewidth=3, label='Robot Arm')
        self.joints_scatter = self.ax.scatter([], [], c='red', s=100, zorder=5, label='Joints')
        self.end_effector = self.ax.scatter([], [], c='green', s=150, marker='*', zorder=6, label='End Effector')
        self.objects_scatter = self.ax.scatter([], [], c='orange', s=200, marker='s', zorder=4, label='Objects')
        self.targets_scatter = self.ax.scatter([], [], c='purple', s=200, marker='x', zorder=4, label='Targets')
        
        self.ax.legend()
    
    def add_object(self, x, y):
        """Add an object to pick up"""
        self.objects.append([x, y])
    
    def add_target(self, x, y):
        """Add a target location for placing objects"""
        self.target_locations.append([x, y])
    
    def interpolate_path(self, start_angles, end_angles, steps=50):
        """
        Interpolate between two joint configurations
        
        Args:
            start_angles (array): Starting joint angles
            end_angles (array): Ending joint angles
            steps (int): Number of interpolation steps
            
        Returns:
            array: Interpolated joint angles
        """
        path = []
        for i in range(steps):
            t = i / (steps - 1)
            interpolated = start_angles + t * (end_angles - start_angles)
            path.append(interpolated)
        return np.array(path)
    
    def plan_pick_and_place(self):
        """
        Plan the complete pick and place sequence
        
        Returns:
            list: Sequence of joint angle configurations
        """
        sequence = []
        current_angles = self.robot.joint_angles.copy()
        
        # Home position
        home_angles = np.zeros(self.robot.num_joints)
        sequence.extend(self.interpolate_path(current_angles, home_angles))
        current_angles = home_angles
        
        # For each object, pick it up and place it
        for i, obj in enumerate(self.objects):
            if i < len(self.target_locations):
                target = self.target_locations[i]
                
                # Move to pick position
                pick_angles = self.robot.inverse_kinematics(obj[0], obj[1])
                if pick_angles is not None:
                    sequence.extend(self.interpolate_path(current_angles, pick_angles))
                    current_angles = pick_angles
                    
                    # Simulate picking (pause)
                    for _ in range(10):
                        sequence.append(current_angles.copy())
                    
                    # Move to place position
                    place_angles = self.robot.inverse_kinematics(target[0], target[1])
                    if place_angles is not None:
                        sequence.extend(self.interpolate_path(current_angles, place_angles))
                        current_angles = place_angles
                        
                        # Simulate placing (pause)
                        for _ in range(10):
                            sequence.append(current_angles.copy())
                        
                        # Move object to target location
                        obj[0] = target[0]
                        obj[1] = target[1]
        
        # Return to home
        sequence.extend(self.interpolate_path(current_angles, home_angles))
        
        return sequence
    
    def update_animation(self, frame):
        """Update function for animation"""
        if frame < len(self.animation_data):
            angles = self.animation_data[frame]
            self.robot.set_joint_angles(angles)
            
            # Get current robot configuration
            joint_positions = self.robot.get_joint_positions()
            end_pos, _ = self.robot.forward_kinematics()
            
            # Update arm visualization
            self.arm_line.set_data(joint_positions[:, 0], joint_positions[:, 1])
            self.joints_scatter.set_offsets(joint_positions[:-1])  # Exclude end effector
            self.end_effector.set_offsets([[end_pos[0], end_pos[1]]])
            
            # Update objects
            if self.objects:
                objects_array = np.array(self.objects)
                self.objects_scatter.set_offsets(objects_array)
            
            # Update targets
            if self.target_locations:
                targets_array = np.array(self.target_locations)
                self.targets_scatter.set_offsets(targets_array)
        
        return self.arm_line, self.joints_scatter, self.end_effector, self.objects_scatter, self.targets_scatter
    
    def run_simulation(self):
        """Run the pick and place simulation"""
        # Plan the motion
        self.animation_data = self.plan_pick_and_place()
        
        # Create animation
        anim = FuncAnimation(
            self.fig, self.update_animation, frames=len(self.animation_data),
            interval=50, blit=True, repeat=True
        )
        
        plt.tight_layout()
        plt.show()
        return anim


def demo_pick_and_place():
    """Demonstration of pick and place simulation"""
    # Create a 3-link robotic arm
    link_lengths = [3.0, 2.5, 1.5]
    robot = RoboticArm(link_lengths)
    
    # Create simulation
    sim = PickAndPlaceSimulation(robot)
    
    # Add objects to pick up
    sim.add_object(4.0, 2.0)
    sim.add_object(3.5, -1.5)
    sim.add_object(-2.0, 3.0)
    
    # Add target locations
    sim.add_target(-4.0, 1.0)
    sim.add_target(-3.0, -2.0)
    sim.add_target(1.0, -4.0)
    
    print("Starting pick and place simulation...")
    print("Objects to pick:", sim.objects)
    print("Target locations:", sim.target_locations)
    
    # Run simulation
    animation = sim.run_simulation()
    return animation


if __name__ == "__main__":
    demo_pick_and_place()