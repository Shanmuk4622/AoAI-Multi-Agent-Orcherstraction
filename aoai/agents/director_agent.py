"""
Agent B — Director
Responsible for: Scene planning and animation choreography
API Provider: Groq (Qwen / Llama-vision)
"""
import json
import sys
from pathlib import Path
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.prompts import get_prompt
from utils.json_schemas import validate_director_output


class DirectorAgent:
    """Converts reasoning into Manim scene structure"""
    
    MAX_RETRY = 2
    
    def __init__(self, llm_client):
        self.llm = llm_client
        print("✓ Director Agent initialized")
    
    def process(self, reasoning_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes structured reasoning and plans visual scenes.
        
        Args:
            reasoning_output: Output from Logician Agent
            
        Returns:
            {
                "scenes": [
                    {
                        "title": "...",
                        "objects": [...],
                        "animations": [...]
                    }
                ]
            }
        """
        print(f"\n{'='*60}")
        print("🎬 AGENT B — DIRECTOR (Scene Planning Phase)")
        print(f"{'='*60}")
        print(f"📥 Input: {reasoning_output['concept']} with {len(reasoning_output['steps'])} steps")
        
        # Build prompt with reasoning context
        prompt = get_prompt('director', reasoning_json=json.dumps(reasoning_output, indent=2))
        
        # Try to get valid response
        for attempt in range(1, self.MAX_RETRY + 1):
            print(f"\n🔄 Attempt {attempt}/{self.MAX_RETRY}")
            
            try:
                # Call LLM
                raw_response = self.llm.generate(
                    prompt=prompt,
                    max_tokens=2048,
                    temperature=0.6
                )
                
                print(f"\n📄 Raw response preview: {raw_response[:200]}...")
                
                # Validate output
                is_valid, result = validate_director_output(raw_response)
                
                if is_valid:
                    print(f"\n✅ Validation passed")
                    print(f"📤 Output:")
                    print(f"   Scenes: {len(result['scenes'])}")
                    for i, scene in enumerate(result['scenes'], 1):
                        print(f"   Scene {i}: {scene['title']}")
                        print(f"      Objects: {len(scene['objects'])}, Animations: {len(scene['animations'])}")
                    return result
                else:
                    print(f"\n❌ Validation failed: {result}")
                    if attempt < self.MAX_RETRY:
                        print("   Retrying with clarification...")
                        prompt += "\n\nIMPORTANT: Return ONLY valid JSON with scenes array containing title, objects, and animations."
                    else:
                        raise ValueError(f"Failed to get valid scene manifest: {result}")
            
            except json.JSONDecodeError as e:
                print(f"\n❌ JSON decode error: {str(e)}")
                if attempt >= self.MAX_RETRY:
                    raise ValueError(f"LLM returned invalid JSON: {str(e)}")
            
            except Exception as e:
                print(f"\n❌ Error in Director Agent: {str(e)}")
                raise
        
        raise ValueError("Failed to generate valid scene manifest")
