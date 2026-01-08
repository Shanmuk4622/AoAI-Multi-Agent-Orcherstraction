"""
Agent D — Fixer
Responsible for: Patching broken Manim code
API Provider: Groq (same model as Logician for stability)
"""
import json
import sys
import re
from pathlib import Path
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.prompts import get_prompt
from utils.json_schemas import validate_fixer_output


class FixerAgent:
    """Self-healing agent that patches execution errors"""
    
    MAX_RETRY = 2
    
    def __init__(self, llm_client):
        self.llm = llm_client
        print("✓ Fixer Agent initialized")
    
    def _extract_code_from_markdown(self, text: str) -> str:
        """Extract Python code from markdown code blocks."""
        # Pattern to match ```python ... ``` or ``` ... ```
        patterns = [
            r'```python\s*(.*?)\s*```',
            r'```\s*(.*?)\s*```',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                return match.group(1).strip()
        
        # If no code block found, return as-is
        return text.strip()
    
    def process(self, broken_code: str, error_log: str) -> str:
        """
        Takes failing code + error and returns patched version.
        
        Args:
            broken_code: The Python script that failed
            error_log: stderr output from Manim execution
            
        Returns:
            Corrected Python script
        """
        print(f"\n{'='*60}")
        print("🔧 AGENT D — FIXER (Error Correction Phase)")
        print(f"{'='*60}")
        print(f"📥 Input:")
        print(f"   Code length: {len(broken_code)} chars")
        print(f"   Error preview: {error_log[:200]}...")
        
        # Build prompt with code and error context
        prompt = get_prompt('fixer', code=broken_code, error=error_log)
        
        # Try to get fixed code
        for attempt in range(1, self.MAX_RETRY + 1):
            print(f"\n🔄 Attempt {attempt}/{self.MAX_RETRY}")
            
            try:
                # Call LLM
                raw_response = self.llm.generate(
                    prompt=prompt,
                    max_tokens=4096,
                    temperature=0.2  # Very low temp for fixes
                )
                
                # Extract code from markdown if needed
                fixed_code = self._extract_code_from_markdown(raw_response)
                
                print(f"\n📄 Fixed code length: {len(fixed_code)} chars")
                
                # Validate fixed code
                is_valid, error_msg = validate_fixer_output(fixed_code)
                
                if is_valid:
                    print(f"\n✅ Fixed code validation passed")
                    print(f"📤 Output: Patched Manim script")
                    
                    # Check if code actually changed
                    if fixed_code.strip() == broken_code.strip():
                        print("   ⚠️  Warning: Code unchanged, LLM may not have understood the error")
                    else:
                        print(f"   Code was modified (diff: {abs(len(fixed_code) - len(broken_code))} chars)")
                    
                    return fixed_code
                else:
                    print(f"\n❌ Fixed code validation failed: {error_msg}")
                    if attempt < self.MAX_RETRY:
                        print("   Retrying with emphasis on minimal changes...")
                        prompt += "\n\nIMPORTANT: Make ONLY minimal changes to fix the specific error. Do not redesign."
                    else:
                        # If validation fails but we have code, return it anyway (better than nothing)
                        print("   ⚠️  Returning code despite validation failure (last resort)")
                        return fixed_code
            
            except Exception as e:
                print(f"\n❌ Error in Fixer Agent: {str(e)}")
                if attempt >= self.MAX_RETRY:
                    # Return original code if fixer completely fails
                    print("   ⚠️  Fixer failed, returning original code")
                    return broken_code
        
        # Fallback: return original code
        print("\n⚠️  All fix attempts failed, returning original code")
        return broken_code
