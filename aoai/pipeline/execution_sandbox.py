""".
Execution Sandbox
Safely runs Manim scripts and captures output/errors
"""
import subprocess
import os
import shutil
from pathlib import Path
from typing import Dict, Any, Optional


class ExecutionSandbox:
    """Isolated environment for running Manim renders"""
    
    def __init__(self, storage_path: str):
        self.storage_path = Path(storage_path)
        self.outputs_dir = self.storage_path / "outputs"
        self.temp_dir = self.storage_path / "temp"
        
        # Create directories if they don't exist
        self.outputs_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"✓ Execution Sandbox initialized")
        print(f"   Output directory: {self.outputs_dir}")
        print(f"   Temp directory: {self.temp_dir}")
    
    def run(self, code: str, scene_name: str = "GeneratedScene") -> Dict[str, Any]:
        """
        Execute Manim script and capture results.
        
        Args:
            code: Python script containing Manim scene
            scene_name: Name of the Scene class to render
            
        Returns:
            {
                "success": bool,
                "video_path": str | None,
                "stdout": str,
                "stderr": str,
                "exit_code": int
            }
        """
        print(f"\n{'='*60}")
        print("🎬 EXECUTING MANIM RENDER")
        print(f"{'='*60}")
        
        # Save code to temp file
        script_path = self.temp_dir / "scene.py"
        try:
            script_path.write_text(code, encoding='utf-8')
            print(f"📝 Saved script to: {script_path}")
        except Exception as e:
            return {
                "success": False,
                "video_path": None,
                "stdout": "",
                "stderr": f"Failed to save script: {str(e)}",
                "exit_code": -1
            }
        
        # Build Manim command
        cmd = [
            "manim",
            "-qm",  # Medium quality
            "-o", "output.mp4",  # Output filename
            str(script_path),
            scene_name
        ]
        
        print(f"🔧 Running: {' '.join(cmd)}")
        print(f"   Scene: {scene_name}")
        print(f"   Quality: Medium")
        
        try:
            # Run Manim subprocess
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.temp_dir),
                timeout=300  # 5 minute timeout
            )
            
            stdout = result.stdout
            stderr = result.stderr
            exit_code = result.returncode
            
            print(f"\n📊 Execution completed")
            print(f"   Exit code: {exit_code}")
            print(f"   Stdout length: {len(stdout)} chars")
            print(f"   Stderr length: {len(stderr)} chars")
            
            # Check if successful
            if exit_code == 0:
                # Find generated video
                video_path = self._find_video_output(scene_name)
                
                if video_path and video_path.exists():
                    # Move video to outputs directory
                    final_path = self.outputs_dir / video_path.name
                    shutil.move(str(video_path), str(final_path))
                    
                    print(f"\n✅ Render successful!")
                    print(f"📹 Video: {final_path}")
                    
                    return {
                        "success": True,
                        "video_path": str(final_path),
                        "stdout": stdout,
                        "stderr": stderr,
                        "exit_code": exit_code
                    }
                else:
                    print(f"\n⚠️  Warning: Exit code 0 but no video found")
                    return {
                        "success": False,
                        "video_path": None,
                        "stdout": stdout,
                        "stderr": "Video file not found after render",
                        "exit_code": exit_code
                    }
            else:
                # Execution failed
                print(f"\n❌ Render failed (exit code {exit_code})")
                if stderr:
                    print(f"\n🔴 Error output (first 500 chars):")
                    print(stderr[:500])
                
                return {
                    "success": False,
                    "video_path": None,
                    "stdout": stdout,
                    "stderr": stderr,
                    "exit_code": exit_code
                }
        
        except subprocess.TimeoutExpired:
            error_msg = "Manim execution timed out (>5 minutes)"
            print(f"\n❌ {error_msg}")
            return {
                "success": False,
                "video_path": None,
                "stdout": "",
                "stderr": error_msg,
                "exit_code": -2
            }
        
        except FileNotFoundError:
            error_msg = "Manim command not found. Is Manim installed? Run: pip install manim"
            print(f"\n❌ {error_msg}")
            return {
                "success": False,
                "video_path": None,
                "stdout": "",
                "stderr": error_msg,
                "exit_code": -3
            }
        
        except Exception as e:
            error_msg = f"Unexpected error during execution: {str(e)}"
            print(f"\n❌ {error_msg}")
            return {
                "success": False,
                "video_path": None,
                "stdout": "",
                "stderr": error_msg,
                "exit_code": -4
            }
    
    def _find_video_output(self, scene_name: str) -> Optional[Path]:
        """
        Find the generated video file in Manim's output structure.
        Manim typically outputs to: media/videos/scene/{quality}/output.mp4
        
        Args:
            scene_name: Name of the scene class
            
        Returns:
            Path to video file or None
        """
        # Manim output structure
        media_dir = self.temp_dir / "media" / "videos" / "scene"
        
        if not media_dir.exists():
            return None
        
        # Search for mp4 files in quality subdirectories
        for quality_dir in media_dir.iterdir():
            if quality_dir.is_dir():
                for video_file in quality_dir.glob("*.mp4"):
                    return video_file
        
        return None
    
    def cleanup_temp(self):
        """Clean up temporary files after execution"""
        try:
            if self.temp_dir.exists():
                # Remove all contents but keep the directory
                for item in self.temp_dir.iterdir():
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
                print("🧹 Cleaned up temporary files")
        except Exception as e:
            print(f"⚠️  Warning: Failed to clean temp directory: {str(e)}")
