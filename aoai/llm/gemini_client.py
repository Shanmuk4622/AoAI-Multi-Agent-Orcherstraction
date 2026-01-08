"""
Gemini API Client
Handles connection and requests to Google's Gemini API
"""
import os
import time
import re
from typing import Optional, Dict, Any
import google.generativeai as genai


class GeminiClient:
    """Wrapper for Gemini API (optimized for code generation)"""
    
    # Using legacy API for compatibility with google-generativeai 0.1.0rc1
    # Available legacy models
    MODELS = [
        "text-bison-001",  # Text generation model
    ]
    
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("❌ GEMINI_API_KEY not found in environment")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        self.current_model = self.MODELS[0]
        
        print(f"✓ Gemini Client initialized (using legacy API)")
        print(f"   Note: Using google-generativeai 0.1.0rc1 (legacy API)")
    
    def generate(self, prompt: str, max_tokens: int = 4096, temperature: float = 0.3) -> str:
        """
        Send prompt to Gemini API and return response.
        
        Args:
            prompt: Input text (code generation instructions)
            max_tokens: Max response length
            temperature: Lower temp for code generation
            
        Returns:
            Generated code as string
        """
        print(f"\n🌐 Calling Gemini API (legacy)...")
        print(f"   Model: {self.current_model}")
        print(f"   Prompt length: {len(prompt)} chars")
        
        last_error = None
        
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                print(f"   Attempt {attempt}/{self.MAX_RETRIES}...")
                
                # Use legacy text generation API
                response = genai.generate_text(
                    model=self.current_model,
                    prompt=prompt,
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                    candidate_count=1
                )
                
                # Extract text from response
                if response.result:
                    content = response.result
                    
                    # Extract code from markdown if present
                    content = self._extract_code_from_markdown(content)
                    
                    print(f"   ✓ Response received ({len(content)} chars)")
                    return content
                else:
                    raise Exception("Empty response from Gemini API")
                
            except Exception as e:
                last_error = e
                error_msg = str(e).lower()
                
                print(f"   ⚠️  Error: {str(e)[:100]}")
                
                # Check for rate limiting or quota issues
                if "quota" in error_msg or "rate" in error_msg or "limit" in error_msg:
                    if attempt < self.MAX_RETRIES:
                        print(f"   Waiting {self.RETRY_DELAY}s before retry...")
                        time.sleep(self.RETRY_DELAY)
                    else:
                        raise Exception(f"Gemini API quota exhausted: {last_error}")
                
                else:
                    # Other error, retry with delay
                    if attempt < self.MAX_RETRIES:
                        time.sleep(self.RETRY_DELAY)
                    else:
                        raise Exception(f"Gemini API failed after {self.MAX_RETRIES} attempts: {last_error}")
        
        raise Exception(f"Gemini API failed: {last_error}")
    
    def _extract_code_from_markdown(self, text: str) -> str:
        """
        Extract code from markdown code blocks if present.
        
        Args:
            text: Response text that may contain markdown
            
        Returns:
            Extracted code or original text
        """
        # Check for python code blocks
        pattern = r'```python\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        
        if matches:
            print("   📝 Extracted code from markdown block")
            return matches[0].strip()
        
        # Check for generic code blocks
        pattern = r'```\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        
        if matches:
            print("   📝 Extracted code from markdown block")
            return matches[0].strip()
        
        # No code blocks found, return as is
        return text.strip()
