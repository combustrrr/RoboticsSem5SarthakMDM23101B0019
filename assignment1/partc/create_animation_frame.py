"""
Create a static frame showing the sorting animation
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from conveyor_sorting_system import SortingSystem

def create_sorting_animation_frame():
    """Create a static frame showing the sorting operation"""
    print("Creating sorting animation frame...")
    
    system = SortingSystem()
    
    # Populate with objects in different states
    from conveyor_sorting_system import ConveyorObject
    
    # Object being detected
    obj1 = ConveyorObject(x=-0.5, y=-3.0, size='medium', color='red', width=0.4, height=0.4)
    
    # Object being picked
    obj2 = ConveyorObject(x=0.0, y=-2.7, size='small', color='blue', width=0.2, height=0.2)
    obj2.picked = True
    
    # Object moving on belt
    obj3 = ConveyorObject(x=-2.0, y=-3.1, size='large', color='green', width=0.6, height=0.6)
    
    system.conveyor.objects = [obj1, obj2, obj3]
    
    # Set arm in picking position
    pick_config = np.array([np.pi/6, np.pi/4, 0.8, -np.pi/4])
    system.arm.set_joint_configuration(pick_config)
    
    # Create visualization
    fig, ax = plt.subplots(figsize=(12, 8))
    system.visualize_system(ax)
    
    # Add animation state indicators
    ax.text(-4, 3.5, "SORTING OPERATION IN PROGRESS", 
           fontsize=14, fontweight='bold', 
           bbox=dict(boxstyle="round,pad=0.5", facecolor="yellow", alpha=0.8))
    
    # Add object status annotations
    ax.annotate('Detecting', xy=(-0.5, -3.0), xytext=(-0.5, -1.5),
               arrowprops=dict(arrowstyle='->', color='red', lw=2),
               fontsize=10, ha='center', color='red', fontweight='bold')
    
    ax.annotate('Picking', xy=(0.0, -2.7), xytext=(1.0, -1.0),
               arrowprops=dict(arrowstyle='->', color='blue', lw=2),
               fontsize=10, ha='center', color='blue', fontweight='bold')
    
    ax.annotate('Moving on Belt', xy=(-2.0, -3.1), xytext=(-2.0, -1.5),
               arrowprops=dict(arrowstyle='->', color='green', lw=2),
               fontsize=10, ha='center', color='green', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('sorting_animation_frame.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Saved sorting_animation_frame.png")

if __name__ == "__main__":
    create_sorting_animation_frame()