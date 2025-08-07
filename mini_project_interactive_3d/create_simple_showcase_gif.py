"""
Simple Showcase GIF Generator
Creates a demonstration GIF showcasing developed features using existing functionality
"""
import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

class SimpleShowcaseGenerator:
    """Generates showcase GIF using existing materials"""
    
    def __init__(self):
        """Initialize showcase generator"""
        self.output_dir = Path("showcase_output")
        self.output_dir.mkdir(exist_ok=True)
        
    def create_title_frames(self):
        """Create title and feature showcase frames"""
        print("Creating title and feature frames...")
        
        # Main title frame
        title_frame = self.create_text_frame(
            "🚜 JCB Interactive Robotic Arm System",
            "Complete CAD Integration & VFX-Quality Simulation",
            (255, 180, 0),
            (30, 30, 50)
        )
        
        # Save title frame multiple times for duration
        for i in range(45):  # 1.5 seconds at 30fps
            title_frame.save(self.output_dir / f"title_{i:03d}.png")
        
        # Feature frames
        features = [
            {
                "title": "🎮 Interactive 4-DOF Control",
                "subtitle": "Real-time sliders • Boom • Stick • Bucket • Rotation",
                "color": (0, 255, 120)
            },
            {
                "title": "📦 Authentic CAD Integration", 
                "subtitle": "Raushan Tiwari Engineering Files • IGS • STEP • SLDPRT",
                "color": (255, 100, 0)
            },
            {
                "title": "📷 Multiple Camera Views",
                "subtitle": "Wide Shot • Operator View • Action Shot • Dramatic Angles",
                "color": (100, 150, 255)
            },
            {
                "title": "🎬 VFX-Quality Rendering",
                "subtitle": "Professional Lighting • Realistic Textures • Construction Site",
                "color": (255, 100, 150)
            },
            {
                "title": "⚡ Real-Time Physics",
                "subtitle": "240Hz Simulation • PyBullet Engine • Authentic Dynamics",
                "color": (150, 255, 100)
            }
        ]
        
        for idx, feature in enumerate(features):
            feature_frame = self.create_text_frame(
                feature["title"],
                feature["subtitle"], 
                feature["color"],
                (20, 25, 35)
            )
            
            # Save feature frame for 30 frames (1 second)
            for i in range(30):
                feature_frame.save(self.output_dir / f"feature_{idx}_{i:03d}.png")
    
    def create_text_frame(self, title, subtitle, color, bg_color):
        """Create a text frame with professional styling"""
        img = Image.new('RGB', (1920, 1080), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Create gradient background
        for y in range(1080):
            alpha = y / 1080
            r = int(bg_color[0] + (50 - bg_color[0]) * alpha)
            g = int(bg_color[1] + (50 - bg_color[1]) * alpha) 
            b = int(bg_color[2] + (80 - bg_color[2]) * alpha)
            draw.line([(0, y), (1920, y)], fill=(r, g, b))
        
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 100)
            subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 60)
        except:
            # Fallback fonts
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
        
        # Calculate text positions
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (1920 - title_width) // 2
        title_y = 350
        
        subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        subtitle_width = subtitle_bbox[2] - subtitle_bbox[0] 
        subtitle_x = (1920 - subtitle_width) // 2
        subtitle_y = 500
        
        # Add text shadows for depth
        shadow_offset = 4
        draw.text((title_x + shadow_offset, title_y + shadow_offset), title, 
                 font=title_font, fill=(0, 0, 0, 128))
        draw.text((subtitle_x + shadow_offset, subtitle_y + shadow_offset), subtitle,
                 font=subtitle_font, fill=(0, 0, 0, 128))
        
        # Add main text
        draw.text((title_x, title_y), title, font=title_font, fill=color)
        draw.text((subtitle_x, subtitle_y), subtitle, font=subtitle_font, fill=(255, 255, 255))
        
        # Add decorative elements
        draw.ellipse([(title_x - 100, title_y - 20), (title_x - 20, title_y + 20)], fill=color)
        draw.ellipse([(title_x + title_width + 20, title_y - 20), 
                     (title_x + title_width + 100, title_y + 20)], fill=color)
        
        return img
    
    def create_code_showcase_frames(self):
        """Create frames showing code capabilities"""
        print("Creating code showcase frames...")
        
        code_examples = [
            {
                "title": "PyBullet Integration",
                "code": "# Real-time 3D physics simulation\narm = JCBRoboticArm()\narm.setup_interactive_controls()\narm.run_simulation()",
                "color": (0, 255, 100)
            },
            {
                "title": "CAD File Processing", 
                "code": "# Multi-format CAD support\nprocessor = CADProcessor()\nprocessor.load_jcb_files(['IGS', 'STEP', 'SLDPRT'])\nprocessor.optimize_for_pybullet()",
                "color": (255, 150, 0)
            },
            {
                "title": "Interactive Controls",
                "code": "# 4-DOF real-time control\ncontrols = {\n    'boom': slider_boom.value,\n    'stick': slider_stick.value,\n    'bucket': slider_bucket.value\n}",
                "color": (100, 150, 255)
            }
        ]
        
        for idx, example in enumerate(code_examples):
            code_frame = self.create_code_frame(example["title"], example["code"], example["color"])
            
            # Save code frame for 40 frames
            for i in range(40):
                code_frame.save(self.output_dir / f"code_{idx}_{i:03d}.png")
    
    def create_code_frame(self, title, code, color):
        """Create a frame showing code example"""
        img = Image.new('RGB', (1920, 1080), (15, 15, 25))
        draw = ImageDraw.Draw(img)
        
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
            code_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 50)
        except:
            title_font = ImageFont.load_default()
            code_font = ImageFont.load_default()
        
        # Title
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (1920 - title_width) // 2
        draw.text((title_x, 200), title, font=title_font, fill=color)
        
        # Code box background
        draw.rectangle([(200, 350), (1720, 750)], fill=(25, 25, 35), outline=color, width=3)
        
        # Code text
        code_lines = code.split('\n')
        for i, line in enumerate(code_lines):
            draw.text((250, 400 + i * 60), line, font=code_font, fill=(255, 255, 255))
        
        return img
    
    def copy_existing_gifs(self):
        """Copy existing GIF files for inclusion"""
        print("Including existing demonstration materials...")
        
        existing_gifs = [
            "enhanced_jcb_interactive_demo.gif",
            "interactive_jcb_robotic_arm_demo.gif"
        ]
        
        frame_count = len(os.listdir(self.output_dir))
        
        for gif_file in existing_gifs:
            if os.path.exists(gif_file):
                try:
                    # Extract frames from existing GIF
                    gif = Image.open(gif_file)
                    for frame_idx in range(min(30, gif.n_frames)):  # Limit frames
                        gif.seek(frame_idx)
                        frame = gif.copy()
                        frame = frame.resize((1920, 1080), Image.Resampling.LANCZOS)
                        frame.save(self.output_dir / f"existing_{frame_count + frame_idx:03d}.png")
                    frame_count += 30
                except Exception as e:
                    print(f"Could not process {gif_file}: {e}")
    
    def compile_final_gif(self):
        """Compile all frames into final GIF"""
        print("Compiling final showcase GIF...")
        
        # Get all frames in order
        frame_files = sorted([f for f in os.listdir(self.output_dir) if f.endswith('.png')])
        
        if not frame_files:
            print("No frames found!")
            return None
        
        print(f"Processing {len(frame_files)} frames...")
        
        # Load frames
        frames = []
        for frame_file in frame_files:
            frame_path = self.output_dir / frame_file
            img = Image.open(frame_path)
            # Optimize size for web
            img = img.resize((960, 540), Image.Resampling.LANCZOS)
            frames.append(img)
        
        # Create final GIF
        output_path = Path("comprehensive_jcb_showcase.gif")
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=100,  # 100ms per frame = 10fps
            loop=0,
            optimize=True,
            quality=85
        )
        
        file_size = output_path.stat().st_size / (1024 * 1024)
        print(f"\n🎉 GIF created successfully!")
        print(f"📁 File: {output_path}")
        print(f"📊 Size: {file_size:.1f} MB")
        print(f"🎬 Frames: {len(frames)}")
        print(f"⏱️  Duration: ~{len(frames) * 0.1:.1f} seconds")
        
        return output_path

def main():
    """Generate comprehensive showcase GIF"""
    print("🚜 Generating JCB Interactive Arm Showcase GIF...")
    print("=" * 60)
    
    generator = SimpleShowcaseGenerator()
    
    # Create different types of frames
    generator.create_title_frames()
    generator.create_code_showcase_frames() 
    generator.copy_existing_gifs()
    
    # Compile final GIF
    gif_path = generator.compile_final_gif()
    
    if gif_path:
        print("\n" + "=" * 60)
        print("🎯 SHOWCASE FEATURES DEMONSTRATED:")
        print("   ✅ Interactive 4-DOF Control System")
        print("   ✅ Authentic CAD File Integration") 
        print("   ✅ Multiple Professional Camera Views")
        print("   ✅ VFX-Quality Rendering & Lighting")
        print("   ✅ Real-Time Physics Simulation")
        print("   ✅ Professional JCB Styling")
        print("=" * 60)
        print(f"🎬 Your showcase GIF is ready: {gif_path}")
    else:
        print("❌ Failed to create GIF")

if __name__ == "__main__":
    main()