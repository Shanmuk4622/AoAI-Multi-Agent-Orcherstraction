"""
Agent C — Engineer
Responsible for: Manim code generation
API Provider: Gemini (Gemini 3.0 Flash)
"""
import json
import sys
import re
from pathlib import Path
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.prompts import get_prompt
from utils.json_schemas import validate_engineer_output


class EngineerAgent:
    """Generates executable Manim CE scripts from scene manifests"""
    
    MAX_RETRY = 2
    
    def __init__(self, llm_client):
        self.llm = llm_client
        print("✓ Engineer Agent initialized")
    
    def _extract_code_from_markdown(self, text: str) -> str:
        """Extract code from markdown blocks"""
        # Check for python code blocks
        pattern = r'```python\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        
        if matches:
            return matches[0].strip()
        
        # Check for generic code blocks
        pattern = r'```\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        
        if matches:
            return matches[0].strip()
        
        # No code blocks, return as is
        return text.strip()
    
    def process(self, scene_manifest: Dict[str, Any]) -> str:
        """
        Takes scene manifest and generates Manim Python code.
        
        Args:
            scene_manifest: Output from Director Agent
            
        Returns:
            Complete Python script as string
        """
        print(f"\n{'='*60}")
        print("⚙️  AGENT C — ENGINEER (Code Generation Phase)")
        print(f"{'='*60}")
        print(f"📥 Input: {len(scene_manifest['scenes'])} scenes to implement")
        
        # Build prompt with scene manifest
        prompt = get_prompt('engineer', scene_manifest=json.dumps(scene_manifest, indent=2))
        
        # Try to get valid code
        for attempt in range(1, self.MAX_RETRY + 1):
            print(f"\n🔄 Attempt {attempt}/{self.MAX_RETRY}")
            
            try:
                # Call LLM (Gemini for code generation)
                raw_response = self.llm.generate(
                    prompt=prompt,
                    max_tokens=4096,
                    temperature=0.3  # Lower temperature for code
                )
                
                print(f"\n📄 Generated code length: {len(raw_response)} chars")
                print(f"   First 100 chars: {raw_response[:100]}...")
                
                # Extract code from markdown if present (Groq returns markdown)
                code = self._extract_code_from_markdown(raw_response)
                
                # Validate code structure
                is_valid, error_msg = validate_engineer_output(code)
                
                if is_valid:
                    print(f"\n✅ Code validation passed")
                    print(f"📤 Output: Generated Manim script")
                    print(f"   Lines of code: {len(raw_response.splitlines())}")
                    print(f"   Contains imports: {'from manim import' in code}")
                    print(f"   Contains Scene class: {'class GeneratedScene' in code}")
                    return code
                else:
                    print(f"\n❌ Code validation failed: {error_msg}")
                    if attempt < self.MAX_RETRY:
                        print("   Retrying with stricter instructions...")
                        prompt += "\n\nCRITICAL: Code MUST include 'from manim import *' and 'class GeneratedScene(Scene)'. Return ONLY the Python code."
                    else:
                        raise ValueError(f"Generated code is invalid: {error_msg}")
            
            except Exception as e:
                print(f"\n❌ Error in Engineer Agent: {str(e)}")
                if attempt >= self.MAX_RETRY:
                    raise
        
        raise ValueError("Failed to generate valid Manim code")
