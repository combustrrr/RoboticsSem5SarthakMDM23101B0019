"""
Test workspace analysis without interactive plotting
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

from workspace_analysis import WorkspaceAnalyzer
from robot_simulation import RobotArm
import matplotlib.pyplot as plt


def test_workspace_analysis():
    """Test workspace analysis functionality."""
    print("Testing Workspace Analysis...")
    
    # Create robot and analyzer
    robot = RobotArm(link1_length=3.0, link2_length=2.0)
    analyzer = WorkspaceAnalyzer(robot)
    
    # Test workspace point generation
    x_points, y_points, theta1_vals, theta2_vals = analyzer.generate_workspace_points(
        theta1_resolution=20, theta2_resolution=10
    )
    
    print(f"Generated {len(x_points)} workspace points")
    print(f"X range: {min(x_points):.2f} to {max(x_points):.2f}")
    print(f"Y range: {min(y_points):.2f} to {max(y_points):.2f}")
    
    # Test reachability map
    X, Y, reachability_map = analyzer.calculate_reachability_map(
        x_range=(-2, 2), y_range=(-2, 2), resolution=0.5
    )
    
    reachable_count = int(reachability_map.sum())
    total_count = reachability_map.size
    print(f"Reachability map: {reachable_count}/{total_count} points reachable")
    
    # Test manipulability calculation
    manipulability = analyzer.calculate_manipulability(
        x_points[:10], y_points[:10], theta1_vals[:10], theta2_vals[:10]
    )
    
    print(f"Manipulability test: calculated {len(manipulability)} values")
    print(f"Mean manipulability: {manipulability.mean():.4f}")
    
    # Test Jacobian calculation
    J = analyzer.calculate_jacobian(0.5, 0.5)
    print(f"Jacobian test: shape {J.shape}")
    print(f"Jacobian determinant: {J[0,0]*J[1,1] - J[0,1]*J[1,0]:.4f}")
    
    # Generate and save workspace statistics
    analyzer.print_workspace_statistics()
    
    # Create a simple plot and save it
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(x_points, y_points, c='lightblue', s=1, alpha=0.6)
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_title('Robot Workspace Test')
    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    
    plt.savefig('/tmp/workspace_test.png', dpi=150, bbox_inches='tight')
    print("Workspace plot saved to /tmp/workspace_test.png")
    plt.close()


if __name__ == "__main__":
    test_workspace_analysis()
    print("Workspace analysis test completed!")