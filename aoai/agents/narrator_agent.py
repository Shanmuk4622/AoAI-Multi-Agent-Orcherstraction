"""
Agent E — Narrator
Responsible for: Generating audio narration scripts
API Provider: Groq (same as other agents)
"""
import json
import sys
from pathlib import Path
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.prompts import get_prompt


class NarratorAgent:
    """Generates voiceover scripts synchronized with animation scenes"""
    
    MAX_RETRY = 2
    
    def __init__(self, llm_client):
        self.llm = llm_client
        print("✓ Narrator Agent initialized")
    
    def process(self, scene_manifest: Dict[str, Any], reasoning: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes scene manifest and reasoning to generate narration.
        
        Args:
            scene_manifest: Output from Director Agent
            reasoning: Output from Logician Agent
            
        Returns:
            {
                "narrations": [
                    {
                        "scene_index": 0,
                        "text": "Welcome to...",
                        "duration": 3
                    }
                ]
            }
        """
        print(f"\n{'='*60}")
        print("🎙️  AGENT E — NARRATOR (Narration Generation Phase)")
        print(f"{'='*60}")
        print(f"📥 Input: {len(scene_manifest['scenes'])} scenes")
        
        # Build prompt with scene and reasoning context
        prompt = get_prompt(
            'narrator',
            scene_manifest=json.dumps(scene_manifest, indent=2),
            reasoning=json.dumps(reasoning, indent=2)
        )
        
        # Try to get valid narration
        for attempt in range(1, self.MAX_RETRY + 1):
            print(f"\n🔄 Attempt {attempt}/{self.MAX_RETRY}")
            
            try:
                # Call LLM
                raw_response = self.llm.generate(
                    prompt=prompt,
                    max_tokens=2048,
                    temperature=0.7
                )
                
                print(f"\n📄 Generated narration length: {len(raw_response)} chars")
                
                # Try to parse JSON
                try:
                    narration_data = json.loads(raw_response)
                    
                    # Validate structure
                    if "narrations" in narration_data and isinstance(narration_data["narrations"], list):
                        print(f"\n✅ Validation passed")
                        print(f"📤 Output:")
                        print(f"   Narrations: {len(narration_data['narrations'])} segments")
                        for i, narr in enumerate(narration_data["narrations"]):
                            print(f"   Scene {i}: '{narr.get('text', '')[:50]}...'")
                        return narration_data
                    else:
                        print(f"\n❌ Invalid structure: missing 'narrations' array")
                        
                except json.JSONDecodeError as e:
                    print(f"\n❌ JSON decode error: {str(e)}")
                    # Try to extract JSON from markdown
                    if "```json" in raw_response:
                        json_match = raw_response.split("```json")[1].split("```")[0]
                        narration_data = json.loads(json_match.strip())
                        if "narrations" in narration_data:
                            return narration_data
                
            except Exception as e:
                print(f"\n❌ Error in Narrator Agent: {str(e)}")
                if attempt >= self.MAX_RETRY:
                    raise
        
        # Fallback: create basic narration
        print("\n⚠️  Using fallback narration")
        return {
            "narrations": [
                {
                    "scene_index": i,
                    "text": scene["title"],
                    "duration": 3
                }
                for i, scene in enumerate(scene_manifest["scenes"])
            ]
        }
