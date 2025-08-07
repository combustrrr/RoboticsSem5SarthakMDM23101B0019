"""
Web-Based Interface for Realistic JCB Robotic Arm
Provides browser-based control with realistic texture showcase
"""
import os
import time
import math
import threading
import base64
from pathlib import Path
from flask import Flask, render_template_string, jsonify, request, send_file
import webbrowser
from realistic_texture_system import EnhancedRealisticRoboticArm, RealisticTextureManager
import pybullet as p
import numpy as np
from PIL import Image
import io


class RealisticWebInterface:
    """Web interface for realistic JCB robotic arm control"""
    
    def __init__(self):
        """Initialize web interface"""
        self.app = Flask(__name__)
        self.arm = None
        self.texture_manager = None
        self.current_joint_positions = [0, 0, 0, 0]
        self.setup_routes()
        
    def setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            return render_template_string(self.get_html_template())
        
        @self.app.route('/api/control', methods=['POST'])
        def control_arm():
            try:
                data = request.json
                self.current_joint_positions = [
                    data.get('base_rotation', 0),
                    data.get('boom_angle', 0),
                    data.get('stick_angle', 0),
                    data.get('bucket_angle', 0)
                ]
                
                if self.arm:
                    # Apply joint positions
                    for i, pos in enumerate(self.current_joint_positions):
                        p.setJointMotorControl2(
                            self.arm.robot_id,
                            i,
                            p.POSITION_CONTROL,
                            targetPosition=pos,
                            force=1000
                        )
                    p.stepSimulation()
                
                return jsonify({'status': 'success', 'positions': self.current_joint_positions})
            except Exception as e:
                return jsonify({'status': 'error', 'message': str(e)})
        
        @self.app.route('/api/screenshot')
        def get_screenshot():
            try:
                if self.arm:
                    # Take screenshot
                    width, height = 800, 600
                    view_matrix = p.computeViewMatrixFromYawPitchRoll(
                        cameraTargetPosition=[0, 0, 2],
                        distance=8,
                        yaw=45,
                        pitch=-20,
                        roll=0,
                        upAxisIndex=2
                    )
                    proj_matrix = p.computeProjectionMatrixFOV(
                        fov=60,
                        aspect=width/height,
                        nearVal=0.1,
                        farVal=100.0
                    )
                    
                    img_data = p.getCameraImage(
                        width, height,
                        view_matrix,
                        proj_matrix,
                        renderer=p.ER_BULLET_HARDWARE_OPENGL
                    )
                    
                    # Convert to base64
                    img_array = np.array(img_data[2]).reshape((height, width, 4))
                    img_array = img_array[:, :, :3]  # Remove alpha channel
                    img = Image.fromarray(img_array)
                    
                    buffer = io.BytesIO()
                    img.save(buffer, format='PNG')
                    img_str = base64.b64encode(buffer.getvalue()).decode()
                    
                    return jsonify({'status': 'success', 'image': img_str})
                else:
                    return jsonify({'status': 'error', 'message': 'Arm not initialized'})
            except Exception as e:
                return jsonify({'status': 'error', 'message': str(e)})
        
        @self.app.route('/api/textures')
        def get_texture_info():
            try:
                if self.texture_manager:
                    texture_info = []
                    for name, path in self.texture_manager.textures.items():
                        texture_info.append({
                            'name': name,
                            'path': path,
                            'description': self.get_texture_description(name)
                        })
                    return jsonify({'status': 'success', 'textures': texture_info})
                else:
                    return jsonify({'status': 'error', 'message': 'Texture manager not available'})
            except Exception as e:
                return jsonify({'status': 'error', 'message': str(e)})
        
        @self.app.route('/api/demo/<demo_type>')
        def run_demo(demo_type):
            try:
                if demo_type == 'excavation':
                    self.run_excavation_demo()
                elif demo_type == 'material_handling':
                    self.run_material_handling_demo()
                elif demo_type == 'precision_work':
                    self.run_precision_demo()
                
                return jsonify({'status': 'success', 'message': f'Running {demo_type} demo'})
            except Exception as e:
                return jsonify({'status': 'error', 'message': str(e)})
    
    def get_texture_description(self, texture_name):
        """Get description for texture type"""
        descriptions = {
            'jcb_body': 'Authentic JCB yellow with wear patterns, panel lines, and logo areas',
            'jcb_boom': 'JCB orange with hydraulic mounts, scratches, and working wear',
            'steel_hydraulic': 'Weathered steel with hydraulic stains, rust, and metallic variation',
            'rubber_black': 'Heavy-duty rubber with earth stains, scratches, and surface texture',
            'weathered_metal': 'Aged metal with rust, corrosion, and paint wear patterns'
        }
        return descriptions.get(texture_name, 'Realistic texture for robotic arm components')
    
    def get_html_template(self):
        """Get HTML template for web interface"""
        return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Realistic JCB Robotic Arm Control</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1fr 400px;
            gap: 20px;
        }
        
        .main-panel {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .control-panel {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            max-height: 90vh;
            overflow-y: auto;
        }
        
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        .jcb-title {
            background: linear-gradient(45deg, #f1c40f, #f39c12);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .screenshot-container {
            text-align: center;
            margin-bottom: 30px;
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
        }
        
        #screenshot {
            max-width: 100%;
            max-height: 500px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .control-section {
            margin-bottom: 25px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #3498db;
        }
        
        .control-section h3 {
            color: #2c3e50;
            margin-top: 0;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .slider-container {
            margin: 15px 0;
        }
        
        .slider-label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #34495e;
        }
        
        .slider {
            width: 100%;
            height: 8px;
            border-radius: 5px;
            background: #ddd;
            outline: none;
            -webkit-appearance: none;
        }
        
        .slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #3498db;
            cursor: pointer;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        
        .slider::-moz-range-thumb {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #3498db;
            cursor: pointer;
            border: none;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        
        .value-display {
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.9em;
            min-width: 50px;
            text-align: center;
        }
        
        .demo-buttons {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 20px;
        }
        
        .demo-btn {
            background: linear-gradient(45deg, #f39c12, #e67e22);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 3px 10px rgba(0,0,0,0.2);
        }
        
        .demo-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        
        .update-btn {
            background: linear-gradient(45deg, #27ae60, #2ecc71);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            width: 100%;
            margin-top: 15px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.2);
        }
        
        .update-btn:hover {
            background: linear-gradient(45deg, #229954, #27ae60);
        }
        
        .texture-info {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
            padding: 15px;
            margin-top: 20px;
        }
        
        .texture-item {
            margin: 10px 0;
            padding: 10px;
            background: white;
            border-radius: 5px;
            border-left: 3px solid #f39c12;
        }
        
        .texture-name {
            font-weight: bold;
            color: #2c3e50;
        }
        
        .texture-desc {
            font-size: 0.9em;
            color: #7f8c8d;
            margin-top: 5px;
        }
        
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-connected {
            background: #27ae60;
        }
        
        .status-disconnected {
            background: #e74c3c;
        }
        
        @media (max-width: 1024px) {
            .container {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="main-panel">
            <h1><span class="jcb-title">JCB</span> Realistic Robotic Arm</h1>
            
            <div class="screenshot-container">
                <img id="screenshot" src="" alt="Robotic Arm View" style="display: none;">
                <div id="loading" style="padding: 100px; color: #7f8c8d;">
                    🚜 Loading realistic JCB robotic arm...
                </div>
            </div>
            
            <div style="text-align: center;">
                <button class="update-btn" onclick="updateScreenshot()">
                    📸 Update Live View
                </button>
            </div>
        </div>
        
        <div class="control-panel">
            <div class="control-section">
                <h3>🎮 Arm Controls</h3>
                <span class="status-indicator" id="connectionStatus"></span>
                <span id="statusText">Connecting...</span>
                
                <div class="slider-container">
                    <label class="slider-label">Base Rotation</label>
                    <input type="range" class="slider" id="baseSlider" 
                           min="-3.14" max="3.14" step="0.1" value="0">
                    <span class="value-display" id="baseValue">0.0°</span>
                </div>
                
                <div class="slider-container">
                    <label class="slider-label">Boom Angle</label>
                    <input type="range" class="slider" id="boomSlider" 
                           min="-1.57" max="0.785" step="0.1" value="0">
                    <span class="value-display" id="boomValue">0.0°</span>
                </div>
                
                <div class="slider-container">
                    <label class="slider-label">Stick Angle</label>
                    <input type="range" class="slider" id="stickSlider" 
                           min="-1.047" max="1.047" step="0.1" value="0">
                    <span class="value-display" id="stickValue">0.0°</span>
                </div>
                
                <div class="slider-container">
                    <label class="slider-label">Bucket Angle</label>
                    <input type="range" class="slider" id="bucketSlider" 
                           min="-1.57" max="0.785" step="0.1" value="0">
                    <span class="value-display" id="bucketValue">0.0°</span>
                </div>
            </div>
            
            <div class="control-section">
                <h3>🎬 Demonstration Modes</h3>
                <div class="demo-buttons">
                    <button class="demo-btn" onclick="runDemo('excavation')">
                        ⛏️ Excavation
                    </button>
                    <button class="demo-btn" onclick="runDemo('material_handling')">
                        📦 Material Handling
                    </button>
                    <button class="demo-btn" onclick="runDemo('precision_work')">
                        🎯 Precision Work
                    </button>
                    <button class="demo-btn" onclick="resetPosition()">
                        🔄 Reset
                    </button>
                </div>
            </div>
            
            <div class="texture-info">
                <h3>🎨 Realistic Textures</h3>
                <div id="textureList">
                    <div class="texture-item">
                        <div class="texture-name">JCB Body Texture</div>
                        <div class="texture-desc">Authentic yellow with wear patterns and logo areas</div>
                    </div>
                    <div class="texture-item">
                        <div class="texture-name">Boom/Stick Texture</div>
                        <div class="texture-desc">JCB orange with hydraulic mounts and scratches</div>
                    </div>
                    <div class="texture-item">
                        <div class="texture-name">Steel Hydraulics</div>
                        <div class="texture-desc">Weathered steel with stains and rust</div>
                    </div>
                    <div class="texture-item">
                        <div class="texture-name">Bucket Texture</div>
                        <div class="texture-desc">Heavy-duty rubber with earth stains</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let isConnected = false;
        
        // Initialize sliders
        const sliders = ['baseSlider', 'boomSlider', 'stickSlider', 'bucketSlider'];
        const valueDisplays = ['baseValue', 'boomValue', 'stickValue', 'bucketValue'];
        
        sliders.forEach((sliderId, index) => {
            const slider = document.getElementById(sliderId);
            const display = document.getElementById(valueDisplays[index]);
            
            slider.addEventListener('input', function() {
                const value = parseFloat(this.value);
                const degrees = (value * 180 / Math.PI).toFixed(1);
                display.textContent = degrees + '°';
                sendControlCommand();
            });
        });
        
        function sendControlCommand() {
            const data = {
                base_rotation: parseFloat(document.getElementById('baseSlider').value),
                boom_angle: parseFloat(document.getElementById('boomSlider').value),
                stick_angle: parseFloat(document.getElementById('stickSlider').value),
                bucket_angle: parseFloat(document.getElementById('bucketSlider').value)
            };
            
            fetch('/api/control', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    updateConnectionStatus(true);
                } else {
                    updateConnectionStatus(false);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                updateConnectionStatus(false);
            });
        }
        
        function updateConnectionStatus(connected) {
            isConnected = connected;
            const indicator = document.getElementById('connectionStatus');
            const statusText = document.getElementById('statusText');
            
            if (connected) {
                indicator.className = 'status-indicator status-connected';
                statusText.textContent = 'Connected to Robotic Arm';
            } else {
                indicator.className = 'status-indicator status-disconnected';
                statusText.textContent = 'Connection Failed';
            }
        }
        
        function updateScreenshot() {
            fetch('/api/screenshot')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const img = document.getElementById('screenshot');
                    const loading = document.getElementById('loading');
                    
                    img.src = 'data:image/png;base64,' + data.image;
                    img.style.display = 'block';
                    loading.style.display = 'none';
                } else {
                    console.error('Screenshot error:', data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
        
        function runDemo(demoType) {
            fetch('/api/demo/' + demoType)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    console.log('Demo started:', data.message);
                } else {
                    console.error('Demo error:', data.message);
                }
            });
        }
        
        function resetPosition() {
            document.getElementById('baseSlider').value = 0;
            document.getElementById('boomSlider').value = 0;
            document.getElementById('stickSlider').value = 0;
            document.getElementById('bucketSlider').value = 0;
            
            valueDisplays.forEach(displayId => {
                document.getElementById(displayId).textContent = '0.0°';
            });
            
            sendControlCommand();
        }
        
        // Auto-update screenshot every 5 seconds
        setInterval(updateScreenshot, 5000);
        
        // Initial screenshot
        setTimeout(updateScreenshot, 2000);
        
        // Test connection
        setTimeout(sendControlCommand, 1000);
    </script>
</body>
</html>
        '''
    
    def run_excavation_demo(self):
        """Run excavation demonstration sequence"""
        if not self.arm:
            return
        
        # Excavation sequence
        demo_sequence = [
            [0, -0.5, 0.8, -0.3],    # Approach ground
            [0, -0.8, 1.2, 0.2],    # Dig into ground
            [0, -0.5, 0.5, 0.5],    # Lift with material
            [1.5, 0.2, 0.2, 0.8],   # Rotate and dump
            [0, 0, 0, 0]             # Return to rest
        ]
        
        self.run_demo_sequence(demo_sequence)
    
    def run_material_handling_demo(self):
        """Run material handling demonstration"""
        if not self.arm:
            return
        
        # Material handling sequence
        demo_sequence = [
            [0, 0.2, -0.3, 0.2],     # Approach material
            [0, 0.1, -0.1, -0.1],    # Grab material
            [0, 0.5, -0.5, 0.3],     # Lift material
            [-1.5, 0.3, -0.2, 0.5],  # Move to new location
            [-1.5, 0.1, 0.1, 0.8],   # Place material
            [0, 0, 0, 0]             # Return to rest
        ]
        
        self.run_demo_sequence(demo_sequence)
    
    def run_precision_demo(self):
        """Run precision work demonstration"""
        if not self.arm:
            return
        
        # Precision work sequence
        demo_sequence = [
            [0, 0.3, -0.2, 0.1],     # Fine positioning
            [0.5, 0.25, -0.15, 0.05], # Precise adjustment
            [0.8, 0.3, -0.25, 0.15],  # Careful placement
            [0.5, 0.2, -0.1, 0.0],    # Final adjustment
            [0, 0, 0, 0]              # Return to rest
        ]
        
        self.run_demo_sequence(demo_sequence)
    
    def run_demo_sequence(self, sequence):
        """Run a demonstration sequence"""
        def animate_sequence():
            for positions in sequence:
                # Smoothly interpolate to each position
                current_pos = self.current_joint_positions[:]
                steps = 30
                
                for step in range(steps):
                    alpha = step / (steps - 1)
                    interpolated_pos = []
                    
                    for i in range(4):
                        start = current_pos[i]
                        end = positions[i]
                        pos = start + alpha * (end - start)
                        interpolated_pos.append(pos)
                    
                    # Apply positions
                    for i, pos in enumerate(interpolated_pos):
                        p.setJointMotorControl2(
                            self.arm.robot_id,
                            i,
                            p.POSITION_CONTROL,
                            targetPosition=pos,
                            force=1000
                        )
                    
                    p.stepSimulation()
                    time.sleep(0.05)
                
                self.current_joint_positions = positions[:]
                time.sleep(0.5)  # Pause between movements
        
        # Run animation in separate thread
        threading.Thread(target=animate_sequence, daemon=True).start()
    
    def initialize_arm(self):
        """Initialize the robotic arm in background"""
        try:
            print("🚜 Initializing realistic JCB robotic arm...")
            self.arm = EnhancedRealisticRoboticArm(gui=False)  # Headless mode for web
            self.texture_manager = self.arm.texture_manager
            print("✅ Robotic arm initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize arm: {e}")
    
    def run(self, host='localhost', port=5000, debug=False):
        """Run the web interface"""
        print("🌐 Starting realistic JCB robotic arm web interface...")
        print(f"🔗 Access at: http://{host}:{port}")
        
        # Initialize arm in background
        init_thread = threading.Thread(target=self.initialize_arm, daemon=True)
        init_thread.start()
        
        # Open browser
        if not debug:
            threading.Timer(2, lambda: webbrowser.open(f'http://{host}:{port}')).start()
        
        # Run Flask app
        self.app.run(host=host, port=port, debug=debug, threaded=True)


def main():
    """Main function to run web interface"""
    print("🚜 JCB Robotic Arm - Realistic Web Interface")
    print("=" * 50)
    
    interface = RealisticWebInterface()
    interface.run(host='0.0.0.0', port=5000, debug=False)


if __name__ == "__main__":
    main()