"""
CAD File Integration Setup Script
Prepares the system for using real JCB CAD files from Raushan Tiwari
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path
import zipfile

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    
    requirements = [
        "pybullet>=3.2.0",
        "trimesh>=3.15.0", 
        "open3d>=0.16.0",
        "pillow>=9.0.0",
        "numpy>=1.21.0",
        "beautifulsoup4>=4.11.0",
        "requests>=2.28.0"
    ]
    
    for req in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", req])
            print(f"   ✅ {req}")
        except subprocess.CalledProcessError:
            print(f"   ⚠️  Failed to install {req}")
    
    print("✅ Package installation complete")

def setup_directories():
    """Setup required directories"""
    print("📁 Setting up directories...")
    
    directories = [
        "cad_integration_project",
        "cad_integration_project/original_cad",
        "cad_integration_project/processed_meshes", 
        "cad_integration_project/authentic_textures",
        "demonstration_output"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(exist_ok=True, parents=True)
        print(f"   📂 {dir_path}")
    
    print("✅ Directory setup complete")

def check_zip_file():
    """Check for CAD ZIP file"""
    print("🔍 Checking for CAD ZIP file...")
    
    # Look for the specific ZIP file
    zip_patterns = [
        "jcb-back-arm-1.snapshot.4.zip",
        "jcb-back-arm-1*.zip",
        "*jcb*.zip"
    ]
    
    found_zip = None
    for pattern in zip_patterns:
        zip_files = list(Path(".").glob(pattern))
        if zip_files:
            found_zip = zip_files[0]
            break
    
    if found_zip:
        print(f"✅ Found CAD ZIP file: {found_zip}")
        return str(found_zip)
    else:
        print("📋 No CAD ZIP file found")
        print("\n💡 To use real CAD files:")
        print("   1. Download jcb-back-arm-1.snapshot.4.zip")
        print("   2. Place it in this directory")
        print("   3. Run this setup script again")
        return None

def extract_cad_files(zip_path):
    """Extract CAD files"""
    print(f"📦 Extracting {zip_path}...")
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            extract_path = Path("cad_integration_project/original_cad")
            zip_ref.extractall(extract_path)
        
        # List extracted files
        extracted_files = list(extract_path.rglob("*"))
        cad_files = [f for f in extracted_files if f.suffix.lower() in 
                    ['.igs', '.step', '.stp', '.sldprt', '.obj', '.stl']]
        image_files = [f for f in extracted_files if f.suffix.lower() in 
                      ['.png', '.jpg', '.jpeg']]
        
        print(f"   📄 {len(cad_files)} CAD files extracted")
        print(f"   🖼️  {len(image_files)} image files extracted")
        
        return True
        
    except Exception as e:
        print(f"❌ Error extracting ZIP: {e}")
        return False

def create_quick_start_guide():
    """Create a quick start guide"""
    guide_content = """# JCB CAD Integration Quick Start Guide

## 🚜 Enhanced CAD-Integrated JCB Robotic Arm System

This system utilizes authentic JCB CAD files created by Raushan Tiwari for professional simulation.

## 🎮 How to Use

### 1. Basic Interactive System
```bash
python enhanced_cad_interactive_arm.py
```

**Controls:**
- 🎚️ **Sliders**: Control each joint (Boom, Stick, Bucket, Rotation) 
- 📷 **Camera View**: Switch between 4 cinematic camera angles
- 🎬 **Demo Mode**: Automatic excavation demonstration
- ⌨️ **Keyboard**: Press 'q' to quit

### 2. CAD File Processing
```bash
python cad_file_processor.py
```

Processes authentic CAD files and creates optimized meshes for simulation.

### 3. Original Interactive Systems
```bash
python interactive_3d_robotic_arm.py     # Original PyBullet system
python realistic_texture_system.py       # Photorealistic textures
python realistic_web_interface.py        # Web-based control
```

## 📐 JCB Specifications

- **Max Reach**: 8.0m
- **Max Dig Depth**: 6.2m  
- **Bucket Capacity**: 1.2m³
- **Operating Weight**: 14,500kg
- **Engine Power**: 100kW

## 🎯 Perfect for Computer Graphics Projects

- ✅ **Photorealistic 3D Rendering**
- ✅ **Real-time Interactive Control**
- ✅ **Professional VFX-Quality Lighting**
- ✅ **Authentic JCB Design Elements**
- ✅ **Multiple Camera Angles for Presentation**

## 📁 File Structure

```
mini_project_interactive_3d/
├── enhanced_cad_interactive_arm.py       # Main enhanced system
├── cad_file_processor.py                 # CAD file processing
├── realistic_texture_system.py           # Photorealistic textures
├── realistic_web_interface.py            # Web interface
├── cad_integration_project/              # CAD files and processing
│   ├── original_cad/                     # Original CAD files
│   ├── processed_meshes/                 # Processed mesh files
│   └── authentic_textures/               # Reference images
└── demonstration_output/                 # Generated demonstrations
```

## 🔧 CAD File Sources

- **Original Files**: Created by Raushan Tiwari (Mechanical Engineer)
- **Source**: GrabCAD (https://grabcad.com/library/jcb-back-arm-1)
- **Formats Supported**: IGS, STEP, SLDPRT, OBJ, STL
- **Reference Images**: JCB Arm.png, JCB Arm 1.png, JCB Arm 2.png

---

Ready to showcase your virtual robot prototype! 🚜✨
"""
    
    with open("QUICK_START_GUIDE.md", 'w') as f:
        f.write(guide_content)
    
    print("📋 Created QUICK_START_GUIDE.md")

def main():
    """Main setup function"""
    print("🚜 JCB CAD Integration Setup")
    print("=" * 40)
    
    # Install requirements
    install_requirements()
    
    # Setup directories
    setup_directories()
    
    # Check for ZIP file
    zip_path = check_zip_file()
    
    # Extract if found
    if zip_path:
        if extract_cad_files(zip_path):
            print("✅ CAD files ready for processing")
        
        # Run CAD processor
        print("\n🔧 Running CAD processor...")
        try:
            subprocess.run([sys.executable, "cad_file_processor.py"])
        except:
            print("⚠️  CAD processor will run when needed")
    
    # Create quick start guide
    create_quick_start_guide()
    
    print("\n🎯 Setup Complete!")
    print("\n🚀 To start the enhanced system:")
    print("   python enhanced_cad_interactive_arm.py")
    print("\n📖 See QUICK_START_GUIDE.md for full instructions")

if __name__ == "__main__":
    main()