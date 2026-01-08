"""
Agent A — Logician
Responsible for: Mathematical reasoning and concept breakdown
API Provider: Groq (Llama-3 / Mixtral)
"""
import json
import sys
from pathlib import Path
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.prompts import get_prompt
from utils.json_schemas import validate_logician_output


class LogicianAgent:
    """Breaks down math concepts into structured reasoning steps"""
    
    MAX_RETRY = 2  # Retry if JSON validation fails
    
    def __init__(self, llm_client):
        self.llm = llm_client
        print("✓ Logician Agent initialized")
    
    def process(self, user_prompt: str) -> Dict[str, Any]:
        """
        Takes user input and generates structured mathematical reasoning.
        
        Args:
            user_prompt: Natural language math question
            
        Returns:
            {
                "concept": "...",
                "steps": ["step1", "step2", ...]
            }
        """
        print(f"\n{'='*60}")
        print("🧠 AGENT A — LOGICIAN (Reasoning Phase)")
        print(f"{'='*60}")
        print(f"📥 Input: {user_prompt}")
        
        # Build prompt
        prompt = get_prompt('logician', user_input=user_prompt)
        
        # Try to get valid response (with retries)
        for attempt in range(1, self.MAX_RETRY + 1):
            print(f"\n🔄 Attempt {attempt}/{self.MAX_RETRY}")
            
            try:
                # Call LLM
                raw_response = self.llm.generate(
                    prompt=prompt,
                    max_tokens=2048,
                    temperature=0.7
                )
                
                print(f"\n📄 Raw response preview: {raw_response[:200]}...")
                
                # Validate output
                is_valid, result = validate_logician_output(raw_response)
                
                if is_valid:
                    print(f"\n✅ Validation passed")
                    print(f"📤 Output:")
                    print(f"   Concept: {result['concept']}")
                    print(f"   Steps: {len(result['steps'])} steps")
                    return result
                else:
                    print(f"\n❌ Validation failed: {result}")
                    if attempt < self.MAX_RETRY:
                        print("   Retrying with clarification...")
                        prompt = get_prompt('logician', user_input=user_prompt) + "\n\nIMPORTANT: Return ONLY valid JSON, no additional text."
                    else:
                        raise ValueError(f"Failed to get valid JSON after {self.MAX_RETRY} attempts: {result}")
            
            except json.JSONDecodeError as e:
                print(f"\n❌ JSON decode error: {str(e)}")
                if attempt >= self.MAX_RETRY:
                    raise ValueError(f"LLM returned invalid JSON: {str(e)}")
            
            except Exception as e:
                print(f"\n❌ Error in Logician Agent: {str(e)}")
                raise
        
        raise ValueError("Failed to generate valid reasoning output")
