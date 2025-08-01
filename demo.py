"""
Demo script for robot simulation - shows animated pick and place
This script demonstrates the robot simulation with minimal user interaction.
"""

from robot_simulation import PickPlaceSimulation
import matplotlib.pyplot as plt
import time


def automated_demo():
    """Run automated demo without user input."""
    print("Industrial Robot Pick and Place Simulation - Automated Demo")
    print("=" * 60)
    
    # Create simulation
    simulation = PickPlaceSimulation()
    
    # Show the plot
    plt.ion()  # Turn on interactive mode
    plt.show()
    
    # Initial robot position
    simulation.robot.joint1_angle = 0.5
    simulation.robot.joint2_angle = 0.3
    simulation.update_robot_plot()
    plt.pause(2.0)
    
    print("Starting automated pick and place sequence...")
    
    # Execute the sequence with automatic timing
    sequence_steps = [
        ("Moving to home position...", simulation.home_position),
        ("Moving to pick location...", simulation.pick_location),
        ("Picking object...", None),
        ("Moving to place location...", simulation.place_location),
        ("Placing object...", None),
        ("Returning to home position...", simulation.home_position),
    ]
    
    for step_name, target_pos in sequence_steps:
        print(step_name)
        
        if target_pos is not None:
            # Move to position
            trajectory = simulation.robot.move_to_position(target_pos[0], target_pos[1])
            simulation.animate_trajectory(trajectory, delay=0.1)
        else:
            # Pick or place action
            if "Picking" in step_name:
                simulation.robot.carrying_object = True
                simulation.object_at_pick = False
            elif "Placing" in step_name:
                simulation.robot.carrying_object = False
                simulation.object_circle.center = simulation.place_location
            
            simulation.update_robot_plot()
            plt.pause(1.5)
    
    print("\nPick and place sequence completed!")
    print("Close the plot window when ready.")
    
    # Keep the plot open until user closes it
    try:
        plt.show(block=True)
    except KeyboardInterrupt:
        print("Demo interrupted by user.")


def interactive_demo():
    """Run interactive demo with user prompts."""
    print("Industrial Robot Pick and Place Simulation - Interactive Demo")
    print("=" * 60)
    
    simulation = PickPlaceSimulation()
    simulation.run_simulation()


def workspace_demo():
    """Run workspace analysis demo."""
    print("Robot Workspace Analysis Demo")
    print("=" * 30)
    
    from workspace_analysis import WorkspaceAnalyzer, RobotArm
    
    # Create robot and analyzer
    robot = RobotArm(link1_length=3.0, link2_length=2.0)
    analyzer = WorkspaceAnalyzer(robot)
    
    # Print statistics
    analyzer.print_workspace_statistics()
    
    # Show plots
    print("\nGenerating comprehensive workspace analysis...")
    fig = analyzer.plot_comprehensive_analysis()
    plt.show()


def main():
    """Main demo menu."""
    print("Robot Simulation Demo Options:")
    print("1. Automated Pick & Place Demo (no interaction required)")
    print("2. Interactive Pick & Place Demo (press Enter to proceed)")
    print("3. Workspace Analysis Demo")
    print("4. Run all tests")
    
    try:
        choice = input("\nEnter your choice (1-4) [default: 1]: ").strip()
        if not choice:
            choice = "1"
    except (EOFError, KeyboardInterrupt):
        choice = "1"
        print("1")  # Show what was selected
    
    if choice == "1":
        automated_demo()
    elif choice == "2":
        interactive_demo()
    elif choice == "3":
        workspace_demo()
    elif choice == "4":
        print("Running all tests...")
        import test_kinematics
        import test_simulation
        print("All tests completed!")
        print("\nNow running automated demo...")
        time.sleep(2)
        automated_demo()
    else:
        print("Invalid choice, running automated demo...")
        automated_demo()


if __name__ == "__main__":
    main()