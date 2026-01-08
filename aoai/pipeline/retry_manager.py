"""
Retry Manager
Handles error correction loops with Agent D (Fixer)
"""
from typing import Dict, Any, Callable


class RetryManager:
    """Manages retry attempts when Manim execution fails"""
    
    MAX_RETRIES = 3
    
    def __init__(self, fixer_agent, sandbox):
        self.fixer = fixer_agent
        self.sandbox = sandbox
        print(f"✓ Retry Manager initialized (max retries: {self.MAX_RETRIES})")
    
    def execute_with_retry(self, initial_code: str, scene_name: str = "GeneratedScene") -> Dict[str, Any]:
        """
        Try to execute code, fix errors if needed, retry up to MAX_RETRIES times.
        
        Args:
            initial_code: First version of Manim script
            scene_name: Scene class to render
            
        Returns:
            Final execution result (success or final failure)
        """
        print(f"\n{'='*60}")
        print("🔄 RETRY MANAGER STARTING")
        print(f"{'='*60}")
        
        current_code = initial_code
        execution_history = []
        
        for attempt in range(1, self.MAX_RETRIES + 1):
            print(f"\n{'='*60}")
            print(f"🔄 ATTEMPT {attempt}/{self.MAX_RETRIES}")
            print(f"{'='*60}")
            
            # Try to execute current code
            result = self.sandbox.run(current_code, scene_name)
            execution_history.append({
                "attempt": attempt,
                "exit_code": result["exit_code"],
                "success": result["success"]
            })
            
            if result["success"]:
                print(f"\n✅ Success on attempt {attempt}!")
                result["attempts"] = attempt
                result["execution_history"] = execution_history
                return result
            
            # Execution failed
            print(f"\n❌ Attempt {attempt} failed (exit code: {result['exit_code']})")
            
            if attempt < self.MAX_RETRIES:
                print(f"\n🔧 Calling Fixer Agent to patch code...")
                
                try:
                    # Use Fixer Agent to correct the code
                    current_code = self.fixer.process(current_code, result["stderr"])
                    print(f"✓ Fixer returned modified code")
                except Exception as e:
                    print(f"❌ Fixer Agent failed: {str(e)}")
                    print(f"   Stopping retry loop")
                    break
            else:
                print(f"\n❌ Max retries ({self.MAX_RETRIES}) reached")
        
        # All retries exhausted
        print(f"\n{'='*60}")
        print(f"❌ RETRY MANAGER FAILED")
        print(f"   Total attempts: {len(execution_history)}")
        print(f"{'='*60}")
        
        result["attempts"] = len(execution_history)
        result["execution_history"] = execution_history
        return result
