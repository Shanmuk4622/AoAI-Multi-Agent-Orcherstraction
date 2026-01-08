"""
Groq API Client
Handles connection, retry logic, and model fallback for Groq inference
"""
import os
import time
from typing import Optional, Dict, Any
from groq import Groq


class GroqClient:
    """Wrapper for Groq API with automatic model fallback"""
    
    # Model presets for different tasks
    REASONING_MODELS = [
        "llama-3.3-70b-versatile",  # Best for reasoning and planning
        "llama-3.1-70b-versatile",
        "mixtral-8x7b-32768"
    ]
    
    CODE_MODELS = [
        "llama-3.3-70b-versatile",  # Best available for code on Groq
        "llama-3.1-70b-versatile",
        "mixtral-8x7b-32768"
    ]
    
    # Default models list
    MODELS = REASONING_MODELS
    
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds
    
    def __init__(self, api_key: Optional[str] = None, model_type: str = "reasoning"):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("❌ GROQ_API_KEY not found in environment")
        
        # Initialize Groq client
        self.client = Groq(api_key=self.api_key)
        
        # Select model list based on task type
        if model_type == "code":
            self.MODELS = self.CODE_MODELS
        else:
            self.MODELS = self.REASONING_MODELS
            
        self.current_model = self.MODELS[0]
        print(f"✓ Groq Client initialized ({model_type} mode, model: {self.current_model})")
    
    def generate(self, prompt: str, max_tokens: int = 2048, temperature: float = 0.7) -> str:
        """
        Send prompt to Groq API and return response.
        
        Args:
            prompt: Input text
            max_tokens: Max response length
            temperature: Sampling temperature
            
        Returns:
            Model response as string
        """
        print(f"\n🌐 Calling Groq API...")
        print(f"   Model: {self.current_model}")
        print(f"   Prompt length: {len(prompt)} chars")
        
        last_error = None
        
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                print(f"   Attempt {attempt}/{self.MAX_RETRIES}...")
                
                # Call Groq API
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    model=self.current_model,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                
                # Extract response
                response = chat_completion.choices[0].message.content
                
                print(f"   ✓ Response received ({len(response)} chars)")
                return response
                
            except Exception as e:
                last_error = e
                error_msg = str(e).lower()
                
                print(f"   ⚠️  Error: {str(e)[:100]}")
                
                # Check if rate limited or model unavailable
                if "rate" in error_msg or "limit" in error_msg or "quota" in error_msg:
                    if attempt < self.MAX_RETRIES:
                        print(f"   Waiting {self.RETRY_DELAY}s before retry...")
                        time.sleep(self.RETRY_DELAY)
                    else:
                        # Try fallback model
                        try:
                            self._fallback_model()
                            return self.generate(prompt, max_tokens, temperature)
                        except Exception as fallback_error:
                            raise Exception(f"All Groq models failed: {fallback_error}")
                
                elif "model" in error_msg and attempt == self.MAX_RETRIES:
                    # Model not available, try fallback
                    try:
                        self._fallback_model()
                        return self.generate(prompt, max_tokens, temperature)
                    except Exception as fallback_error:
                        raise Exception(f"Model fallback failed: {fallback_error}")
                
                else:
                    # Other error, retry with delay
                    if attempt < self.MAX_RETRIES:
                        time.sleep(self.RETRY_DELAY)
                    else:
                        raise Exception(f"Groq API failed after {self.MAX_RETRIES} attempts: {last_error}")
        
        raise Exception(f"Groq API failed: {last_error}")
    
    def _fallback_model(self):
        """Switch to next available model"""
        current_idx = self.MODELS.index(self.current_model)
        if current_idx < len(self.MODELS) - 1:
            self.current_model = self.MODELS[current_idx + 1]
            print(f"⚠️  Falling back to: {self.current_model}")
        else:
            raise Exception("All Groq models exhausted")
