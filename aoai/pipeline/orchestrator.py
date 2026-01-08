"""
Pipeline Orchestrator
Coordinates the 4-agent workflow from prompt to video
"""
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import json

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.file_io import save_json_log, save_code


class Orchestrator:
    """Main pipeline controller that routes data between agents"""
    
    def __init__(self, agents: Dict[str, Any], storage_path: Path, sandbox=None, retry_manager=None):
        """
        Args:
            agents: Dictionary containing initialized agents
                    {'logician': ..., 'director': ..., 'engineer': ..., 'fixer': ...}
            storage_path: Path to storage directory
            sandbox: Optional ExecutionSandbox instance
            retry_manager: Optional RetryManager instance
        """
        self.logician = agents['logician']
        self.director = agents['director']
        self.engineer = agents['engineer']
        self.fixer = agents['fixer']
        self.narrator = agents.get('narrator')  # Optional narrator agent
        self.sandbox = sandbox
        self.retry_manager = retry_manager
        
        # Set up storage paths
        self.storage_path = Path(storage_path)
        self.outputs_dir = self.storage_path / "outputs"
        self.logs_dir = self.storage_path / "logs"
        self.temp_dir = self.storage_path / "temp"
        
        # Create directories if they don't exist
        self.outputs_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        print("\n" + "="*60)
        print("🎯 AOAI ORCHESTRATOR INITIALIZED")
        print("="*60)
        print(f"📁 Storage: {self.storage_path}")
        print(f"📁 Outputs: {self.outputs_dir}")
        print(f"📁 Logs: {self.logs_dir}")
    
    def run(self, user_prompt: str, save_logs: bool = True, execute: bool = False) -> Dict[str, Any]:
        """
        Execute full pipeline: Reasoning → Planning → Generation → (Optional) Execution
        
        Args:
            user_prompt: User's natural language input
            save_logs: Whether to save intermediate logs
            execute: Whether to execute Manim rendering (requires manim installed)
            
        Returns:
            {
                "success": bool,
                "code_path": str | None,
                "video_path": str | None,
                "logs": {...},
                "error": str | None
            }
        """
        print(f"\n🚀 Starting pipeline for: '{user_prompt}'")
        print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        start_time = datetime.now()
        session_logs = {
            "user_prompt": user_prompt,
            "start_time": start_time.isoformat(),
            "stages": {}
        }
        
        try:
            # ========================================
            # Phase 1: Mathematical Reasoning (Agent A)
            # ========================================
            print("\n" + "="*60)
            print("📍 PHASE 1: Mathematical Reasoning")
            print("="*60)
            
            reasoning = self.logician.process(user_prompt)
            session_logs["stages"]["reasoning"] = reasoning
            
            if save_logs:
                save_json_log(reasoning, self.logs_dir, "logician")
            
            # ========================================
            # Phase 2: Scene Planning (Agent B)
            # ========================================
            print("\n" + "="*60)
            print("📍 PHASE 2: Scene Planning")
            print("="*60)
            
            scene_manifest = self.director.process(reasoning)
            session_logs["stages"]["scene_manifest"] = scene_manifest
            
            if save_logs:
                save_json_log(scene_manifest, self.logs_dir, "director")
            
            # ========================================
            # Phase 3: Code Generation (Agent C)
            # ========================================
            print("\n" + "="*60)
            print("📍 PHASE 3: Code Generation")
            print("="*60)
            
            manim_code = self.engineer.process(scene_manifest)
            session_logs["stages"]["code_length"] = len(manim_code)
            
            # Save generated code
            code_path = save_code(manim_code, self.outputs_dir, "scene.py")
            
            # ========================================
            # Phase 4: Execution (Optional)
            # ========================================
            video_path = None
            if execute:
                print("\n" + "="*60)
                print("📍 PHASE 4: Manim Execution")
                print("="*60)
                
                # Execute the generated Manim code with auto-retry on errors
                execution_result = self.retry_manager.execute_with_retry(manim_code)
                
                if execution_result["success"]:
                    video_path = execution_result.get("video_path")
                    print(f"✅ Video rendering completed!")
                    if video_path:
                        print(f"📹 Video saved: {video_path}")
                else:
                    print(f"❌ Execution failed after {execution_result.get('attempts', 0)} attempts")
                    print(f"   Last error: {execution_result.get('stderr', 'Unknown error')[:200]}...")
            
            # ========================================
            # Pipeline Complete
            # ========================================
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            session_logs["end_time"] = end_time.isoformat()
            session_logs["duration_seconds"] = duration
            session_logs["success"] = True
            session_logs["video_path"] = video_path
            
            # Save complete session log
            if save_logs:
                save_json_log(session_logs, self.logs_dir, "session")
            
            print("\n" + "="*60)
            print("✅ PIPELINE COMPLETED SUCCESSFULLY")
            print("="*60)
            print(f"⏱️  Duration: {duration:.2f}s")
            print(f"📄 Code saved: {code_path}")
            if video_path:
                print(f"📹 Video saved: {video_path}")
            print(f"📊 Logs saved: {self.logs_dir}")
            print("="*60)
            
            return {
                "success": True,
                "code_path": str(code_path),
                "video_path": video_path,
                "logs": session_logs,
                "error": None
            }
            
        except Exception as e:
            # ========================================
            # Handle Pipeline Failure
            # ========================================
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            error_msg = str(e)
            
            session_logs["end_time"] = end_time.isoformat()
            session_logs["duration_seconds"] = duration
            session_logs["success"] = False
            session_logs["error"] = error_msg
            
            # Save error log
            if save_logs:
                save_json_log(session_logs, self.logs_dir, "session_error")
            
            print("\n" + "="*60)
            print("❌ PIPELINE FAILED")
            print("="*60)
            print(f"⏱️  Duration: {duration:.2f}s")
            print(f"❗ Error: {error_msg}")
            print(f"📊 Error log saved: {self.logs_dir}")
            print("="*60)
            
            return {
                "success": False,
                "code_path": None,
                "error": error_msg,
                "logs": session_logs
            }
