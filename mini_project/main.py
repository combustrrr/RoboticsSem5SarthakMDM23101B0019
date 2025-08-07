#!/usr/bin/env python3
"""
Interactive 3D JCB Robotic Arm Mini Project
==========================================

Main entry point for the interactive 3D robotic arm simulation system.
This system provides multiple interfaces for controlling and visualizing
a professional JCB-style robotic arm with realistic physics and rendering.

Author: Sarthak MDM23101B0019
Course: Robotics Semester 5
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("🚜 INTERACTIVE 3D JCB ROBOTIC ARM SIMULATION")
    print("=" * 60)
    print("Author: Sarthak MDM23101B0019")
    print("Course: Robotics Semester 5")
    print("=" * 60)

def show_menu():
    """Display main menu options"""
    print("\nAvailable Simulation Modes:")
    print("1. Enhanced CAD Interactive Arm (Recommended)")
    print("2. Web-Based Interactive Interface") 
    print("3. Real CAD Integration System")
    print("4. Matplotlib Interactive Visualization")
    print("5. Realistic Texture System Demo")
    print("6. Exit")
    print("-" * 40)

def main():
    """Main application entry point"""
    print_banner()
    
    while True:
        show_menu()
        try:
            choice = input("Select mode (1-6): ").strip()
            
            if choice == '1':
                print("\n🚜 Starting Enhanced CAD Interactive Arm...")
                from enhanced_cad_interactive_arm import main as enhanced_main
                enhanced_main()
                
            elif choice == '2':
                print("\n🌐 Starting Web-Based Interface...")
                from web_interactive_arm import main as web_main
                web_main()
                
            elif choice == '3':
                print("\n📐 Starting Real CAD Integration...")
                from real_cad_integration import main as cad_main
                cad_main()
                
            elif choice == '4':
                print("\n📊 Starting Matplotlib Visualization...")
                from interactive_matplotlib_arm import main as matplotlib_main
                matplotlib_main()
                
            elif choice == '5':
                print("\n🎨 Starting Realistic Texture Demo...")
                from realistic_texture_system import main as texture_main
                texture_main()
                
            elif choice == '6':
                print("\n👋 Thank you for using the JCB Robotic Arm Simulator!")
                break
                
            else:
                print("❌ Invalid choice. Please select 1-6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Exiting application...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please check that all dependencies are installed.")

if __name__ == "__main__":
    main()